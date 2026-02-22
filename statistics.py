import tkinter
import dataclasses
import datetime
import calendar
import os
from create_base_journal_entries import load_current_settings_profile, convert_to_month, convert_to_long_date

USER_SETTINGS: dict

@dataclasses.dataclass
class JournalStatistic:
	date: datetime.date
	title_word_count: int
	body_word_count: int
	word_rating: str
	number_rating: int
	weather: str
	number_of_photos: int

def main():
	USER_SETTINGS = load_current_settings_profile()
	earliest_journal_dict: dict = USER_SETTINGS["other"]["earliest_journal"]
	earliest_journal: datetime.date = datetime.date(earliest_journal_dict["year"], earliest_journal_dict["month"], earliest_journal_dict["day"])
	today: datetime.date = datetime.date.today()

	statistics = []

	for year in range(earliest_journal.year, today.year + 1):
		year_folder_path: str = USER_SETTINGS["journal_root"] + "/" + str(year)
		if not os.path.exists(year_folder_path):
			continue

		# use the month end or start from the earliest journal or today if applicable
		start_month: int = earliest_journal.month if year == earliest_journal.year else 1
		end_month: int = today.month if year == today.year else 12
		for month in range(start_month, end_month + 1):
			month_file_path: str = f"{year_folder_path}/{convert_to_month(month)[1]} {str(year)}.md"
			if not os.path.exists(month_file_path):
				continue

			with open(month_file_path, "r", encoding="UTF-8") as journal_file:
				journal_lines: list[str] = journal_file.readlines()

				# use the day end or start from the earliest journal or today if applicable
				start_day: int = earliest_journal.day if month == earliest_journal.month and year == earliest_journal.year else 1
				end_day: int = today.day if month == today.month and year == today.year else calendar.monthrange(year, month)[1] # get days in month
				for day in range(start_day, end_day):
					entry_date = datetime.date(year, month, day)
					long_date: str = convert_to_long_date(entry_date)

					for line in journal_lines: 
						title_prefix: str = f"# {long_date}: "
						if not line.startswith(title_prefix): # check if it is the specific entry in the file
							continue

						new_statistic: JournalStatistic = JournalStatistic(
							entry_date,
							len(line[len(title_prefix):].split(" ")),
							0,
							"good",
							0,
							"cloudy",
							0
						)

if __name__ == "__main__":
	main()