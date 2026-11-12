"""Tarot collection, 0, The Fool: sunny motley with harlequin diamonds and a white rose."""
from ._tarot import EYESHINE, FOIL, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # the symbol goes on the chest, the numeral on the forehead
EXTRA_LAYERS = [EYESHINE, FOIL]
retexture, extra_layer = make("fool")
