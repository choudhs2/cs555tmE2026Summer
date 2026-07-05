import unittest
from io import StringIO
from GEDCOMParser import GEDCOMParser

class TestCheckCorrectGenderForRole(unittest.TestCase):
    #1: Only correct genders
    def test_no_errors(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckCorrectGenderForRole()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    #2: Husband has the wrong gender
    def test_wrong_gender_husband(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX F\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckCorrectGenderForRole()
        # print(parser.errorStr)
        self.assertIn("US07", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)

    #3: Wife has the wrong gender
    def test_wrong_gender_wife(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX M\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckCorrectGenderForRole()
        # print(parser.errorStr)     
        self.assertIn("US07", parser.errorStr)
        self.assertIn("@I2@", parser.errorStr)

    #4: Husband as an individual does not exist
    def test_missing_husband_id(self):
        individuals = """0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckCorrectGenderForRole()
        # print(parser.errorStr)     
        self.assertEqual(parser.errorStr, "")

    #5: Neither husband nor wife as individuals exist
    def test_missing_husband_and_wife(self):
        individuals = """0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckCorrectGenderForRole()
        # print(parser.errorStr)     
        self.assertEqual(parser.errorStr, "")

    #6: Individuals exist but no family exists
    def test_no_families(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.CheckCorrectGenderForRole()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

if __name__ == "__main__":
    unittest.main()
