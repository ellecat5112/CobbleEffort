"""Arc Light collection, look 'tesla' (see _arc.py)."""
from ._arc import ARC, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [ARC]
retexture, extra_layer = make("tesla")
