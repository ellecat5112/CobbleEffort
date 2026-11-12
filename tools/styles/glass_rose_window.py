"""Stained Glass collection, look 'rose_window' (see _glass.py)."""
from ._glass import BACKLIGHT, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [BACKLIGHT]
retexture, extra_layer = make("rose_window")
