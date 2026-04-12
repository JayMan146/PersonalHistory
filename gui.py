import tkinter as tk
import journal_system
import settings

primary_window: tk.Tk = tk.Tk()

USER_SETTINGS: dict = settings.load_current_selected_profile()

class MainMenuButton(tk.Button):
	def __init__(self, **kwargs):
		super().__init__(primary_window, width=20, height=1, **kwargs)

def edit_settings():
	settings_window: tk.Toplevel = tk.Toplevel()
	settings_window.title("Journal System Settings")
	
	tk.Label(settings_window, text="Settings", width=35).grid(column=0, row=0)

def quit():
	primary_window.destroy()

def gui():
	primary_window.title("Journal System")

	tk.Label(primary_window, text="Welcome to the Journal System!", width=35).grid(column=0, row=0)
	MainMenuButton(text="Move Photos", command=journal_system.move_photos_from_photo_locations).grid(column=0, row=1)
	MainMenuButton(text="Create New Entries", command=journal_system.create_all_recent_missing_entries).grid(column=0, row=2)
	MainMenuButton(text="Edit Settings...", command=edit_settings).grid(column=0, row=3)
	MainMenuButton(text="Quit", command=quit).grid(column=0, row=4)

	primary_window.mainloop()

if __name__ == "__main__":
	gui()