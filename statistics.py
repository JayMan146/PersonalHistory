import tkinter
import dataclasses
import datetime
from create_base_journal_entries import load_settings, get_entry_markdown_path

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

    current_day = earliest_journal
    while current_day < today:
        entry = get_entry_markdown_path(current_day)

        current_day += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()