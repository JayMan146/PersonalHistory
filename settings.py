import mergedeep
import json
import enum

class ConsoleOutputLevel(enum.Enum):
	NONE = 0
	MINIMUM = 1
	MEDIUM = 2
	MAXIMUM = 3

USER_SETTINGS: dict[str, dict]
CURRENT_CONSOLE_OUTPUT_LEVEL: ConsoleOutputLevel

def merge_with_default_settings(settings: dict[str, dict]) -> dict[str, dict]:
	"""Deep merges `settings` with the default settings (profile `settings_default`)"""
	new_settings: dict = load_settings_profile("settings_default", False)
	mergedeep.merge(new_settings, settings)
	return new_settings

def determine_console_output_level(setting: str | int) -> ConsoleOutputLevel:
	global CURRENT_CONSOLE_OUTPUT_LEVEL
	# set console output level by int or str, with default of NONE
	settings_console_output_level: str | int = setting
	if isinstance(settings_console_output_level, str):
		CURRENT_CONSOLE_OUTPUT_LEVEL = ConsoleOutputLevel[settings_console_output_level.upper()]
	elif isinstance(settings_console_output_level, int):
		CURRENT_CONSOLE_OUTPUT_LEVEL = ConsoleOutputLevel(settings_console_output_level)
	else:
		CURRENT_CONSOLE_OUTPUT_LEVEL = ConsoleOutputLevel.NONE

	return CURRENT_CONSOLE_OUTPUT_LEVEL
		
def load_settings_profile(profile: str, should_determine_console_output_level: bool=True) -> dict:
	"""Sets the global variable USER_SETTINGS to the selected profile, as well as returning it."""
	global USER_SETTINGS, CURRENT_CONSOLE_OUTPUT_LEVEL
	with open(profile + ".json", "r", encoding="UTF-8") as settings_file:
		USER_SETTINGS = json.load(settings_file)

	other_settings_section: dict | None = USER_SETTINGS.get("other")
	console_output_level_setting: str | int | None = other_settings_section.get("console_output_level") if other_settings_section is not None else None
	if console_output_level_setting and should_determine_console_output_level:
		determine_console_output_level(console_output_level_setting)
		
	return USER_SETTINGS

def get_current_profile() -> str:
	"""Gets the currently selected profile in `settings_profile.txt`"""
	
	with open("./settings_profile.txt", "r", encoding="UTF-8") as settings_profile_file:
		profile: str = settings_profile_file.readline().strip()

	return profile

def load_current_settings_profile(use_defaults: bool=True) -> dict:
	"""Loads the settings of the current profile"""
	global USER_SETTINGS

	USER_SETTINGS = load_settings_profile(get_current_profile())
	if use_defaults:
		USER_SETTINGS = merge_with_default_settings(USER_SETTINGS)

	return USER_SETTINGS