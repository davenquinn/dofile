import sys
from subprocess import run
import click
from click import style

__prefix = style('redo ',fg='green')

def echo(msg, **kwargs):
    click.echo(msg, err=True, **kwargs)

gb = lambda x: style(x,fg='green', bold=True)

def redo_ifchange(*args):
    """
    Redo if the arguments have changed
    """

    # Logic here to get file paths of python objects

    run(['redo-ifchange',*args])

__file_ignores = ('site-packages','Python.framework')

def find_user_modules(*ignored_modules):
    from sys import modules

    echo(__prefix+gb("Tracking python dependencies"))
    for name, module in modules.items():
        try:
            fn = module.__file__
        except AttributeError:
            # Builtins
            continue

        # Don't worry about system modules
        # TODO: check for Linux/Windows patterns
        if any(x in fn for x in __file_ignores):
            continue
        # Get rid of ignored modules
        if any(x in name for x in ignored_modules):
            continue

        echo("     "+name)
        yield fn

def get_name(module):
    try:
        return module.__name__
    except AttributeError:
        # Presumably we have passed a string
        return module

def redo_modules(*ignored_modules):
    """
    You can call this in a dofile or in a script
    to update dependencies for this task
    """
    ignores = list(ignored_modules)+['__main__', '__mp_main__']
    ignored_module_names = (get_name(i) for i in ignores)

    files = list(find_user_modules(*ignored_module_names))
    echo(__prefix+gb("{} modules found".format(len(files))))
    redo_ifchange(*files)

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

