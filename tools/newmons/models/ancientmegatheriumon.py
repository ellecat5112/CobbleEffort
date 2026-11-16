"""Ancient Megatheriumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of ice, a colossal shaggy beast. A great mound of long white-blue
fur hanging to the ground in locks bound with red rings, a pale face with a blue gem on its brow, two huge curled
brown horns, gold bands on its stout legs and brown claws. 35 blocks tall.

Front is -z, y is up. 54 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import fur, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 54
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a colossal shaggy beast: a mound of long white-blue fur in locks bound with red rings, a pale face with a "
        "blue brow gem, two huge curled brown horns, gold leg bands and brown claws")
BASE = {"fur": (226, 236, 250), "fur_dark": (120, 150, 200), "fur_tip": (250, 252, 255), "horn": (170, 110, 50),
        "horn_dark": (100, 60, 24), "horn_light": (220, 170, 100), "ring": (200, 70, 50), "face": (226, 200, 170),
        "face_dark": (170, 140, 110), "gem": (60, 170, 240), "gem_light": (190, 240, 255), "gold": (226, 180, 60),
        "gold_dark": (150, 110, 30), "claw": (110, 70, 40), "eye": (30, 20, 20)}
SHINY = {"fur": (240, 200, 160), "fur_dark": (190, 120, 70), "fur_tip": (255, 236, 210), "gem": (240, 70, 90),
         "gem_light": (255, 180, 190)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_tip", length=2.2)
LOCK = strands(P, "fur", "fur_dark", tip="fur_tip")
HORN = metal(P, "horn", dark="horn_dark", light="horn_light", streak=2.4)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("ancientmegatheriumon")
    top = m.bone("ancientmegatheriumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    for i in range(6):                                           # the hump of the fur mound
        z0 = -14 + i * 5.0
        r = 14.0 - abs(i - 2.2) * 1.8
        slab_z(m, bd, 0, 26.0 + (2.0 - abs(i - 2) * 0.8), z0, z0 + 5.4, r, r * 0.9, FUR)
    sk = m.bone("skirt", bd, (0, 26, 0))
    for i in range(30):                                          # long locks hanging to the ground, ringed in red
        ang = math.radians(i * 12)
        top_p = (12.0 * math.sin(ang), 34.0 - 4.0 * abs(math.cos(ang)), 14.0 * math.cos(ang) * 0.95)
        bot = (15.0 * math.sin(ang), 4.0 + (i % 3), 17.0 * math.cos(ang))
        rod(m, sk, top_p, bot, 3, LOCK, extend=0.4, t2=2)
        mid = tuple(t + (b - t) * 0.35 for t, b in zip(top_p, bot))
        if i % 2 == 0:
            rod(m, sk, mid, tuple(t + (b - t) * 0.42 for t, b in zip(top_p, bot)), 4, solid(P, "ring"), extend=0.1)
    hd = m.bone("head", bd, (0, 28, -16))
    m.round_box(hd, 0, -18.0, 4.0, 3.4, 20.0, 30.0, skin(P, "face", dark="face_dark"), cut=1)     # long face
    m.box(hd, -3.0, 18.0, -22.0, 3.0, 22.0, -18.0, skin(P, "face", dark="face_dark"))            # muzzle
    ball(m, hd, (0, 31.0, -19.0), 6.0, FUR, layers=4)                                           # fur crown
    m.round_box(hd, 0, -21.6, 1.4, 0.6, 27.0, 29.6, gem(P, "gem", "gem_light"), cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 2.2 - 0.6, 25.0, -21.6, sx * 2.2 + 0.6, 26.0, -21.2, solid(P, "eye"))
        pts = [(sx * 4.0, 28.0, -16.0), (sx * 10.0, 32.0, -17.0), (sx * 16.0, 29.0, -20.0), (sx * 18.0, 22.0, -24.0),
               (sx * 15.0, 17.0, -27.0), (sx * 11.0, 18.0, -26.0)]       # the curled horns
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 4 - j * 0.5, HORN, extend=0.5)
    for front, zz in ((True, -9.0), (False, 9.0)):
        for sx in (1, -1):
            nm = f"leg_{'front' if front else 'back'}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 8.0, 14.0, zz))
            m.round_box(lg, sx * 8.0, zz, 3.4, 3.4, 0.0, 14.0, skin(P, "face", dark="face_dark"), cut=1)
            m.round_box(lg, sx * 8.0, zz, 3.8, 3.8, 6.0, 9.0, GOLD, cut=1)
            for t in range(3):
                spike(m, lg, (sx * 8.0 + (t - 1) * 1.8, 0.8, zz - 3.4), (0, -0.3, -1), 1.2, 2.6, solid(P, "claw"))
    return m
