import unittest
from io import StringIO
from GEDCOMParser import GEDCOMParser
class TestCheckPossibleDates(unittest.TestCase):
   
    #1: All dates before current date
    def test_all_valid(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 DEAT\n2 DATE 12 JUN 1990\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 1970\n1 DIV\n2 DATE 11 MAY 1980"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")
    #2: Birthday in the future
    def test_birthday_in_future(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 2068"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertIn("US08", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)
        self.assertIn("Birthday", parser.errorStr)

    #3: Death date in the future
    def test_death_date_in_future(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 DEAT\n2 DATE 12 JUN 2099"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertIn("US08", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)
        self.assertIn("Death date", parser.errorStr)

    #4: No birthday at all
    def test_no_birthdate(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    #5: Birthday but no death date
    def test_no_deathdate(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    #6: Marriage date in the future
    def test_marriage_after_current(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 DEAT\n2 DATE 12 JUN 1990\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 2099"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertIn("US08", parser.errorStr)
        self.assertIn("Married date", parser.errorStr)

    #7: Divorce date in the future
    def test_divorce_after_current(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n1 DEAT\n2 DATE 12 JUN 1990\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIF @I2@\n1 MARR\n2 DATE 11 MAY 1970\n1 DIV\n2 DATE 11 MAY 2099"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertIn("US08", parser.errorStr)
        self.assertIn("Divorced date", parser.errorStr)

    #8: No individual
    def test_no_indiv(self):
        individuals = """0 HEAD\n0 NOTE Empty"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckPossibleDates()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

if __name__ == "__main__":
    unittest.main()