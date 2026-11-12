"""Kitsune collection, look 'kitsunebi' (see _kitsune.py)."""
from ._kitsune import FOXFIRE, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [FOXFIRE]
retexture, extra_layer = make("kitsunebi")
