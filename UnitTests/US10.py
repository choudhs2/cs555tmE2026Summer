import unittest
import io
from datetime import date
from GEDCOMParser import *

class TestMarriedAndDeathDateValidation(unittest.TestCase):

    def test_marriage_before_death(self): #normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 16 MAY 1991
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
3 NOTE The above will show no error, because it is before anyone dies""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckMarriedBeforeDeaths()
        self.assertEqual(parser.errorStr, "") #function worked if errorStr is still empty

    def test_married_same_as_death(self): #technically possible, albeit tragic, no error
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
3 NOTE The above will show no error, because it is at the same time""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckMarriedBeforeDeaths()
        self.assertEqual(parser.errorStr, "") #function worked if errorStr is still empty

    def test_marriage_after_death(self):
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
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
3 NOTE The above will show error, because it is after someone dies""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckMarriedBeforeDeaths()
        self.assertNotEqual(parser.errorStr, "") #not empty, there was an error

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
        parser.extract_entities() #get individuals and families
        parser.CheckMarriedBeforeDeaths()
        self.assertEqual(parser.errorStr, "") #empty, there was no error


    def test_marriage_no_marriage_date_defined(self):
        fakeFile = fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 13 APR 1999
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 BIRT
2 DATE 13 JUL 1947
1 BIRT
2 DATE 11 SEP 2000
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
3 NOTE The above will show no error, but it is a weird case where marriage date was not defined""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.CheckMarriedBeforeDeaths()
        self.assertEqual(parser.errorStr, "") #empty, there was no error


if __name__ == '__main__':
    unittest.main()