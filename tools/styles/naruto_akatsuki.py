"""Naruto collection, 'Akatsuki': a black cloak with red, white-edged clouds and Sharingan eyes that glow."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("akatsuki")
