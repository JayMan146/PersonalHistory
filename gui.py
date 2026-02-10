import tkinter
from create_base_journal_entries import move_photos_from_photo_locations, create_all_recent_missing_entries, load_settings

primary_window: tkinter.Tk = tkinter.Tk()

USER_SETTINGS: dict = load_settings()

class MainMenuButton(tkinter.Button):
	def __init__(self, **kwargs):
		super().__init__(primary_window, width=20, height=1, **kwargs)

def edit_settings():
	global settings_window
	settings_window: tkinter.Toplevel = tkinter.Toplevel()
	settings_window.title("Journal System Settings")
	
	tkinter.Label(settings_window, text="Settings", width=35).grid(column=0, row=0)

def quit():
	primary_window.destroy()

def main():
	primary_window.title("Journal System")

	tkinter.Label(primary_window, text="Welcome to the Journal System!", width=35).grid(column=0, row=0)
	MainMenuButton(text="Move Photos", command=move_photos_from_photo_locations).grid(column=0, row=1)
	MainMenuButton(text="Create New Entries", command=create_all_recent_missing_entries).grid(column=0, row=2)
	MainMenuButton(text="Edit Settings...", command=edit_settings).grid(column=0, row=3)
	MainMenuButton(text="Quit", command=quit).grid(column=0, row=4)

	primary_window.mainloop()

if __name__ == "__main__":
	main()