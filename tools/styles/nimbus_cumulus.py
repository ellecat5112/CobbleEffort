"""Nimbus collection, look 'cumulus' (see _nimbus.py)."""
from ._nimbus import SKY, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True
EXTRA_LAYERS = [SKY]
retexture, extra_layer = make("cumulus")
