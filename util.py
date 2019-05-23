"""
util.py

Modified by Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)


This script includes a context manager wrapper function to suppress
alsa errors from voice_recognition.py.

Acknowledgement
This code is adapted from:
https://stackoverflow.com/a/17673011
"""

from contextlib import contextmanager
from ctypes import *

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)