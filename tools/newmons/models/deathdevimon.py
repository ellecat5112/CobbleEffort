"""Death Devimon (a Digimon of the CobbleEffort: Digital crossover; after the manga art on wikimon.net, the C'mon
Digimon story, where Deathmon takes Devimon's shape): a corrupted fallen angel. A gaunt, long-limbed devil in tight
grey-black hide stitched with red seams, a long head with slanted glowing yellow eyes, tall swept horns and a fanged
grin, enormous clawed hands with long red talons, red bands round its arms and legs and great tattered bat wings.
15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import cutout, leather, local, noise2, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a gaunt long-limbed devil in grey-black hide with red seams, slanted glowing eyes, tall swept horns, a fanged "
        "grin, huge red-taloned hands and tattered bat wings")
BASE = {"hide": (60, 60, 70), "hide_dark": (20, 20, 26), "hide_light": (130, 130, 150), "red": (200, 30, 40),
        "red_dark": (110, 10, 20), "eye": (255, 220, 60), "horn": (220, 214, 200), "tooth": (250, 248, 240),
        "mouth": (100, 10, 20), "wing": (50, 46, 60), "wing_dark": (110, 20, 40)}
SHINY = {"hide": (60, 90, 70), "hide_dark": (20, 40, 26), "hide_light": (120, 170, 130), "wing_dark": (40, 120, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "hide", dark="hide_dark", light="hide_light", var=0.06)
BAND = leather(P, "red", "red_dark")


def seamf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and abs(abs(x) - 2.0 - 0.1 * (y - 40.0)) < 0.15:
        return tone(p["red"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(y - (59.0 + (abs(x) - 1.4) * 0.5)) < 0.35 and 0.6 < abs(x) < 2.4 and x * sx > 0:
                return p["eye"], p["eye"]
        if abs(y - 56.0 - 0.08 * x * x) < 0.5 and abs(x) < 2.2:
            return tone(p["tooth"] if (x * 2.0) % 1.0 < 0.6 else p["mouth"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["wing_dark"] if v / max(H, 1e-6) < 0.3 else p["wing"], face), None


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return noise2(u * 0.7, v * 0.5, 13) < 0.8 and v / max(H, 1e-6) > 0.1 * abs(math.sin(u * 1.7))


def build():
    m = Model("deathdevimon")
    mats = {"skin": seamf, "chest": seamf, "abs": seamf, "pelvis": HIDE, "neck": HIDE, "deltoid": HIDE,
            "upper_arm": HIDE, "forearm": HIDE, "hand": HIDE, "finger": HIDE, "claw": solid(P, "red"),
            "thigh": HIDE, "knee": HIDE, "shin": HIDE, "calf": HIDE, "foot": HIDE, "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=1.0, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="deathdevimon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.6, 3.2, 54.4, 61.6, headf, cut=1)                     # long head
    for sx in (-1, 1):
        pts = [(sx * 2.0, 61.0, 0), (sx * 4.0, 65.0, 2.0), (sx * 5.0, 70.0, 5.0), (sx * 4.6, 74.0, 9.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                              # tall swept horns
            rod(m, hd, p0, p1, 2 if j < 2 else 1, solid(P, "horn"), extend=0.4)
    for nm in ("arm_left", "arm_right"):
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        m.round_box(ar["bone"], hx, hz, 2.6, 2.6, hy - 1.0, hy + 2.6, HIDE, cut=1)   # enormous hands
        for j in range(4):
            spike(m, ar["bone"], (hx + (j - 1.5) * 1.2, hy - 1.0, hz - 1.0), (0, -1, -0.4), 0.9, 6.0,
                  solid(P, "red"), tip=0.2)
        el = ar["elbow"]
        m.round_box(ar["bone"], el[0], el[2], 2.0, 2.0, el[1] - 4.0, el[1] - 2.4, BAND, cut=1)
    for nm in ("leg_left", "leg_right"):
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], kn[2], 2.4, 2.4, kn[1] - 4.0, kn[1] - 2.4, BAND, cut=1)
    for side in (1, -1):                                                              # tattered bat wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 50.0, 3.4))
        bat_wing(m, wb, (side * 2.6, 50.0, 3.4), 26.0, 24.0, 4, HIDE, cutout(tatter, wingf), side=side, sweep=25)
    return m
