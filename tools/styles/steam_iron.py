"""Steampunk collection, look 'iron' (see _steam.py)."""
from ._steam import BOILER, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [BOILER]
retexture, extra_layer = make("iron")
