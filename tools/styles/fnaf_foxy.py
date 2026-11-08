"""Five Nights at Freddy's collection, Classic Foxy (Sandile line): rust-red fox suit, torn open to the endoskeleton, eye patch over one eye, sharp teeth and a glowing amber eye. Shiny: Mangle (white and pink)."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("foxy")
