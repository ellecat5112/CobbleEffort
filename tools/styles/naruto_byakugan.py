"""Naruto collection, 'Byakugan': pale lavender robes and pupil-less glowing eyes with bulging veins."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("byakugan")
