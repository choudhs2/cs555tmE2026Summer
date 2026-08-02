import unittest
import io
from GEDCOMParser import GEDCOMParser


class TestInputLineNumbers(unittest.TestCase):

    def test_duplicate_individual_id_line_number(self):
        """Test duplicate individual ID reports correct line number."""
        gedcom_text = """0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
0 @I1@ INDI
1 NAME Duplicate /Earl/
"""
        parser = GEDCOMParser(io.StringIO(gedcom_text))
        parser.extract_entities()
        parser.checkUniqueIDs()
        self.assertIn(
            "Line 6: ERROR: INDIVIDUAL: US04: @I1@: Duplicated Individual",
            parser.errorStr,
        )

    def test_birth_before_death_line_number(self):
        """Test birth before death error reports individual's line number."""
        gedcom_text = """0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 2025
1 DEAT
2 DATE 16 MAY 2020
"""
        parser = GEDCOMParser(io.StringIO(gedcom_text))
        parser.extract_entities()
        parser.CheckBirthsBeforeDeaths()
        self.assertIn("Line 1: ERROR: INDIVIDUAL: US09: @I1@:", parser.errorStr)

    def test_too_old_age_line_number(self):
        """Test age > 150 reports individual's line number."""
        gedcom_text = """0 @I1@ INDI
1 NAME Old /Person/
1 SEX M
1 BIRT
2 DATE 13 APR 1800
"""
        parser = GEDCOMParser(io.StringIO(gedcom_text))
        parser.extract_entities()
        parser.CheckImpossibleAges()
        self.assertIn("Line 1: ERROR: INDIVIDUAL: US22: @I1@: Too Old", parser.errorStr)

    def test_illegitimate_date_line_number(self):
        """Test illegitimate date reports tag's exact line number."""
        gedcom_text = """0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 31 APR 2000
"""
        parser = GEDCOMParser(io.StringIO(gedcom_text))
        parser.extract_entities()
        parser.RejectIllegitimateDates()
        self.assertIn(
            "Line 5: ERROR: DATE: US23: 31 APR 2000 is not a legitimate date",
            parser.errorStr,
        )

    def test_multiple_errors_all_have_line_numbers(self):
        """Test that all error messages in errorStr start with 'Line <N>: ERROR:'."""
        gedcom_text = """0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 2025
1 DEAT
2 DATE 16 MAY 2020
0 @I1@ INDI
1 NAME Duplicate /Earl/
"""
        parser = GEDCOMParser(io.StringIO(gedcom_text))
        parser.extract_entities()
        parser.checkUniqueIDs()
        parser.CheckBirthsBeforeDeaths()

        errors = [line for line in parser.errorStr.splitlines() if line.strip()]
        self.assertGreater(len(errors), 0)
        for err in errors:
            self.assertTrue(
                err.startswith("Line "), f"Error does not start with 'Line ': {err}"
            )


if __name__ == "__main__":
    unittest.main()
