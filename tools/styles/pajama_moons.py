"""Pajama collection, look 'moons' (see _pajama.py)."""
from ._pajama import GLOW, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [GLOW]
retexture, extra_layer = make("moons")
