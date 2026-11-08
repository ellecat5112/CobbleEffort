"""Five Nights at Freddy's collection, Classic Chica (Torchic line): yellow felt chicken with an orange beak and feet, the 'LET'S EAT!!!' bib, teeth and glowing violet eyes. Shiny: a brighter Toy Chica with rosy cheeks."""
from ._animatronic import EYESHINE, make

EMISSIVE = "retexture"
WANTS_HINTS = True   # wants the model's head/torso face positions
EXTRA_LAYERS = [EYESHINE]
retexture, extra_layer = make("chica")
