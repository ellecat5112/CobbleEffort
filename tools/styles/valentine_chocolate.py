"""Valentine's Day collection, look 'chocolate' (see _valentine.py)."""
from ._valentine import LOVE, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [LOVE]
retexture, extra_layer = make("chocolate")
