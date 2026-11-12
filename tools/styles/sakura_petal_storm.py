"""Sakura collection, look 'petal_storm' (see _sakura.py)."""
from ._sakura import BLOOM, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [BLOOM]
retexture, extra_layer = make("petal_storm")
