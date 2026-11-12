"""Slayer collection, look 'water' (see _slayer.py)."""
from ._slayer import BREATH, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [BREATH]
retexture, extra_layer = make("water")
