"""80s Neon Cyberpunk collection, look 'vaporwave' (see _neon.py)."""
from ._neon import NEON, make

EMISSIVE = "retexture"
WANTS_HINTS = True
WANTS_HEIGHTS = True   # sunsets, horizons and checker floors run from head to toe
EXTRA_LAYERS = [NEON]
retexture, extra_layer = make("vaporwave")
