"""Grand Locomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dark train: a colossal armoured steam locomotive in navy and gunmetal plate with gold
trim, a great glowing blue headlamp eye, a jagged spiked hull, piston-driven wheels along its sides and a huge spiked
drill-wheel at its front grinding up sparks. 35 blocks long.

Front is -z, y is up. 34 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, gem, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = ("a colossal armoured steam locomotive in navy and gunmetal with gold trim, a glowing blue headlamp eye, a spiked "
        "hull and a huge spiked drill-wheel at its front")
BASE = {"navy": (40, 50, 100), "navy_dark": (14, 20, 50), "navy_light": (100, 110, 170), "gun": (130, 134, 146),
        "gun_dark": (60, 64, 76), "gold": (230, 190, 70), "gold_dark": (150, 110, 20), "lamp": (90, 190, 255),
        "lamp_light": (220, 245, 255), "black": (24, 22, 28), "spark": (255, 190, 60), "eye": (230, 40, 40)}
SHINY = {"navy": (120, 30, 40), "navy_dark": (60, 10, 16), "navy_light": (200, 90, 100)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "navy", "navy_dark", light="navy_light", trim="gold", trim_w=0.3, rivets=True)
GUN = riveted(P, "gun", "gun_dark")
STEEL = metal(P, "gun", dark="gun_dark")


def wheelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        cz, cy = box.lo[2] + box.size[2] / 2, box.lo[1] + box.size[1] / 2
        r = math.hypot(z - cz, y - cy)
        if r < 0.8 or abs(r - box.size[1] / 2 + 0.6) < 0.5 or abs(math.atan2(y - cy, z - cz) * 3 / math.pi % 1.0 - 0.5) < 0.08:
            return tone(p["gold"], face), None
        return tone(p["black"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("grandlocomon")
    top = m.bone("grandlocomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 4.0, 8.0, 18.0, 6.0, 24.0, HULL, cut=3)                          # armoured boiler/hull
    m.round_box(bd, 0, 16.0, 7.0, 6.0, 24.0, 32.0, HULL, cut=2)                         # cab
    for j in range(5):                                                                   # jagged hull spikes
        spike(m, bd, ((j % 2 - 0.5) * 6.0, 24.0, -8.0 + j * 5.0), ((j % 2 - 0.5), 1, 0.4), 2.4, 6.0, STEEL, tip=0.9)
    hd = m.bone("head", bd, (0, 16, -14))
    m.round_box(hd, 0, -14.6, 5.0, 1.0, 12.0, 22.0, gem(P, "lamp", "lamp_light"), cut=1)   # glowing headlamp eye
    m.round_box(hd, 0, -13.6, 6.0, 1.4, 10.0, 24.0, metal(P, "gold", dark="gold_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 6.0, sx * 7.4), 22.0, -14.0, max(sx * 6.0, sx * 7.4), 23.0, -12.0, solid(P, "eye", glow=True))
        rod(m, hd, (sx * 3.0, 24.0, -13.0), (sx * 9.0, 25.0, -16.0), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
    m.box(bd, -6.0, 0.0, -24.0, 6.0, 12.0, -22.0, wheelf, rotation=(0, 90, 0), pivot=(0, 6.0, -23.0))   # drill-wheel
    m.round_box(bd, 0, -23.0, 6.0, 2.0, 0.0, 12.0, GUN, cut=2)
    for j in range(8):
        ang = 2 * math.pi * j / 8
        spike(m, bd, (6.4 * math.cos(ang), 6.0 + 6.4 * math.sin(ang), -23.0), (math.cos(ang), math.sin(ang), -0.2), 1.6,
              4.0, STEEL, tip=0.8)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        lg = m.bone(nm, bd, (sx * 8.0, 4.0, -8.0 if "front" in nm else 10.0))
        for j in range(2):
            z0 = (-12.0 if "front" in nm else 6.0) + j * 7.0
            x0, x1 = sorted((sx * 8.0, sx * 9.4))
            m.box(lg, x0, 0.0, z0, x1, 7.0, z0 + 6.0, wheelf)
        rod(m, lg, (sx * 9.6, 3.6, (-12.0 if "front" in nm else 6.0) + 3.0),
            (sx * 9.6, 3.6, (-12.0 if "front" in nm else 6.0) + 10.0), 1, metal(P, "gold", dark="gold_dark"), extend=0)
    return m
