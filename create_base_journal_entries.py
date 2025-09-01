import datetime
from convert_to_header_link import convert_to_header_link
import glob
import os
import shutil
import json
import typing
import traceback

USER_SETTINGS: dict
MONTHS: list[str] = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS_OF_THE_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def convert_to_month(month_date: datetime.date) -> tuple[str, str]:
    """Converts `month_date` into a tuple with the month name and it's number (1 - 12)"""
    month_number: str = str(month_date.month) if month_date.month >= 10 else f"0{month_date.month}"
    month_name: str = MONTHS[month_date.month - 1]
    numbered_month: str = f"{month_number} {month_name}"
    return (month_name, numbered_month)

def convert_to_long_date(short_date: datetime.date) -> str:
    """Converts `short_date` into a long date format like Monday, February 3rd, 2025."""
    weekday: str = DAYS_OF_THE_WEEK[short_date.weekday()].title()
    month: str = MONTHS[short_date.month - 1].title()
    day_string: str = str(short_date.day)
    ending: str = "th"
    if not (day_string.startswith("1") and len(day_string) > 1):
        ending = get_ordinal_number_ending(day_string)
    return f"{weekday}, {month} {short_date.day}{ending}, {short_date.year}"

def convert_date_to_journal_path(journal_date: datetime.date) -> tuple[str, str]:
    """Converts `journal_date` into the file path for the appropriate journal, returning a tuple with the year folder and the markdown file path."""
    numbered_month: str = convert_to_month(journal_date)[1]
    year_folder: str = f"{USER_SETTINGS["folder_paths"]["journal_root"]}/{journal_date.year}"
    markdown_file_path: str = f"{year_folder}/{numbered_month} {journal_date.year}.md"
    return (year_folder, markdown_file_path)

def get_ordinal_number_ending(number: str) -> str:
    ending: str
    match number[-1]:
        case "1":
            ending = "st"
        case "2":
            ending = "nd"
        case "3":
            ending = "rd"
        case _:
            ending = "th"
    return ending

def get_entry(entry_date: datetime.date) -> str | None:
    """Searches for and returns the journal entry of `entry_date`."""
    journal_path: str = convert_date_to_journal_path(entry_date)[1]
    if not os.path.exists(journal_path):
        return None
    long_date: str = convert_to_long_date(entry_date) if entry_date.year > 2022 else f"{entry_date.month}/{entry_date.day}/{entry_date.year}"
    
    with open(journal_path, "r", encoding="UTF-8") as journal_file:
        journal_lines: list[str] = journal_file.readlines()

    for line in journal_lines: 
        if not line.startswith(f"# {long_date}"):
            continue
        header: str = convert_to_header_link(line)
        path_with_header: str = f"{journal_path}{header}"
        fixed_path = path_with_header.replace(USER_SETTINGS["folder_paths"]["journal_root"], "..").replace(" ", "%20") # make it a local path and with %20 instead of spaces
        return fixed_path
    return None

def get_entries_matching_year(match_date: datetime.date) -> list[str]:
    """Returns journal entries matching the year of `match_date`."""
    matching_entries: list[str] = []
    for previous_year in range(match_date.year - 1, 2020, -1):
        previous_entry_header_path: str | None = get_entry(match_date.replace(year=previous_year))
        if previous_entry_header_path is not None:
            matching_entries.append(f"[{previous_year}]({previous_entry_header_path})")
    return matching_entries

def get_photo_by_date(photo_date: datetime.date) -> str:
    """Returns the path to photos for `photo date`, omitting the photo number. This file may or may not exist, once the photo number is added. It only returns a format, rather than checking for an actual photo with that date. `get_photo_paths_by_date` returns a real path, and utilizes this function to do that."""
    _, numbered_month = convert_to_month(photo_date)
    day_additional_zero: str = "0" if photo_date.day < 10 else ""
    photo_path: str = f"{USER_SETTINGS["folder_paths"]["journal_root"]}/{photo_date.year}/photos/{numbered_month} {photo_date.year}/{numbered_month} {day_additional_zero}{photo_date.day} {photo_date.year} "
    return photo_path

def get_photo_paths_by_date(photo_date: datetime.date) -> list[str]:
    """Returns the path to all photos with the date `photo_date`. As opposed to `get_photo_by_date`, these are real and valid photos."""
    entry_photo_path: str = get_photo_by_date(photo_date)
    photo_paths: list[str] = []
    for photo_number in range(0, 100):
        additional_zero: str = "0" if photo_number < 10 else ""
        photo_number_string: str = f"{additional_zero}{photo_number}"
        file_path: list = glob.glob(f"{entry_photo_path}{photo_number_string}.*")
        if not file_path:
            continue
        path_to_photo: str = file_path[0].replace(f"{USER_SETTINGS["folder_paths"]["journal_root"]}/{photo_date.year}", ".").replace(" ", "%20")
        photo_paths.append(f"![]({path_to_photo})")
    
    return photo_paths

def generate_custom_journal_formatting() -> str:
    """Generates a list of the custom journal formatting settings to be added to an entry."""
    custom_journal_formatting_settings_path = USER_SETTINGS["journal_format"]["custom"]
    return f"{custom_journal_formatting_settings_path["preliminary_text"]}{custom_journal_formatting_settings_path["separator"].join(custom_journal_formatting_settings_path["items"])}{custom_journal_formatting_settings_path["ending_text"]}"

def generate_requires_programming_journal_formatting(key: str, item_list: list[str]) -> str | None:
    """Generates a line of the requires_programming section of the settings based on `key` and `item_list` (items to be joined together, e.g. `photo_paths`)"""
    requires_programming_settings_path: dict[str, typing.Any] = USER_SETTINGS["journal_format"]["requires_programming"][key]
    if not (requires_programming_settings_path["enabled"] and item_list):
        return
    entry_line: str = f"{requires_programming_settings_path["preliminary_text"]}{requires_programming_settings_path["separator"].join(item_list)}{requires_programming_settings_path["ending_text"]}"
    return entry_line

def get_entry_string(entry_date: datetime.date, matching_entries: list[str], photo_paths: list[str]) -> str:
    """Creates a string of a journal entry with the given parameters."""

    entry_string: str = f"# {convert_to_long_date(entry_date)}: "
    if USER_SETTINGS["journal_format"]["custom_placement"].lower() == "before":
        entry_string += generate_custom_journal_formatting()

    matching_entries_line: str | None = generate_requires_programming_journal_formatting("matching_entries", matching_entries)
    if matching_entries_line is not None:
        entry_string += matching_entries_line
    photos_line: str | None = generate_requires_programming_journal_formatting("photos", photo_paths)
    if photos_line is not None:
        entry_string += photos_line
    
    if USER_SETTINGS["journal_format"]["custom_placement"].lower() != "before":
        entry_string += generate_custom_journal_formatting()

    entry_string += "\n" * USER_SETTINGS["journal_format"]["writing_lines"]

    return entry_string

def get_photo_name_pieces(photo_name: str) -> tuple[int, str, int, int, int] | None:
    """Returns the pieces of `photo_name` in the order of month number, month, day, year, and photo number. Returns `None` if invalid."""
    segments: list[str] = photo_name.split(".")[0].split() #TODO: check file type and covert/disallow
    correct_length: bool = len(segments) == 5
    if not correct_length:
        return
    
    month_number: int = int(segments[0])
    month: str = segments[1]
    day: int = int(segments[2])
    year: int = int(segments[3])
    photo_number: int = int(segments[4])

    return (month_number, month, day, year, photo_number)

def handle_photo_in_location(directory: str, file: str, found_any_photos: bool, found_any_photos_in_this_directory: bool=False) -> None | tuple[bool, bool]:
    if os.path.isdir(file) or not valid_photo_name_format(file):
        return

    if not found_any_photos:    
        found_any_photos = True
    if not found_any_photos_in_this_directory:
        found_any_photos_in_this_directory = True
        print(f"Moving photos from {directory}:") # output, not debugging
    print(f"⮡ {file}") # output, not debugging
    photo_name_pieces = get_photo_name_pieces(file)
    if photo_name_pieces is None: # probably will never be executed because of the validity check, but type safety and just in case yatta yatta
        return
    month_number, month, _, year, _ = photo_name_pieces
    month_number_with_zero = f"0{month_number}" if month_number < 10 else str(month_number)
    new_photo_folder_path: str = f"{USER_SETTINGS["folder_paths"]["journal_root"]}/{year}/photos/{month_number_with_zero} {month} {year}/"
    if not os.path.exists(new_photo_folder_path):
        if USER_SETTINGS["other"]["enable_new_directory_and_file_creation"]:
            print("  ⮡ Warning: unable to move this photo, as directory creation is disabled.")
            return
        os.mkdir(new_photo_folder_path) 
    shutil.move(f"{directory}/{file}", new_photo_folder_path)
    return (found_any_photos, found_any_photos_in_this_directory)

def move_photos_from_photo_locations() -> None:
    """Finds photos with valid names in the downloads folder and moves them to the corresponding location."""
    photo_directory_files: dict[str, list[str]] = {}
    for photo_directory in USER_SETTINGS["folder_paths"]["photo_locations"]:
        photo_directory_files[photo_directory] = os.listdir(photo_directory)

    found_any_photos: bool = False
    for directory, files in photo_directory_files.items():
        found_photos_in_this_directory: bool = False
        for file in files:
            photo_found_status = handle_photo_in_location(directory, file, found_any_photos, found_photos_in_this_directory)
            if isinstance(photo_found_status, tuple):
                found_any_photos, found_photos_in_this_directory = photo_found_status
    if found_any_photos:
        print("")

def valid_photo_name_format(photo_name: str) -> bool:
    """Checks if `photo_name` is a valid photo name."""
    photo_name_pieces = get_photo_name_pieces(photo_name)
    if photo_name_pieces is None:
        return False
    month_number, month, day, year, photo_number = photo_name_pieces
    valid_month_number: bool = 1 <= month_number <= 12
    valid_month: bool = month in MONTHS
    valid_day: bool = 1 <= day <= 31
    valid_year: bool = 2020 <= year <= 2120
    valid_photo_number: bool = 0 <= photo_number <= 99
    return valid_month_number and valid_month and valid_day and valid_year and valid_photo_number    

def generate_entry(entry_date: datetime.date) -> str | None:
    """Generates the entry for `entry_date`."""
    year_folder, _ = convert_date_to_journal_path(entry_date)
    if not os.path.isdir(year_folder) and USER_SETTINGS["other"]["enable_new_directory_and_file_creation"]:
        os.mkdir(year_folder)
        print(f"Making new directory: {year_folder}") # output, not debugging

    matching_entries: list[str]
    if USER_SETTINGS["journal_format"]["requires_programming"]["matching_entries"]:
        matching_entries = get_entries_matching_year(entry_date)
    else:
        matching_entries = []

    photo_paths: list[str]
    if USER_SETTINGS["journal_format"]["requires_programming"]["photos"]:
        photo_paths = get_photo_paths_by_date(entry_date)
    else:
        photo_paths = []

    new_entry: str = get_entry_string(entry_date, matching_entries, photo_paths)
    return new_entry

def determine_preliminary_new_lines(file_lines: list[str]) -> int:
    """Determines how many preliminary new lines are needed for a new entry based on `file_lines`."""
    final_line: str = file_lines[-1]
    preliminary_new_lines: int = 0
    if final_line != "\n":
        if final_line[-1] == "\n":
            preliminary_new_lines = 1
        else:
            preliminary_new_lines = 2
    return preliminary_new_lines

def write_entry(entry: str, entry_date: datetime.date, print_entry: bool=True) -> None:
    """Takes `entry` and writes it to the file corresponding to `entry_date`."""
    _, markdown_file_path = convert_date_to_journal_path(entry_date)
    if not os.path.exists(markdown_file_path) and USER_SETTINGS["other"]["enable_new_directory_and_file_creation"]:
        with open(markdown_file_path, "x", encoding="UTF-8"):
            print(f"Creating new journal file: {markdown_file_path}") # output, not debugging
        
    number_of_preliminary_new_lines: int = 0
    with open(markdown_file_path, "r+", encoding="UTF-8") as journal_file_to_read:
        journal_lines = journal_file_to_read.readlines()
    if len(journal_lines) >= 2:
        number_of_preliminary_new_lines = determine_preliminary_new_lines(journal_lines)
            
    preliminary_new_lines: str = "\n" * number_of_preliminary_new_lines
    with open(markdown_file_path, "a", encoding="UTF-8") as journal_file_to_append:
        if USER_SETTINGS["other"]["enable_writing_to_file"]:
            journal_file_to_append.write(preliminary_new_lines)
            journal_file_to_append.write(entry)
        else:
            pass
            print("Attempted to write to file, but that behavior is disabled.")
    if print_entry:
        print(entry, end="")

def find_all_recent_missing_entries() -> list[datetime.date]:
    """Finds missing entries in the last 100 days, working backwards from today and stopping once it has found a valid entry."""
    starting_date: datetime.date = datetime.date.today()
    current_time: datetime.datetime = datetime.datetime.today()

    crossover_time_json_object: dict[str, int] = USER_SETTINGS["day_crossover"]["time"]
    crossover_time: datetime.datetime = datetime.datetime(
        current_time.year, current_time.month, current_time.day,
        crossover_time_json_object["hour"],
        crossover_time_json_object["minute"],
        crossover_time_json_object["second"]
    )
    day_crossover_move_direction: str = USER_SETTINGS["day_crossover"]["move_direction"]
    if day_crossover_move_direction != "disable":
        if day_crossover_move_direction == "backward" and current_time < crossover_time:
            starting_date -= datetime.timedelta(days=1)
        elif day_crossover_move_direction == "forward" and current_time > crossover_time:
            starting_date += datetime.timedelta(days=1)

    earliest_journal: dict[str, int] = USER_SETTINGS["other"]["earliest_journal"]
    earliest_journal_date: datetime.date = datetime.date(earliest_journal["year"], earliest_journal["month"], earliest_journal["day"])
    current_date: datetime.date = starting_date
    recent_missing_entries: list[datetime.date] = []
    for _ in range(100): # could be formatted as a while loop, though this allows a 100 day limit. also could be formatted to go between a date range, but that sounds annoying to do and this... works.
        current_entry: str | None = get_entry(current_date)
        if current_entry or current_date < earliest_journal_date: # checking if the current entry exists only allows missing entries to be in a row, so it won't go like e.g. jan 24, jan 17, jan 25.
            break
        recent_missing_entries.append(current_date)
        current_date -= datetime.timedelta(days=1)

    return recent_missing_entries

def create_all_recent_missing_entries() -> None:
    """Gets all recent missing entries and then writes them."""

    recent_missing_entries: list[datetime.date] = find_all_recent_missing_entries()
    
    if USER_SETTINGS["other"]["enable_photo_transfer"]:
        move_photos_from_photo_locations()

    print("Journal Text Written to File(s):\n") #output, not debugging

    #iterate backwards since we want the first found missing one to be written first, then the most recent missing one to be written last
    for entry_date in recent_missing_entries[::-1]: 
        entry = generate_entry(entry_date)
        if entry is None:
            continue
        write_entry(entry, entry_date)

def load_settings() -> None:
    global USER_SETTINGS
    with open("./Other/AutomationCode/settings_to_use.txt", "r", encoding="UTF-8") as settings_to_use_file:
        settings_file_name: str = settings_to_use_file.readline().strip()
    if not settings_file_name.endswith(".json"):
        settings_file_name = f"{settings_file_name}.json"
    with open(f"./Other/AutomationCode/{settings_file_name}", "r", encoding="UTF-8") as settings_file:
        USER_SETTINGS = json.load(settings_file)
    if USER_SETTINGS["Confused?"]:
        del USER_SETTINGS["Confused?"]

if __name__ == "__main__":
    load_settings()
    try:
        create_all_recent_missing_entries()
    except FileNotFoundError as error:
        print(f"A file is missing. Double check the paths in settings and settings_to_use.txt file and make sure settings_to_use.txt exists. The full error is:\n{error}")
        traceback.print_tb(error.__traceback__)
    except Exception as error:
        print(f"There's been a miscellaneous error:\n{error}")
        traceback.print_tb(error.__traceback__)