"""Super Mario collection, look 'question_block' (see _mario.py)."""
from ._mario import POWER, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [POWER]
retexture, extra_layer = make("question_block")
