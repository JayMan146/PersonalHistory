# Journal System

This doesn't have any info yet, but I figured I should add the file.

## Settings

Pretty simple, they're settings.

### Folder Paths

There are two folder paths you need to specify.

First, `journal_root`, which is a single string with the full path. It folder should have only your journals, and nothing else. Inside that, there should be `Other/AutomationCode`, where this file and the scripts for the system are stored. The `Other` folder is for any files that you would like to store outside of the system, but still within the `journal_root` folder. It is likely useless for most people, but I've used it. 

The `photo_locations` is a list of the paths of folders you want photos automatically moved from. If you have `enable_photo_transfer` set to `false`, then it is useless. Any file paths in this list will be checked for photos upon running `create_base_journal_entries.py`. The photo must follow the format `<month number with leading 0 if one digit> <full month name, no capitals> <day of the month> <year> <photo number, 0-99, always with two digits>.<file extension>` For example: `08 august 31 2025 02`.

### Journal Format

### Day Crossover

This is a way to make it so that during some part of the day, it counts as a different day. Personally, I use it so that if I run this past midnight, it doesn't count the new day after midnight. It's not the next day until I sleep to me.

This has two fields.

`time` is simple: just specify `hour` (24 hour system), `minute`, and `second` for the time.

`move_direction` is a little more complicated. You can set it to `disable` to get rid of this feature entirely. If set to `backward`, at any point in a day **before** the specified time, it will count as the day **before**. If set to `forward`, at any point in a day **after** the specified time, it will count as the day **after**.

## Other

This is anything that didn't fit anywhere else.

`earliest_journal` is a date object with the fields `day`, `month`, and `year`. This just specifies how far back the program should look for journals, and it won't go past this. Just set it to the first journal you have.

`enable_photo_transfer` enables or disables the functionality of transfering photos, specifically from the `photo_locations` folder path. See [Folder Paths](#folder-paths) for more.

`enable_writing_to_file` enables or disables the functionality of the program writting to the file. It will warn you if it is unable to complete the task. It's mostly helpful as a debug tool. New files and directories will still be created, as that is handled in the below setting.

`enable_new_directory_and_file_creation` enables or disables the creation of new directories or files. Most of the time this doesn't do much, but will sometimes fail to write to a file that doesn't exist or move a photo to a directory that doesn't exist, and therefore will report that.

### Settings to Use

This file serves as a way to have several settings files with different names that you can switch between. Only the first line is read, and that is the file used as the settings. The rest of the file is ignored, so you could put whatever you want there.

If you forget to add the .json file extension, it will be appended automatically.