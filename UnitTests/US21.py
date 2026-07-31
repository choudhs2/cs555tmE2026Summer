import unittest
import io
from datetime import date
from GEDCOMParser import *


class TestMarriedPrinting(unittest.TestCase):

    def test_print_marriage_before_death(self):  # normal case, prints both individuals
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 16 MAY 2027
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
3 NOTE The above will show a table, because it is before anyone dies""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        outStr = parser.PrintLivingMarried()
        self.assertNotEqual(
            outStr, "Living Married Individuals\nNone Found\n"
        )  # function worked if outStr is not the "None Found" string

    def test_print_married_same_as_death(self):  # should only print header
        fakeFile = fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 11 MAY 1960
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
1 DEAT 
2 DATE 15 JUN 1991
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
3 NOTE The above will show None Found, because it is at the same time""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        outStr = parser.PrintLivingMarried()
        self.assertEqual(
            outStr, "Living Married Individuals\nNone Found\n"
        )  # function should return the "None Found" since we only have one marriage

    def test_print_marriage_with_death_unmarried_indiv(self): #someone is not married, should not be counted
        fakeFile = fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 10 MAY 1960
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
1 DEAT 
2 DATE 15 JUN 1991
1 FAMS @F1@
0 @I3@ INDI
1 NAME Jay /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
3 NOTE The above will show None Found, because it is after someone dies and the other person is not married""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        outStr = parser.PrintLivingMarried()
        self.assertEqual(outStr, "Living Married Individuals\nNone Found\n")  # None Found, because marriage ended and other person is single

    def test_marriage_no_death_defined(self):
        fakeFile = fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
3 NOTE The above will show no error, because there is no death yet to check against""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        outStr = parser.PrintLivingMarried()
        self.assertNotEqual(outStr, "Living Married Individuals\nNone Found\n")  # no error


if __name__ == "__main__":
    unittest.main()
