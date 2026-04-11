**PLEASE NOTE! THIS IS LARGELY OUT OF DATE.**

# Journal System

This doesn't have any info yet, but I figured I should add the file.

## Settings

Refer back to the default settings profile for reference and the style of things.

### Format

I'll write this later.

### Day Crossover

This is a way to make it so that during some part of the day, it counts as a different day. Personally, I use it so that if I run this past midnight, it doesn't count the new day after midnight. It's not the next day until I sleep to me.

This has two fields.

`time` is simple: just specify `hour` (24 hour system), `minute`, and `second` for the time. For example:

```json
"time": {
    "hour": 13,
    "minute": 0,
    "second": 0
}
```

`move_direction` can be either `disable`, `forward`, or `backward`. If set to `disable`, nothing happens. If set to `forward`, any point in a day **after** `time` will be considered as the next day. If set to `backward`, any point in a day **before** `time` will be considered as the previous day. Here are some examples, assuming the example for `time` above is used, and it is currently Wednesday:

* `move_direction` is `forward`, and is currently 14:00, it will be considered Thursday.
* `move_direction` is `forward`, and is currently 9:00, it will be considered Wednesday
* `move_direction` is `backward`, and is currently 14:00, it will be considered Wednesday.
* `move_direction` is `backward`, and is currently 9:00, it will be considered Thursday

### Photos

`enable_photo_transfer`, `true` or `false`, enables photo transfers. This is taking specifically named photos in certain directories and moving them automatically to the Journals.

`photo_locations` is a list of file paths that the system will look to transfer photos from.

#### Type Conversion

`type_conversion` is another field which has three sub-fields.

`enabled`, `true` or `false`, turns this feature on or off.

`delete_pre_converted_files`, `true` or `false` allows the deletion of files in their original file type.

`conversions` is a dictionary, of how to convert things. For example:

```json
"type_conversion": {
    "enabled": true,
    "delete_pre_converted_files": true,
    "conversions": {
        "PNG": "png",
        "jpg": "jpeg",
        "heic": "jpeg",
        "heif": "jpeg"
    }
}
```

### Other

This is anything that didn't fit anywhere else.

`earliest_entry` is a date object with the fields `day`, `month`, and `year`. This just specifies how far back the program should look for journals, and it won't go past this. Just set it to the first journal you have.

`enable_writing_to_file` enables or disables the functionality of the program writting to the file. It will warn you if it is unable to complete the task. It's mostly helpful as a debug tool. New files and directories will still be created, as that is handled in the below setting.

`enable_new_directory_and_file_creation` enables or disables the creation of new directories or files. Most of the time this doesn't do much, but will sometimes fail to write to a file that doesn't exist or move a photo to a directory that doesn't exist, and therefore will report that.

`console_output_level` determines how much information will be printed to the console. Can be set to `none`, `minimum`, `medium`, or `maximum`. Setting it to `0`, `1`, `2`, or `3` is the same as the following options

## Settings to Use

This file serves as a way to have several settings files with different names that you can switch between. Only the first line is read, and that is the file used as the settings. The rest of the file is ignored, so you could put whatever you want there.

If you forget to add the .json file extension, it will be appended automatically.