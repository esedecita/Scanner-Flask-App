from flask import Flask, render_template, redirect, request
from TwainWrapper2 import Scanner
import os
from TiffOperations import TIFFManipulation
from PIL import Image

app = Flask(__name__)

_scanner = Scanner()
_scanner.initialize_scanner()
list_of_scanners = _scanner.get_list_of_available_scanners()
_tiff_opr = TIFFManipulation()
app.scanner_mem = list()
_scanner.current_destination_directory = "C:\Users\gpatil\Desktop\Scanner Flask App\static\images"


def list_of_files_in_the_directory():
    os.chdir("C:\Users\gpatil\Desktop\Scanner Flask App\static\images")
    file_list = list()
    file_list_ext = os.listdir(os.getcwd())
    for files in file_list_ext:
        name, ext = os.path.splitext(files)
        if ext.lower() == ".tif":
            file_list.append(name)
    return file_list

app.file_name_array_default = list()
app.file_name_array_default.insert(0, "sample")

@app.route('/')
def select_scanner():
    return render_template('index.html', list_of_scanners=list_of_scanners)


@app.route('/setscanner', methods=['POST'])
def set_selected_scanner():
    _scanner.current_scanner = str(request.form.get('select_panel'))
    return redirect('/homepage')


@app.route('/homepage')
def display_homepage():
    app.scanner_mem.insert(0, _scanner.current_scanner)
    file_list = list_of_files_in_the_directory()
    return render_template('mainpage.html', scanner_name=app.scanner_mem, file_list=file_list, file_name_array=app.file_name_array_default)


@app.route('/scan')
def start_scan():
    _scanner.set_scanner(_scanner.current_scanner, 600)
    _scanner.scan("C:\Users\gpatil\Desktop\Scanner Flask App\static\images")
    _tiff_opr.compress_to_tiffs(_scanner.current_destination_directory, "yes")
    _tiff_opr.tif_to_png(_scanner.current_destination_directory, "no")
    return redirect('/homepage')


@app.route('/rename', methods=['POST'])
def rename():
    os.chdir(_scanner.current_destination_directory)
    new_file_name = str(request.form.get('renamed'))
    old_file_name = str(request.form.get('original'))
    list_of_files_in_destination = []
    list_of_files_in_destination = os.listdir(_scanner.current_destination_directory)
    for files in list_of_files_in_destination:
        name, ext = os.path.splitext(files)
        if name == old_file_name:
            os.rename(os.path.join(os.getcwd(), files), os.path.join(os.getcwd(), new_file_name + ext))

    return redirect("/homepage")


@app.route('/rotate', methods=['POST'])
def rotate():
    os.chdir(_scanner.current_destination_directory)
    angle = int(request.form.get('angle'))
    file_name = str(request.form.get('fileName'))
    file_name_array = list()
    file_name_array.insert(0, file_name)
    file_list = list_of_files_in_the_directory()
    imTif = Image.open(file_name+".tif")
    imPng = Image.open(file_name+".png")
    imTif = imTif.rotate(angle, expand=True)
    imPng = imTif.rotate(angle, expand=True)
    imTif.save(file_name+".tif")
    imPng.save(file_name+".png")
    app.file_name_array_default.insert(0, file_name)
    return redirect('/homepage')


if __name__ == "__main__":
    app.run(debug=True)

