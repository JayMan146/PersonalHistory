# Journal System

This Journal System, with the work-in-progress name of Personal History is a some-in-one solution for digital journaling. It can handle photos in journals, linking back to old ones from increments of one year ago, and has a ton of customizability. When run, the scripts will put outlines into files for you to write in, based on your settings. However, you will need a text editor to write your journals. This can be Windows Notepad, VSCode, or anything that can edit plain text files.

## Usage

The easiest way to use this is to run the script `easy_run.py`. This will transfer any specified photos (if enabled) and puts in any entries that are needed. The program will place the specified outline of any journals that don't exist in the past 100 days (planned to be changed at some point, see [TODO](./TODO.md)).

Alternatively, once I actually make it functional, use `gui.py` to use an interface to handle your journals. See [TODO](./TODO.md)

You can write anywhere in the journals, just don't mess with the dates in the headers of the journals (e.g. `## Wednesday 04 March 2026`)

## Integration Between the System and Your Journals

Since this is an open-source software, it is meant to be very free. The journals are just plain text files, so you can stop or start using this system whenever you want. It tracks no information, and is entirely local. It's only interaction with what you have written is skipping over it to find certain entries, just based on the headers.

## File System

Files are arranged into folders for each year, and then one markdown file for each month. Why is it like this, you may ask? Because I like it that way. And, it seems like a good balance between not everything being in one big file and a bunch of files (like one per entry). I think it adds novelty to the new month. In each year folder, there is a photos folder along with month folders for each month's photos. In general, don't mess with the names of any of these—the system will handle it all. Just write down your entry. But, you can do whatever you want with it. They're your files.

Something I would like to specifically highlight here is the naming scheme of the photos. Using the [Photo Transfer Setting](#photos) requires a specific format, and moves them to the month folders in the photos directory. However, since the photos in the journals are just links to the photos, they can be anywhere and be named anything. The program just does this for the sake of uniformity.

## Settings

Refer back to the default settings profile for reference and the style of things. This assumes you understand the basics of json.

### Format

`format` is an object for items that go between the heading of the journal and the actual entry itself, which can include extra information you want. It also has a few other parameters for the format.

`writing_lines` is an integer for the number of lines to place between the format items and the next entry for writing.

`custom_placement` is either `before` or `after` and determines if the [Custom](#custom) Format Items are before or after the [Requires Programming](#requires-programming) Format Items. 

`header_suffix` is a string to place after the header (date) for each journal entry.

#### Requires Programming

The `required_programming` object is for specifically made format items that require specific implementation. It currently has two objects: `matching_entries` and `photos`. They have the same format, as follows:

`enabled`, a boolean to toggle it.

`separator`, a string to separate each instance of the item (between each matching entry or photo)

`prefix`, a string to put before this item.

`suffix`, a string to put after this item.

#### Custom

The `custom` object is for custom format items in the entry. This has the following items:

`items`, a list of strings for all of the custom items.

There are also `separator`, `prefix`, and `suffix` fields exactly the same as in the [Requires Programming](#requires-programming) section.

### Day Crossover

`day_crossover` is an object to make it so that during some part of the day, it counts as a different day. Personally, I use it so that if I use this past midnight, it doesn't count the new day after midnight. It's not the next day until I sleep to me. It has two fields:

`time` is an object with 3 integers: `hour` (0 to 23, using 24hr time), `minute`, and `second` for the time.

`move_direction` is a string that can be either `disable`, `forward`, or `backward`. If set to `disable`, nothing happens. If set to `forward`, any point in a day **after** `time` will be considered as the next day. If set to `backward`, any point in a day **before** `time` will be considered as the previous day. Here are some examples, assuming that time is set to 13:00:00, and it is currently Wednesday:

* `move_direction` is `forward`, and is currently 14:00, it will be considered Thursday.
* `move_direction` is `forward`, and is currently 9:00, it will be considered Wednesday
* `move_direction` is `backward`, and is currently 14:00, it will be considered Wednesday.
* `move_direction` is `backward`, and is currently 9:00, it will be considered Thursday
* `move_direction` is `disabled` and it is anytime, it will be considered Wednesday.

### Photos

`enable_photo_transfer` is a boolean to control photo transfer. This is taking specifically named photos in certain directories and moving them automatically to the Journals.

`photo_locations` is a list of file paths (strings) that the system will look to transfer photos from.

#### Type Conversion

`type_conversion` is an object for converting between different file types of photos. It has the following fields:

`enabled`, a boolean

`delete_pre_converted_files`, a boolean, allows the deletion of files in their original file type.

`conversions` is a dictionary, of how to convert things. For example:

```json
"conversions": {
    "PNG": "png",
    "jpg": "jpeg",
    "heic": "jpeg",
    "heif": "jpeg"
}
```

### Earliest Entry

`earliest_entry` is an object with the integers `day`, `month`, and `year`. This just specifies how far back the program should look for journals, and it won't go past this. Just set it to the first journal you have.

### Permissions

`enable_writing_to_file` is a boolean that enables or disables the functionality of the program writting to the file. It will warn you if it is unable to complete the task. It's mostly helpful as a debug tool. New files and directories will still be created, as that is handled in the below setting.

`enable_new_directory_and_file_creation` is a boolean enables or disables the creation of new directories or files. Most of the time this doesn't do much, but will sometimes fail to write to a file that doesn't exist or move a photo to a directory that doesn't exist, and therefore will report that.

### Console Output Level

`console_output_level` is an integer or string that determines how much information will be printed to the console. Can be set to `none`, `minimum`, `medium`, or `maximum`. Setting it to `0`, `1`, `2`, or `3` is the same as the previous options.

## Settings Profile

In the JouranlSystem directory, there is a file named `settings_profile.txt`. This file serves as a way to have several settings profiles that you can switch between. Only the first line is read, and that is the file used as the settings. Do not add the .json file extension, just the name of the file. The rest of the file is ignored, so you could put whatever you want there. This will be easier to do once I implement the GUI (see [TODO](./TODO.md)).

The existance file is how the system checks if you have used it before (and have written any journals). So, if you delete the file, then it assume this is the first time you run it.