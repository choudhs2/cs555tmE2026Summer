import unittest
from io import StringIO
from GEDCOMParser import GEDCOMParser


class TestMarriageAfterFourteen(unittest.TestCase):
    # 1: Marriage well after age 14
    def test_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 FAMS @F1@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 1970"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 2: Husband married under 14
    def test_husband_not_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1990\n1 FAMS @F1@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 1990"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertIn("US11", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)

    # 3: Wife married under 14
    def test_wife_not_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 FAMS @F1@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1990\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 2000"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertIn("US11", parser.errorStr)
        self.assertIn("@I2@", parser.errorStr)

    # 4: Marriage exactly at 14
    def test_exact_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1986\n1 FAMS @F1@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 2000"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 5: No marriage date
    def test_no_marriage_date(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1990\n1 FAMS @F1@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1992\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 6: Both married under 14
    def test_both_not_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1990\n1 FAMS @F1@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1992\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 2000"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertIn("US11", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)
        self.assertIn("@I2@", parser.errorStr)

    # 7: Individual married twice with one underage
    def test_double_one_not_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 FAMS @F1@\n1 FAMS @F2@\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @I3@ INDI\n1 NAME June /Bug/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1990\n1 FAMS @F2@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 1970\n0 @F2@ FAM\n1 HUSB @I1@\n1 WIF @I3@\n1 MARR\n2 DATE 11 MAY 2000"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.MarriageAfterFourteen()
        # print(parser.errorStr)
        self.assertIn("US11", parser.errorStr)
        self.assertIn("@I3@", parser.errorStr)


if __name__ == "__main__":
    unittest.main()
