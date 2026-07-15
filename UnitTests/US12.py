import unittest
import io
from datetime import date
from GEDCOMParser import *

class TestForBigamyValidation(unittest.TestCase):

    def test_marriage_no_remarriage(self): #normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
3 NOTE The above will show no error, because it has no divorce or remarriage""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckBigamy()
        self.assertEqual(parser.errorStr, "") #function worked if errorStr is still empty

    def test_remarried_after_partner_death(self): #possible, albeit tragic, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1962
1 FAMS @F1@
0 @I3@ INDI
1 NAME Jay /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1990
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 14 MAY 1964
3 NOTE The above will show no error, because it has remarriage after the wife passes""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckBigamy()
        self.assertEqual(parser.errorStr, "") #function worked if errorStr is still empty

    def test_remarriage_after_divorce(self): #possible, normal, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 FAMS @F1@
0 @I3@ INDI
1 NAME Jay /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1990
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
1 DIV
2 DATE 12 MAY 1962
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 14 MAY 1964
3 NOTE The above will show no error, because it has remarriage after the divorce""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckBigamy()
        self.assertEqual(parser.errorStr, "") #empty, there was no error

    def test_remarriage_while_married(self): #the case where the person is committing bigamy, there will be error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1965
1 FAMS @F1@
0 @I3@ INDI
1 NAME Jay /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1990
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 MARR
2 DATE 14 MAY 1964
3 NOTE The above will show error, because it has remarriage while already married""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckBigamy()
        self.assertNotEqual(parser.errorStr, "") #not empty, there was an error


    def test_marriages_no_marriage_date_defined(self): #unclear, show error for unclear marriage time
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMS @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1962
1 FAMS @F1@
0 @I3@ INDI
1 NAME Jay /O'naise/
1 SEX F
1 BIRT
2 DATE 12 MAY 1930
1 DEAT
2 DATE 12 MAY 1990
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 @F2@ FAM
1 HUSB @I1@
1 WIFE @I3@
3 NOTE The above will show error, because it has unclear marriage date(s)""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckBigamy()
        self.assertNotEqual(parser.errorStr, "") #not empty, there was an error: Unclear Marriage Date


if __name__ == '__main__':
    unittest.main()