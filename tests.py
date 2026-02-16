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
			(f"{main.JOURNAL_ROOT}/2003", f"{main.JOURNAL_ROOT}/2003/08 august 2003.md"))
		self.assertEqual(main.convert_date_to_journal_path(datetime.date(2025, 2, 3)), \
			(f"{main.JOURNAL_ROOT}/2025", f"{main.JOURNAL_ROOT}/2025/02 february 2025.md"))
		self.assertEqual(main.convert_date_to_journal_path(datetime.date(2029, 3, 18)), \
			(f"{main.JOURNAL_ROOT}/2029", f"{main.JOURNAL_ROOT}/2029/03 march 2029.md"))
		
	def test_get_photo_name_pieces(self):
		self.assertEqual(main.get_photo_name_pieces("30 02 august 2003"), (30, 2, "august", 2003))
		self.assertEqual(main.get_photo_name_pieces("03 00 february 2025"), (3, 0, "february", 2025))
		self.assertEqual(main.get_photo_name_pieces("18 17 march 2029"), (18, 17, "march", 2029))

	def test_valid_photo_name_format(self):
		self.assertTrue(main.valid_photo_name_format("30 02 august 2003"))
		self.assertTrue(main.valid_photo_name_format("03 00 february 2025"))
		self.assertTrue(main.valid_photo_name_format("18 17 march 2029"))
		self.assertFalse(main.valid_photo_name_format("FunnyMeme"))
		self.assertFalse(main.valid_photo_name_format("00 00 00 00"))
		self.assertFalse(main.valid_photo_name_format("03 00 february 3001"))
		self.assertFalse(main.valid_photo_name_format("18. 17 march 2029"))
		self.assertFalse(main.valid_photo_name_format("32 00 june 2020"))
	
	def test_determine_preliminary_new_lines(self):
		self.assertEqual(main.determine_preliminary_new_lines([
			"stuff\n", "written entry\n", "\n"    
		]), 0)
		self.assertEqual(main.determine_preliminary_new_lines([
			"stuff\n", "written entry\n"    
		]), 1)
		self.assertEqual(main.determine_preliminary_new_lines([
			"stuff\n", "written entry"    
		]), 2)

	def test_modify_date_by_crossover(self):
		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.datetime(1, 1, 1, 3, 0, 0), True
		), datetime.timedelta(0))
		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 3, 2, 20, 11), datetime.datetime(1, 1, 1, 3, 0, 0), True
		), datetime.timedelta(days=-1))

		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.datetime(1, 1, 1, 21, 0, 0), False
		), datetime.timedelta(0))
		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 1, 22, 20, 11), datetime.datetime(1, 1, 1, 21, 0, 0), False
		), datetime.timedelta(days=1))

		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.datetime(1, 1, 1, 3, 0, 0), None
		), datetime.timedelta(0))
		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 3, 2, 20, 11), datetime.datetime(1, 1, 1, 3, 0, 0), None
		), datetime.timedelta(0))
		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.datetime(1, 1, 1, 21, 0, 0), None
		), datetime.timedelta(0))
		self.assertEqual(main.modify_date_by_crossover(
			datetime.datetime(2003, 8, 1, 22, 20, 11), datetime.datetime(1, 1, 1, 21, 0, 0), None
		), datetime.timedelta(0))

if __name__ == "__main__":
	main.determine_root_paths()
	main.load_current_profile_settings()
	unittest.main()