"""Stained Glass collection, look 'tiffany' (see _glass.py)."""
from ._glass import BACKLIGHT, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [BACKLIGHT]
retexture, extra_layer = make("tiffany")
