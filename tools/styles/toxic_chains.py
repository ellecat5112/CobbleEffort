"""Toxic Chain collection, look 'chains' (see _toxic.py)."""
from ._toxic import TOXIN, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [TOXIN]
retexture, extra_layer = make("chains")
