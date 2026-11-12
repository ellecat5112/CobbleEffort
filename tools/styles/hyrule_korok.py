"""Zelda collection, look 'korok' (see _hyrule.py)."""
from ._hyrule import SHEIKAH, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SHEIKAH]
retexture, extra_layer = make("korok")
