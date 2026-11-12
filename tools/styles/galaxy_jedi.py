"""Star Wars collection, look 'jedi' (see _galaxy.py)."""
from ._galaxy import KYBER, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [KYBER]
retexture, extra_layer = make("jedi")
