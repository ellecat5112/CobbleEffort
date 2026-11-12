"""Bioluminescent Deep Sea collection, look 'jellyfish' (see _abyss.py)."""
from ._abyss import LIGHT, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [LIGHT]
retexture, extra_layer = make("jellyfish")
