"""Toxic Chain collection, look 'sludge' (see _toxic.py)."""
from ._toxic import TOXIN, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [TOXIN]
retexture, extra_layer = make("sludge")
