import journal_system
import settings
import traceback
import sys

def easy_run() -> None:
	settings.load_current_selected_profile(use_defaults=True) # this must happen first	

	ignore_today: bool = False
	if "--ignore-today" in sys.argv:
		ignore_today = True

	entries_only = False
	if "-e" in sys.argv or "--entries-only" in sys.argv:
		entries_only = True

	photos_only = False
	if ("-p" in sys.argv or "--photos-only" in sys.argv): # give entries only priority over photos only
		if entries_only:
			journal_system.output_to_console_by_level([
				settings.ConsoleOutput([settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], "Cannot use --photos-only (-p) and --entries-only (-e) together. Quitting.")
			])
			return
		photos_only = True

	no_only_flags = not entries_only and not photos_only
	if photos_only or no_only_flags:
		journal_system.move_photos_from_photo_locations() # then get the photos moved before making the entries

	if entries_only or no_only_flags:
		journal_system.create_all_recent_missing_entries(ignore_today) # actually make 'em

def handled_easy_run() -> None:
	try:
		easy_run()
	except FileNotFoundError as error:
		print(f"A file is missing. Double check the paths in settings and selected_profile.txt file and make sure selected_profile.txt exists. The full error is:\n{error}") # output, not debugging
		traceback.print_tb(error.__traceback__)
	except KeyError as error:
		print("Something was missing in a dictionary. Double check the README to make sure you have every setting in your settings file set. The full error is:\n{error}") # output, not debugging
		traceback.print_tb(error.__traceback__)
	except Exception as error:
		print(f"There's been a miscellaneous error:\n{error}") # output, not debugging
		traceback.print_tb(error.__traceback__)

if __name__ == "__main__":
	handled_easy_run()