"""Death Tyranomon (a Digimon of the CobbleEffort: Digital crossover; after the manga art on wikimon.net, the C'mon
Digimon story, where Deathmon takes a tyrannosaur's shape): a corpse-grey tyrannosaur with livid violet stripes, a
pale ribbed belly, bone-white dorsal spikes, a red fanged maw, steel claws and a leather belt. 15 blocks tall.

Front is -z, y is up. 46 units tall; Adult stage.
"""
from _digi import sized
from _variant import clone

_T = clone("_darktyranomon", "deathtyranomon",
           base={"grey": (130, 128, 140), "grey_dark": (60, 58, 70), "grey_light": (200, 198, 210), "red": (120, 50, 160),
                 "green": (230, 226, 210), "green_dark": (150, 146, 130), "eye": (240, 220, 80)},
           shiny={"grey": (90, 120, 100), "grey_dark": (40, 60, 50), "grey_light": (160, 200, 170)})

HEIGHT = 46
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a corpse-grey tyrannosaur with violet stripes, a pale ribbed belly, bone-white dorsal spikes, a red fanged "
        "maw, steel claws and a leather belt")
build = _T.make("deathtyranomon")
