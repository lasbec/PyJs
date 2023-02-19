import subprocess
import os
from Py2Js import *

def run_py_file(filePath):
    result = subprocess.run(['py', filePath], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def run_js_file(filePath):
    result = subprocess.run(['node', filePath], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")
    


def test_eq_console_output(py_file_path, verbose):
    try:
        js_file_path = translate_py_to_js_file(py_file_path, verbose)
        js_output = run_js_file(js_file_path)
        py_output = run_py_file(py_file_path)
        try:
            assert js_output == py_output
            print("passed", py_file_path)
        except AssertionError:
            print("--FAILED--", py_file_path)
            print("py output:", py_output)
            print("js output:", js_output)
    except Exception as e:
        print("FATAL--FAILURE:", py_file_path,"::", e)
        if(verbose):
            print(e.with_traceback())

    




