"""Pokemon Unite collection, look 'beach' (see _unite.py)."""
from ._unite import HOLO, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [HOLO]
retexture, extra_layer = make("beach")
