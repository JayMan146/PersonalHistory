import datetime
import glob
import os
import zipfile
import shutil
import typing
from PIL import Image
from pillow_heif import register_heif_opener

from ConvertToHeaderLink.convert_to_header_link import convert_to_header_link
import settings

JOURNAL_ROOT: str = os.getcwd().rsplit("/", 1)[0] # gets the cwd, current working directory, and discards the last directory (giving the root)

MONTHS: list[str] = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

is_heif_registered: bool = False

def output_to_console_by_level(outputs: list[settings.ConsoleOutput]) -> None:
	"""Uses each output in `outputs` and checks if it matches settings.CURRENT_CONSOLE_OUTPUT_LEVEL. If so, print it."""
	for output in outputs:
		if settings.CURRENT_CONSOLE_OUTPUT_LEVEL in output.levels:
			print(output.message, **output.print_kwargs)

def add_leading_zero(num: int) -> str:
	"""Adds a leading zero to `num`. For example: 7 -> 07, 3 -> 03, 18 -> 18"""
	return f"0{num}" if num < 10 else str(num)

def convert_to_month(month: int) -> tuple[str, str]:
	"""Converts `month_date` into a tuple with the month name and the numbered month (the month with it's number, 1-12). eg. ("july", "07 july")"""
	if month < 1 or month > 12:
		raise ValueError("Invalid month number")
	month_number: str = add_leading_zero(month)
	month_name: str = MONTHS[month - 1]
	numbered_month: str = f"{month_number} {month_name}"
	return (month_name, numbered_month)

def convert_to_long_date(short_date: datetime.date) -> str:
	"""Converts `short_date` into a long date format like Monday 03 February 2025"""

	DAYS_OF_THE_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	weekday: str = DAYS_OF_THE_WEEK[short_date.weekday()].title()
	day_with_leading_zero: str = add_leading_zero(short_date.day)
	month: str = MONTHS[short_date.month - 1].title() # subtract one since month number and indexes are separate

	return f"{weekday} {day_with_leading_zero} {month} {short_date.year}"

def convert_date_to_journal_path(journal_date: datetime.date) -> tuple[str, str]:
	"""Converts `journal_date` into the file path for the appropriate journal, returning a tuple with the year folder and the markdown file path."""
	numbered_month: str = convert_to_month(journal_date.month)[1]
	year_folder: str = f"{JOURNAL_ROOT}/{journal_date.year}"
	markdown_file_path: str = f"{year_folder}/{numbered_month} {journal_date.year}.md"
	return (year_folder, markdown_file_path)

def get_entry_markdown_path(entry_date: datetime.date) -> str | None:
	"""Searches for and returns the journal entry of `entry_date`."""
	journal_markdown_file_path: str = convert_date_to_journal_path(entry_date)[1]
	if not os.path.exists(journal_markdown_file_path):
		return None
	
	long_date: str = convert_to_long_date(entry_date)
	with open(journal_markdown_file_path, "r", encoding="UTF-8") as journal_file:
		journal_lines: list[str] = journal_file.readlines()

	for line in journal_lines: 
		if not line.startswith(f"## {long_date}"): # check if it is the specific entry in the file
			continue
		header: str = convert_to_header_link(line)
		path_with_header: str = f"{journal_markdown_file_path}{header}" # adds the header to the file path (as it is in .md format)
		fixed_path = path_with_header.replace(JOURNAL_ROOT, "..").replace(" ", "%20") # make it a local path and with %20 instead of spaces
		return fixed_path
	return None # technically, it will do this since it won't return anything if it doesn't find it, but i prefer explicit None returns (sometimes).

def get_entries_matching_year(match_date: datetime.date) -> list[str]:
	"""Returns all journal entries matching the year of `match_date`, besides the original."""
	matching_entries: list[str] = []
	for previous_year in range(match_date.year - 1, settings.USER_SETTINGS["earliest_entry"]["year"] - 1, -1): # loop over previous years until earliest journal, backwards
		previous_entry_header_path: str | None = get_entry_markdown_path(match_date.replace(year=previous_year))
		if previous_entry_header_path is not None:
			matching_entries.append(f"[{previous_year}]({previous_entry_header_path})")
	return matching_entries

def get_photo_paths_by_date(photo_date: datetime.date) -> list[str]:
	"""Returns the path to all photos with the date `photo_date`."""

	month, numbered_month = convert_to_month(photo_date.month)
	photo_day_string: str = add_leading_zero(photo_date.day)
	# "./" is used as the actual text here. it is replaced with journal root to search using glob.
	# Note: don't make it use journal root out right, and break it. did that once already. shhh
	entry_photo_path: str = f"./photos/{numbered_month} {photo_date.year}/{photo_day_string} <photo_number> {month} {photo_date.year}" # photos with date, but not with photo number. Once added, the photo may not exist

	photo_paths: list[str] = []
	for photo_number in range(0, 100):
		photo_number_string: str = add_leading_zero(photo_number)
		photo_path_with_photo_number: str = entry_photo_path.replace("<photo_number>", photo_number_string)
		full_path: str = photo_path_with_photo_number.replace("./", f"{JOURNAL_ROOT}/{photo_date.year}/")
		file_path: list = glob.glob(f"{full_path}.*")
		if not file_path: # doesn't exist
			continue
		file_extension: str = file_path[0].split(".")[-1] # dissects the glob output and gives the file extension of the first (and hopefully only) result
		markdown_version_path_to_photo: str = f"{photo_path_with_photo_number}.{file_extension}".replace(" ", "%20") # gotta replace that for md to like it, idk why
		photo_paths.append(f"![]({markdown_version_path_to_photo})") # the ![](<photo path>) is the markdown format for photos
	
	return photo_paths

def generate_custom_formatting() -> str:
	"""Generates a list of the custom journal formatting settings to be added to an entry."""
	custom_formatting_settings_path = settings.USER_SETTINGS["format"]["custom"]

	prefix: str = custom_formatting_settings_path["prefix"]
	suffix: str = custom_formatting_settings_path["suffix"]

	item_separator: str = custom_formatting_settings_path["separator"]
	items: list[str] = custom_formatting_settings_path["items"]
	joined_items = item_separator.join(items)

	return prefix + joined_items + suffix

def generate_requires_programming_formatting(key: str, item_list: list[str]) -> str | None:
	"""Generates a line of the requires_programming section of the settings based on `key` and `item_list` (items to be joined together, e.g. `photo_paths`)"""
	requires_programming_settings_path: dict[str, typing.Any] = settings.USER_SETTINGS["format"]["requires_programming"][key]

	is_disabled: bool = not requires_programming_settings_path["enabled"]
	is_empty: bool = not bool(item_list)
	if is_disabled or is_empty:
		return
	
	prefix: str = requires_programming_settings_path["prefix"]
	suffix: str = requires_programming_settings_path["suffix"]

	item_separator: str = requires_programming_settings_path["separator"]
	joined_items = item_separator.join(item_list)

	return prefix + joined_items + suffix

def get_photo_name_pieces(photo_name: str) -> tuple[int, int, str, int] | None:
	"""Returns the pieces of `photo_name` in the order of day, photo number, month, year. Returns `None` if invalid."""

	segments: list[str] = photo_name.split(".")[0].split() # get name, without extension, then split by space
	
	is_correct_length: bool = len(segments) == 4
	if not is_correct_length:
		return None
	
	try:
		day: int = int(segments[0])
		photo_number: int = int(segments[1])
		month: str = segments[2]
		year: int = int(segments[3])
	except ValueError:
		return None # invalid if can't convert to the type

	return (day, photo_number, month, year) # ordered by appearance

def extract_zipped_photo(file_path: str) -> None:
	*directories, _ = file_path.split("/")
	directory: str = "/".join(directories) # full directory to photo
	
	temporary_directory: str = directory + "/temp" # temporary place to extract .zip file to
	with zipfile.ZipFile(file_path + ".zip", "r") as zip_archive:
		zip_archive.extractall(temporary_directory) # extract photos

	mov_files: list[str] = glob.glob(temporary_directory + "/*.mov") + glob.glob(temporary_directory + "/*.MOV")
	for mov_file in mov_files:
		os.remove(mov_file) # delete all .mov or .MOV files

	first_remaining_file = os.listdir(temporary_directory)[0] # can only take one, so just choose first!
	remaining_file_extension: str = first_remaining_file.split(".")[-1]
	shutil.move(temporary_directory + "/" + first_remaining_file, file_path + f".{remaining_file_extension}")
	
	shutil.rmtree(temporary_directory) # remove temporary directory and all remaining files

	output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], "  ⮡ Extracted heic photo from zip archive.")])

def delete_unconverted_photo(file_path: str, original_extension: str) -> None:
	"""Removes an unconverted photo at `file_path` with the extension of `original_extension`, following rules in settings.USER_SETTINGS."""

	if settings.USER_SETTINGS["photos"]["type_conversion"]["delete_pre_converted_files"]:
		os.remove(file_path)
		output_to_console_by_level([
			settings.ConsoleOutput([settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], 
			f"\t⮡ Deleted unconverted photo of file type {original_extension}.")
		])

def handle_zip_photo(file_path: str, file_path_without_extension: str):
	"""Handles the case of a photo being converted from a zip file"""
	if not settings.USER_SETTINGS["photos"]["enable_google_photos_extraction"]: return

	extract_zipped_photo(file_path_without_extension)
	convert_photo_file_type([file for file in glob.glob(file_path_without_extension + ".*") if file.split(".")[-1] != "zip"][0])
	delete_unconverted_photo(file_path, "zip")

def convert_photo_file_type(file_path: str) -> None:
	"""Converts `file_path` (with extension included) to the file type of what is specified in the settings file."""
	
	global is_heif_registered

	if not settings.USER_SETTINGS["photos"]["type_conversion"]["enabled"]: return

	file_path_split_by_periods: list[str] = file_path.split(".")
	file_path_without_extension = ".".join(file_path_split_by_periods[:-1])
	extension: str = file_path_split_by_periods[-1].lower()

	if extension == "zip":
		handle_zip_photo(file_path, file_path_without_extension)
		return

	output_type: str = settings.USER_SETTINGS["photos"]["type_conversion"]["conversions"].get(extension) # other wise, use settings mapping
	if output_type is None: return # don't convert without mapping
	
	# we only register it as this point to make sure we only register once it's actually needed (and only once)
	if not is_heif_registered and extension in ["heic", "heif"]:
		register_heif_opener() 
		is_heif_registered = True

	image = Image.open(file_path)
	image.save(f"{file_path_without_extension}.{output_type}", format=output_type)

	output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], f"  ⮡ Converted to file type {output_type}.")])

	delete_unconverted_photo(file_path, extension)

def get_photo_directory(photo_name: str) -> str | None:
	"""Returns the directory that a photo would go to based on it's name"""
	photo_name_pieces = get_photo_name_pieces(photo_name)
	if photo_name_pieces is None: # probably will never be executed because of the validity check, but type safety and just in case yatta yatta
		return
	
	_, _, month, year = photo_name_pieces
	month_number_with_zero = add_leading_zero(MONTHS.index(month) + 1)
	photo_folder_name: str = f"{month_number_with_zero} {month} {year}"
	new_photo_folder_path: str = f"{JOURNAL_ROOT}/{year}/photos/{photo_folder_name}/"

	if not os.path.exists(new_photo_folder_path): # create the photo folder if it doesn't exist
		if not settings.USER_SETTINGS["permissions"]["enable_new_directory_and_file_creation"]:
			output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MEDIUM], "  ⮡ Warning: unable to move this photo, as directory creation is disabled.")])
			return None
		os.makedirs(new_photo_folder_path) 
		output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MEDIUM], f"Making new directory: {new_photo_folder_path}\n")])

	return new_photo_folder_path

def handle_photo_in_location(photo_origin_directory: str, photo_name: str, found_any_photos: bool, found_any_photos_in_this_directory: bool=False) -> None | tuple[bool, bool]:
	"""Goes through the process of checking and moving one photo from the directories"""
	photo_origin_path: str = f"{photo_origin_directory}/{photo_name}"

	is_directory: bool = os.path.isdir(photo_origin_path)
	has_invalid_photo_name_format: bool = not valid_photo_name_format(photo_name)
	if is_directory or has_invalid_photo_name_format:
		return

	if not found_any_photos:
		output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MINIMUM], "Moving photos.")])
	found_any_photos = True

	if not found_any_photos_in_this_directory:
		output_to_console_by_level([
			settings.ConsoleOutput([settings.ConsoleOutputLevels.MEDIUM], f"Moving photos from {photo_origin_directory}."),
			settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], f"Moving photos from {photo_origin_directory}:")
		])
	found_any_photos_in_this_directory = True

	output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], f"⮡ {photo_name}")])
 
	new_photo_folder_path: str | None = get_photo_directory(photo_name)
	if new_photo_folder_path is None:
		return None
	
	new_photo_path: str = f"{new_photo_folder_path}{photo_name}"
	
	# this check does not have a setting, because it will throw an error if you don't check for this
	# i was going to make it a setting. it does check for more than what throws the error, technically.
	wildcard_extension_photo_path: str = ".".join(new_photo_path.split(".")[:-1]) + ".*"
	if glob.glob(wildcard_extension_photo_path):
		output_to_console_by_level([
			settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], "  ⮡ Warning: unable to move this photo, as a photo with this name already exists."),
			settings.ConsoleOutput([settings.ConsoleOutputLevels.NONE, settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM], f"Warning: unable to move {photo_name}, as a photo with this name already exists.")
		])
		return None
	
	shutil.move(photo_origin_path, new_photo_folder_path)
	convert_photo_file_type(new_photo_path)
	
	return (found_any_photos, found_any_photos_in_this_directory) # keep this through iterations

def move_photos_from_photo_locations() -> None:
	"""Finds photos with valid names in the downloads folder and moves them to the corresponding location."""

	photo_moving_enabled: bool = settings.USER_SETTINGS["photos"]["enable_photo_transfer"]
	if not photo_moving_enabled:
		return
	
	# get all directories and their associated files within
	photo_directory_files: dict[str, list[str]] = {}
	for photo_directory in settings.USER_SETTINGS["photos"]["photo_locations"]:
		photo_directory_files[photo_directory] = os.listdir(photo_directory)

	# handle each photo in each directory
	has_found_any_photos: bool = False
	for directory, files in photo_directory_files.items():
		has_found_photos_in_this_directory: bool = False
		for file in files:
			photo_found_status = handle_photo_in_location(directory, file, has_found_any_photos, has_found_photos_in_this_directory)
			if isinstance(photo_found_status, tuple): # if bools were returned, updated them
				has_found_any_photos, has_found_photos_in_this_directory = photo_found_status
	if has_found_any_photos: 
		output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], "")])
		
def valid_photo_name_format(photo_name: str) -> bool:
	"""Checks if `photo_name` is a valid photo name."""
	photo_name_pieces = get_photo_name_pieces(photo_name)
	if photo_name_pieces is None:
		return False
	
	day, photo_number, month, year = photo_name_pieces
	is_valid_day: bool = 1 <= day <= 31
	is_valid_photo_number: bool = 0 <= photo_number <= 99
	is_valid_month: bool = month in MONTHS
	is_valid_year: bool = 0 <= year <= 3000

	return (is_valid_day and is_valid_photo_number and is_valid_month and is_valid_year)

def generate_entry(entry_date: datetime.date, header_suffix: str) -> str:
	"""Generates the entry for `entry_date`."""

	entry_string: str = f"## {convert_to_long_date(entry_date)}{header_suffix}" # header

	if settings.USER_SETTINGS["format"]["custom_placement"].lower() == "before": # place custom stuff first if that's in settinsg
		entry_string += generate_custom_formatting() # repeated code, shut up.

	# add the generated matching entries lines if valid  
	if settings.USER_SETTINGS["format"]["requires_programming"]["matching_entries"]:
		matching_entries: list[str] = []
		matching_entries = get_entries_matching_year(entry_date)
		matching_entries_line: str | None = generate_requires_programming_formatting("matching_entries", matching_entries)
		if matching_entries_line is not None:
			entry_string += matching_entries_line
	
	# add the generated photos lines if valid
	if settings.USER_SETTINGS["format"]["requires_programming"]["photos"]:
		photo_paths: list[str] = []
		photo_paths = get_photo_paths_by_date(entry_date)
		photos_line: str | None = generate_requires_programming_formatting("photos", photo_paths)
		if photos_line is not None:
			entry_string += photos_line
	
	if settings.USER_SETTINGS["format"]["custom_placement"].lower() != "before": # place custom stuff after if that's in settinsg
		entry_string += generate_custom_formatting() # repeated code, shut up.

	entry_string += "\n" * settings.USER_SETTINGS["format"]["writing_lines"] # add new lines for writing based on settings | ahh, python string multiplication
	
	return entry_string

def determine_preliminary_new_lines(file_lines: list[str]) -> int:
	"""Determines how many preliminary new lines are needed for a new entry based on `file_lines`."""

	final_line: str = file_lines[-1]
	is_final_line_newline: bool = final_line == "\n"
	is_final_character_newline: bool = final_line[-1] == "\n"

	preliminary_new_lines: int = 0
	if not is_final_line_newline:
		if is_final_character_newline:
			preliminary_new_lines = 1
		else:
			preliminary_new_lines = 2
	return preliminary_new_lines

def write_entry(entry: str, entry_date: datetime.date, any_entries_written: bool=False) -> bool: # this function is large, maybe break it up TODO
	"""Takes `entry` and writes it to the file corresponding to `entry_date`."""
	year_folder, markdown_file_path = convert_date_to_journal_path(entry_date)
	
	if not os.path.isdir(year_folder):
		if not settings.USER_SETTINGS["permissions"]["enable_new_directory_and_file_creation"]:
			output_to_console_by_level([
				settings.ConsoleOutput([settings.ConsoleOutputLevels.NONE, settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], 
				"Warning: unable to write entry, as directory creation is disabled.")
			])
			return False
		os.mkdir(year_folder)
		output_to_console_by_level([
			settings.ConsoleOutput([settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], 
			f"Making new directory: {year_folder}\n")
		])

	if not os.path.exists(markdown_file_path):
		if not settings.USER_SETTINGS["permissions"]["enable_new_directory_and_file_creation"]:
			output_to_console_by_level([
				settings.ConsoleOutput([settings.ConsoleOutputLevels.NONE, settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], 
				"Warning: unable to write entry, as file creation is disabled.")
			])
			return False
		with open(markdown_file_path, "x", encoding="UTF-8") as new_journal_file:
			output_to_console_by_level([
				settings.ConsoleOutput([settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], 
				f"Creating new journal file: {markdown_file_path}\n")
			])
			if not settings.USER_SETTINGS["permissions"]["enable_writing_to_file"]:
				output_to_console_by_level([
					settings.ConsoleOutput([settings.ConsoleOutputLevels.NONE, settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], 
					"Attempted to write header to file, but that behavior is disabled.")
				])
			new_journal_file.write(f"# {convert_to_month(entry_date.month)[0].title()} {entry_date.year}\n\n")
		
	number_of_preliminary_new_lines: int = 0
	with open(markdown_file_path, "r+", encoding="UTF-8") as journal_file_to_read:
		journal_lines = journal_file_to_read.readlines()

	if len(journal_lines) >= 2: # if is a new file, we won't need to check for newlines. this isn't checked by the above if statement, as the file could be empty without being generated by the code.
		number_of_preliminary_new_lines = determine_preliminary_new_lines(journal_lines)
			
	preliminary_new_lines: str = "\n" * number_of_preliminary_new_lines
	with open(markdown_file_path, "a", encoding="UTF-8") as journal_file_to_append:
		if settings.USER_SETTINGS["permissions"]["enable_writing_to_file"]:
			journal_file_to_append.write(preliminary_new_lines)
			journal_file_to_append.write(entry)
		else:
			output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.NONE, settings.ConsoleOutputLevels.MINIMUM, settings.ConsoleOutputLevels.MEDIUM, settings.ConsoleOutputLevels.MAXIMUM], "Attempted to write entry to file, but that behavior is disabled.")])

	if not any_entries_written:
		output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], "Journal Text Written to File(s):\n")])
		any_entries_written = True

	output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], entry, {"end": ""})]) # show what was written to file

	return any_entries_written

def modify_date_by_crossover(time_to_modify: datetime.datetime, crossover_time: datetime.time, move_backward: bool | None) -> datetime.timedelta:
	if move_backward is None: return datetime.timedelta()

	crossover_date: datetime.datetime = datetime.datetime(
		time_to_modify.year, time_to_modify.month, time_to_modify.day,
		crossover_time.hour, crossover_time.minute, crossover_time.second
	)
	if move_backward and time_to_modify < crossover_date:
		return datetime.timedelta(days=-1)
	elif not move_backward and time_to_modify > crossover_date:
		return datetime.timedelta(days=1)
		
	return datetime.timedelta()

def find_all_recent_missing_entries() -> list[datetime.date]:
	"""Finds missing entries in the last 100 days, working backwards from today and stopping once it has found a valid entry."""
	starting_date: datetime.datetime = datetime.datetime.today()

	crossover_time_setting: dict[str, int] = settings.USER_SETTINGS["day_crossover"]["time"]
	crossover_time = datetime.time(crossover_time_setting["hour"], crossover_time_setting["minute"], crossover_time_setting["second"])
	crossover_direction_setting: str = settings.USER_SETTINGS["day_crossover"]["move_direction"]
	crossover_direction: bool | None = None if crossover_direction_setting == "disabled" else crossover_direction_setting == "backward"
	starting_date += modify_date_by_crossover(starting_date, crossover_time, crossover_direction)

	earliest_entry_json_object: dict[str, int] = settings.USER_SETTINGS["earliest_entry"]
	earliest_entry_date: datetime.date = datetime.date(earliest_entry_json_object["year"], earliest_entry_json_object["month"], earliest_entry_json_object["day"])

	current_date: datetime.date = starting_date.date()
	recent_missing_entries: list[datetime.date] = []
	search_length: int = 100
	for _ in range(search_length): # could be formatted as a while loop, though this allows a limit. also could be formatted to go between a date range, but that sounds annoying to do and this... works.
		current_entry: str | None = get_entry_markdown_path(current_date)
		if current_entry or current_date < earliest_entry_date: # checking if the current entry exists only allows missing entries to be in a row, so it won't go like e.g. jan 24, jan 17, jan 25. though, i guess this doesn't allow for like "missing" a day... TODO
			break
		recent_missing_entries.append(current_date)
		current_date -= datetime.timedelta(days=1)

	return recent_missing_entries

def create_all_recent_missing_entries() -> None:
	"""Gets all recent missing entries and then writes them."""

	recent_missing_entries: list[datetime.date] = find_all_recent_missing_entries()

	# iterate backwards since we want the first found missing one to be written first, then the most recent missing one to be written last
	any_entries_written: bool = False
	for entry_date in recent_missing_entries[::-1]: 
		entry = generate_entry(entry_date, settings.USER_SETTINGS["format"]["header_suffix"])
		any_entries_written = write_entry(entry, entry_date, any_entries_written)

	if not any_entries_written:
		output_to_console_by_level([settings.ConsoleOutput([settings.ConsoleOutputLevels.MAXIMUM], "No Text Was Written to Any Files.")])
		
def on_first_time_run() -> None:
	"""What is done if it is the first time the user runs the system. Creates a single entry for today."""
	today = datetime.date.today()
	entry = generate_entry(today, settings.USER_SETTINGS["format"]["header_suffix"])
	write_entry(entry, today)