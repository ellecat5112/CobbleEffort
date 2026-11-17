"""Death Airdramon (a Digimon of the CobbleEffort: Digital crossover; after the manga art on wikimon.net, the C'mon
Digimon story, where Deathmon disguises itself as Airdramon): a corrupted winged serpent. Airdramon's body turned
deathly: an ash-grey scaled serpent with a bone-white skull head masked in black and a burning green eye, a ragged
mane of sickly green and violet feathers, tattered black wings veined with violet and a ghost-green flame at its tail,
plus a crown of extra bone horns. 15 blocks tall.

Front is -z, y is up. 48 units tall (the wings); Adult stage.
"""
from __future__ import annotations

from _boxmodel import spike
from _digidetail import solid
from _variant import clone

_A = clone("airdramon", "deathairdramon",
           base={"blue": (80, 80, 92), "blue_dark": (34, 32, 40), "blue_light": (150, 150, 166),
                 "belly": (170, 168, 176), "eye": (90, 250, 120), "red": (110, 40, 150), "orange": (90, 200, 90),
                 "yellow": (190, 250, 140), "wing": (60, 50, 70), "wing_dark": (110, 40, 150),
                 "wing_edge": (16, 14, 18), "flame": (90, 250, 160, 220), "mouth": (110, 20, 60)},
           shiny={"blue": (150, 40, 40), "blue_dark": (80, 14, 14), "blue_light": (220, 110, 100),
                  "wing": (40, 40, 40), "wing_dark": (180, 40, 30)})

HEIGHT, SCALE, HITBOX, KIND, K = _A.HEIGHT, _A.SCALE, _A.HITBOX, _A.KIND, _A.K
LOOK = ("a corrupted winged serpent: an ash-grey scaled body, a black-masked skull head with a burning green eye, a "
        "ragged green-and-violet feather mane, tattered black wings veined violet and extra bone horns")


def build():
    m = _A.build()
    head = next(b for b in m.boxes if b.bone == "head")
    cx = (head.lo[0] + head.lo[0] + head.size[0]) / 2
    top = max(b.lo[1] + b.size[1] for b in m.boxes if b.bone == "head")
    zc = sum(b.lo[2] + b.size[2] / 2 for b in m.boxes if b.bone == "head") / sum(1 for b in m.boxes if b.bone == "head")
    for i in range(5):                                                          # crown of bone horns
        sx = (i - 2) * 0.5
        spike(m, "head", (cx + sx * 2.0, top - 0.6, zc + 1.0), (sx, 1.0, 0.8), 1.2, 4.0 + (2 - abs(i - 2)) * 1.5,
              solid(_A.P, "skull"), tip=0.25)
    return m
