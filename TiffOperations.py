import os
import subprocess
import datetime
import shutil
from PythonMagick import Image
import stat


class TIFFManipulation(object):

    recent_converted_directory = ""

    def __init__(self):
        pass

    @staticmethod
    def convert_directory_to_tiff(source, destination, remove_source_directory):
        """This method converts a directory containing bitmaps to tiffs and stores them in a new location. PythonMagick
        is used in the process of conversion the resulting images are uncompressed and are of the same size as the
        original bitmaps therefore implying loss-less conversion

        remove_source_directory takes 'yes' or 'no'
        """
        if remove_source_directory == 'yes' or 'no':
            list_of_files_in_the_directory = os.listdir(source)
            for files in list_of_files_in_the_directory:
                name, ext = os.path.splitext(files)
                if ext.lower() == '.bmp':
                    Image(os.path.join(source, files)).write(os.path.join(source, name + str('.tiff')))
            refresh_list = os.listdir(source)
            tiff_folder = os.path.join(destination, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            TIFFManipulation.recent_converted_directory = tiff_folder
            os.mkdir(tiff_folder)
            for tiffs in refresh_list:
                name, ext = os.path.splitext(tiffs)
                if ext.lower() == '.tiff':
                    shutil.move(os.path.join(source, tiffs), os.path.join(tiff_folder, tiffs))
            if remove_source_directory == 'yes':
                def on_rm_error(func, path, exc_info):
                    # path contains the path of the file that couldn't be removed
                    # let's just assume that it's read-only and unlink it.
                    os.chmod(path, stat.S_IWRITE)
                    os.unlink(path)

                shutil.rmtree(source, onerror=on_rm_error)
        else:
            print "The third argument is either the string 'yes' or 'no'"

    @staticmethod
    def merge_tiff_files(list_of_files, path, destination):
        os.chdir(path)
        #list of files to CSV
        csv_file_names = ",".join(list_of_files)
        merged_tiff_filename = "Merge" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + ".tif"
        newMergedFile = os.path.join(destination, merged_tiff_filename)
        subprocess.Popen("i_view32 /multitif=" + "(" + newMergedFile + "," + csv_file_names + ")", shell=True,
                         stdout=subprocess.PIPE,  env={'PATH': os.getenv('PATH')}).stdout.read()

    @staticmethod
    def compress_to_tiffs(source, remove_old_files):
        """
        This method compresses all the tiff files in a given folder. The Huffman algorithm is used for compression
        provided in the Irfan view software.
        :param source
        :param remove_old_files: 'yes' or 'no'
        :return:
        """
        os.chdir(source)
        subprocess.Popen("i_view32.exe *.bmp /tifc=5 /convert=*.tif", shell=True,
                         stdout=subprocess.PIPE, env={'PATH': os.getenv('PATH')}).stdout.read()
        if remove_old_files == 'yes':
            list_of_files_in_the_folder = os.listdir(source)
            for files in list_of_files_in_the_folder:
                name, ext = os.path.splitext(files)
                if ext.lower() == ".bmp":
                    os.remove(os.path.join(source, files))

    @staticmethod
    def tif_to_png(source, remove_old_files):
        """
        This method compresses all the tiff files in a given folder. The Huffman algorithm is used for compression
        provided in the Irfan view software.
        :param source
        :param remove_old_files: 'yes' or 'no'
        :return:
        """
        os.chdir(source)
        subprocess.Popen("i_view32.exe *.tif /tifc=5 /convert=*.png", shell=True,
                         stdout=subprocess.PIPE, env={'PATH': os.getenv('PATH')}).stdout.read()
        if remove_old_files == 'yes':
            list_of_files_in_the_folder = os.listdir(source)
            for files in list_of_files_in_the_folder:
                name, ext = os.path.splitext(files)
                if ext.lower() == ".tif":
                    os.remove(os.path.join(source, files))
