# TODO

## Necessary Features

* Update README to say Python is required, and line about externally managed environment or whatever
* More tests, and a way of testing non-helper functions
* Barebones GUI for easy use
    * Settings editor
    * Settings profiles
    * Import photos by opening/dragging whatever
* Allow extract from iCloud photos zips and others?
* Allow keeping the .MOV from .zip files and further customization for zip extraction

## Extra Features

* Statistics
* Some method for customizability of formats of folders, photo names, journal headers, etc. At the very least, the latter.
* Better ordering that "before" or "after" for custom journal format
* Add more than just previous years as intervals for previous journals
* Fancier printing (yellow text for warnings, etc.)

## Refactoring

* Break up write_entry into smaller functions
* Follow [ISO 8601](https://iso8601.com/), to a degree. This involves changing the photo format and folders. Journal headers should stay the same.
* Convert checks of USER_SETTINGS to be arguments (in some cases) rather than just explicit checks to make easier to test etc. and more reusable
* Further split up journal_system into separate files: settings, journal, photos, util (possibly better name)

## Bug Fixes

* Allow for "missing days" by implementing better search

## Tweaks (None)