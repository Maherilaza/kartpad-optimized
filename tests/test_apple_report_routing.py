"""Execute the Apple report-copy and draft construction against Foundation."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AppleReportRoutingTests(unittest.TestCase):
    def test_export_copy_and_mac_draft(self):
        if not shutil.which('xcrun'):
            self.skipTest('Apple SDK unavailable')
        ios = (ROOT / 'apple/ios/KartPadRuntimeOverlayHost.mm').read_text()
        start = ios.index('  NSString *report = reportURL ?', ios.index('- (void)createDiagnosticReportFromPrompt:'))
        export = ios[start:ios.index('  if (reportURL == nil && !openGitHub)', start)]
        mac = (ROOT / 'apple/macos/KartPadMacShell.mm').read_text()
        start = mac.index('  NSBundle *bundle', mac.index('- (void)reportProblem:'))
        draft = mac[start:mac.index('  if (draft.URL != nil)', start)]
        source = '''#import <Foundation/Foundation.h>
#include <cassert>
static NSURL *Export(NSURL *reportURL) {
  NSError *error = nil;
''' + export + '''
  return reportURL;
}
static NSURL *Draft() {
''' + draft + '''
  return draft.URL;
}
int main() { @autoreleasepool {
  NSURL *dir = [NSURL fileURLWithPath:[NSTemporaryDirectory() stringByAppendingPathComponent:NSUUID.UUID.UUIDString]];
  assert([NSFileManager.defaultManager createDirectoryAtURL:dir withIntermediateDirectories:YES attributes:nil error:nil]);
  NSURL *original = [dir URLByAppendingPathComponent:@"SunPad-report.txt"];
  NSString *input = @"SunPad Diagnostic Report v2\\nissuesURL=https://github.com/chrissotraidis/sunpad/issues\\nreviewed log";
  assert([input writeToURL:original atomically:YES encoding:NSUTF8StringEncoding error:nil]);
  NSURL *output = Export(original);
  assert([output.lastPathComponent isEqual:@"Latest-KartPad-Diagnostic.log"]);
  NSString *text = [NSString stringWithContentsOfURL:output encoding:NSUTF8StringEncoding error:nil];
  assert([text containsString:@"KartPad Diagnostic Report v2"]);
  assert([text containsString:@"reportOrigin=KartPad"]);
  assert([text containsString:@"issuesURL=https://github.com/chrissotraidis/kartpad/issues"]);
  assert([text containsString:@"reviewed log"]);
  assert([[NSString stringWithContentsOfURL:original encoding:NSUTF8StringEncoding error:nil] isEqual:input]);
  assert(Export(nil) == nil);
  assert([NSFileManager.defaultManager removeItemAtURL:dir error:nil]);
  NSURLComponents *url = [NSURLComponents componentsWithURL:Draft() resolvingAgainstBaseURL:NO];
  assert([url.host isEqual:@"github.com"]);
  assert([url.path isEqual:@"/chrissotraidis/kartpad/issues/new"]);
  NSMutableDictionary *fields = [NSMutableDictionary dictionary];
  for (NSURLQueryItem *item in url.queryItems) fields[item.name] = item.value;
  assert([fields[@"template"] isEqual:@"bug_report.yml"]);
  assert([fields[@"platform"] containsString:NSProcessInfo.processInfo.operatingSystemVersionString]);
  assert([fields[@"context"] containsString:@"KartPad (modified WiiCompiled"]);
  assert([fields[@"diagnostics"] containsString:@"No diagnostic file has been uploaded"]);
  assert([fields[@"diagnostics"] containsString:@"attach it manually"]);
} }
'''
        with tempfile.TemporaryDirectory() as temp:
            cpp = Path(temp) / 'report.mm'
            exe = Path(temp) / 'report'
            cpp.write_text(source)
            subprocess.run(['xcrun', 'clang++', '-std=c++17', '-fobjc-arc', '-Wall', '-Wextra', '-Werror', '-framework', 'Foundation', str(cpp), '-o', str(exe)], check=True)
            subprocess.run([str(exe)], check=True)
