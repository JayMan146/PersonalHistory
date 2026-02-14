import create_base_journal_entries as main
import datetime
import unittest

class TestHelperFunctions(unittest.TestCase):
    def test_add_leading_zero(self):
        self.assertEqual(main.add_leading_zero(3), "03")
        self.assertEqual(main.add_leading_zero(7), "07")
        self.assertEqual(main.add_leading_zero(18), "18")
        self.assertEqual(main.add_leading_zero(99), "99")

    def test_convert_to_month(self):
        self.assertEqual(main.convert_to_month(1), ("january", "01 january"))
        self.assertEqual(main.convert_to_month(7), ("july", "07 july"))
        self.assertEqual(main.convert_to_month(12), ("december", "12 december"))

    def test_convert_to_long_date(self):
        self.assertEqual(main.convert_to_long_date(datetime.date(2003, 8, 30)), "Saturday 30 August 2003")
        self.assertEqual(main.convert_to_long_date(datetime.date(2025, 2, 3)), "Monday 03 February 2025")
        self.assertEqual(main.convert_to_long_date(datetime.date(2029, 3, 18)), "Sunday 18 March 2029")

    def test_convert_date_to_journal_path(self):
        self.assertEqual(main.convert_date_to_journal_path(datetime.date(2003, 8, 30)), \
            (f"{main.USER_SETTINGS["journal_root"]}/2003", f"{main.USER_SETTINGS["journal_root"]}/2003/08 august 2003.md"))
        self.assertEqual(main.convert_date_to_journal_path(datetime.date(2025, 2, 3)), \
            (f"{main.USER_SETTINGS["journal_root"]}/2025", f"{main.USER_SETTINGS["journal_root"]}/2025/02 february 2025.md"))
        self.assertEqual(main.convert_date_to_journal_path(datetime.date(2029, 3, 18)), \
            (f"{main.USER_SETTINGS["journal_root"]}/2029", f"{main.USER_SETTINGS["journal_root"]}/2029/03 march 2029.md"))

if __name__ == "__main__":
    main.load_settings()
    unittest.main()