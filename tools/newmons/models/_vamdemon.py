"""Shared builder for Vamdemon and Vamdemon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the vampire lord: a tall gaunt figure in a fitted navy suit with gold buttons and a belt, a huge black
cape lined in red with a high pointed collar, a red half-mask with swept gold horns over a pale face, red clawed
gloves with green cuffs, tall black boots with a skull on the toe, and little bats circling it. X-Antibody: a black
suit with a crimson waistcoat, a ragged red cape with pink crystal claw-tips, a purple fur collar, blond hair, a chain
across its chest and red cuffs. Shiny: violet suit / white suit."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, bat_wing
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, leather, metal, skin, solid, strands
from _route import pal, tone

LOOKS = {False: {"suit": (40, 50, 120), "suit_dark": (16, 20, 60), "cuff": (60, 150, 70), "glove": (200, 40, 50),
                 "glove_dark": (120, 14, 20)},
         True: {"suit": (36, 34, 40), "suit_dark": (12, 12, 14), "cuff": (190, 30, 40), "glove": (40, 38, 44),
                "glove_dark": (14, 14, 16)}}
COMMON = {"cape": (30, 28, 34), "cape_dark": (10, 10, 12), "lining": (190, 30, 40), "lining_dark": (110, 10, 16),
          "gold": (240, 200, 70), "gold_dark": (170, 120, 30), "skin": (220, 214, 230), "skin_dark": (160, 150, 180),
          "mask": (200, 40, 50), "boot": (30, 28, 32), "skull": (240, 236, 226), "eye": (250, 230, 90),
          "pink": (250, 120, 200, 220), "fur": (110, 70, 160), "fur_dark": (60, 30, 100), "hair": (240, 220, 150),
          "hair_dark": (190, 160, 90), "bat": (40, 36, 44), "steel": (180, 184, 196)}
SHINY = {"suit": (110, 60, 150), "suit_dark": (60, 24, 90), "lining": (40, 90, 180), "lining_dark": (16, 40, 110)}


def make(name, x=False):
    base = dict(COMMON, **LOOKS[x])

    def P(v):
        return pal(base, SHINY, v)

    SUIT = fabric(P, "suit", "suit_dark")
    GLOVE = leather(P, "glove", "glove_dark")

    def chestf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            if not x and abs(abs(xx) - 1.8) < 0.5 and int(y * 0.7) % 2 == 0 and y > 36:
                return tone(p["gold"], face), None
            if x and abs(xx) < 2.6:
                return tone(p["lining"], face), None
        return SUIT(xx, y, z, face, variant, box=box, **k)

    def capef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        c = p["lining"] if face == "north" else p["cape"]
        return tone(c, face), None

    def bootf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not x and face == "north" and y < 3.0 and abs(xx - (box.lo[0] + box.size[0] / 2 if box else 0)) < 1.0:
            return tone(p["skull"], face), None
        return leather(P, "boot", "boot")(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": SUIT, "chest": chestf, "abs": SUIT, "pelvis": SUIT, "deltoid": SUIT, "upper_arm": SUIT,
                "forearm": SUIT, "hand": GLOVE, "finger": GLOVE, "thigh": SUIT, "knee": SUIT, "shin": bootf,
                "calf": bootf, "foot": bootf, "neck": skin(P, "skin", dark="skin_dark")}
        a = humanoid(m, mats, bulk=0.9, arm_bulk=0.85, leg_bulk=0.9, claws=True, name=name)
        bd = a["body"]
        m.round_box(bd, 0, 0, 4.6, 3.4, 30.0, 31.8, leather(P, "boot", "boot"), cut=1)
        for nm in ("arm_left", "arm_right"):
            w = a[nm]["wrist"]
            m.round_box(a[nm]["bone"], w[0], w[2], 1.8, 1.8, w[1] + 0.2, w[1] + 2.2, solid(P, "cuff"), cut=0)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, skin(P, "skin", dark="skin_dark"), cut=1)
        if x:
            m.round_box(hd, 0, 0.8, 3.2, 3.0, 58.0, 62.0, strands(P, "hair", "hair_dark"), cut=1)
            for j in range(5):
                spike(m, hd, ((j - 2) * 1.2, 61.0, 1.0), ((j - 2) * 0.3, -1, 0.4), 1.4, 6.0, strands(P, "hair",
                      "hair_dark"), tip=0.8)
        else:
            m.box(hd, -3.0, 57.4, -3.4, 3.0, 60.4, -2.8, solid(P, "mask"))
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.4, 60.0, -1.0), (sx * 0.8, 1, 0.2), 1.4, 6.0, metal(P, "gold"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 58.6, -3.6, max(sx * 0.6, sx * 1.8), 59.2, -3.3, solid(P, "eye", glow=True))
            m.box(bd, min(sx * 2.0, sx * 6.6), 50.0, 0.0, max(sx * 2.0, sx * 6.6), 62.0, 1.0, capef,
                  rotation=(-10, 0, sx * 18), pivot=(sx * 2.0, 50.0, 0.5))                 # high collar
        if x:
            m.round_box(bd, 0, 0.6, 6.4, 4.6, 49.0, 52.6, fur(P, "fur", "fur_dark"), cut=2)
            for j in range(6):
                ball(m, bd, (-4.0 + j * 1.6, 46.0 - j * 1.4, -4.4), 0.6, metal(P, "steel"), layers=1)
        cb = m.bone("cape", bd, (0, 52, 4))
        cape(m, cb, 52.0, 18.0, 50.0, capef, z=4.4, flare=0.9 if x else 0.7, panels=8, seed=6)
        if x:
            for j in range(5):
                spike(m, cb, (-12.0 + j * 6.0, 4.0, 5.0 + abs(j - 2)), (0, -1, 0), 1.4, 3.0, solid(P, "pink", glow=True),
                      tip=0.8)
        else:
            bb = m.bone("bats", bd, (0, 50, 0))
            for i in range(5):
                ang = i * 2 * math.pi / 5
                cx, cy, cz = 14.0 * math.cos(ang), 52.0 + 6.0 * math.sin(ang * 2), 14.0 * math.sin(ang) * 0.4
                ball(m, bb, (cx, cy, cz), 0.9, solid(P, "bat"), layers=1)
                for sx in (-1, 1):
                    m.box(bb, min(cx, cx + sx * 3.0), cy - 0.2, cz - 0.6, max(cx, cx + sx * 3.0), cy + 0.6, cz + 0.6,
                          solid(P, "bat"), rotation=(0, 0, sx * 20), pivot=(cx, cy, cz))
        return m
    return build
