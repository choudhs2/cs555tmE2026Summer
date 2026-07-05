import unittest
import io
from GEDCOMParser import GEDCOMParser

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


class TestUS05(unittest.TestCase):
    """
    US05: Creating list/collection for Individuals and Families
    """

    def setUp(self):
        self.file_like = io.StringIO(SAMPLE_GEDCOM)
        self.parser = GEDCOMParser(self.file_like)
        self.parser.extract_entities()

    def test_individual_collection_exists(self):
        # 1. Test that the individuals collection dictionary is created and not empty
        self.assertIsNotNone(self.parser.individuals)
        self.assertIsInstance(self.parser.individuals, dict)
        self.assertEqual(len(self.parser.individuals), 2)

    def test_individual_collection_details(self):
        # 2. Test that individual records are stored with correct IDs, names, and genders
        self.assertEqual(len(self.parser.individuals), 2)
        self.assertIn("@I1@", self.parser.individuals)
        self.assertEqual(self.parser.individuals["@I1@"].name, "Earl /Grey/")
        self.assertEqual(self.parser.individuals["@I1@"].gender, "M")

    def test_family_collection_exists(self):
        # 3. Test that the families collection dictionary is created and not empty
        self.assertIsNotNone(self.parser.families)
        self.assertIsInstance(self.parser.families, dict)
        self.assertEqual(len(self.parser.families), 1)

    def test_family_collection_details(self):
        # 4. Test that family records are stored with correct IDs, spouse IDs, and children
        self.assertEqual(len(self.parser.families), 1)
        self.assertIn("@F1@", self.parser.families)
        fam = self.parser.families["@F1@"]
        self.assertEqual(fam.husband_id, "@I1@")
        self.assertEqual(fam.wife_id, "@I2@")
        self.assertEqual(fam.children, {"@I3@"})

    def test_family_name_cross_referencing(self):
        # 5. Test that family husband and wife names are populated from the individual records
        fam = self.parser.families["@F1@"]
        self.assertEqual(fam.husband_name, "Earl /Grey/")
        self.assertEqual(fam.wife_name, "May /O'naise/")

    def test_empty_input_parsing(self):
        # Edge case / failure: Parsing empty input yields empty collections rather than crashing
        parser = GEDCOMParser(io.StringIO(""))
        parser.extract_entities()
        self.assertEqual(parser.individuals, {})
        self.assertEqual(parser.families, {})

    def test_missing_spouse_names_in_family_cross_reference(self):
        # Edge case: Spouse IDs are provided in Family but do not exist in the individuals collection
        SAMPLE_MISSING_GEDCOM = """0 HEAD
1 CHAR UTF-8
0 @F1@ FAM
1 HUSB @I99@
1 WIFE @I98@
0 TRLR"""
        file_like = io.StringIO(SAMPLE_MISSING_GEDCOM)
        parser = GEDCOMParser(file_like)
        parser.extract_entities()

        self.assertIn("@F1@", parser.families)
        fam = parser.families["@F1@"]
        self.assertEqual(fam.husband_id, "@I99@")
        self.assertEqual(fam.husband_name, "N/A")
        self.assertEqual(fam.wife_id, "@I98@")
        self.assertEqual(fam.wife_name, "N/A")

    def test_extracted_helpers(self):
        # Test new helper methods extracted during refactoring (_process_individual_tag, _process_family_tag, _apply_date)
        from models import Individual, Family, date
        from GEDCOMParser import Tag

        parser = GEDCOMParser(io.StringIO(""))
        indi = Individual("@I100@")
        tag = Tag("1 NAME John /Doe/", None)
        res = parser._process_individual_tag(indi, tag)
        self.assertEqual(indi.name, "John /Doe/")
        self.assertIsNone(res)

        tag_birt = Tag("1 BIRT", None)
        res_birt = parser._process_individual_tag(indi, tag_birt)
        self.assertEqual(res_birt, "BIRT")

        fam = Family("@F100@")
        tag_husb = Tag("1 HUSB @I100@", None)
        res_husb = parser._process_family_tag(fam, tag_husb)
        self.assertEqual(fam.husband_id, "@I100@")
        self.assertIsNone(res_husb)

        parser._apply_date(indi, "BIRT", date(1990, 1, 1))
        self.assertEqual(indi.birthday, date(1990, 1, 1))


if __name__ == "__main__":
    unittest.main()
