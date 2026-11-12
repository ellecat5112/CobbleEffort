"""Sunburst collection, look 'tropical' (see _sunburst.py)."""
from ._sunburst import SUNLIGHT, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SUNLIGHT]
retexture, extra_layer = make("tropical")
