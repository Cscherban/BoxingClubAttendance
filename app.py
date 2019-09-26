from flask import Flask, request,render_template, redirect
import glob
from recordProcessor import BoxingClubProcessor
import os
import sys
from datetime import datetime
from pytz import timezone
import webbrowser
from threading import Timer


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

current_dir = os.path.dirname(sys.argv[0])
processor = None
error = "None"
print(current_dir)

@app.route('/')
def hello_world():
    return render_template("start-screen.html")


@app.route('/initialize', methods=['POST'])
def init():
    global error
    global processor
    global current_dir
    error = "None"
    try:
        if getattr(sys, 'frozen', False):
            csv_dir = os.path.join(current_dir, "*.csv")
        else:
            csv_dir = "*.csv"
        print(csv_dir)
        print(current_dir)
        csvs = glob.glob(csv_dir)
        print(csvs)
        if len(csvs) != 0:
            processor = BoxingClubProcessor(fileName=csvs[0])
    except Exception as e:
        error = str(e)
        return render_template("start-screen.html", error=error)

    return redirect('/table')


@app.route('/set-date-today', methods=['POST'])
def set_today_as_recording_date():
    global processor
    global error
    tz = timezone('US/Eastern')
    try:
        date_string = datetime.now(tz).today().strftime('%m/%d/%Y')
        processor.set_date(date_string)
        processor.add_date_to_csv(date_string)
    except Exception as e:
        error = str(e)
        return render_template("table-visual.html", table_visual=processor.get_html(), date_initialized=True,
                               error=error)

    return redirect('/table')


@app.route('/terminate', methods=['GET'])
def terminate():
    os._exit(0)
    return None

@app.route('/add-new-person', methods=['POST'])
def add_new_person():
    global error
    global processor
    error = "None"
    try:
        if processor is None:
            return redirect('/')

        if request.method == 'POST':
            name = request.form.get('name')
            gtid = request.form.get('gtid')
            processor.add_new_person(gtid,name)
            return redirect('/table')

    except Exception as e:
        error = str(e)
        return render_template("table-visual.html", table_visual=processor.get_html(), date_initialized=True, error=error)



@app.route('/table', methods=['GET', 'POST'])
def handle_table():
    global error
    global processor
    error = "None"
    if processor is None:
        return redirect('/')

    date_set = processor.date is not None
    try:
        if request.method == 'POST':
            scanner_input = request.form.get('scannerInput')
            gtid = processor.process_scanner_output(scanner_input)
            print(gtid)
            if gtid is None:
                return render_template("table-visual.html", invalid="true", date_initialized=date_set,table_visual=processor.get_html(), error=error)
            exists = processor.check_exists(gtid)
            print exists
            if exists:
                processor.mark_as_attended(gtid)
            return render_template("table-visual.html", exists=exists, date_initialized=date_set, table_visual=processor.get_html(), error=error)
        else:
            return render_template("table-visual.html", table_visual=processor.get_html(), date_initialized=date_set, error=error)
    except Exception as e:
        error = str(e)
        return render_template("table-visual.html", table_visual=processor.get_html(), date_initialized=date_set, error=error)

@app.route('/person/<gtid>', methods=['POST', 'DELETE'])
def person_stuff(gtid):
    if request.method == 'POST':
        name = request.form.get('name')
        processor.add_new_person(gtid, name)
        return redirect("/table")
    elif request.method == 'DELETE':
        processor.remove_gtid(gtid)
        return redirect("/table")


@app.route('/date/', methods=['POST'])
def remove_date():
    date = request.form.get('date')
    processor.remove_date(date)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:2000/')


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=2000)
