"""Bio Darkdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a Bio Hybrid dragon-knight. Navy-blue armour with yellow lightning stripes and red
trim, a green dragon helm, white claws, a long segmented steel tail ending in a hooked axe-blade, pale glowing wings
and a long steel lance. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a Bio Hybrid dragon-knight in navy armour with yellow lightning stripes, a green dragon helm, white claws, a "
        "segmented steel tail with an axe-blade, pale glowing wings and a long steel lance")
BASE = {"navy": (30, 40, 120), "navy_dark": (12, 16, 60), "navy_light": (90, 110, 200), "yellow": (250, 210, 40),
        "red": (210, 30, 40), "green": (60, 160, 90), "green_dark": (20, 90, 40), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 128), "wing": (190, 230, 250, 140), "eye": (255, 220, 60)}
SHINY = {"navy": (120, 30, 40), "navy_dark": (60, 10, 16), "navy_light": (210, 90, 100), "green": (220, 180, 40),
         "green_dark": (150, 110, 10), "wing": (250, 200, 230, 140)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def boltf(x, y, z, face, variant, box=None, **k):
    """Navy armour crossed by yellow lightning zigzags."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    zig = abs(((v * 0.5) % 2.0) - 1.0) * W * 0.4 + W * 0.3
    if face not in ("up", "down") and abs(u - zig) < 0.45:
        return tone(p["yellow"], face), None
    return armour(P, "navy", "navy_dark", light="navy_light", trim="red", trim_w=0.3)(x, y, z, face, variant,
                                                                                     box=box, **k)


def build():
    m = Model("biodarkdramon")
    mats = {"skin": boltf, "hand": STEEL, "finger": solid(P, "steel"), "claw": solid(P, "steel"),
            "talon": solid(P, "steel"), "foot": boltf}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.15, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                 name="biodarkdramon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.6, 3.0, 54.4, 60.6, armour(P, "green", "green_dark"), cut=1)
    m.box(hd, -1.8, 55.0, -7.4, 1.8, 58.0, -2.6, armour(P, "green", "green_dark"))
    m.box(hd, -1.8, 58.0, -3.9, 1.8, 58.8, -3.6, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.0, 0.0), (sx * 0.3, 0.6, 1), 1.4, 5.0, solid(P, "red"))
    shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, boltf)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 1.6, 50.0, 0.3), 4.4, 4.0, boltf, layers=3)
    tl = m.bone("tail", bd, (0, 31, 3))
    p = (0.0, 31.0, 3.0)
    for j in range(10):                                          # segmented steel tail
        q = (j * 0.6, 28.0 - j * 2.6, 6.0 + j * 1.6)
        m.round_box(tl, (p[0] + q[0]) / 2, (p[2] + q[2]) / 2, 1.8 - j * 0.06, 1.6, q[1], p[1] + 0.4, STEEL, cut=1)
        p = q
    m.box(tl, p[0] - 0.4, p[1] - 3.0, p[2] - 2.0, p[0] + 0.4, p[1] + 1.0, p[2] + 6.0, STEEL)   # axe-blade
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # pale glowing wings
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        for j, ang in enumerate((40, 15, -10)):
            x0, x1 = sorted((sx * 3.0, sx * 24.0))
            m.box(wb, x0, 44.0, 4.0 + j, x1, 54.0, 4.0 + j,
                  lambda x, y, z, face, variant=None, box=None, **k: (P(variant)["wing"], P(variant)["wing"][:3]),
                  rotation=(0, 0, sx * ang), pivot=(sx * 3.0, 49.0, 4.0 + j))
    h = a["arm_right"]["hand"]                                   # the long lance
    rod(m, a["arm_right"]["bone"], (h[0] + 4.0, h[1] - 6.0, h[2] + 12.0), (h[0] - 8.0, h[1] + 12.0, h[2] - 30.0), 2,
        STEEL, extend=0)
    return m
