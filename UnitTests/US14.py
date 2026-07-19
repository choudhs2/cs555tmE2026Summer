import unittest
from io import StringIO
from GEDCOMParser import GEDCOMParser


class TestLessThanFiveBirths(unittest.TestCase):
    # 1: Extactly five siblings on the same date
    def test_exactly_five(self):
        individuals = """0 @I1@ INDI\n1 NAME CHild /One/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I2@ INDI\n1 NAME Child /Two/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I3@ INDI\n1 NAME Child/Three/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I4@ INDI\n1 NAME Child/ Four/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I5@ INDI\n1 NAME Child /Five/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I6@ INDI\n1 NAME Parent /One/\n1 SEX M\n1 FAMS @F1@\n1 FAMS @F1@\n0 @I7@ INDI\n1 NAME Parent /Two/\n1 SEX F\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I6@\n1 WIF @I7@\n1 CHIL @I1@\n1 CHIL @I2@\n1 CHIL @I3@\n1 CHIL @I4@\n1 CHIL @I5@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.LessThanFiveBirths()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 2: Six siblings on same date
    def test_six_siblings(self):
        individuals = """0 @I1@ INDI\n1 NAME CHild /One/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I2@ INDI\n1 NAME Child /Two/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I3@ INDI\n1 NAME Child/Three/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I4@ INDI\n1 NAME Child/ Four/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I5@ INDI\n1 NAME Child /Five/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I6@ INDI\n1 NAME Child /Six/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I7@ INDI\n1 NAME Parent /One/\n1 SEX M\n1 FAMS @F1@\n1 FAMS @F1@\n0 @I8@ INDI\n1 NAME Parent /Two/\n1 SEX F\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I7@\n1 WIF @I8@\n1 CHIL @I1@\n1 CHIL @I2@\n1 CHIL @I3@\n1 CHIL @I4@\n1 CHIL @I5@\n1 CHIL @I6@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.LessThanFiveBirths()
        # print(parser.errorStr)
        self.assertIn("US14", parser.errorStr)
        self.assertIn("@F1@", parser.errorStr)

    # 3: six sibling but different dates
    def test_six_siblings_different(self):
        individuals = """0 @I1@ INDI\n1 NAME CHild /One/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I2@ INDI\n1 NAME Child /Two/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2002\n1 FAMC @F1@\n0 @I3@ INDI\n1 NAME Child/Three/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2003\n1 FAMC @F1@\n0 @I4@ INDI\n1 NAME Child/ Four/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2004\n1 FAMC @F1@\n0 @I5@ INDI\n1 NAME Child /Five/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2005\n1 FAMC @F1@\n0 @I6@ INDI\n1 NAME Child /Six/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2006\n1 FAMC @F1@\n0 @I7@ INDI\n1 NAME Parent /One/\n1 SEX M\n1 FAMS @F1@\n1 FAMS @F1@\n0 @I8@ INDI\n1 NAME Parent /Two/\n1 SEX F\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I7@\n1 WIF @I8@\n1 CHIL @I1@\n1 CHIL @I2@\n1 CHIL @I3@\n1 CHIL @I4@\n1 CHIL @I5@\n1 CHIL @I6@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.LessThanFiveBirths()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 4: Two families with no errors
    def test_two_families(self):
        individuals = """0 @I1@ INDI\n1 NAME CHild /One/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I2@ INDI\n1 NAME Child /Two/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2010\n1 FAMC @F1@\n0 @I3@ INDI\n1 NAME Child/Three/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I4@ INDI\n1 NAME Child/ Four/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I5@ INDI\n1 NAME Child /Five/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I6@ INDI\n1 NAME Child /Six/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I7@ INDI\n1 NAME Parent /One/\n1 SEX M\n1 FAMS @F1@\n1 FAMS @F1@\n0 @I8@ INDI\n1 NAME Parent /Two/\n1 SEX F\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I7@\n1 WIF @I8@\n1 CHIL @I1@\n1 CHIL @I2@\n1 CHIL @I3@\n1 CHIL @I4@\n1 CHIL @I5@\n1 CHIL @I6@\n0 @I9@ INDI\n1 NAME Chile /Seven/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2015\n1 FAMC @F2@\n0 @I10@ INDI\n1 NAME Child /Eight/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2016\n1 FAMC @F2@\n0 @I11@ INDI\n1 NAME Parent /Three/\n1 SEX M\n1 FAMS @F2@\n0 @I12@ INDI\n1 NAME Parent /Four/\n1 SEX F\n1 FAMS @F2@\n0 @F2@ FAM\n1 HUSB @I11@\n1 WIF @I12@\n1 CHIL @I9@\n1 CHIL @I10@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.LessThanFiveBirths()
        # print(parser.errorStr)
        self.assertEqual(parser.errorStr, "")

    # 5: One family with no erros and another with six on the same date
    def test_six_siblings_and_no_errors(self):
        individuals = """0 @I1@ INDI\n1 NAME CHild /One/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I2@ INDI\n1 NAME Child /Two/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I3@ INDI\n1 NAME Child/Three/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I4@ INDI\n1 NAME Child/ Four/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I5@ INDI\n1 NAME Child /Five/\n1 SEX M\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I6@ INDI\n1 NAME Child /Six/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2000\n1 FAMC @F1@\n0 @I7@ INDI\n1 NAME Parent /One/\n1 SEX M\n1 FAMS @F1@\n1 FAMS @F1@\n0 @I8@ INDI\n1 NAME Parent /Two/\n1 SEX F\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I7@\n1 WIF @I8@\n1 CHIL @I1@\n1 CHIL @I2@\n1 CHIL @I3@\n1 CHIL @I4@\n1 CHIL @I5@\n1 CHIL @I6@\n0 @I9@ INDI\n1 NAME Chile /Seven/\n1 SEX M\n1 BIRT\n2 DATE 1 Jan 2015\n1 FAMC @F2@\n0 @I10@ INDI\n1 NAME Child /Eight/\n1 SEX F\n1 BIRT\n2 DATE 1 JAN 2016\n1 FAMC @F2@\n0 @I11@ INDI\n1 NAME Parent /Three/\n1 SEX M\n1 FAMS @F2@\n0 @I12@ INDI\n1 NAME Parent /Four/\n1 SEX F\n1 FAMS @F2@\n0 @F2@ FAM\n1 HUSB @I11@\n1 WIF @I12@\n1 CHIL @I9@\n1 CHIL @I10@"""
        parser = GEDCOMParser(StringIO(individuals))
        parser.extract_entities()
        parser.errorStr = ""
        parser.LessThanFiveBirths()
        # print(parser.errorStr)
        self.assertIn("US14", parser.errorStr)
        self.assertIn("@F1@", parser.errorStr)
        self.assertNotIn("@F2@", parser.errorStr)


if __name__ == "__main__":
    unittest.main()
