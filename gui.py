import tkinter as tk
import journal_system
import settings

primary_window: tk.Tk = tk.Tk()

class MainMenuButton(tk.Button):
	def __init__(self, **kwargs):
		super().__init__(primary_window, width=20, height=1, **kwargs)

def edit_settings():
	def create_new_profile():
		pass

	settings_window: tk.Toplevel = tk.Toplevel()
	settings_window.title("Personal History Settings")
	
	tk.Button(settings_window, command=create_new_profile, text="+ New Profile",width=15).grid(column=0, row=0)
	tk.Entry(settings_window).grid(column=1, row=0)
	tk.Label(settings_window, text="Profile: ", width=15).grid(column=0, row=1)
	
	selectable_profiles: list = settings.get_all_profiles()
	tk.OptionMenu(settings_window, tk.StringVar(value=settings.get_selected_profile()), *selectable_profiles).grid(column=1, row=1)

def quit():
	primary_window.destroy()

def gui():
	primary_window.title("Personal History")

	tk.Label(primary_window, text="Welcome to Personal History!", width=35).grid(column=0, row=0)
	MainMenuButton(text="Move Photos", command=journal_system.move_photos_from_photo_locations).grid(column=0, row=1)
	MainMenuButton(text="Create New Entries", command=journal_system.create_all_recent_missing_entries).grid(column=0, row=2)
	MainMenuButton(text="Edit Settings...", command=edit_settings).grid(column=0, row=3)
	MainMenuButton(text="Quit", command=quit).grid(column=0, row=4)

	primary_window.mainloop()

if __name__ == "__main__":
	gui()