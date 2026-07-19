import unittest
from datetime import date
from models import parse_date, validBirthAndDeath


class TestParseDate(unittest.TestCase):
    def test_valid_date(self):
        result = parse_date("01 Jan 2000")
        self.assertIsInstance(result, date)

    def test_valid_date_single_digit_day(self):
        result = parse_date("1 Jan 2000")
        self.assertIsInstance(result, date)

    def test_invalid_date_extra_characters(self):
        result = parse_date("01 Jan 2000a")
        self.assertIsNone(result)

    def test_invalid_month(self):
        result = parse_date("01 MayX 2000")
        self.assertIsNone(result)

    def test_invalid_year(self):
        result = parse_date("01 Jan 200a")
        self.assertIsNone(result)


class TestBirthAndDeathDateValidation(unittest.TestCase):

    def test_birth_before_death(self):
        birth = parse_date("01 Jan 2000")
        death = parse_date("02 Jan 2000")
        self.assertTrue(validBirthAndDeath(birth, death))

    def test_birth_equal_to_death(self):
        birth = parse_date("01 Jan 2000")
        death = parse_date("01 Jan 2000")
        self.assertTrue(validBirthAndDeath(birth, death))

    def test_birth_after_death(self):
        birth = parse_date("02 Jan 2000")
        death = parse_date("01 Jan 2000")
        self.assertFalse(validBirthAndDeath(birth, death))

    def test_invalid_birth_valid_death(self):
        birth = parse_date("32 Jan 2000")
        death = parse_date("02 Feb 2000")
        self.assertIsNone(birth)  # Birth date is invalid
        self.assertIsNotNone(death)  # Death date is valid
        self.assertFalse(
            validBirthAndDeath(birth, death)
        )  # invalid birth date is false

    def test_missing_birth_valid_death(self):
        birth = parse_date("")
        death = parse_date("02 Jan 2000")
        self.assertIsNone(birth)  # Birth date is missing == invalid
        self.assertIsNotNone(death)  # Death date is valid
        self.assertFalse(
            validBirthAndDeath(birth, death)
        )  # invalid birth date is false

    def test_valid_birth_missing_death(self):
        birth = parse_date("01 Jan 2000")
        death = parse_date("")
        self.assertIsNotNone(birth)  # Birth date is valid
        self.assertIsNone(death)  # Death date is invalid
        self.assertTrue(
            validBirthAndDeath(birth, death)
        )  # valid birth no death is true


if __name__ == "__main__":
    unittest.main()
