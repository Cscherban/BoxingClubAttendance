###Boxing Club Scheduler:
___
#####Usage:
Run the appropriately named executable in the same director as the csv file that you want to use to track the schedle

**Note:** This will take the first CSV it sees, so only run it with 1 other csv in the directory


###Generating a New executable 
Windows:

`pyinstaller -w -F -n windowsVersion --add-data "templates;templates" app.py`

Linux:

`pyinstaller -w -F -n linuxVersion --add-data "templates:templates" app.py`

Mac:

`pyinstaller -w -F -n macVersion --add-data "templates:templates" app.py`
