import unittest
import io
from datetime import date
from GEDCOMParser import *


class TestCousinMarriage(unittest.TestCase):

    def test_first_cousins_married(self):  # positive case: first cousins married
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Father1 /Parent/
1 SEX M
1 FAMC @F4@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Mother2 /Parent/
1 SEX F
1 FAMC @F4@
1 FAMS @F3@
0 @I3@ INDI
1 NAME Cousin1 /Cous/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I4@ INDI
1 NAME Cousin2 /Cous/
1 SEX F
1 FAMC @F3@
1 FAMS @F1@
0 @I5@ INDI
1 NAME Grandfather /Grand/
1 SEX M
1 FAMS @F4@
0 @I6@ INDI
1 NAME Grandmother /Grand/
1 SEX F
1 FAMS @F4@
0 @I7@ INDI
1 NAME Mother1 /Parent/
1 SEX F
1 FAMS @F2@
0 @I8@ INDI
1 NAME Father2 /Parent/
1 SEX M
1 FAMS @F3@
0 @F1@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 MARR
2 DATE 10 MAY 2000
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I7@
1 CHIL @I3@
0 @F3@ FAM
1 HUSB @I8@
1 WIFE @I2@
1 CHIL @I4@
0 @F4@ FAM
1 HUSB @I5@
1 WIFE @I6@
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertNotEqual(parser.errorStr, "")
        self.assertIn(
            "ERROR: FAMILY: US18: @F1@: Husband @I3@ and Wife @I4@ are first cousins.",
            parser.errorStr,
        )

    def test_siblings_married(
        self,
    ):  # negative case: sibling marriage should trigger US16 but not US18
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Brother /Bro/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME Sister /Sis/
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 @F2@ FAM
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_uncle_niece_married(
        self,
    ):  # negative case: uncle/niece should trigger US17 but not US18
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Father /Parent/
1 SEX M
1 FAMC @F3@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Uncle /Unc/
1 SEX M
1 FAMC @F3@
1 FAMS @F1@
0 @I3@ INDI
1 NAME Niece /Nie/
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I3@
0 @F2@ FAM
1 HUSB @I1@
1 CHIL @I3@
0 @F3@ FAM
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_aunt_nephew_married(self):  # negative case: aunt/nephew should trigger US17 but not US18
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Mother /Parent/
1 SEX F
1 FAMC @F3@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Aunt /Aunt/
1 SEX F
1 FAMC @F3@
1 FAMS @F1@
0 @I3@ INDI
1 NAME Nephew /Neph/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I3@
1 WIFE @I2@
0 @F2@ FAM
1 WIFE @I1@
1 CHIL @I3@
0 @F3@ FAM
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_parent_child_married(
        self,
    ):  # negative case: parent-child marriage should not trigger US18
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Father /Parent/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Daughter /Dau/
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 @F2@ FAM
1 HUSB @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_unrelated_marriage(self):  # negative case: unrelated spouses
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Husband /Husb/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME Wife /Wife/
1 SEX F
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_second_cousins_married(
        self,
    ):  # negative case: second cousins should not trigger US18
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Husband /Husb/
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME Wife /Wife/
1 FAMC @F3@
1 FAMS @F1@
0 @I3@ INDI
1 NAME Father1 /Parent/
1 FAMC @F4@
1 FAMS @F2@
0 @I4@ INDI
1 NAME Father2 /Parent/
1 FAMC @F5@
1 FAMS @F3@
0 @I5@ INDI
1 NAME GFather1 /GParent/
1 FAMC @F6@
1 FAMS @F4@
0 @I6@ INDI
1 NAME GFather2 /GParent/
1 FAMC @F6@
1 FAMS @F5@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 @F2@ FAM
1 HUSB @I3@
1 CHIL @I1@
0 @F3@ FAM
1 HUSB @I4@
1 CHIL @I2@
0 @F4@ FAM
1 HUSB @I5@
1 CHIL @I3@
0 @F5@ FAM
1 HUSB @I6@
1 CHIL @I4@
0 @F6@ FAM
1 CHIL @I5@
1 CHIL @I6@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_missing_parent_family(self):  # edge case: missing parent family details
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Husband /Husb/
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME Wife /Wife/
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkCousinMarriage()
        self.assertEqual(parser.errorStr, "")


if __name__ == "__main__":
    unittest.main()
