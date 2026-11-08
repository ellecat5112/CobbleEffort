"""Five Nights at Freddy's collection, FNAF 2 'Toy': glossy plastic, brighter colours, rosy cheeks and shiny blue eyes."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("toy")
