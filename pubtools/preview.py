from . import run

def open_data(data):
    run.run(["open","-a", "Preview", "-f"], data)

def open_filepath(filepath):
    run.run(["open","-a", "Preview", filepath])