"""Naruto collection, 'Leaf Shinobi': a navy-toned uniform, olive flak vest with scroll pockets and a Leaf forehead protector."""
from ._shinobi import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso/ear face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("leaf_shinobi")
