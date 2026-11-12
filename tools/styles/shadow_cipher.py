"""Shadow collection, look 'cipher' (see _shadow.py)."""
from ._shadow import DARKAURA, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [DARKAURA]
retexture, extra_layer = make("cipher")
