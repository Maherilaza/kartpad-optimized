import unittest
from pathlib import Path


MATRIX = Path(__file__).parents[1] / "docs" / "COMPATIBILITY-MATRIX.md"
VALID_STATES = {
    "verified-pass",
    "reproduced-open",
    "partial",
    "candidate-awaiting-device",
    "awaiting-reporter",
    "awaiting-device",
    "unverified",
    "not-evaluated",
    "closed-historical",
}


class CompatibilityMatrixContractTests(unittest.TestCase):
    def test_device_rows_have_stable_schema_and_unique_keys(self):
        rows = []
        for line in MATRIX.read_text().splitlines():
            if line.startswith("| `"):
                columns = [column.strip() for column in line.strip("|").split("|")]
                self.assertEqual(len(columns), 7, line)
                rows.append(columns)

        self.assertGreaterEqual(len(rows), 15)
        keys = [row[0].strip("`") for row in rows]
        self.assertEqual(len(keys), len(set(keys)))

        for row in rows:
            self.assertIn(row[4].strip("`"), VALID_STATES)
            self.assertRegex(row[5], r"#\d+")
            self.assertTrue(row[6])

    def test_matrix_declares_non_generalization_rule(self):
        text = MATRIX.read_text()
        self.assertIn("Do not generalize a", text)
        self.assertIn("row to a vendor", text)
        self.assertIn("Every non-pass row must have one named next gate", text)


if __name__ == "__main__":
    unittest.main()
