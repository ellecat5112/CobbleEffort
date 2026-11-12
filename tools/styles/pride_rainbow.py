"""LGBTQIA+ Pride collection, look 'rainbow' (see _pride.py)."""
from ._pride import SPARKLE, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SPARKLE]
retexture, extra_layer = make("rainbow")
