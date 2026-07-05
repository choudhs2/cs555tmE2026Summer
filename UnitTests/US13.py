import unittest
import io
from datetime import date
from GEDCOMParser import GEDCOMParser
from models import Individual, Family


class TestUS13(unittest.TestCase):
    """
    US13: Sibling spacing (more than 8 months or less than 2 days)
    """

    def test_sibling_spacing_valid_twins(self):
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Family with twins born 1 day apart
        fam = Family("@F1@")
        fam.children = {"@I1@", "@I2@"}
        parser.families["@F1@"] = fam

        i1 = Individual("@I1@")
        i1.birthday = date(2020, 5, 10)
        i2 = Individual("@I2@")
        i2.birthday = date(2020, 5, 11)  # 1 day apart

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckSiblingSpacing()
        self.assertEqual(parser.errorStr, "")

    def test_sibling_spacing_invalid(self):
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Siblings born 2 days apart (not twins, but less than 8 months)
        fam = Family("@F1@")
        fam.children = {"@I1@", "@I2@"}
        parser.families["@F1@"] = fam

        i1 = Individual("@I1@")
        i1.birthday = date(2020, 5, 10)
        i2 = Individual("@I2@")
        i2.birthday = date(2020, 5, 12)  # 2 days apart

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckSiblingSpacing()
        # Verify the exact, explicit error output
        expected = "\nERROR: FAMILY: US13: @F1@: Siblings @I1@ and @I2@ have invalid spacing of 0 months\n"
        self.assertEqual(parser.errorStr, expected)

    def test_sibling_spacing_valid_large_gap(self):
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Siblings born 9 months apart
        fam = Family("@F1@")
        fam.children = {"@I1@", "@I2@"}
        parser.families["@F1@"] = fam

        i1 = Individual("@I1@")
        i1.birthday = date(2020, 5, 10)
        i2 = Individual("@I2@")
        i2.birthday = date(2021, 2, 10)  # 9 months apart

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckSiblingSpacing()
        self.assertEqual(parser.errorStr, "")

    def test_sibling_spacing_multiple_siblings(self):
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Triplet-like spacing and one invalid spacing
        fam = Family("@F1@")
        fam.children = {"@I1@", "@I2@", "@I3@"}
        parser.families["@F1@"] = fam

        i1 = Individual("@I1@")
        i1.birthday = date(2020, 5, 10)
        i2 = Individual("@I2@")
        i2.birthday = date(2020, 5, 10)
        i3 = Individual("@I3@")
        i3.birthday = date(2020, 8, 10)

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2
        parser.individuals["@I3@"] = i3

        parser.CheckSiblingSpacing()
        # Verify the exact, explicit list of error outputs
        expected = (
            "\nERROR: FAMILY: US13: @F1@: Siblings @I1@ and @I3@ have invalid spacing of 3 months\n"
            "ERROR: FAMILY: US13: @F1@: Siblings @I2@ and @I3@ have invalid spacing of 3 months\n"
        )
        self.assertEqual(parser.errorStr, expected)

    def test_sibling_spacing_missing_birthday(self):
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # One sibling missing birthday should be skipped silently
        fam = Family("@F1@")
        fam.children = {"@I1@", "@I2@"}
        parser.families["@F1@"] = fam

        i1 = Individual("@I1@")
        i1.birthday = date(2020, 5, 10)
        i2 = Individual("@I2@")
        i2.birthday = None

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckSiblingSpacing()
        self.assertEqual(parser.errorStr, "")

    def test_sibling_spacing_single_child(self):
        # Edge case / failure check: Family with only 1 child (cannot violate sibling spacing)
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        fam = Family("@F1@")
        fam.children = {"@I1@"}
        parser.families["@F1@"] = fam

        i1 = Individual("@I1@")
        i1.birthday = date(2020, 5, 10)
        parser.individuals["@I1@"] = i1

        parser.CheckSiblingSpacing()
        self.assertEqual(parser.errorStr, "")


if __name__ == "__main__":
    unittest.main()
