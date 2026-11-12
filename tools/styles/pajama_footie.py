"""Pajama collection, look 'footie' (see _pajama.py)."""
from ._pajama import GLOW, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [GLOW]
retexture, extra_layer = make("footie")
