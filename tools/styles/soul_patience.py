"""Undertale collection, look 'patience' (see _undertale.py)."""
from ._undertale import SOUL, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SOUL]
retexture, extra_layer = make("patience")
