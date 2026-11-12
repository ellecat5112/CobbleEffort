"""Cosmic Starlight collection, look 'nebula' (see _cosmic.py)."""
from ._cosmic import STARLIGHT, make

EMISSIVE = "retexture"
WANTS_HINTS = True     # the chest's centre (galaxy core, accretion ring)
WANTS_HEIGHTS = True   # bands from head to toe (planet bands, aurora)
EXTRA_LAYERS = [STARLIGHT]
retexture, extra_layer = make("nebula")
