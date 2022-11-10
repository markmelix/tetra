import os, sys

sys.path.append(os.path.dirname(__file__))

del os, sys

import database
import appearance
import menu
import tabbar
import edit_buffer
import statusbar

MODULES = list(filter(lambda m: not m.startswith("__"), globals().keys()))
