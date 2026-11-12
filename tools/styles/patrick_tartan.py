"""St. Patrick's Day collection, look 'tartan' (see _patrick.py)."""
from ._patrick import LUCK, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [LUCK]
retexture, extra_layer = make("tartan")
