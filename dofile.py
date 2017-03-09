import sys
from subprocess import run

def redo_ifchange(*args):
    """
    Redo if the arguments have changed
    """

    # Logic here to get file paths of python objects

    run(['redo-ifchange',*args])
