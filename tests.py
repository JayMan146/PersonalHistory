import create_base_journal_entries as main
import datetime

def helper_function_tests():
    assert main.add_leading_zero(3) == "03"
    assert main.add_leading_zero(7) == "07"
    assert main.add_leading_zero(18) == "18"
    assert main.add_leading_zero(99) == "99"

    assert main.convert_to_month(1) == ("january", "01 january")
    assert main.convert_to_month(7) == ("july", "07 july")
    assert main.convert_to_month(12) == ("december", "12 december")

    assert main.convert_to_long_date(datetime.date(2003, 8, 30)) == "Saturday 30 August 2003"
    assert main.convert_to_long_date(datetime.date(2025, 2, 3)) == "Monday 03 February 2025"
    assert main.convert_to_long_date(datetime.date(2029, 3, 18)) == "Sunday 18 March 2029"

    assert main.convert_date_to_journal_path(datetime.date(2003, 8, 30)) == \
        (f"{main.USER_SETTINGS["journal_root"]}/2003", f"{main.USER_SETTINGS["journal_root"]}/2003/03 august 2003.md")
    assert main.convert_date_to_journal_path(datetime.date(2025, 2, 3)) == \
        (f"{main.USER_SETTINGS["journal_root"]}/2025", f"{main.USER_SETTINGS["journal_root"]}/2025/03 february 2025.md")
    assert main.convert_date_to_journal_path(datetime.date(2029, 3, 18)) == \
        (f"{main.USER_SETTINGS["journal_root"]}/2029", f"{main.USER_SETTINGS["journal_root"]}/2029/03 march 2029.md")

def test():
    main.load_settings()
    helper_function_tests()

    print("All tests passed.")

if __name__ == "__main__":
    test()