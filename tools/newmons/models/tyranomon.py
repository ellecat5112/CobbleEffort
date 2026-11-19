"""Tyranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a red tyrannosaur with dark red stripes, a ribbed white belly, green leaf-like dorsal spikes, a fanged
red mouth and steel claws. 15 blocks.

Front is -z, y is up. Adult stage. Built by _darktyranomon.make, recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_T = clone("_darktyranomon", "tyranomon",
           base={"grey": (210, 50, 40), "grey_dark": (130, 20, 14), "grey_light": (250, 120, 100), "red": (120, 14, 14),
                 "belly": (246, 246, 250), "belly_dark": (190, 190, 204)},
           shiny={"grey": (60, 130, 200), "grey_dark": (20, 70, 130), "grey_light": (140, 200, 250), "red": (20, 50, 100)})
HEIGHT = 46
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a red tyrannosaur with dark red stripes, a ribbed white belly, green dorsal spikes and steel claws"
build = _T.make("tyranomon", x=False)
