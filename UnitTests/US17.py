import unittest
import io
from datetime import date
from GEDCOMParser import *


class TestAuntUncleMarriage(unittest.TestCase):

    def test_uncle_married_to_niece(self):  # positive case: uncle married to niece
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
0 @I4@ INDI
1 NAME Grandfather /Grand/
1 SEX M
1 FAMS @F3@
0 @I5@ INDI
1 NAME Grandmother /Grand/
1 SEX F
1 FAMS @F3@
0 @I6@ INDI
1 NAME Mother /Parent/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I3@
1 MARR
2 DATE 10 MAY 2000
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I6@
1 CHIL @I3@
0 @F3@ FAM
1 HUSB @I4@
1 WIFE @I5@
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkAuntUncleMarriage()
        self.assertNotEqual(parser.errorStr, "")
        self.assertIn(
            "ERROR: FAMILY: US17: @F1@: Husband @I2@ is uncle of Wife @I3@.",
            parser.errorStr,
        )

    def test_aunt_married_to_nephew(self):  # positive case: aunt married to nephew
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
0 @I4@ INDI
1 NAME Grandfather /Grand/
1 SEX M
1 FAMS @F3@
0 @I5@ INDI
1 NAME Grandmother /Grand/
1 SEX F
1 FAMS @F3@
0 @I6@ INDI
1 NAME Father /Parent/
1 SEX M
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I3@
1 WIFE @I2@
1 MARR
2 DATE 10 MAY 2000
0 @F2@ FAM
1 HUSB @I6@
1 WIFE @I1@
1 CHIL @I3@
0 @F3@ FAM
1 HUSB @I4@
1 WIFE @I5@
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkAuntUncleMarriage()
        self.assertNotEqual(parser.errorStr, "")
        self.assertIn(
            "ERROR: FAMILY: US17: @F1@: Wife @I2@ is aunt of Husband @I3@.",
            parser.errorStr,
        )

    def test_marriage_of_cousins(
        self,
    ):  # negative case: cousins married, should not trigger US17
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
0 @F1@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 MARR
2 DATE 10 MAY 2000
0 @F2@ FAM
1 HUSB @I1@
1 CHIL @I3@
0 @F3@ FAM
1 WIFE @I2@
1 CHIL @I4@
0 @F4@ FAM
1 CHIL @I1@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkAuntUncleMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_marriage_no_parent_family(
        self,
    ):  # negative case: one individual has no parent family, should not trigger US17
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Husband /Husb/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME Wife /Wife/
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @I3@ INDI
1 NAME Father /Parent/
1 SEX M
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 10 MAY 2000
0 @F2@ FAM
1 HUSB @I3@
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkAuntUncleMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_marriage_no_parent_siblings(
        self,
    ):  # negative case: parents have no siblings, should not trigger US17
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Husband /Husb/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME Wife /Wife/
1 SEX F
1 FAMC @F3@
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 10 MAY 2000
0 @F2@ FAM
1 CHIL @I1@
0 @F3@ FAM
1 CHIL @I2@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkAuntUncleMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_parent_id_not_in_individuals(
        self,
    ):  # negative case: parent ID is not in individuals dict
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Husband /Husb/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME Wife /Wife/
1 SEX F
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 @F2@ FAM
1 HUSB @I3@
1 CHIL @I1@
""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()
        parser.checkAuntUncleMarriage()
        self.assertEqual(parser.errorStr, "")

    def test_parent_is_spouse(
        self,
    ):  # negative case: parent is the spouse itself (parent-child marriage, not aunt-uncle)
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Parent /Parent/
1 SEX M
1 FAMS @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME Child /Child/
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
        parser.checkAuntUncleMarriage()
        self.assertEqual(parser.errorStr, "")


if __name__ == "__main__":
    unittest.main()
