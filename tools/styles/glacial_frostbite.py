"""Glacial collection, look 'frostbite' (see _glacial.py)."""
from ._glacial import FROST, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [FROST]
retexture, extra_layer = make("frostbite")
