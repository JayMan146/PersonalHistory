import journal_system
import settings
import datetime
import unittest

class TestHelperFunctions(unittest.TestCase):
	def test_add_leading_zero(self):
		self.assertEqual(journal_system.add_leading_zero(3), "03")
		self.assertEqual(journal_system.add_leading_zero(7), "07")
		self.assertEqual(journal_system.add_leading_zero(18), "18")
		self.assertEqual(journal_system.add_leading_zero(99), "99")

	def test_convert_to_month(self):
		self.assertEqual(journal_system.convert_to_month(1), ("january", "01 january"))
		self.assertEqual(journal_system.convert_to_month(7), ("july", "07 july"))
		self.assertEqual(journal_system.convert_to_month(12), ("december", "12 december"))

	def test_convert_to_long_date(self):
		self.assertEqual(journal_system.convert_to_long_date(datetime.date(2003, 8, 30)), "Saturday 30 August 2003")
		self.assertEqual(journal_system.convert_to_long_date(datetime.date(2025, 2, 3)), "Monday 03 February 2025")
		self.assertEqual(journal_system.convert_to_long_date(datetime.date(2029, 3, 18)), "Sunday 18 March 2029")

	def test_convert_date_to_journal_path(self):
		self.assertEqual(journal_system.convert_date_to_journal_path(datetime.date(2003, 8, 30)), \
			(f"{journal_system.JOURNAL_ROOT}/2003", f"{journal_system.JOURNAL_ROOT}/2003/08 august 2003.md"))
		self.assertEqual(journal_system.convert_date_to_journal_path(datetime.date(2025, 2, 3)), \
			(f"{journal_system.JOURNAL_ROOT}/2025", f"{journal_system.JOURNAL_ROOT}/2025/02 february 2025.md"))
		self.assertEqual(journal_system.convert_date_to_journal_path(datetime.date(2029, 3, 18)), \
			(f"{journal_system.JOURNAL_ROOT}/2029", f"{journal_system.JOURNAL_ROOT}/2029/03 march 2029.md"))
		
	def test_get_photo_name_pieces(self):
		self.assertEqual(journal_system.get_photo_name_pieces("30 02 august 2003"), (30, 2, "august", 2003))
		self.assertEqual(journal_system.get_photo_name_pieces("03 00 february 2025"), (3, 0, "february", 2025))
		self.assertEqual(journal_system.get_photo_name_pieces("18 17 march 2029"), (18, 17, "march", 2029))

	def test_valid_photo_name_format(self):
		self.assertTrue(journal_system.valid_photo_name_format("30 02 august 2003"))
		self.assertTrue(journal_system.valid_photo_name_format("03 00 february 2025"))
		self.assertTrue(journal_system.valid_photo_name_format("18 17 march 2029"))
		self.assertFalse(journal_system.valid_photo_name_format("FunnyMeme"))
		self.assertFalse(journal_system.valid_photo_name_format("00 00 00 00"))
		self.assertFalse(journal_system.valid_photo_name_format("03 00 february 3001"))
		self.assertFalse(journal_system.valid_photo_name_format("18. 17 march 2029"))
		self.assertFalse(journal_system.valid_photo_name_format("32 00 june 2020"))
	
	def test_determine_preliminary_new_lines(self):
		self.assertEqual(journal_system.determine_preliminary_new_lines([
			"stuff\n", "written entry\n", "\n"    
		]), 0)
		self.assertEqual(journal_system.determine_preliminary_new_lines([
			"stuff\n", "written entry\n"    
		]), 1)
		self.assertEqual(journal_system.determine_preliminary_new_lines([
			"stuff\n", "written entry"    
		]), 2)

	def test_modify_date_by_crossover(self):
		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.time(3, 0, 0), True
		), datetime.timedelta(0))
		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 3, 2, 20, 11), datetime.time(3, 0, 0), True
		), datetime.timedelta(days=-1))

		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.time(21, 0, 0), False
		), datetime.timedelta(0))
		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 1, 22, 20, 11), datetime.time(21, 0, 0), False
		), datetime.timedelta(days=1))

		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.time(3, 0, 0), None
		), datetime.timedelta(0))
		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 3, 2, 20, 11), datetime.time(3, 0, 0), None
		), datetime.timedelta(0))
		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 2, 15, 20, 11), datetime.time(21, 0, 0), None
		), datetime.timedelta(0))
		self.assertEqual(journal_system.modify_date_by_crossover(
			datetime.datetime(2003, 8, 1, 22, 20, 11), datetime.time(21, 0, 0), None
		), datetime.timedelta(0))

	def test_convert_to_header_link(self):
		self.assertEqual(journal_system.convert_to_header_link("# How To Eat Monkeys!"), "#how-to-eat-monkeys")
		self.assertEqual(journal_system.convert_to_header_link("### I... (might) tHINK that... someone—who shall be unamed—is 15-years-old."), "#i-might-think-that-someonewho-shall-be-unamedis-15-years-old")
		
class TestSettings(unittest.TestCase):
	def test_determine_console_output_level(self):
		none_various_caps: str = "NonE"
		minimum_various_caps: str = "mINImUm"
		medium_various_caps: str = "medIUm"
		maximum_various_caps: str = "MAXiMUM"
		self.assertEqual(settings.determine_console_output_level(none_various_caps.lower()), settings.ConsoleOutputLevels.NONE)
		self.assertEqual(settings.determine_console_output_level(minimum_various_caps.lower()), settings.ConsoleOutputLevels.MINIMUM)
		self.assertEqual(settings.determine_console_output_level(medium_various_caps.lower()), settings.ConsoleOutputLevels.MEDIUM)
		self.assertEqual(settings.determine_console_output_level(maximum_various_caps.lower()), settings.ConsoleOutputLevels.MAXIMUM)
		self.assertEqual(settings.determine_console_output_level(none_various_caps), settings.ConsoleOutputLevels.NONE)
		self.assertEqual(settings.determine_console_output_level(minimum_various_caps), settings.ConsoleOutputLevels.MINIMUM)
		self.assertEqual(settings.determine_console_output_level(medium_various_caps), settings.ConsoleOutputLevels.MEDIUM)
		self.assertEqual(settings.determine_console_output_level(maximum_various_caps), settings.ConsoleOutputLevels.MAXIMUM)
		self.assertEqual(settings.determine_console_output_level(none_various_caps.upper()), settings.ConsoleOutputLevels.NONE)
		self.assertEqual(settings.determine_console_output_level(minimum_various_caps.upper()), settings.ConsoleOutputLevels.MINIMUM)
		self.assertEqual(settings.determine_console_output_level(medium_various_caps.upper()), settings.ConsoleOutputLevels.MEDIUM)
		self.assertEqual(settings.determine_console_output_level(maximum_various_caps.upper()), settings.ConsoleOutputLevels.MAXIMUM)
		self.assertEqual(settings.determine_console_output_level(0), settings.ConsoleOutputLevels.NONE)
		self.assertEqual(settings.determine_console_output_level(1), settings.ConsoleOutputLevels.MINIMUM)
		self.assertEqual(settings.determine_console_output_level(2), settings.ConsoleOutputLevels.MEDIUM)
		self.assertEqual(settings.determine_console_output_level(3), settings.ConsoleOutputLevels.MAXIMUM)
	
if __name__ == "__main__":
	settings.load_current_selected_profile()
	unittest.main()