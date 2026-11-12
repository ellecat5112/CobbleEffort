"""Steampunk collection, look 'clockwork' (see _steam.py)."""
from ._steam import BOILER, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [BOILER]
retexture, extra_layer = make("clockwork")
FRAMES = 4   # the gears turn
FPS = 4
