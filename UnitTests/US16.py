import unittest
import io
from datetime import date
from GEDCOMParser import *

class TestForSiblingMarriageValidation(unittest.TestCase):

    def test_marriage_not_siblings(self): #normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 FAMC @F3@
1 FAMS @F1@
0 @I3@ INDI
1 NAME P1 /O'naise/
1 SEX F
1 FAMS @F2@
0 @I4@ INDI
1 NAME P2 /O'naise/
1 SEX F
1 FAMS @F2@
0 @I5@ INDI
1 NAME P3 /O'naise/
1 SEX F
1 FAMS @F3@
0 @I6@ INDI
1 NAME P4 /O'naise/
1 SEX F
1 FAMS @F3@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
0 @F2@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I1@
0 @F3@ FAM
1 HUSB @I5@
1 WIFE @I6@
1 CHIL @I2@
3 NOTE The above will show no error, because they are not siblings""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.checkSiblingMarriage()
        self.assertEqual(parser.errorStr, "") #function worked if errorStr is still empty

    def test_marriage_of_siblings(self): #error case, siblings
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @I3@ INDI
1 NAME P1 /O'naise/
1 SEX F
1 FAMS @F2@
0 @I4@ INDI
1 NAME P2 /O'naise/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
0 @F2@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I1@
1 CHIL @I2@
3 NOTE The above will show no error, because they are not siblings""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.checkSiblingMarriage()
        self.assertNotEqual(parser.errorStr, "") #They are siblings, they are not valid to be married

    def test_marriage_no_parent_family(self): #not error case, one person has no parent family defined, this is ok
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME May /O'naise/
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @I3@ INDI
1 NAME P1 /O'naise/
1 SEX F
1 FAMS @F2@
0 @I4@ INDI
1 NAME P2 /O'naise/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 11 MAY 1960
0 @F2@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I2@
3 NOTE The above will show no error, because they are not siblings""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.checkSiblingMarriage()
        self.assertEqual(parser.errorStr, "") #They are siblings, they are not valid to be married

    def test_marriage_of_self(self): #error case, same person
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 FAMC @F2@
1 FAMS @F1@
0 @I3@ INDI
1 NAME P1 /O'naise/
1 SEX F
1 FAMS @F2@
0 @I4@ INDI
1 NAME P2 /O'naise/
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I1@
1 MARR
2 DATE 11 MAY 1960
0 @F2@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I1@
3 NOTE The above will show no error, because they are not siblings""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities() #get individuals and families
        parser.checkSiblingMarriage()
        self.assertNotEqual(parser.errorStr, "") #They are siblings, they are not valid to be married

if __name__ == '__main__':
    unittest.main()