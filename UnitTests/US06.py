import unittest
import io
from prettytable import PrettyTable
from GEDCOMParser import GEDCOMParser
from models import Individual, Family

SAMPLE_GEDCOM = """0 HEAD
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Earl /Grey/
1 SEX M
1 BIRT
2 DATE 13 APR 1945
1 DEAT
2 DATE 12 APR 1945
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
1 CHIL @I3@
1 MARR
2 DATE 11 MAY 1988
0 TRLR"""


class TestUS06(unittest.TestCase):
    """
    US06: Import and apply prettytable module to list of individuals and families
    """

    def setUp(self):
        self.file_like = io.StringIO(SAMPLE_GEDCOM)
        self.parser = GEDCOMParser(self.file_like)
        self.parser.extract_entities()

    def test_prettytable_import_and_instantiation(self):
        # 1. Verify that PrettyTable is imported and can be successfully instantiated
        pt = PrettyTable()
        self.assertIsInstance(pt, PrettyTable)

    def test_individual_row_formatting_length(self):
        # 2. Verify that individual row formatting returns the expected number of fields (9)
        indi = self.parser.individuals["@I2@"]
        row = indi.get_pt_row()
        self.assertEqual(len(row), 9)

    def test_individual_row_formatting_values(self):
        # 3. Verify specific individual table row field values and formatting
        indi = self.parser.individuals["@I2@"]
        row = indi.get_pt_row()
        self.assertEqual(
            row,
            [
                "@I2@",
                "May /O'naise/",
                "F",
                "1947-07-13",
                row[4],
                True,
                "N/A",
                "N/A",
                {"@F1@"},
            ],
        )

    def test_family_row_formatting_values(self):
        # 4. Verify specific family table row field values and formatting
        fam = self.parser.families["@F1@"]
        row = fam.get_pt_row()
        self.assertEqual(
            row,
            [
                "@F1@",
                "1988-05-11",
                "N/A",
                "@I1@",
                "Earl /Grey/",
                "@I2@",
                "May /O'naise/",
                {"@I3@"},
            ],
        )

    def test_prettytable_output_rendering(self):
        # 5. Verify that PrettyTable builds the table string representation with headers and cell values
        pt = PrettyTable()
        pt.field_names = [
            "ID",
            "Name",
            "Gender",
            "Birthday",
            "Age",
            "Alive",
            "Death",
            "Child",
            "Spouse",
        ]
        pt.add_row(self.parser.individuals["@I1@"].get_pt_row())

        table_str = str(pt)
        self.assertIn("Earl /Grey/", table_str)
        self.assertIn("1945-04-13", table_str)
        self.assertIn("False", table_str)
        self.assertIn("1945-04-12", table_str)

    def test_row_formatting_with_missing_fields(self):
        # Edge case / failure: Formatting objects when all data except the ID is missing
        indi = Individual("@I99@")
        row_indi = indi.get_pt_row()
        self.assertEqual(
            row_indi, ["@I99@", "N/A", "N/A", "N/A", "N/A", True, "N/A", "N/A", "N/A"]
        )

        fam = Family("@F99@")
        row_fam = fam.get_pt_row()
        self.assertEqual(
            row_fam, ["@F99@", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
        )


if __name__ == "__main__":
    unittest.main()
