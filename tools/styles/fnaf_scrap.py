"""Five Nights at Freddy's collection, FNAF 6 'Scrap': rusted and patched with mismatched panels, burns, endoskeleton and wires; one eye glows."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("scrap")
