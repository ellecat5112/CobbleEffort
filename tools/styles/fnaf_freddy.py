"""Five Nights at Freddy's collection, Classic Freddy (Teddiursa line): brown felt bear with a pale muzzle, black top hat and bow tie, animatronic teeth and glowing blue eyes. Shiny: Golden Freddy."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("freddy")
