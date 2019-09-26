Boxing Club Scheduler:
===
<h4>Usage:<h4>
<hr>
Run the appropriately named executable in the same director as the csv file that you want to use to track the schedle

<b>Note:</b> This will take the first CSV it sees, so only run it with 1 other csv in the directory

<b>Note:</b> this MUST USE PYINSTALLER <b>3.4</b> in order for windows not to think the program is a virus

<h4>Generating a New executable:<h4>
<hr>
Windows:

`pyinstaller -w -F -n windowsVersion --add-data "templates;templates" app.py`

Linux:

`pyinstaller -w -F -n linuxVersion --add-data "templates:templates" app.py`

Mac:

`pyinstaller -w -F -n macVersion --add-data "templates:templates" app.py`
