import mergedeep
import json
import enum
import dataclasses
import os
from typing import Any

class ConsoleOutputLevels(enum.IntEnum):
	NONE = 0
	MINIMUM = 1
	MEDIUM = 2
	MAXIMUM = 3

@dataclasses.dataclass
class ConsoleOutput:
	levels: list[ConsoleOutputLevels]
	message: str
	print_kwargs: dict = dataclasses.field(default_factory=dict)

USER_SETTINGS: dict[str, Any]
CURRENT_CONSOLE_OUTPUT_LEVEL: ConsoleOutputLevels

def merge_with_default_settings(settings: dict[str, dict]) -> dict[str, dict]:
	"""Deep merges `settings` with the default settings (profile `settings_default`)"""
	new_settings: dict = load_settings_profile("settings_default", False)
	mergedeep.merge(new_settings, settings)
	return new_settings

def determine_console_output_level(setting: str | int) -> ConsoleOutputLevels:
	# set console output level by int or str, with default of NONE
	settings_console_output_level: str | int = setting
	if isinstance(settings_console_output_level, str):
		current_console_output_level = ConsoleOutputLevels[settings_console_output_level.upper()]
	elif isinstance(settings_console_output_level, int):
		current_console_output_level = ConsoleOutputLevels(settings_console_output_level)
	else:
		current_console_output_level = ConsoleOutputLevels.NONE

	return current_console_output_level
		
def load_settings_profile(profile: str, should_determine_console_output_level: bool=True) -> dict:
	"""Sets the global variable USER_SETTINGS to the selected profile, as well as returning it."""
	global USER_SETTINGS, CURRENT_CONSOLE_OUTPUT_LEVEL
	with open(profile + ".json", "r", encoding="UTF-8") as settings_file:
		USER_SETTINGS = json.load(settings_file)

	console_output_level_setting: str | int | None = USER_SETTINGS.get("console_output_level")
	if console_output_level_setting and should_determine_console_output_level:
		CURRENT_CONSOLE_OUTPUT_LEVEL = determine_console_output_level(console_output_level_setting)
		
	return USER_SETTINGS

def create_default_settings_profile_txt() -> None:
	# don't create if it exists
	if os.path.exists("./settings_profile.txt"): return

	with open("./settings_profile.txt", "x", encoding="UTF-8") as settings_profile_file:
		settings_profile_file.write("settings_default")

def get_current_profile() -> str:
	global is_first_time_run
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