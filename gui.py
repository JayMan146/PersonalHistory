import tkinter
from create_base_journal_entries import move_photos_from_photo_locations, create_all_recent_missing_entries, load_settings

primary_window: tkinter.Tk = tkinter.Tk()

def edit_settings():
    raise NotImplementedError()

def main():
    load_settings()
    primary_window.title("Journal System")

    tkinter.Label(primary_window, text="Welcome to the Journal System!", width=35).grid(column=0, row=0)
    tkinter.Button(primary_window, text="Move Photos", command=move_photos_from_photo_locations, width=20, height=1).grid(column=0, row=1)
    tkinter.Button(primary_window, text="Create New Entries", command=create_all_recent_missing_entries, width=20, height=1).grid(column=0, row=2)
    tkinter.Button(primary_window, text="Edit Settings...", command=edit_settings, width=20, height=1).grid(column=0, row=3)
    tkinter.Button(primary_window, text="Quit", command=primary_window.destroy, width=20, height=1).grid(column=0, row=3)

    primary_window.mainloop()

if __name__ == "__main__":
    main()