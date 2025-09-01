#import os
#import glob

"""This code is not meant to be good, nor permanent."""

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
years = [str(year) for year in range(2024, 2026)]
numbered_months = []
numbered_percent20_months = []
for month_number, month in enumerate(months, start=1):
    if month_number < 10:
        month_number = f"0{month_number}"
    numbered_months.append(f"{month_number} {month}")
    numbered_percent20_months.append(f"{month_number}%20{month}" )
file_extensions = [".png", ".jpg", ".jpeg", ".MOV", ".JPEG"]

def automate():
    for year in years:
        for numbered_month, numbered_percent20_month, month in zip(numbered_months, numbered_percent20_months, months):
            journal_path = rf"C:\Users\jerem\OneDrive\Desktop\Jeremy\Journals\{year}\{numbered_month} {year}.md"
            with open(journal_path, "r", encoding="UTF-8") as journal:
                full_journal = "".join(journal.readlines())
            for day in range(1, 32):
                day_str = f"0{day}" if day < 10 else str(day)
                for num in range(0, 8):
                    old_format = f"{numbered_percent20_month}/{month}{day_str}_0{num}"
                    new_format = f"{numbered_percent20_month}%20{year}/{numbered_percent20_month}%20{day_str}%20{year}%200{num}"
                    full_journal = full_journal.replace(old_format, new_format)
                    print(old_format, new_format)
            full_journal = full_journal.split("\n")
            ending_journal = []
            for line in full_journal:
                ending_journal.append(f"{line}\n")
            #print(full_journal)
            with open(journal_path, "w", encoding="UTF-8") as journal:
                journal.writelines(ending_journal)
                #journal.write(full_journal)
            #if month == "may":
            #    break
        #break
            

if __name__ == "__main__":
    automate()