"""Siriusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the light dragon knight of the dog star: a sleek dragon-knight in silver-white armour edged with
pink and cyan light-lines, a horned helm with a green gem, great navy-and-white swept wings like a cloak, a pink
energy sabre trailing light, a tall gun-pylon on its back, and clawed silver feet. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a sleek silver-white dragon-knight edged with pink and cyan light, a green-gemmed horned helm, swept navy wings and a pink energy sabre"
BASE = {"silver": (226, 230, 240), "silver_dark": (130, 136, 160), "pink": (250, 90, 200), "cyan": (90, 230, 250),
        "navy": (40, 50, 110), "navy_dark": (14, 18, 50), "white": (246, 248, 252), "green": (90, 240, 140),
        "blade": (255, 120, 220, 210)}
SHINY = {"silver": (60, 60, 74), "silver_dark": (24, 24, 30), "pink": (250, 200, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs((y + abs(x) * 0.5) % 6.0 - 3.0) < 0.15:
        c = p["pink"] if int(y / 6.0) % 2 else p["cyan"]
        return c, c
    return armour(P, "silver", "silver_dark")(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["white"] if face == "north" else p["navy"], face), None


def build():
    m = Model("siriusmon")
    mats = {"skin": platef, "talon": metal(P, "silver"), "claw": metal(P, "silver")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=0.95, talons=True, claws=True, digitigrade=True,
                 name="siriusmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, platef, cut=1)
    m.box(hd, -0.8, 58.6, -4.5, 0.8, 60.0, -4.2, gem(P, "green", "white"))
    m.box(hd, -1.8, 57.0, -4.5, 1.8, 57.8, -4.3, solid(P, "cyan", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 60.0, -1.0), (sx * 0.6, 1, 0.6), 1.4, 8.0, platef, tip=0.8)
        for j in range(5):                                                               # swept navy wings
            ang = math.radians(-10 + j * 20)
            x0, x1 = sorted((sx * 3.0, sx * (28.0 - j * 3.0)))
            m.box(bd, x0, 46.0 - j, 4.0 + j * 0.3, x1, 52.0 - j, 4.0 + j * 0.3, wingf,
                  rotation=(10, -sx * 15, sx * math.degrees(ang) * -1), pivot=(sx * 3.0, 50.0, 4.0))
    rod(m, bd, (4.0, 44.0, 5.0), (8.0, 70.0, 6.0), 2, armour(P, "navy", "navy_dark"), extend=0.4)   # gun-pylon
    m.box(bd, 6.4, 64.0, 4.0, 9.6, 72.0, 8.0, solid(P, "pink", glow=True))
    w = a["arm_right"]["wrist"]                                                          # pink energy sabre
    m.box(a["arm_right"]["bone"], w[0] - 0.6, w[1] - 32.0, w[2] - 2.2, w[0] + 0.6, w[1] - 2.0, w[2] - 0.6,
          solid(P, "blade", glow=True), rotation=(-25, 0, 0), pivot=(w[0], w[1], w[2]))
    return m
