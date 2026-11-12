"""Gilded collection, look 'filigree' (see _gilded.py)."""
from ._gilded import GLINT, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [GLINT]
retexture, extra_layer = make("filigree")
