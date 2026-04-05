# TODO

## Necessary Features

* Move all of this to testing area, have some sort of "release" version or git clone or something in my Journal
* More tests, and a way of testing non-helper functions (related to above bullet point)
* Write README.md
* Barebones GUI for easy use
    * Settings editor
    * Settings profiles
    * Import photos by opening/dragging whatever
* Allow extract from iCloud photos zips and others?
* Allow keeping the .MOV from .zip files and further settings for zip extraction
* Add method for initial setup
* Prevent outputting "Journal Text Written to File(s):" if nothing was actually written. Instead, output something like "No Text Was Written to Any Files."

## Extra Features

* Statistics
* Better ordering that "before" or "after" for custom journal format
* Add more than just previous years as intervals for previous journals
* Fancier printing (yellow text for warnings, etc.)

## Refactoring

* Follow [ISO 8601](https://iso8601.com/), to a degree. This involves changing the photo format, headers of journals, and folder structure
* Optional, make each entry a separate file. Folders for each month, photos directory per month.
* Convert checks of USER_SETTINGS to be arguments (in some cases) rather than just explicit checks to make easier to test etc. and more reusable
* Split up create_base_journal_entries into separate modules: settings, journal, photos, util (possibly better name)

## Bug Fixes

* Allow for "missing days" by implementing better search

## Tweaks (None)