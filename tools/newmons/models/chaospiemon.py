"""Chaos Piemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): the corrupted jester. A tall clown in a dark grey coat with a red-lined cape, a white ruffled
collar, a half white, half black mask under a tall dark crest, huge white gloves with long silver fingers, baggy pale
blue trousers, pointed pale boots, and four great silver swords crossed on its back. 35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import fabric, local, metal, solid
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall corrupted jester in a dark grey coat and red-lined cape, a white ruff, a half black-and-white mask, "
        "huge white gloves, baggy pale trousers and four silver swords crossed on its back")
BASE = {"coat": (70, 70, 80), "coat_dark": (30, 30, 36), "red": (200, 30, 40), "red_dark": (110, 10, 18),
        "white": (240, 240, 246), "white_dark": (180, 184, 196), "pale": (200, 220, 230), "pale_dark": (140, 160, 176),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "black": (24, 24, 30), "eye": (250, 200, 40),
        "hilt": (130, 130, 140)}
SHINY = {"coat": (120, 40, 140), "coat_dark": (60, 14, 80), "red": (230, 180, 40), "red_dark": (160, 110, 10)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "coat", "coat_dark", axis="y", period=2.8)
PALE = fabric(P, "pale", "pale_dark", axis="y", period=2.0)
STEEL = metal(P, "steel", dark="steel_dark")


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(x - 1.1) < 0.6 and abs(y - 58.2) < 0.4:
            return p["eye"], p["eye"]
        if abs(x + 1.1) < 0.6 and abs(y - 58.2) < 0.4:
            return tone(p["red"], face), None
    return tone(p["white"] if x < 0 else p["black"], face), None


def build():
    m = Model("chaospiemon")
    mats = {"skin": COAT, "pelvis": COAT, "hand": solid(P, "white"), "finger": STEEL, "thigh": PALE, "knee": PALE,
            "shin": PALE, "calf": PALE, "foot": solid(P, "pale"), "toe": solid(P, "pale")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.05, leg_bulk=1.3, name="chaospiemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.6, 61.0, maskf, cut=1)
    for i in range(5):                                                      # tall dark crest
        spike(m, hd, ((i - 2) * 0.9, 60.6, 0.0), ((i - 2) * 0.1, 1, 0.2), 1.4, 5.0 + (2 - abs(i - 2)) * 1.4,
              solid(P, "coat_dark"), tip=0.4)
    for i in range(14):                                                     # the white ruff
        ang = math.radians(i * 360 / 14)
        c = (4.6 * math.sin(ang), 51.6, 0.2 - 3.6 * math.cos(ang))
        m.box(bd, c[0] - 1.4, c[1] - 1.0, c[2] - 0.8, c[0] + 1.4, c[1] + 1.4, c[2] + 0.8, solid(P, "white"),
              rotation=(0, -math.degrees(ang), 25), pivot=c)
    for nm in ("arm_left", "arm_right"):                                    # huge white gloves
        h = a[nm]["hand"]
        m.round_box(a[nm]["bone"], h[0], h[2], 2.8, 2.8, h[1] - 2.0, h[1] + 3.0, solid(P, "white"), cut=1)
    cb = m.bone("cap", bd, (0, 52, 3))                                      # red-lined cape
    cape(m, cb, 52.0, 20.0, 40.0, fabric(P, "red", "red_dark", axis="y"), z=4.2, flare=1.0, panels=8, sweep=(0, 4),
         seed=9)
    sb = m.bone("swords", bd, (0, 46, 5))                                   # four crossed swords
    for j, (sx, ang) in enumerate(((1, 40), (-1, 40), (1, 70), (-1, 70))):
        r = math.radians(ang)
        a0 = (-sx * 10.0 * math.cos(r), 46.0 - 10.0 * math.sin(r), 6.0 + j * 0.8)
        a1 = (sx * 12.0 * math.cos(r), 46.0 + 12.0 * math.sin(r), 6.0 + j * 0.8)
        rod(m, sb, a0, a1, 1, STEEL, extend=0, t2=2)
        m.box(sb, a0[0] - 1.4, a0[1] - 1.4, a0[2] - 0.5, a0[0] + 1.4, a0[1] + 1.4, a0[2] + 0.5, solid(P, "hilt"))
    return m
