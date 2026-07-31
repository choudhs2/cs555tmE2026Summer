import unittest
from io import StringIO
from GEDCOMParser import GEDCOMParser

class TestUniqueNameAndBirth(unittest.TestCase):
    #1: Two individuals with different names and birthdays
    def test_unique(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n0 @I2@ INDI\n1 NAME May /O'naise/\n1 SEX F\n1 BIRT\n2 DATE 13 JUL 1947"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.UniqueNameandBirth()
        self.assertEqual(parser.errorStr, "")

    #2: Two individuals with the same name and birthday
    def test_one_duplicate(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n0 @I2@ INDI\n1 NAME Earl /Grey/\n1 SEX F\n1 BIRT\n2 DATE 13 APR 1945"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.UniqueNameandBirth()
        self.assertIn("US19", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)
        self.assertIn("@I2@", parser.errorStr)

    #3: Same name, different birthday
    def test_duplicate_name(self):
            individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n0 @I2@ INDI\n1 NAME Earl /Grey/\n1 SEX F\n1 BIRT\n2 DATE 13 APR 1955"""
            parser = GEDCOMParser(StringIO(individuals))
            parser.extract_entities()
            parser.errorStr = ""
            parser.UniqueNameandBirth()
            self.assertEqual(parser.errorStr, "")
            
    #4: Same Birthday, different name
    def test_duplicate_birthday(self):
            individuals = """0 @I1@ INDI\n1 NAME Earla /Gray/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945\n0 @I2@ INDI\n1 NAME Earl /Grey/\n1 SEX F\n1 BIRT\n2 DATE 13 APR 1945"""
            parser = GEDCOMParser(StringIO(individuals))
            parser.extract_entities()
            parser.errorStr = ""
            parser.UniqueNameandBirth()
            self.assertEqual(parser.errorStr, "")

if __name__ =="__main__":
    unittest.main()