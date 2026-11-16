"""Ancient Volcamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of earth, a hulking gorilla of cratered brown rock with an erupting
volcano for a back. A small horned black head sunk between massive shoulders, huge arms bound in black straps and
iron cuffs, lava bursting from the crater with a plume of ash, and short legs with orange claws. 35 blocks tall.

Front is -z, y is up. 62 units tall (the ash plume); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, flame_inside, leather, local, metal, mix, plane, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking gorilla of cratered brown rock with an erupting volcano back, a small horned black head, huge arms "
        "bound in black straps and iron cuffs, and orange claws")
BASE = {"rock": (150, 80, 40), "rock_dark": (80, 40, 20), "rock_light": (200, 130, 80), "crater": (60, 30, 16),
        "black": (34, 32, 36), "black_light": (90, 88, 96), "iron": (110, 112, 120), "iron_dark": (50, 52, 58),
        "lava": (255, 120, 30, 230), "lava_core": (255, 220, 90, 240), "ash": (170, 170, 176, 200),
        "claw": (240, 110, 40), "horn": (230, 210, 170), "eye": (255, 220, 60)}
SHINY = {"rock": (70, 70, 84), "rock_dark": (30, 30, 40), "rock_light": (120, 120, 140), "lava": (80, 160, 255, 230),
         "lava_core": (190, 235, 255, 240)}


def P(v):
    return pal(BASE, SHINY, v)


STRAP = leather(P, "black", "black_light")
IRON = metal(P, "iron", dark="iron_dark")


def rockf(x, y, z, face, variant, box=None, **k):
    """Cratered rock: round pits with a lit rim, on a mottled brown hide."""
    p = P(variant)
    a, b = plane(x, y, z, face)
    cu, cv = round(a / 3.4) * 3.4 + 0.8 * math.sin(round(b / 3.4) * 1.7), round(b / 3.4) * 3.4
    d = math.hypot(a - cu, b - cv)
    if (round(a / 3.4) + 2 * round(b / 3.4)) % 3 == 0:
        if d < 0.9:
            return tone(p["crater"], face), None
        if d < 1.2:
            return tone(p["rock_light"], face), None
    t = 0.5 + 0.5 * math.sin(a * 0.9 + b * 1.3) * math.sin(b * 0.6)
    return tone(mix(p["rock_dark"], p["rock"], 0.5 + 0.5 * t), face), None


def lavaf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["lava_core"] if v / max(H, 1e-6) < 0.4 else p["lava"]
    return c, c[:3]


def build():
    m = Model("ancientvolcamon")
    top = m.bone("ancientvolcamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 30.0, 2.0), 13.0, rockf, layers=8, squash=0.9)                     # the massive rock torso
    for i in range(5):                                            # the volcano cone rising from its back
        r = 8.0 - i * 1.2
        m.round_box(bd, 3.0 + i * 0.8, 6.0 + i * 0.6, r, r, 36.0 + i * 3.0, 39.4 + i * 3.0, rockf, cut=2)
    vc = (7.0, 51.0, 9.0)
    sh = cutout(flame_inside(4, 0.2, 4), lavaf)
    for ang in (0, 60, 120):                                      # the eruption
        m.box(bd, vc[0] - 5.0, vc[1], vc[2], vc[0] + 5.0, vc[1] + 10.0, vc[2], sh, rotation=(0, ang, -15), pivot=vc)
    ball(m, bd, (vc[0] + 2.0, vc[1] + 10.0, vc[2] + 2.0), 5.0, solid(P, "ash"), layers=4)    # ash plume
    ball(m, bd, (vc[0] - 2.0, vc[1] + 8.0, vc[2] + 4.0), 3.6, solid(P, "ash"), layers=3)
    hd = m.bone("head", bd, (0, 32, -10))
    m.round_box(hd, 0, -12.0, 3.2, 3.0, 28.0, 34.5, solid(P, "black"), cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.6, 31.0, -15.2, sx * 1.4 + 0.6, 31.8, -14.8, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.8, 33.0, -12.0), (sx * 0.8, 0.6, -0.4), 1.4, 4.0, solid(P, "horn"), tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):           # giant arms
        ab = m.bone(nm, bd, (sx * 12.0, 38.0, 0))
        el = (sx * 18.0, 26.0, -3.0)
        fist = (sx * 18.0, 10.0, -6.0)
        ball(m, ab, (sx * 14.0, 38.0, 0.0), 6.4, rockf, layers=4)
        rod(m, ab, (sx * 14.0, 36.0, 0.0), el, 8, rockf, extend=1.0)
        rod(m, ab, el, fist, 9, rockf, extend=1.0)
        m.round_box(ab, fist[0], fist[2], 5.4, 5.0, fist[1] - 6.0, fist[1] + 1.0, rockf, cut=2)
        m.round_box(ab, fist[0], fist[2], 5.8, 5.4, fist[1] + 2.0, fist[1] + 6.0, IRON, cut=2)       # iron cuff
        for j in range(3):                                         # black straps round the arm
            p = tuple(e + (f - e) * (0.2 + j * 0.25) for e, f in zip(el, fist))
            rod(m, ab, p, (p[0], p[1] - 1.2, p[2]), 10, STRAP, extend=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):           # short legs with orange claws
        lg = m.bone(nm, top, (sx * 6.0, 18.0, 2.0))
        m.round_box(lg, sx * 6.5, 1.0, 5.0, 5.0, 4.0, 19.0, rockf, cut=2)
        m.round_box(lg, sx * 6.5, 1.0, 5.4, 5.4, 10.0, 13.0, STRAP, cut=2)
        m.box(lg, sx * 6.5 - 5.0, 0.0, -5.0, sx * 6.5 + 5.0, 4.0, 5.0, rockf)
        for t in range(3):
            spike(m, lg, (sx * 6.5 + (t - 1) * 3.0, 1.6, -5.0), (0, -0.2, -1), 2.2, 4.0, solid(P, "claw"), tip=1.0)
    return m
