"""Naruto collection, 'Sage Mode': orange sage pigment round the eyes, glowing toad eyes, and a red cloak hem with black flames."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("sage_mode")
