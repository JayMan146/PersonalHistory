# TODO

## Necessary Features

* Move all of this to testing area, have some sort of "release" version or git clone or something in my Journal
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