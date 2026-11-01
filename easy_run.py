import journal_system
import settings
import traceback
import sys

def easy_run() -> None:
	ignore_today: bool = False
	if "--ignore-today" in sys.argv:
		ignore_today = True

	settings.load_current_selected_profile(use_defaults=True) # this must happen first
	journal_system.move_photos_from_photo_locations() # then get the photos moved before making the entries
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