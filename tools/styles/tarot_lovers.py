"""Tarot collection, VI, The Lovers: rose pink with little hearts, a heart with an apple leaf."""
from ._tarot import EYESHINE, FOIL, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # the symbol goes on the chest, the numeral on the forehead
EXTRA_LAYERS = [EYESHINE, FOIL]
retexture, extra_layer = make("lovers")
