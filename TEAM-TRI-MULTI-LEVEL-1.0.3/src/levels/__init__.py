from importlib import import_module
from src.screen import Screen
import re
import importlib.machinery
from . import *

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()




def fetch_screen(screen_name, *args, **kwargs):

    try:
        if '.' in screen_name:
            module_name, class_name = screen_name.rsplit('.', 1)
        else:
            module_name = convert(screen_name)
            class_name = screen_name # screen_name.capitalize()

        screen_module = import_module("." + module_name, package='levels')

        screen_class = getattr(screen_module, class_name)

        instance = screen_class(*args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our screen collection!'.format(screen_name))
    else:
        if not issubclass(screen_class, Screen):
            raise ImportError("We currently don't have {}, but you are welcome to send in the request for it!".format(screen_class))

    return instance

def fetch_static_class(screen_name, *args, **kwargs):

    try:
        if '.' in screen_name:
            module_name, class_name = screen_name.rsplit('.', 1)
        else:
            module_name = convert(screen_name)
            class_name = screen_name # screen_name.capitalize()

        screen_module = import_module("." + module_name, package='levels')

        screen_class = getattr(screen_module, class_name)


        # instance = screen_class(*args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our screen collection!'.format(screen_name))
    else:
        if not issubclass(screen_class, Screen):
            raise ImportError("We currently don't have {}, but you are welcome to send in the request for it!".format(screen_class))

    return screen_class
