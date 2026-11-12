"""April Fools' Day collection, look 'clown' (see _fools.py)."""
from ._fools import PRANK, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [PRANK]
retexture, extra_layer = make("clown")
