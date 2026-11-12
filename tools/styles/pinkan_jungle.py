"""Pinkan Island collection, look 'jungle' (see _pinkan.py)."""
from ._pinkan import GLEAM, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [GLEAM]
retexture, extra_layer = make("jungle")
