"""Flare Lizamon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the blazing
lizard, Dark Lizamon's body in fire, a hunched lizard wrapped in shaggy orange-gold flame-fur rising off it in licking
tufts, its head covered by a cracked steel skull mask with burning eyes, smoke puffing from its jaws, and long curved
ivory claws. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from _variant import clone

_L = clone("darklizamon", "flarelizamon",
           base={"fur": (240, 150, 30), "fur_dark": (170, 70, 10), "fur_light": (255, 220, 90),
                 "mask": (190, 194, 206), "mask_dark": (100, 104, 116), "eye": (250, 230, 60)},
           shiny={"fur": (90, 200, 250), "fur_dark": (30, 110, 200), "fur_light": (210, 245, 255)})

HEIGHT, SCALE, HITBOX, KIND, K, ANIM = _L.HEIGHT, _L.SCALE, _L.HITBOX, _L.KIND, _L.K, _L.ANIM
LOOK = ("a hunched lizard wrapped in shaggy orange-gold flame-fur, a cracked steel skull mask with burning eyes, smoke "
        "at its jaws and long curved ivory claws")
build = _L.build
