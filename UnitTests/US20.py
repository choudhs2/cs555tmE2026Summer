import unittest
import io
from datetime import date
from GEDCOMParser import *


class TestDeceasedIndividualsPrinting(unittest.TestCase):

    def test_print_has_deceased_individuals(self):
        """Normal case: single deceased individual should be listed in table."""
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 16 MAY 2020
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        outStr = parser.PrintDeceasedIndividuals()
        self.assertNotEqual(outStr, "\nDeceased Individuals\nNone Found\n")
        self.assertIn("@I1@", outStr)
        self.assertIn("Earl /Grey/", outStr)
        self.assertIn("2020-05-16", outStr)

    def test_print_no_deceased_individuals(self):
        """All individuals living: should output None Found."""
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        outStr = parser.PrintDeceasedIndividuals()
        self.assertEqual(outStr, "\nDeceased Individuals\nNone Found\n")

    def test_print_empty_file(self):
        """Empty GEDCOM: should output None Found."""
        fakeFile = io.StringIO("")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        outStr = parser.PrintDeceasedIndividuals()
        self.assertEqual(outStr, "\nDeceased Individuals\nNone Found\n")

    def test_print_multiple_deceased_individuals(self):
        """Multiple deceased individuals: should list all in sorted order."""
        fakeFile = io.StringIO("""0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
1 DEAT
2 DATE 15 JUN 2010
0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 16 MAY 2020
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        outStr = parser.PrintDeceasedIndividuals()
        self.assertIn("@I1@", outStr)
        self.assertIn("@I2@", outStr)
        self.assertIn("Earl /Grey/", outStr)
        self.assertIn("May /O'naise/", outStr)

    def test_living_and_deceased_mix(self):
        """Mix of living and deceased: only deceased individual should appear."""
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 16 MAY 2020
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        outStr = parser.PrintDeceasedIndividuals()
        self.assertIn("@I1@", outStr)
        self.assertNotIn("@I2@", outStr)


if __name__ == "__main__":
    unittest.main()
