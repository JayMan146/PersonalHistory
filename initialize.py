import datetime
import journal_system
import settings

def intialize_journals() -> None:
	"""Creates a single entry for today."""
	
	# get settings ready for new use
	settings.load_settings_profile("settings_default")
	settings.create_default_settings_profile_txt()

	# to allow the code later on that writes the message in the journal to be positioned better
	settings.USER_SETTINGS["format"]["writing_lines"] = 0
	
	# create journal entry for today
	today = datetime.date.today()
	entry = journal_system.generate_entry(today, settings.USER_SETTINGS["format"]["header_suffix"])
	journal_system.write_entry(entry, today)
	
	# write start message
	first_journal_path: str = journal_system.convert_date_to_journal_path(today)[1]
	with open(first_journal_path, "a") as initialized_entry:
		initialized_entry.write("Welcome to your first journal! To use the program more from here, check out the [Usage section of the README](../PersonalHistory/README#usage), and other sections. If you want your journal to look different, try making your own settings profile. Feel free to delete this line and starting writing your Personal History.\n")
		
	journal_system.output_to_console_by_level([
		settings.ConsoleOutput(
			[settings.ConsoleOutputLevels.NONE, settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], f"The journal system has been successfully initialized! Go check out your first file at \"{first_journal_path}\"!"
		)
	])
	
if __name__ == "__main__":
	intialize_journals()