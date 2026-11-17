"""Shared builder for Duftmon, the Royal Knight strategist (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). make(name, look):

- "base": a slender leopard knight in chocolate-brown armour with white plates, a leopard-masked helm with blue eyes,
  a long blonde mane, white feathered wings, a red sash streaming from its waist, steel-and-blue cuffs, a rapier and a
  long tail ending in a golden ball.
- "x": the X-Antibody form, bulkier in brown armour with teal studs, purple spikes and a violet-lined cape, a blade
  of pink light, golden mane and the gold-tipped tail.
- "leopard": Leopard Mode, a crouching four-legged leopard in the same brown armour with the blonde mane, blue spikes
  on its shoulders, white wings, red claws and the gold-ball tail.
Shiny: silver armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing, quadruped
from _digibody import cape, dome, humanoid
from _digidetail import armour, fabric, feathers, metal, solid, strands
from _route import pal, tone

BASE = {"brown": (110, 70, 50), "brown_dark": (50, 28, 16), "brown_light": (180, 130, 100), "white": (240, 240, 244),
        "white_dark": (180, 184, 196), "blonde": (250, 220, 120), "blonde_dark": (200, 160, 60), "red": (200, 30, 40),
        "red_dark": (110, 10, 20), "blue": (50, 90, 200), "teal": (80, 220, 210), "purple": (110, 50, 150),
        "purple_dark": (50, 20, 80), "gold": (240, 200, 60), "steel": (210, 214, 226), "steel_dark": (100, 104, 116),
        "pink": (255, 120, 200, 210), "feather": (246, 246, 250), "feather_dark": (190, 194, 210), "eye": (60, 140, 250)}
SHINY = {"brown": (180, 184, 200), "brown_dark": (90, 94, 110), "brown_light": (240, 240, 250)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "brown", "brown_dark", light="brown_light", trim="gold", trim_w=0.25)
WHITE = armour(P, "white", "white_dark")
STEEL = metal(P, "steel", dark="steel_dark")
MANE = strands(P, "blonde", "blonde_dark")
WING = feathers(P, "feather", "feather_dark", size=(1.4, 2.8))


def tail(m, bone, pts):
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bone, p0, p1, 1, ARM, extend=0.5)
    e = pts[-1]
    m.round_box(bone, e[0], e[2], 1.6, 1.6, e[1] - 1.6, e[1] + 1.6, solid(P, "gold"), cut=1)


def make(name, look="base"):
    def build():
        m = Model(name)
        if look == "leopard":
            mats = {"skin": ARM, "belly": WHITE, "neck": WHITE, "head": ARM, "snout": ARM, "jaw": ARM,
                    "mouth": solid(P, "red_dark"), "tooth": solid(P, "white"), "leg_upper": ARM, "leg_lower": ARM,
                    "paw": ARM, "claw": solid(P, "red"), "tail": ARM}
            a = quadruped(m, mats, name, length=30.0, body_y=16.0, body_rx=5.6, body_ry=5.6, chest_bulk=1.3,
                          neck=((0, 20, -13), (0, 25, -17)), head_len=8.0, head_w=3.4, head_h=3.8, snout=0.5,
                          mouth_open=16, teeth=3, leg_bulk=1.4, toes=4,
                          tail=((0, 18, 15), (3, 22, 21), (6, 26, 25)), tail_r=(1.2, 1.0, 0.8))
            bd, hd = a["body"], a["head"]
            ex, ey, ez = a["eye"]
            for sx in (-1, 1):
                m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3,
                      ez + 0.6, solid(P, "red", glow=True))
                spike(m, bd, (sx * 5.0, 22.0, -10.0), (sx, 0.6, -0.4), 1.6, 6.0, solid(P, "blue"), tip=0.4)
            for i in range(9):                                                      # blonde mane
                ang = math.radians(-80 + i * 20)
                rod(m, hd, (2.6 * math.sin(ang), ey + 1.6, ez + 2.0), (5.0 * math.sin(ang), ey - 4.0, ez + 6.0), 2,
                    MANE, extend=0.3, t2=1)
            e = a["tail_pts"][-1]
            m.round_box(a["tail"], e[0], e[2], 1.6, 1.6, e[1] - 1.6, e[1] + 1.6, solid(P, "gold"), cut=1)
            for side in (1, -1):
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 22.0, 0))
                feather_wing(m, wb, (side * 3.0, 22.0, 0), 14.0, 8.0, 2, WING, side=side, sweep=35, droop=-8.0)
            return m
        x = look == "x"
        mats = {"skin": ARM, "chest": WHITE if not x else ARM, "abs": ARM, "pelvis": WHITE if not x else ARM,
                "neck": ARM, "deltoid": ARM, "upper_arm": ARM, "forearm": ARM, "hand": ARM, "finger": ARM,
                "thigh": WHITE if not x else ARM, "knee": STEEL, "shin": ARM, "calf": ARM, "foot": ARM, "toe": ARM}
        a = humanoid(m, mats, bulk=0.9 if not x else 1.35, arm_bulk=0.9 if not x else 1.4,
                     leg_bulk=0.95 if not x else 1.3, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, ARM, cut=1)                         # leopard-masked helm
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.0), 57.4, -4.5, max(sx * 0.8, sx * 2.0), 58.0, -4.3,
                  solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, 59.6, 0), (sx * 0.3, 1, 0.2), 1.2, 2.6, ARM, tip=0.4)  # ears
        for i in range(12):                                                                 # long blonde mane
            ang = math.radians(-110 + i * 20)
            rod(m, hd, (2.4 * math.sin(ang), 59.6, 0.8 + math.cos(ang)), (4.0 * math.sin(ang), 46.0, 5.0), 2, MANE,
                extend=0.3, t2=1)
        for nm in ("arm_left", "arm_right"):                                                # steel-and-blue cuffs
            w = a[nm]["wrist"]
            m.round_box(a[nm]["bone"], w[0], w[2], 2.0, 2.0, w[1] + 0.4, w[1] + 2.4, STEEL, cut=1)
        tl = m.bone("tail", bd, (0, 32, 3))
        tail(m, tl, [(0, 32.0, 3.0), (2.0, 24.0, 10.0), (6.0, 14.0, 14.0), (10.0, 8.0, 12.0)])
        ar = a["arm_right"]
        hx, hy, hz = ar["hand"]
        if not x:
            rod(m, ar["bone"], (hx, hy, hz), (hx - 2.0, hy + 20.0, hz - 12.0), 1, STEEL, extend=0, t2=1)   # rapier
            for sx in (-1, 1):                                                              # red sash
                pts = [(sx * 3.0, 32.0, 2.0), (sx * 8.0, 24.0, 6.0), (sx * 12.0, 14.0, 4.0), (sx * 10.0, 4.0, 8.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, bd, p0, p1, 1, fabric(P, "red", "red_dark"), extend=0.5, t2=3)
            for side in (1, -1):
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 50.0, 3.4))
                feather_wing(m, wb, (side * 2.6, 50.0, 3.4), 14.0, 8.0, 2, WING, side=side, sweep=30, droop=-6.0)
        else:
            rod(m, ar["bone"], (hx, hy, hz), (hx + 12.0, hy - 6.0, hz - 14.0), 1, solid(P, "pink", glow=True),
                extend=0, t2=3)                                                              # pink light blade
            for sx in (-1, 1):
                dome(m, bd, (sx * 8.4, 49.0, 0), 4.0, 3.4, ARM)
                spike(m, bd, (sx * 10.0, 50.0, 0), (sx, 0.3, 0), 1.8, 7.0, solid(P, "purple"), tip=0.4)
                for j in range(2):
                    m.round_box(bd, sx * 8.4, -3.6, 0.8, 0.6, 48.0 + j * 2.0, 49.0 + j * 2.0, solid(P, "teal", glow=True),
                                cut=0)
            cape(m, bd, 52.0, 14.0, 42.0, fabric(P, "purple", "purple_dark"), z=4.0, flare=0.9)
        return m
    return build
