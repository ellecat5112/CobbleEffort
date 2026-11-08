"""Naruto collection, 'Uzumaki': Naruto's orange and black, whisker marks, a red swirl and a Leaf forehead protector."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("uzumaki")
