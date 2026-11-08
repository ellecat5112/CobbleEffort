"""Five Nights at Freddy's collection, FNAF 4 'Nightmare': near-black, with jagged tears lined with teeth, a mouth of sharp teeth and red pinprick eyes."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("nightmare")
