"""Ancient Irismon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of wind. A slender winged figure in a white bodysuit with gold
armour pieces, a gold bird-crest helm with a blue visor, a long green-and-white streamer cape, great wings of
rainbow feathers (gold, green, blue, violet) and a long gold rapier. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, fabric, local, metal, mix, skin, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender winged warrior in a white bodysuit with gold armour, a gold bird-crest helm with a blue visor, a "
        "green streamer cape, wings of rainbow feathers and a long gold rapier")
BASE = {"white": (246, 246, 250), "white_dark": (180, 184, 204), "gold": (236, 190, 60), "gold_dark": (160, 112, 26),
        "gold_light": (255, 240, 170), "green": (150, 210, 80), "green_dark": (70, 140, 40), "blue": (70, 140, 230),
        "violet": (150, 90, 210), "visor": (60, 160, 240), "f1": (250, 210, 60), "f2": (120, 210, 90),
        "f3": (70, 150, 240), "f4": (150, 90, 220)}
SHINY = {"green": (230, 120, 170), "green_dark": (160, 50, 100), "f1": (250, 140, 170), "f2": (240, 90, 120),
         "f3": (200, 70, 170), "f4": (130, 60, 190), "visor": (240, 90, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = skin(P, "white", dark="white_dark", var=0.02)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
GOLD_ARM = armour(P, "gold", "gold_dark", light="gold_light")
CAPE = fabric(P, "green", "green_dark", axis="y", period=2.6)


def rainbow(x, y, z, face, variant, box=None, **k):
    """A feather whose colour runs gold -> green -> blue -> violet from root to tip, with a pale shaft."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = 1 - v / max(H, 1e-6)
    if abs(u - W / 2) < 0.2:
        return tone(p["white"], face), None
    cols = [p["f1"], p["f2"], p["f3"], p["f4"]]
    i = min(2, int(t * 3))
    return tone(mix(cols[i], cols[i + 1], t * 3 - i), face), None


def build():
    m = Model("ancientirismon")
    mats = {"skin": SUIT, "chest": GOLD_ARM, "abs": SUIT, "pelvis": SUIT, "neck": SUIT, "deltoid": GOLD_ARM,
            "upper_arm": SUIT, "forearm": GOLD_ARM, "hand": SUIT, "finger": SUIT, "thigh": SUIT, "knee": GOLD,
            "shin": GOLD_ARM, "calf": SUIT, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.78, leg_bulk=0.85, name="ancientirismon", hand_pose="open",
                 chest_depth=0.9)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, GOLD_ARM, cut=1)
    m.box(hd, -1.8, 56.6, -2.8, 1.8, 58.2, -2.2, solid(P, "visor", glow=True))
    rod(m, hd, (0, 60.0, -2.0), (0, 63.0, -4.5), 2, GOLD, extend=0.3)               # bird crest: beak forward
    spike(m, hd, (0, 63.0, -4.5), (0, -0.4, -1), 1.4, 2.6, GOLD)
    for sx in (-1, 1):                                           # crest wings swept back off the helm
        rod(m, hd, (sx * 2.0, 60.0, 0), (sx * 5.0, 65.0, 4.0), 1, GOLD, extend=0.2, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 0.8, 49.5, 0.2), 2.8, 2.6, GOLD_ARM, layers=3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # rainbow wings
        wb = m.bone(nm, bd, (sx * 3.0, 50.0, 3.0))
        rod(m, wb, (sx * 3.0, 50.0, 3.0), (sx * 12.0, 60.0, 7.0), 2, GOLD, extend=0.3)
        for i in range(10):
            t = i / 9
            base = (sx * (3.0 + 9.0 * t), 50.0 + 10.0 * t, 3.0 + 4.0 * t)
            ln = 14.0 + 12.0 * t
            m.box(wb, base[0] - 1.2, base[1] - ln, base[2], base[0] + 1.2, base[1], base[2], rainbow,
                  rotation=(-16, 0, -sx * (70 - 50 * t)), pivot=base)
    cb = m.bone("cap", bd, (0, 50, 3))                           # long green streamer cape
    for i in range(5):
        x = -4 + i * 2
        m.box(cb, x - 1.0, 10.0, 4.0 + abs(x) * 0.3, x + 1.0, 50.0, 4.0 + abs(x) * 0.3, CAPE,
              rotation=(10, 0, x * 1.5), pivot=(x, 50.0, 4.0))
    ar = a["arm_right"]                                          # the rapier
    h = ar["hand"]
    sw = m.bone("sword", ar["bone"], h)
    m.box(sw, h[0] - 1.6, h[1] - 0.6, h[2] - 1.6, h[0] + 1.6, h[1] + 0.6, h[2] + 1.6, GOLD)        # guard
    rod(m, sw, (h[0], h[1], h[2]), (h[0] - 6.0, h[1] - 26.0, h[2] - 10.0), 1, solid(P, "white_dark"), extend=0)
    for sx in (-1, 1):                                           # gold armour pieces on the hips
        m.box(bd, sx * 3.4 - 1.4, 28.0, -3.8, sx * 3.4 + 1.4, 32.0, -3.0, GOLD_ARM)
    return m
