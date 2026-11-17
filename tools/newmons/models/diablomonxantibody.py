"""Diablomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Diablomon awakened by the X-Antibody: slender limbs of translucent pink crystal with magenta clawed gauntlets, a head of jagged magenta blades, long flowing mint-green hair and a curved silver blade at one foot.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from _diablomon import make
from _digi import sized

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "slender translucent pink crystal limbs with magenta clawed gauntlets, a head of jagged magenta blades, flowing mint-green hair and a silver foot blade"
build = make("diablomonxantibody", x=True)
