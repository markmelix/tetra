import os, sys

sys.path.append(os.path.dirname(__file__))

del os, sys

import appearance, menu, edit_buffer, statusbar

MODULES = list(filter(lambda m: not m.startswith("__"), globals().keys()))
