"""Tarot collection, IX, The Hermit: grey-indigo cloak in falling snow, a lantern holding a six-pointed star."""
from ._tarot import EYESHINE, FOIL, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # the symbol goes on the chest, the numeral on the forehead
EXTRA_LAYERS = [EYESHINE, FOIL]
retexture, extra_layer = make("hermit")
