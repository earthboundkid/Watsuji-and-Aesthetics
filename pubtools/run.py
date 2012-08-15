#!/usr/local/bin/python3

"Convenience module for subprocess."

from subprocess import Popen, PIPE

class ReturnedError(Exception): pass

def run(command, input="", binaryout=False, encoding="UTF-8",
        stdin=PIPE, stdout=PIPE, stderr=PIPE):
    """Returns result of running 'command'. 
    'command' can be string (will be split) or a list."""
    
    #Deal with unicode
    #If you want some other encoding, send us bytes.
    if not isinstance(input, bytes):
        input = bytes(input, encoding=encoding)
    
    #Subprocess wants a list of commands
    if hasattr(command, "split"):
        command = command.split()
    
    process = Popen(command, stdin=stdin, stdout=stdout, stderr=stderr)
    output, err = process.communicate(input)
    
    if not binaryout: 
        output = output.decode(encoding)
    
    #Raise errors, but make the output salvagable
    if err:
        e = ReturnedError(err)
        e.output = output
        raise e
    
    return output