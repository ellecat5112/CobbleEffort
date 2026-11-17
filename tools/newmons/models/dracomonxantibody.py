"""Dracomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Dracomon awakened by the X-Antibody, leaner and fiercer, with a gold X on its brow, tall pink crest horns, a pink chest gem, bigger red wings and a whip tail.
Child stage, 1 block tall.

Front is -z, y is up. 32 units tall; Child stage.
"""
from _digi import sized
from _dracomon import make

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean fierce teal dragon with a gold X brow mark, tall pink crest horns, a pink chest gem, red wings and a whip tail"
build = make("dracomonxantibody", x=True)
