import os
import sys


def get_resource_path(relative_path):
    """ Get absolute path to resource, resource files are located to exe file directory
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
