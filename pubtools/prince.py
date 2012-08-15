from . import run

PRINCE_PATH = "/Users/cjohnson/bin/prince"

def pdf_from_data(data):
    return run.run([PRINCE_PATH, "-"], data, binaryout=True)

def pdf_from_file(input_filepath, output_filepath):
    return run.run([PRINCE_PATH, input_filepath, output_filepath])