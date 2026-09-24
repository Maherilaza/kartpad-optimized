#!/usr/bin/env python3
"""Check the production FIFO burst walker against ordered XF/CP/BP packets."""

from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / "vendor/runtimes/android/runtime/src/hle/gx/gx_fifo.cpp").read_text()
start = source.index("static uint32_t ApplyFifoPacketsDirect(")
end = source.index("\n// Display-list recording", start)
walker = source[start:end]

program = r'''
#include <cassert>
#include <cstdint>
#include <vector>
using u32 = uint32_t;
constexpr uint8_t GX_NOP_CMD = 0x00;
constexpr uint8_t GX_LOAD_CP_REG_CMD = 0x08;
constexpr uint8_t GX_LOAD_XF_REG_CMD = 0x10;
constexpr uint8_t GX_LOAD_BP_REG_CMD = 0x61;
constexpr uint8_t GX_OPCODE_MASK_CMD = 0xF8;
struct { bool inBegin = false; size_t fifoByteCount = 0; } g_hleGxState;
bool recording = false;
bool IsDisplayListActive() { return recording; }
uint16_t ReadBE16(const uint8_t* p) { return uint16_t(p[0] << 8 | p[1]); }
uint32_t ReadBE32(const uint8_t* p) {
  return uint32_t(p[0]) << 24 | uint32_t(p[1]) << 16 | uint32_t(p[2]) << 8 | p[3];
}
std::vector<unsigned> events;
unsigned calls = 0;
unsigned marks = 0;
void GXMarkFrameWork() { ++marks; }
void GXApplyBPReg(uint8_t reg, uint32_t) { events.push_back(0x20000 | reg); }
namespace GxCpDecode {
void ApplyCpRegWrite(uint8_t reg, uint32_t) { events.push_back(0x30000 | reg); }
}
void GXCallDisplayList(const void* raw, uint32_t bytes) {
  ++calls;
  const auto* data = static_cast<const uint8_t*>(raw);
  for (uint32_t pos = 0; pos < bytes;) {
    assert(data[pos] == GX_LOAD_XF_REG_CMD);
    const uint32_t count = uint32_t(ReadBE16(data + pos + 1)) + 1;
    const uint32_t packetBytes = 5 + 4 * count;
    assert(pos + packetBytes <= bytes);
    events.push_back(0x10000 | data[pos + 5]);
    pos += packetBytes;
  }
}
''' + walker + r'''
int main() {
  const std::vector<uint8_t> stream{
      0x10,0,0,0,0,1,0,0,0, 0x10,0,0,0,0,2,0,0,0,
      0x10,0,0,0,0,3,0,0,0, 0x61,4,0,0,0,
      0x08,5,0,0,0,0, 0x10,0,0,0,0,6,0,0,0};
  assert(ApplyFifoPacketsDirect(stream.data(), stream.size()) == stream.size());
  assert((events == std::vector<unsigned>{0x10001,0x10002,0x10003,0x20004,0x30005,0x10006}));
  assert(calls == 2 && marks == 2);

  events.clear(); calls = marks = 0;
  const std::vector<uint8_t> incomplete{0x10,0,0,0,0,7,0,0,0, 0x10,0,1};
  assert(ApplyFifoPacketsDirect(incomplete.data(), incomplete.size()) == 9);
  assert((events == std::vector<unsigned>{0x10007}));
  assert(calls == 1 && marks == 1);

  events.clear(); calls = marks = 0;
  g_hleGxState.fifoByteCount = 1;
  assert(ApplyFifoPacketsDirect(stream.data(), stream.size()) == 0);
  g_hleGxState.fifoByteCount = 0;
  recording = true;
  assert(ApplyFifoPacketsDirect(stream.data(), stream.size()) == 0);
  assert(events.empty() && calls == 0 && marks == 0);
}
'''

with tempfile.TemporaryDirectory(prefix="kartpad-gx-xf-burst-") as temp:
    source_file = Path(temp) / "burst.cpp"
    binary = Path(temp) / "burst"
    source_file.write_text(program)
    subprocess.run(["clang++", "-std=c++20", "-O2", "-Wall", "-Wextra", "-Werror",
                    str(source_file), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)

print("PASS: XF burst grouping preserves packet order and truncated/recording boundaries")
