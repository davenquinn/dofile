import sys
from subprocess import run
import click
from click import style

__prefix = style('redo ',fg='green')

def echo(msg, **kwargs):
    click.echo(msg, err=True, **kwargs)

gb = lambda x: style(x,fg='green', bold=True)

def __redo_ifchange(*args):
    """
    Redo if the arguments have changed
    """

    # Logic here to get file paths of python objects

    run(['redo-ifchange',*args])

__file_ignores = ('site-packages','Python.framework')

has_any = lambda fn, patterns: any(x in fn for x in patterns)

def find_user_modules(match=None, ignore=[]):
    from sys import modules

    echo(__prefix+gb("Tracking python dependencies"))
    for name, module in list(modules.items()):
        try:
            fn = module.__file__
        except AttributeError:
            # Builtins
            continue

        # Don't worry about system modules
        # TODO: check for Linux/Windows patterns
        if has_any(fn,__file_ignores):
            continue
        # Get rid of explicitly ignored modules
        __sys_ignores = ['__main__', '__mp_main__']
        if has_any(name,__sys_ignores):
            continue
        if has_any(name,ignore):
            echo("     "+style("ignored ",fg='red')+name)
            continue

        # If we specify patterns to match, then we must
        # find the string within these
        if not (match is None or has_any(name,match)):
            continue

        echo("     "+name)
        yield fn

def get_name(module):
    try:
        return module.__name__
    except AttributeError:
        # Presumably we have passed a string
        return module

def redo_modules(*modules, ignore=[]):
    """
    You can call this in a dofile or in a script
    to update dependencies for this task
    """
    ignored_module_names = (get_name(i) for i in ignore)

    files = list(find_user_modules(*modules, ignore=ignore))
    echo(__prefix+gb("Tracking {} python modules".format(len(files))))
    __redo_ifchange(*files)

def redo_ifchange(*args, modules=True, ignore=[]):
    # A synthesis which will track modules by default
    # as well as files that it is asked to track
    # Could check for open file handlers as well?
    if modules:
        redo_modules(ignore=ignore)
    __redo_ifchange(*args)

def redirect():
    sys.stdout = sys.stderr

## Monkey-patch IPython embed to redirect stdout (experimental)
# import IPython
# We need to do something with pty forks I think
# __base_embed = IPython.embed
# def embed():
    # # Python 3.4+
    # from contextlib import redirect_stdout
    # with redirect_stdout('/dev/tty'):
        # IPython.embed()
# #__base_embed
# Also look at tty.setraw() function which I think does what we need
# import sys
# import tty
# sys.stdout = sys.stderr
# tty.setcbreak(sys.stdout)
# from IPython import embed
# embed()

