import tkinter
import dataclasses
import datetime
import calendar
from create_base_journal_entries import load_settings

USER_SETTINGS: dict

@dataclasses.dataclass
class JournalStatistic:
    title_word_count: int
    body_word_count: int
    word_rating: str
    number_rating: int
    weather: str
    number_of_photos: int

def main():
    USER_SETTINGS = load_settings()
    earliest_journal_dict: dict = USER_SETTINGS["earliest_journal"]
    earliest_journal: datetime.date = datetime.date(earliest_journal_dict["year"], earliest_journal_dict["month"], earliest_journal_dict["day"])
    today: datetime.date = datetime.date.today()

    statistics = []

    for year in range(earliest_journal.year, today.year + 1):
        # use the month end or start from the earliest journal or today if applicable
        start_month: int = earliest_journal.month if year == earliest_journal.year else 1
        end_month: int = today.month if year == today.year else 12
        for month in range(start_month, end_month):
            # use the day end or start from the earliest journal or today if applicable
            start_day: int = earliest_journal.day if month == earliest_journal.month and year == earliest_journal.year else 1
            end_day: int = today.day if month == today.month and year == today.year else calendar.monthrange(year, month)[1] # get days in month
            for day in range(start_day, end_day):
                pass

if __name__ == "__main__":
    main()