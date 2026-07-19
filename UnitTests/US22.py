import unittest
import io
from datetime import date
from GEDCOMParser import *


class TestImpossibleAgeValidation(unittest.TestCase):

    def test_normal_age_with_death(self):  # normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 16 MAY 1991""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        parser.CheckImpossibleAges()
        self.assertEqual(
            parser.errorStr, ""
        )  # function worked if errorStr is still empty

    def test_normal_age_with_no_death(self):  # normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        parser.CheckImpossibleAges()
        self.assertEqual(
            parser.errorStr, ""
        )  # function worked if errorStr is still empty

    def test_big_but_valid_age_with_death(self):  # normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1878
1 DEAT
2 DATE 16 MAY 1991""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        parser.CheckImpossibleAges()
        self.assertEqual(
            parser.errorStr, ""
        )  # function worked if errorStr is still empty

    def test_big_but_valid_age_with_no_death(self):  # normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1878""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        parser.CheckImpossibleAges()
        self.assertEqual(
            parser.errorStr, ""
        )  # function worked if errorStr is still empty

    def test_invalid_age_with_death(self):  # normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1850
1 DEAT
2 DATE 16 MAY 2001""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        parser.CheckImpossibleAges()
        self.assertNotEqual(
            parser.errorStr, ""
        )  # function worked if errorStr is still empty

    def test_invalid_age_with_no_death(self):  # normal case, no error
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1850""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        parser.CheckImpossibleAges()
        self.assertNotEqual(
            parser.errorStr, ""
        )  # function worked if errorStr is still empty


if __name__ == "__main__":
    unittest.main()
