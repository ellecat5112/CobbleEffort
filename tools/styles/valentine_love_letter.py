"""Valentine's Day collection, look 'love_letter' (see _valentine.py)."""
from ._valentine import LOVE, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [LOVE]
retexture, extra_layer = make("love_letter")
