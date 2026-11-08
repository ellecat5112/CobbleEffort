"""Naruto collection, 'Karma' (Boruto): a spreading black Karma seal and one glowing blue Jougan eye."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("karma")
