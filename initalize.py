import datetime
import journal_system
import settings

def intialize_journals() -> None:
	"""Creates a single entry for today."""
	
    # get settings ready for new use
	settings.load_settings_profile("settings_default")
	settings.create_default_settings_profile_txt()
	
    # create journal entry for today
	today = datetime.date.today()
	entry = journal_system.generate_entry(today, settings.USER_SETTINGS["format"]["header_suffix"])
	journal_system.write_entry(entry, today)
	
if __name__ == "__main__":
	intialize_journals()