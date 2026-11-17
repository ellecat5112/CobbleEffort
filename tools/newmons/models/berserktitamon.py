"""Berserk Titamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a god of the Titans driven mad, a colossus of rotting dark armour split by glowing red
cracks. Huge spiked shoulders and arms, curved horns, a ragged body plate with a red eye-emblem, crimson tatters
hanging from it, clawed feet and a great jagged red-veined greatsword. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, gem, local, metal, plane, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a mad Titan god: a colossus of rotting dark armour split by glowing red cracks, huge spiked shoulders, curved "
        "horns, crimson tatters, clawed feet and a jagged red-veined greatsword")
BASE = {"dark": (70, 50, 46), "dark_d": (30, 20, 18), "dark_l": (130, 100, 90), "crack": (240, 40, 40),
        "rag": (150, 20, 30), "rag_dark": (80, 8, 14), "eye": (255, 60, 40), "eye_l": (255, 200, 160)}
SHINY = {"dark": (60, 70, 90), "dark_d": (20, 26, 40), "dark_l": (120, 140, 170), "crack": (80, 200, 255),
         "rag": (40, 80, 150), "eye": (90, 220, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def cracked(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    n = math.sin(a * 0.9 + math.sin(b * 0.5) * 2.2) * math.sin(b * 0.7 + a * 0.3)
    if abs(n) < 0.06:
        return p["crack"], p["crack"]
    return armour(P, "dark", "dark_d", light="dark_l")(x, y, z, face, variant, box=box, **k)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.2 * abs(math.sin((box.lo[0] + box.lo[2] + u) * 2.3))


def build():
    m = Model("berserktitamon")
    mats = {"skin": cracked}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.7, leg_bulk=1.5, digitigrade=True, claws=True, talons=True,
                 name="berserktitamon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.0, 54.4, 61.0, cracked, cut=1)
    m.box(hd, -2.0, 57.4, -3.8, 2.0, 58.4, -3.4, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                           # curved horns
        pts = [(sx * 2.0, 60.0, 0.0), (sx * 3.0, 65.0, 0.6), (sx * 2.4, 70.0, 0.0), (sx * 1.6, 72.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, cracked, extend=0.3, t2=2)
    shell(m, bd, (0, 0, 0.6), 7.2, 41.0, 51.0, -85, 85, 9, 1.4, cracked)
    m.box(bd, -2.2, 44.0, -9.0, 2.2, 48.0, -7.8, gem(P, "eye", "eye_l"))               # red eye-emblem
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 2.4, 50.0, 0.3), 6.0, 5.0, cracked, layers=4)
        for j in range(4):
            spike(m, ab, (sh[0] + sx * 4.0, 52.0, -2.0 + j * 1.6), (sx * 0.7, 0.8, 0.2), 2.0, 6.0 - j * 0.6, cracked,
                  tip=0.8)
    sk = m.bone("skirt", bd, (0, 32, 0))
    for i in range(8):                                           # crimson tatters
        ang = math.radians(-150 + i * 43)
        c = (6.0 * math.sin(ang), 32.0, -5.4 * math.cos(ang))
        m.box(sk, c[0] - 2.0, 14.0, c[2], c[0] + 2.0, 32.0, c[2], cutout(torn, solid(P, "rag")),
              rotation=(0, -math.degrees(ang), 0), pivot=c)
    ar = a["arm_right"]                                          # the jagged greatsword
    h = ar["hand"]
    sw = m.bone("sword", ar["bone"], h)
    m.box(sw, h[0] - 3.0, h[1] - 1.0, h[2] - 1.0, h[0] + 3.0, h[1] + 1.0, h[2] + 1.0, cracked)
    m.box(sw, h[0] - 3.0, h[1] - 40.0, h[2] - 0.6, h[0] + 3.0, h[1] - 1.0, h[2] + 0.6, cracked)
    for j in range(6):
        sx = 1 if j % 2 else -1
        spike(m, sw, (h[0] + sx * 3.0, h[1] - 6.0 - j * 5.6, h[2]), (sx, -0.4, 0), 1.0, 2.6, cracked)
    return m
