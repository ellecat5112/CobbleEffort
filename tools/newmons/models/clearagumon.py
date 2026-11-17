"""Clear Agumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an Agumon built from toy bricks. Glossy translucent studded bricks stacked into Agumon's shape: a
red and yellow head with a green eye, a green body, yellow and red legs, grey studded claw-hands, a blue brick tail
and a translucent red brick flame. Child stage.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import gem, local, mix, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = ("an Agumon built from glossy studded toy bricks: a red and yellow head, a green body, yellow and red legs, grey "
        "studded claw-hands and a translucent red brick flame")
BASE = {"red": (220, 40, 40), "yellow": (250, 210, 40), "green": (50, 170, 80), "blue": (50, 110, 220),
        "grey": (190, 194, 206), "eye": (60, 200, 120), "pupil": (10, 40, 20), "white": (255, 255, 255),
        "flame": (255, 90, 40, 200)}
SHINY = {"red": (160, 70, 220), "yellow": (240, 240, 250), "green": (240, 140, 40), "blue": (240, 90, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def brick(key):
    """A glossy toy brick: bright, with a highlight streak and darker edges."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        edge = min(u, W - u, v, H - v)
        col = p[key]
        if edge < 0.3:
            col = mix(col, (0, 0, 0), 0.25)
        elif (u + v * 0.6) % 4.0 < 0.5:
            col = mix(col, (255, 255, 255), 0.45)
        return tone(col, face), None
    return s


def studs(m, bone, x0, x1, z0, z1, y, key):
    xs = [x0 + 1.0 + i * 2.0 for i in range(max(1, int((x1 - x0) / 2.0)))]
    zs = [z0 + 1.0 + i * 2.0 for i in range(max(1, int((z1 - z0) / 2.0)))]
    for x in xs:
        for z in zs:
            m.box(bone, x - 0.6, y, z - 0.6, x + 0.6, y + 0.8, z + 0.6, brick(key))


def build():
    m = Model("clearagumon")
    top = m.bone("clearagumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -3.0, 8.0, -2.0, 3.0, 14.0, 4.0, brick("green"))                       # body bricks
    m.box(bd, -2.4, 14.0, -1.6, 2.4, 16.0, 3.0, brick("green"))
    hd = m.bone("head", bd, (0, 16, 0))
    m.box(hd, -3.0, 16.0, -6.0, 3.0, 19.0, 2.0, brick("yellow"))                     # yellow jaw block
    m.box(hd, -3.0, 19.0, -5.0, 3.0, 22.0, 2.0, brick("red"))                        # red skull block
    studs(m, hd, -3.0, 3.0, -5.0, 2.0, 22.0, "red")
    studs(m, hd, -3.0, 3.0, -6.0, -4.0, 19.0, "yellow")
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.0, sx * 3.2), 19.4, -3.6, max(sx * 3.0, sx * 3.2), 21.2, -1.8,
              gem(P, "eye", "white", glow=False))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 13.0, 0))
        m.box(ab, min(sx * 3.0, sx * 6.0), 11.0, -2.0, max(sx * 3.0, sx * 6.0), 13.0, 1.0, brick("grey"))
        for j in range(3):
            x0, x1 = sorted((sx * 6.0, sx * 7.6))
            m.box(ab, x0, 10.4, -2.0 + j * 1.1, x1, 12.4, -1.2 + j * 1.1, brick("grey"))
    for sx, nm, key in ((1, "leg_left", "red"), (-1, "leg_right", "yellow")):
        lg = m.bone(nm, top, (sx * 1.8, 8.0, 0))
        x0, x1 = sorted((sx * 0.4, sx * 3.4))
        m.box(lg, x0, 2.0, -1.4, x1, 8.0, 2.0, brick(key))
        m.box(lg, x0, 0.0, -3.4, x1, 2.0, 2.0, brick("green" if key == "red" else "red"))
        studs(m, lg, x0, x1, -3.4, -1.4, 2.0, "green" if key == "red" else "red")
    tl = m.bone("tail", bd, (0, 9, 4))
    m.box(tl, -1.4, 8.0, 4.0, 1.4, 10.4, 8.0, brick("blue"))
    m.box(tl, -1.0, 7.4, 8.0, 1.0, 9.4, 11.0, brick("blue"))
    fb = m.bone("flame", bd, (-9, 6, -4))                                             # translucent brick flame
    m.box(fb, -11.0, 2.0, -5.0, -7.0, 6.0, -3.0, solid(P, "flame", glow=True))
    spike(m, fb, (-9.0, 6.0, -4.0), (0.3, 1, 0), 2.6, 3.0, solid(P, "flame", glow=True))
    return m
