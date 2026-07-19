import unittest
import io
from GEDCOMParser import GEDCOMParser
from models import Individual, Family


class TestUS15(unittest.TestCase):
    """
    US15: No marriage to descendants
    """

    def test_marriage_to_descendant_valid(self):
        # Normal family, husband and wife are not descendants of each other
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        fam1 = Family("@F1@")
        fam1.husband_id = "@I1@"
        fam1.wife_id = "@I2@"
        parser.families["@F1@"] = fam1

        i1 = Individual("@I1@")
        i2 = Individual("@I2@")
        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckMarriageToDescendants()
        self.assertEqual(parser.errorStr, "")

    def test_marriage_to_descendant_husband_is_descendant(self):
        # Husband is a child (descendant) of the wife
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Family 1: wife @I2@ is parent of husband @I1@
        fam_parent = Family("@F_parent@")
        fam_parent.wife_id = "@I2@"
        fam_parent.children = {"@I1@"}
        parser.families["@F_parent@"] = fam_parent

        # Family 2: husband @I1@ is married to @I2@
        fam_marriage = Family("@F_marriage@")
        fam_marriage.husband_id = "@I1@"
        fam_marriage.wife_id = "@I2@"
        parser.families["@F_marriage@"] = fam_marriage

        i1 = Individual("@I1@")
        i1.child = {"@F_parent@"}
        i2 = Individual("@I2@")

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckMarriageToDescendants()
        # Verify the exact, explicit error output
        expected = "\nERROR: FAMILY: US15: @F_marriage@: Husband @I1@ is a descendant of Wife @I2@.\n"
        self.assertEqual(parser.errorStr, expected)

    def test_marriage_to_descendant_wife_is_descendant(self):
        # Wife is a grandchild (descendant) of the husband
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Family 1: Husband @I1@ has child @I3@ (parent of wife @I2@)
        fam1 = Family("@F1@")
        fam1.husband_id = "@I1@"
        fam1.children = {"@I3@"}
        parser.families["@F1@"] = fam1

        # Family 2: Parent @I3@ has child @I2@ (wife)
        fam2 = Family("@F2@")
        fam2.husband_id = "@I3@"
        fam2.children = {"@I2@"}
        parser.families["@F2@"] = fam2

        # Family 3: Husband @I1@ is married to grandchild @I2@
        fam3 = Family("@F3@")
        fam3.husband_id = "@I1@"
        fam3.wife_id = "@I2@"
        parser.families["@F3@"] = fam3

        i1 = Individual("@I1@")
        i2 = Individual("@I2@")
        i2.child = {"@F2@"}
        i3 = Individual("@I3@")
        i3.child = {"@F1@"}

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2
        parser.individuals["@I3@"] = i3

        parser.CheckMarriageToDescendants()
        # Verify the exact, explicit error output
        expected = (
            "\nERROR: FAMILY: US15: @F3@: Wife @I2@ is a descendant of Husband @I1@.\n"
        )
        self.assertEqual(parser.errorStr, expected)

    def test_marriage_to_uncle_not_descendant(self):
        # Uncle married to niece: collateral relationship, not a descendant relationship (valid under US15)
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Family 1: Grandparents have Mother @I2@ and Uncle @I3@
        fam_gp = Family("@F_gp@")
        fam_gp.husband_id = "@I_gpf@"
        fam_gp.wife_id = "@I_gpm@"
        fam_gp.children = {"@I2@", "@I3@"}
        parser.families["@F_gp@"] = fam_gp

        # Family 2: Mother @I2@ has child Niece @I4@
        fam_parent = Family("@F_parent@")
        fam_parent.wife_id = "@I2@"
        fam_parent.children = {"@I4@"}
        parser.families["@F_parent@"] = fam_parent

        # Family 3: Uncle @I3@ marries Niece @I4@
        fam_marriage = Family("@F_marriage@")
        fam_marriage.husband_id = "@I3@"
        fam_marriage.wife_id = "@I4@"
        parser.families["@F_marriage@"] = fam_marriage

        # Define individuals and set their parent-family links
        igpf = Individual("@I_gpf@")
        igpm = Individual("@I_gpm@")
        i2 = Individual("@I2@")
        i2.child = {"@F_gp@"}
        i3 = Individual("@I3@")
        i3.child = {"@F_gp@"}
        i4 = Individual("@I4@")
        i4.child = {"@F_parent@"}

        parser.individuals["@I_gpf@"] = igpf
        parser.individuals["@I_gpm@"] = igpm
        parser.individuals["@I2@"] = i2
        parser.individuals["@I3@"] = i3
        parser.individuals["@I4@"] = i4

        parser.CheckMarriageToDescendants()
        # Should not flag descendant error because uncle is a collateral relative, not a descendant
        self.assertEqual(parser.errorStr, "")

    def test_marriage_to_descendant_cycle_prevention(self):
        # Edge case / failure check: Cyclic parent-child relationship (prevents infinite recursion)
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        parser.errorStr = ""

        # Family 1: Husband @I1@ is a child of his own family
        fam1 = Family("@F1@")
        fam1.husband_id = "@I1@"
        fam1.wife_id = "@I2@"
        fam1.children = {"@I1@"}
        parser.families["@F1@"] = fam1

        i1 = Individual("@I1@")
        i1.child = {"@F1@"}  # Cyclic parent link
        i2 = Individual("@I2@")

        parser.individuals["@I1@"] = i1
        parser.individuals["@I2@"] = i2

        parser.CheckMarriageToDescendants()
        # Check that it safely exits and formats the expected output
        expected = (
            "\nERROR: FAMILY: US15: @F1@: Husband @I1@ is a descendant of Wife @I2@.\n"
        )
        self.assertEqual(parser.errorStr, expected)


if __name__ == "__main__":
    unittest.main()
