"""Arcturusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a dragon-man of the stars. Navy-black armour edged in gold, a spiked helm with magenta spines,
a glowing magenta core in its chest, two huge black bat-wings with crimson membranes, and long gold-and-magenta drill
lances on both forearms. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a star dragon-man in navy-black armour edged in gold: a spiked helm with magenta spines, a glowing magenta "
        "chest core, huge black bat-wings with crimson membranes and gold drill lances on its forearms")
BASE = {"navy": (40, 40, 80), "navy_dark": (14, 14, 34), "navy_light": (100, 100, 160), "gold": (226, 180, 60),
        "gold_dark": (150, 104, 26), "gold_light": (255, 236, 160), "magenta": (240, 60, 180), "magenta_light": (255, 170, 230),
        "black": (24, 24, 30), "black_light": (80, 80, 96), "membrane": (150, 20, 40, 230), "eye": (255, 60, 170)}
SHINY = {"navy": (220, 220, 230), "navy_dark": (150, 150, 166), "navy_light": (255, 255, 255),
         "magenta": (60, 200, 255), "magenta_light": (180, 240, 255), "membrane": (40, 90, 170, 230)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark", light="navy_light", trim="gold")
NAVY_PLAIN = armour(P, "navy", "navy_dark", light="navy_light")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
BLACK = metal(P, "black", dark="black", light="black_light", streak=2.0)


def drillf(x, y, z, face, variant, box=None, **k):
    """A drill: gold spiral bands with magenta grooves."""
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) if box else 0
    u, v, W, H = local(x, y, z, face, box)
    if abs(((t * 0.8 + u * 0.5) % 2.0) - 1.0) < 0.25:
        return tone(p["magenta"], face), p["magenta"]
    return GOLD(x, y, z, face, variant, box=box, **k)


def membrane_inside(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.15 * (1 + math.sin(u * 1.2))


def membranef(x, y, z, face, variant, box=None, **k):
    return P(variant)["membrane"], None


def build():
    m = Model("arcturusmon")
    mats = {"skin": NAVY_PLAIN, "chest": NAVY, "abs": NAVY_PLAIN, "pelvis": NAVY, "neck": NAVY_PLAIN, "deltoid": NAVY,
            "upper_arm": NAVY_PLAIN, "forearm": NAVY, "hand": NAVY_PLAIN, "finger": GOLD, "claw": GOLD,
            "thigh": NAVY, "knee": GOLD, "shin": NAVY, "calf": NAVY_PLAIN, "foot": NAVY, "talon": GOLD}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.2, leg_bulk=1.1, digitigrade=True, claws=True, talons=True,
                 name="arcturusmon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.6, 60.6, NAVY, cut=1)
    m.box(hd, -1.8, 57.4, -3.3, 1.8, 58.2, -2.9, solid(P, "eye", glow=True))
    for i in range(7):                                           # magenta spines crowning the helm
        ang = math.radians(-60 + i * 20)
        spike(m, hd, (2.0 * math.sin(ang), 60.0, 0.6), (math.sin(ang) * 0.6, 1, 0.4), 1.2, 4.0,
              solid(P, "magenta", glow=True))
    m.box(bd, -1.6, 44.0, -5.4, 1.6, 47.4, -3.6, gem(P, "magenta", "magenta_light"))
    shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, NAVY)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.6, 50.0, 0.3), 4.4, 4.0, NAVY, layers=4)
        spike(m, ab, (sh[0] + sx * 3.0, 53.0, 0.0), (sx * 0.6, 1, 0.2), 1.6, 5.0, solid(P, "magenta", glow=True))
        el, wr = a[nm]["elbow"], a[nm]["wrist"]
        tip = (wr[0] + (wr[0] - el[0]) * 1.6, wr[1] + (wr[1] - el[1]) * 1.6, wr[2] + (wr[2] - el[2]) * 1.6)
        for j in range(4):                                        # the drill lance, tapering
            p0 = tuple(e + (t - e) * j / 4 for e, t in zip(el, tip))
            p1 = tuple(e + (t - e) * (j + 1) / 4 for e, t in zip(el, tip))
            rod(m, ab, p0, p1, 5 - j, drillf, extend=0.3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # huge bat wings
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        wrist, tips = bat_wing(m, wb, (sx * 3.0, 49.0, 3.0), 34.0, 18.0, 4, BLACK,
                               cutout(membrane_inside, membranef), side=sx)
        for t in tips:
            spike(m, wb, t, (sx, 0, 0.2), 1.0, 2.6, BLACK)
    return m
