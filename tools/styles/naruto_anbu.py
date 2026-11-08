"""Naruto collection, 'ANBU': dark grey armour and a white porcelain mask with red markings."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("anbu")
