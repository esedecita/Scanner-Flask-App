from flask import Flask, render_template, redirect, request
from TwainWrapper import Scanner
import os
from TiffOperations import TIFFManipulation
from PIL import Image

app = Flask(__name__)

_scanner = Scanner()

_scanner.initialize_scanner()

list_of_scanners = _scanner.get_list_of_available_scanners()

_scanner.current_scanner = list()

_scanner.current_destination_directory = os.path.join(os.path.join(os.getcwd(), "static"), "images")


def list_of_files_in_the_directory(path):
    file_list = list()
    file_list_ext = os.listdir(path)
    for files in file_list_ext:
        name, ext = os.path.splitext(files)
        if ext.lower() == ".tif":
            file_list.append(name)
    return file_list

app.file_name_array_default = list()


@app.route('/')
def select_scanner():
    return render_template('index.html', list_of_scanners=list_of_scanners)


@app.route('/setscanner', methods=['POST'])
def set_selected_scanner():
    _scanner.current_scanner.insert(0, str(request.form.get('select_panel')))
    return redirect('/homepage')


@app.route('/homepage')
def display_homepage():
    file_list = list_of_files_in_the_directory(_scanner.current_destination_directory)
    return render_template('mainpage.html', scanner_name=_scanner.current_scanner, file_list=file_list,
                           file_name_array=app.file_name_array_default)


@app.route('/scan')
def start_scan():
    _scanner.set_scanner(_scanner.current_scanner[0], 600)
    _scanner.scan(_scanner.current_destination_directory)
    TIFFManipulation.compress_to_tiffs(_scanner.current_destination_directory, "yes")
    TIFFManipulation.tif_to_png(_scanner.current_destination_directory, "no")
    return redirect('/homepage')


@app.route('/rename', methods=['POST'])
def rename():
    os.chdir(_scanner.current_destination_directory)
    new_file_name = str(request.form.get('renamed'))
    old_file_name = str(request.form.get('original'))
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
    #file_list = list_of_files_in_the_directory(_scanner.current_destination_directory)
    imTif = Image.open(file_name+".tif")
    imPng = Image.open(file_name+".png")
    imTif = imTif.rotate(angle, expand=True)
    imPng = imTif.rotate(angle, expand=True)
    imTif.save(file_name+".tif")
    imPng.save(file_name+".png")
    app.file_name_array_default.insert(0, file_name)
    return redirect('/homepage')

@app.route('/merge', methods=['POST'])
def merge():
    file_list_csv = str(request.form.get('mergeFileList'))
    file_list_list = file_list_csv.split(",")
    for index, item in enumerate(file_list_list):
        file_list_list[index] = item + ".tif"
    TIFFManipulation.merge_tiff_files(file_list_list, _scanner.current_destination_directory, os.path.join(_scanner.current_destination_directory, "Merged"))
    return redirect("/homepage")


if __name__ == "__main__":
    app.run(debug=True)

