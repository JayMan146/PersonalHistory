# TODO

## Necessary Features

* Output Level
    > 0 is nothing, 1 is very basic (wrote files, moved photos), 2 or 3 is current
* System to prompt for journal root and SETTINGS_DIRECTORY_FROM_ROOT if not found in settings (correctly)
* Put SETTINGS_DIRECTORY_FROM_ROOT in settings
* Write README.md
* Barebones GUI for easy use
    * Settings editor
    * Settings profiles
    * Import photos by opening/dragging whatever
* Allow extract from iCloud photos zips and others?
* Allow keeping the .MOV from .zip files and further settings for zip extraction

## Tweaks

* Convert checks of USER_SETTINGS to be arguments (in some cases) rather than just explicit checks to make easier to test etc. and more reusable
* More tests, and a way of testing non-helper functions (test journal directory, and symlink system to real journals?) 

## Extra Features

* Statistics
* Better ordering that "before" or "after" for custom journal format
* Add more than just previous years as intervals for previous journals
* Fancier printing (yellow text for warnings, etc.)

## Bug Fixes

* Allow for "missing days" by implementing better search