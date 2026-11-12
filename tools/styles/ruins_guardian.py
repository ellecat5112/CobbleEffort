"""Ancient Ruins collection, look 'guardian' (see _ruins.py)."""
from ._ruins import GLYPH, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [GLYPH]
retexture, extra_layer = make("guardian")
