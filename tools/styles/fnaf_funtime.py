"""Five Nights at Freddy's collection, FNAF 5 'Funtime': white glossy plating with pink/purple panels, faceplate seams, rosy cheeks and violet eyes."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("funtime")
