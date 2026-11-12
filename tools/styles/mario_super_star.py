"""Super Mario collection, look 'super_star' (see _mario.py)."""
from ._mario import POWER, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [POWER]
retexture, extra_layer = make("super_star")
