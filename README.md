# Personal History

Personal History is a some-in-one solution for digital journaling. It can handle photos in journals, linking back to old ones from increments of one year ago, and has a ton of customizability. When run, the scripts will put outlines into files for you to write in, based on your settings. However, you will need a text editor to write your journals. This can be Windows Notepad, VSCode, or anything that can edit plain text files.

## Installation

1. Make a directory, anywhere, for your journals to live. For example, I have a folder named `Journals`. 
1. Get the code in some manner, either through downloading it or `git clone`-ing it. Make sure the `PersonalHistory` folder is in there. (So the path to this README file would be `whatever/Journals/PersonalHistory/README.md`.) 
1. If you're running code directly, and not a binary or executable, make sure you have python. Some systems have it already, check by using the command `python` in a terminal. If you see `>>>`, you're good to go. Type `exit()` and hit enter, or close the terminal. If you don't have it, visit the [Python Website](https://www.python.org/downloads/) to download it. On Linux, you can also use the commands `sudo apt update`, `sudo apt upgrade`, and then `sudo apt install python3` and `sudo apt install python3-pip` to get it.
1. Once again, if you're running the code directly, you'll need to install the requirements. To do this, run `pip install -r REQUIREMENTS.txt`, with whichever instance of pip you'll be using. If you get a long paragraph starting with `error: externally-managed-environment`, then take a look at the [section below](#python-venv). 
1. Finally, you'll want to run the [initialize.py](./initialize.py) script to set up the journals. After that, you're good to go, read the the [Usage](#usage) section below on how to use it.

### Python VENV

So, if you get the `externally-managed-environment` error, you'll need a Python VENV, or Virtual Environment.

1. Choose a folder to put this in. Could be on your desktop, or anywhere, really. I'd put it in your home or user directory. 
1. Run the command `python -m venv path/to/your/folder` to create the venv.
    * If you don't have that installed, try installing a new version of python from the website. Alternatively, use the command `sudo apt-get install python3-venv` on Debian-based systems. 
1. After that, use the executable at `path/to/your/folder/bin/python` to run the scripts and `path/to/your/folder/bin/pip` to perform the Requirement installation step (step 4 of [Installation](#installation))

## Usage

The easiest way to use this is to run the script [easy_run.py](./easy_run.py). This will transfer any specified photos (if enabled) and puts in any entries that are needed. Currently, the format of these photos is `<day> <index> <month> <year>.<extension>`. Day is the day of the month, index is the number of the photo for that day, between `00` and `99`. Month is the month of the photo, written out. Year and extension are self-explanatory. Both day and index require leading zeros (for example, `05`, not `5`). Here is an example of a photo name: `12 02 january 2026` Finally, the program will place the specified outline of any journals that don't exist in the past 100 days (planned to be changed at some point, see [TODO](./TODO.md)). If it is your first time using it, it will create an entry only for today and ignore any other days or photos.

Alternatively, once I actually make it functional, use [gui.py](./gui.py) to use an interface to handle your journals. See [TODO](./TODO.md)

You can write anywhere in the journals, just don't mess with the dates in the headers of the journals (e.g. `## Wednesday 04 March 2026`)

## Integration Between the System and Your Journals

Since this is an open-source software, it is meant to be very free. The journals are just plain text files, so you can stop or start using this system whenever you want. It tracks no information, and is entirely local. It's only interaction with what you have written is skipping over it to find certain entries, just based on the headers. That last line will no longer be true once I get the [Statistics](./statistics.py) up and running, but it will stil be entirely local with no data going to anyone.

## File System

Files are arranged into folders for each year, and then one markdown file for each month. Why is it like this, you may ask? Because I like it that way. And, it seems like a good balance between not everything being in one big file and a bunch of files (like one per entry). I think it adds novelty to the new month. In each year folder, there is a photos folder along with month folders for each month's photos. In general, don't mess with the names of any of these—the system will handle it all. Just write down your entry. But, you *can* do whatever you want with it. They're *your* files.

Something I would like to specifically highlight here is the naming scheme of the photos. Using the [Photo Transfer Setting](#photos) requires a specific format, and moves them to the month folders in the photos directory. However, since the photos in the journals are just links to the photos, they can be anywhere and be named anything. The program just does this for the sake of uniformity and simplicity.

## Settings

Refer back to the default settings profile for reference and the style of things. If you don't match the given set of options you can pick from in the settings, it will either cause errors or be defaulted to something usable. I should probably fix it if it is the former case. This assumes you understand the basics of json. If not, do some googling. For quick reference:

* String - any amount of text
* Integer - any number, negative or positive, with no decimal portion
* Float - an integer that can have a decimal portion
* List - a list of any of the other kinds
* Object - a mapping of any of the other kinds.

Here's an example:
```json
{
    "string": "Hi! -146",
    "integer": 2837,
    "float": 22.31102,
    "list": [
        1,
        2,
        "d"
    ],
    "object": {
        "string": "hi again.",
        "list": [
            "woah",
            "another",
            "list!"
        ]
    }
}
```

### Format

`format` is an object for items that go between the heading of the journal and the actual entry itself, which can include extra information you want. It also has a few other parameters for the format. Here's an example of a journal with various custom formatting:

```md
## Saturday 17 August 2013: This is My Journal Title!

![](./photos/17%20august%202013/17%2000%20august%202013.png)
This is a caption I've written for this photo that was automatically inserted by the program.

![](./photos/17%20august%202013/17%2001%20august%202013.png)
Here's another photo I might have.

Previous Same-Date Journals: [2012](../2012/08%20august%202024.md#friday-17-august-2012-a-title-of-a-past-journal), [2011](../2012/08%20august%202024.md#wednesday-17-august-2011-another-title-of-a-past-journal)

Today's Rating: This is a format item about how I would rate the day!

Three Things I'm Grateful for Today:
1. Here is another
2. Format
3. Item!

This is my actual entry. I had a great day involving a lot of pancakes.
```

This example could be achieved with the following `format` object:

```json
"format": {
    "requires_programming": {
        "matching_entries": {
            "enabled": true,
            "separator": ", ",
            "prefix": "\nPrevious Same-Date Journals: ",
            "suffix": "\n"
        },
        "photos": {
            "enabled": true,
            "separator": "\n\n",
            "prefix": "\n",
            "suffix": "\n"
        }
    },
    "custom": {
        "items": [
            "Today's Rating:\n",
            "Three Things I'm Grateful for Today:\n1. \n2. \n3. "
        ],
        "separator": "\n",
        "prefix": "\n\n",
        "suffix": ""
    },
    "custom_placement": "after",
    "writing_lines": 3,
    "header_suffix": ": "
}
```

`writing_lines` is a positive integer for the number of lines to place between the format items and the next entry for writing.

`custom_placement` is either `before` or `after` and determines if the [Custom](#custom) Format Items are before or after the [Requires Programming](#requires-programming) Format Items.

`header_suffix` is a string to place after the header (date) for each journal entry.

#### Requires Programming

The `required_programming` object is for specifically made format items that require specific implementation. It currently has two objects: `matching_entries` and `photos`. Matching entries is for linking back to journals written on the same day, just a different year. For example, the journal for `05 June 2024` will have a link to `05 June 2023`. Photos is hopefully self-explanatory—it holds links to photos that are for the day. Read more about this in the [Photos Section](#photos).

These two format objects have the same format, as follows:

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

`time` is an object with 3 positive integers: `hour` (0 to 23, using 24hr time), `minute`, and `second` for the time.

`move_direction` is a string that can be either `disable`, `forward`, or `backward`. If set to `disable`, nothing happens. If set to `forward`, any point in a day **after** `time` will be considered as the next day. If set to `backward`, any point in a day **before** `time` will be considered as the previous day. Here are some examples, assuming that time is set to 13:00:00, and it is currently Wednesday:

* `move_direction` is `forward`, and is currently 14:00, it will be considered Thursday.
* `move_direction` is `forward`, and is currently 9:00, it will be considered Wednesday
* `move_direction` is `backward`, and is currently 14:00, it will be considered Wednesday.
* `move_direction` is `backward`, and is currently 9:00, it will be considered Thursday
* `move_direction` is `disabled` and it is anytime, it will be considered Wednesday.

### Photos

`enable_photo_transfer` is a boolean to control photo transfer. This is taking specifically named photos in certain directories and moving them automatically to the Journals.

`enable_zip_extraction` is a boolean to control extraction of photos from zip files. If a zip file is named to the correct format, it will take the photo in the zip file and keep the photo file. Then, it is handled like other photos.

`photo_locations` is a list of file paths (strings) that the system will look to transfer photos from.

#### Type Conversion

`type_conversion` is an object for converting between different file types of photos. It has the following fields:

`enabled`, a boolean

`delete_pre_converted_files`, a boolean, allows the deletion of files in their original file type.

`conversions` is a dictionary, of how to convert things. For example:

```json
"conversions": {
    "jpeg": "png",
    "heic": "jpeg",
    "heif": "jpeg"
}
```

### Earliest Entry

`earliest_entry` is an object with the positive integers `day`, `month`, and `year`. This just specifies how far back the program should look for journals, and it won't go past this. Just set it to the first journal you have.

### Permissions

`enable_writing_to_file` is a boolean that enables or disables the functionality of the program writting to the file. It will warn you if it is unable to complete the task. It's mostly helpful as a debug tool. New files and directories will still be created, as that is handled in the below setting.

`enable_new_directory_and_file_creation` is a boolean enables or disables the creation of new directories or files. Most of the time this doesn't do much, but will sometimes fail to write to a file that doesn't exist or move a photo to a directory that doesn't exist, and therefore will report that.

### Console Output Level

`console_output_level` is an integer or string that determines how much information will be printed to the console. Can be set to `none`, `minimum`, `medium`, or `maximum`. Setting it to `0`, `1`, `2`, or `3` is the same as the previous options.

## Settings Profile

In the JouranlSystem directory, there is a file named `selected_profile.txt`. This file serves as a way to have several settings profiles that you can switch between. Only the first line is read, and that is the file used as the settings. Do not add the .json file extension, just the name of the file. The rest of the file is ignored, so you could put whatever you want there. This will be easier to do once I implement the GUI (see [TODO](./TODO.md)).

The existance file is how the system checks if you have used it before (and have written any journals). So, if you delete the file, then it assume this is the first time you run it.