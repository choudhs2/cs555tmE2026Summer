import unittest
import io
from datetime import date
from GEDCOMParser import *


class TestRecentBirthsPrinting(unittest.TestCase):

    def test_print_has_births_within_year(self):  # normal case, prints both individuals
        fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 2026
1 DEAT
2 DATE 16 MAY 2027
3 NOTE The above will show a table, because it is within the last year""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        outStr = parser.PrintRecentlyBorn()
        self.assertNotEqual(
            outStr, "Recently Born Individuals\nNone Found\n"
        )  # function worked if outStr is not the "None Found" string

    def test_print_has_births_over_one_year(self):  # should only print header and None Found
        fakeFile = fakeFile = io.StringIO("""0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 2025
3 NOTE The above will show None Found, because it is over a year ago""")
        fakeFile.seek(0)
        parser = GEDCOMParser(fakeFile)
        parser.extract_entities()  # get individuals and families
        outStr = parser.PrintRecentlyBorn()
        self.assertEqual(
            outStr, "Recentl Born Individuals\nNone Found\n"
        )  # function should return the "None Found" since the birth was over a year ago

if __name__ == "__main__":
    unittest.main()
