import os
import re
from enum import Enum

class Status(Enum):
    unknown = 1
    up = 2
    down = 3

def reverse_readline(filename, buffer_size=8196):
    log = open(filename)
    rest = None
    log.seek(0, os.SEEK_END)
    total_size = current_position = log.tell()
    while current_position > 0:
        read_size = buffer_size
        if current_position < buffer_size:
            read_size = current_position
        current_position -= read_size
        log.seek(current_position)
        read_buffer = log.read(read_size)
        lines = read_buffer.split('\n')
        if rest is not None:
            if read_buffer[-1] != '\n':
                lines[-1] += rest
            else:
                yield rest
        for line in lines[-1:0:-1]:
            yield line
    log.close()

def get_status(filename):
    regex_ok  = re.compile(r'(INFO|DEBUG|WARNING)')
    regex_bad = re.compile(r'(ERROR|CRITICAL)')
    for line in reverse_readline(filename):
        if regex_ok.search(line):
            return Status.up
        elif regex_bad.search(line):
            return Status.down
    return Status.unknown
