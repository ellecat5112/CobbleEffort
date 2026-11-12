"""Tarot collection, II, The High Priestess: deep blue with pomegranates, a crescent moon between the black and white pillars."""
from ._tarot import EYESHINE, FOIL, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # the symbol goes on the chest, the numeral on the forehead
EXTRA_LAYERS = [EYESHINE, FOIL]
retexture, extra_layer = make("high_priestess")
