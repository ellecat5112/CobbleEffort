"""Abyss collection, look 'sigil' (see _void.py)."""
from ._void import GAZE, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [GAZE]
retexture, extra_layer = make("sigil")
