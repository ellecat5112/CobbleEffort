"""Undertale collection, look 'integrity' (see _undertale.py)."""
from ._undertale import SOUL, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SOUL]
retexture, extra_layer = make("integrity")
