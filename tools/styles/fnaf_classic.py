"""Five Nights at Freddy's collection, FNAF 1 'Classic': a worn felt costume with stitched seams, rivets, a little grime, square animatronic teeth and white pinprick pupils that glow in the dark."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("classic")
