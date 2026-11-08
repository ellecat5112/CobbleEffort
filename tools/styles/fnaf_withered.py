"""Five Nights at Freddy's collection, FNAF 2 'Withered': faded and filthy, torn open in places to the metal endoskeleton and wires; one eye has gone dark."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("withered")
