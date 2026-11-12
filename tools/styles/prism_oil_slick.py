"""Prismatic collection, look 'oil_slick' (see _prism.py)."""
from ._prism import SPECTRUM, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SPECTRUM]
retexture, extra_layer = make("oil_slick")
