"""Dobermon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Dobermon awakened by the X-Antibody, heavier and snarling, with a huge ring of steel spikes round its
neck, glowing crimson slashes, steel-banded legs and a great curved silver blade sweeping up from its back. 15 blocks
tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from _digi import sized
from _dobermon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a heavier snarling black demon hound with a huge ring of steel neck spikes, glowing crimson slashes and a great "
        "curved silver back blade")
build = make("dobermonxantibody", x=True)
