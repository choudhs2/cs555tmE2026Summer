import unittest
from io import StringIO
from GEDCOMParser import GEDCOMParser


class TestUniqueIIDs(unittest.TestCase):

    # 1: No duplicates
    def test_all_unique(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n0 @I2@ INDI\n1 NAME May /O'naise/\n0 @I3@ INDI\n1 NAME Ash /Grey/\n0 @I4@ INDI\n1 NAME Mira /Grey/"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.checkUniqueIDs()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 2: One Duplicate
    def test_one_duplicate(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n0 @I1@ INDI\n1 NAME May /O'naise/\n0 @I3@ INDI\n1 NAME Ash /Grey/\n0 @I4@ INDI\n1 NAME Mira /Grey/"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.checkUniqueIDs()
        # print(parser.errorStr)
        self.assertIn("US04", parser.errorStr)
        self.assertIn("@I1@", parser.individuals)
        self.assertIn("@I3@", parser.individuals)
        self.assertIn("@I4@", parser.individuals)

    # 3: One Individual
    def test_one_individual(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.checkUniqueIDs()
        # print(parser.errorStr)
        self.assertIn(parser.errorStr, "")

    # 4: No Individuals
    def test_no_individuals(self):
        individuals = """0 HEAD\n0 NOTE Empty"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.checkUniqueIDs()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 5: Two Duplicates
    def test_two_duplicates(self):
        individuals = """0 @I1@ INDI\n1 NAME Earl /Grey/\n0 @I1@ INDI\n1 NAME May /O'naise/\n0 @I3@ INDI\n1 NAME Ash /Grey/\n0 @I3@ INDI\n1 NAME Mira /Grey/"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.checkUniqueIDs()
        # print(parser.errorStr)
        self.assertIn("US04", parser.errorStr)
        self.assertIn("@I1@", parser.errorStr)
        self.assertIn("@I3@", parser.errorStr)


if __name__ == "__main__":
    unittest.main()
