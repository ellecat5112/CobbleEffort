"""Cendrillmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the glass princess. A very tall slender figure in a crystal visor mask, a blue star-sprinkled
suit under a white fur stole, a long sweeping translucent white gown open in front, glass-crystal legs tapering to
points, and a long golden ribbon of hair swirling behind. Its official design is kept as drawn. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fur, gem, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a very tall slender glass princess with a crystal visor mask, a blue starry suit under a white fur stole, a "
        "sweeping translucent white gown, crystal legs and a long golden hair ribbon")
BASE = {"suit": (110, 180, 230), "suit_dark": (50, 110, 180), "star": (250, 240, 170), "fur": (246, 246, 252),
        "fur_dark": (190, 194, 210), "gown": (236, 240, 255, 170), "gown_edge": (200, 214, 250, 200),
        "glass": (190, 220, 250), "glass_light": (250, 252, 255), "gold": (240, 210, 100), "gold_dark": (190, 150, 40),
        "black": (30, 30, 40), "skin": (240, 226, 230), "visor": (200, 230, 255)}
SHINY = {"suit": (230, 140, 190), "suit_dark": (170, 70, 130), "gold": (220, 230, 250), "gold_dark": (150, 160, 190),
         "glass": (250, 200, 230)}


def P(v):
    return pal(BASE, SHINY, v)


GLASS = gem(P, "glass", "glass_light", glow=False)
FUR = fur(P, "fur", "fur_dark", length=1.2)


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (x * 1.7 + y * 1.3 + z) % 5.0 < 0.35:
        return tone(p["star"], face), None
    return armour(P, "suit", "suit_dark")(x, y, z, face, variant, box=box, **k)


def gownf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["gown_edge"] if v < 1.0 or (u * 0.8) % 3.0 < 0.2 else p["gown"]
    return c, None


def build():
    m = Model("cendrillmon")
    mats = {"skin": suitf, "neck": skin(P, "skin"), "hand": solid(P, "black"), "finger": solid(P, "black"),
            "pelvis": suitf, "thigh": GLASS, "knee": GLASS, "shin": GLASS, "calf": GLASS, "foot": GLASS, "toe": GLASS}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.8, name="cendrillmon")
    bd = a["body"]
    for nm in ("leg_left", "leg_right"):                                    # crystal legs tapering to points
        lg = a[nm]
        an = lg["ankle"]
        spike(m, lg["bone"], (an[0], 2.0, an[2]), (0, -1, 0), 2.4, 2.2, GLASS, tip=0.6)
    m.box(bd, -3.4, 33.4, -3.6, 3.4, 35.0, 3.4, solid(P, "black"))         # belt
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.4, 60.4, skin(P, "skin"), cut=1)
    m.box(hd, -2.6, 56.6, -3.0, 2.6, 59.0, -2.4, gem(P, "visor", "glass_light"))     # crystal visor mask
    spike(m, hd, (0, 60.0, -0.4), (0, 1, 0.3), 3.2, 4.0, GLASS, tip=0.6)
    for i in range(14):                                                     # white fur stole
        ang = math.radians(-100 + i * 15.4)
        c = (5.6 * math.sin(ang), 50.0, 0.4 - 4.0 * math.cos(ang))
        m.round_box(bd, c[0], c[2], 2.0, 2.0, 47.0, 52.4, FUR, cut=1)
    cb = m.bone("cap", bd, (0, 48, 3))                                      # sweeping translucent gown
    cape(m, cb, 48.0, 26.0, 46.0, gownf, z=3.6, flare=1.6, panels=10, sweep=(0, 8), seed=6)
    for sx in (-1, 1):
        m.box(bd, min(sx * 4.0, sx * 9.0), 4.0, -1.0, max(sx * 4.0, sx * 9.0), 34.0, -1.0, gownf,
              rotation=(10, sx * 30, -sx * 8), pivot=(sx * 4.0, 34.0, -1.0))
    hb = m.bone("hair", hd, (0, 59, 2))                                     # the long golden hair ribbon
    pts = [(0, 59.0, 2.0)] + [(-6.0 - 4.0 * math.sin(t), 58.0 - t * 6.0, 6.0 + 4.0 * math.cos(t))
                              for t in (0.4, 1.2, 2.0, 2.8, 3.6, 4.4)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hb, p0, p1, 2, strands(P, "gold", "gold_dark"), extend=0.4, t2=1)
    return m
