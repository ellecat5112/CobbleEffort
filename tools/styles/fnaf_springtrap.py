"""Five Nights at Freddy's collection, FNAF 3 'Springtrap': a rotten olive-yellow suit, stained, with endoskeleton and wires showing."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("springtrap")
