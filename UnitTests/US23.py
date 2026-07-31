import unittest 
from io import StringIO
from GEDCOMParser import GEDCOMParser

class TestRejectIllegitimateDates(unittest.TestCase):
    #1: A valid date
    def test_one_valid_date(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 13 APR 1945"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.RejectIllegitimateDates()
        self.assertEqual(parser.errorStr, "")

    #2: One invalid birth date in february non-leap year
    def test_one_date_nonexistent(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 30 FEB 1990"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.RejectIllegitimateDates()
        self.assertIn("US23", parser.errorStr)

    #3: Valid Feb 29 during a leap year
    def test_valid_date_leap_year(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 29 FEB 2000"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.RejectIllegitimateDates()
        self.assertEqual(parser.errorStr, "")

    #4: Feb 29 in a non leap year
    def test_invalid_date(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 29 FEB 1990"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.RejectIllegitimateDates()
        self.assertIn("US23", parser.errorStr)

    #5: One invalid date different month
    def test_invalid_date_two(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n1 SEX M\n1 BIRT\n2 DATE 31 APR 2000"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.RejectIllegitimateDates()
        self.assertIn("US23", parser.errorStr)

if __name__== "__main__":
    unittest.main() 