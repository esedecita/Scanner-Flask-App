from flask import Flask, render_template, redirect, request
from TwainWrapper import Scanner
import os
app = Flask(__name__)

_scanner = Scanner()
_scanner_object = _scanner.get_sources()
sources_list = _scanner.get_source_list(_scanner_object)
selected_scanner = ''
selected_scanner_arr = []
selected_scanner_arr.append(selected_scanner)

@app.route('/')
def app_launch():
    return render_template('index.html', sources_list=sources_list)


@app.route('/homepage', methods=['POST'])
def home_page():
        result = request.form.get('select_panel')
        app.selected_scanner = str(result)
        scanner_name = []
        scanner_name.append(str(result))
        return render_template('mainpage.html', scanner_name=scanner_name)

@app.route('/scannedsuccessfully')
def scan_done():
    return redirect('/')

@app.route('/scan')
def scan():
    #scanner_name = request.form.get("temp_field")
    #scanner_name = scanner_name.replace("_", " ")
    #_scanner.open_sources(_scanner_object, selected_scanner)
    #_scanner.start_scan("C:\Users\gpatil\Desktop\misc")
    return redirect("/scannedsuccessfully")


if __name__ == "__main__":
    app.run(debug=True)
