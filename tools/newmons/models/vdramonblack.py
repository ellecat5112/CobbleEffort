"""V-dramon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the card
art on wikimon.net): a darker, fiercer V-dramon: charcoal-black hide, a pale V-marked belly and muzzle, a big nose
horn and swept horns, thick arms with long white claws and a short heavy tail. 15 blocks.

Front is -z, y is up. Adult stage. Built by _vdramon.make, recoloured.
"""
from __future__ import annotations

from _digi import sized
from _vdramon import make

HEIGHT = 52
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stocky charcoal-black dragon with a big nose horn and swept horns, a pale V-marked belly and long white claws"
build = make("vdramonblack", colours={"hide": (54, 56, 70), "hide_dark": (20, 20, 28)},
             shiny_colours={"hide": (110, 60, 150), "hide_dark": (60, 24, 90)})
