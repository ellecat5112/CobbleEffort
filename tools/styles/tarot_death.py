"""Tarot collection, XIII, Death: black with pale ribs, the white rose on a black banner."""
from ._tarot import EYESHINE, FOIL, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # the symbol goes on the chest, the numeral on the forehead
EXTRA_LAYERS = [EYESHINE, FOIL]
retexture, extra_layer = make("death")
