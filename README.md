**PLEASE NOTE! THIS IS LARGELY OUT OF DATE.**

# Journal System

## Settings

Refer back to the default settings profile for reference and the style of things. This assumes you understand the basics of json.

### Format

`format` is an object for items that go between the heading of the journal and the actual entry itself, which can include extra information you want. It also has a few other parameters for the format.

`writing_lines` is an integer for the number of lines to place between the format items and the next entry for writing.

`custom_placement` is either `before` or `after` and determines if the [Custom](#custom) Format Items are before or after the [Requires Programming](#requires-programming) Format Items. 

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

### Other

This is anything that didn't fit anywhere else.

`earliest_entry` is an object with the integers `day`, `month`, and `year`. This just specifies how far back the program should look for journals, and it won't go past this. Just set it to the first journal you have.

`enable_writing_to_file` is a boolean that enables or disables the functionality of the program writting to the file. It will warn you if it is unable to complete the task. It's mostly helpful as a debug tool. New files and directories will still be created, as that is handled in the below setting.

`enable_new_directory_and_file_creation` is a boolean enables or disables the creation of new directories or files. Most of the time this doesn't do much, but will sometimes fail to write to a file that doesn't exist or move a photo to a directory that doesn't exist, and therefore will report that.

`console_output_level` determines how much information will be printed to the console. Can be set to `none`, `minimum`, `medium`, or `maximum`. Setting it to `0`, `1`, `2`, or `3` is the same as the previous options.

## Settings to Use

This file serves as a way to have several settings files with different names that you can switch between. Only the first line is read, and that is the file used as the settings. The rest of the file is ignored, so you could put whatever you want there.

If you forget to add the .json file extension, it will be appended automatically.