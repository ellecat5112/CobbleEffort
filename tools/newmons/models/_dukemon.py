"""Shared builder for Dukemon, the crimson Royal Knight (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). make(name, look):

- "base": a knight in white armour with crimson plates and gold trim, a red-and-white helm with a white crest-blade
  and two long trailing antennae, a long crimson cape, the lance Gram (a long silver cone with a red grip) and the
  great round silver shield Aegis with a gold rim and a red triangle emblem.
- "x": the X-Antibody form, sleeker armour edged in teal, a spray of crimson crest blades, a glowing teal crystal
  lance and a gold sun-ringed shield with a great blue jewel.
- "crimson": Crimson Mode, the armour turned red and gold, a lance and shield of white light and ten white feathered
  wings of light.
Shiny: black armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digibody import cape, dome, humanoid
from _digidetail import armour, fabric, feathers, gem, metal, solid
from _route import pal, tone

BASE = {"white": (240, 240, 246), "white_dark": (170, 174, 190), "white_light": (255, 255, 255), "red": (200, 30, 40),
        "red_dark": (110, 10, 20), "red_light": (250, 120, 120), "gold": (240, 200, 60), "gold_dark": (160, 120, 20),
        "silver": (214, 218, 230), "silver_dark": (110, 114, 128), "teal": (80, 230, 220, 220), "blue": (40, 100, 230),
        "blue_light": (170, 210, 255), "light": (240, 250, 255, 200), "eye": (60, 220, 120)}
SHINY = {"white": (60, 60, 70), "white_dark": (20, 20, 26), "white_light": (130, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", light="white_light", trim="gold", trim_w=0.25)
RED = armour(P, "red", "red_dark", light="red_light", trim="gold", trim_w=0.3)
SILVER = metal(P, "silver", dark="silver_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def aegisf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
        r = math.hypot(x - cx, y - cy)
        if r > 8.0:                                                      # gold rim (shield radius 9)
            return tone(p["gold"], face), None
        ty = y - cy + 2.0
        if 0 < ty < 4.0 and abs(x - cx) < (4.0 - ty) * 0.6:
            return tone(p["red"], face), None                           # the red triangle
    return SILVER(x, y, z, face, variant, box=box, **k)


def make(name, look="base"):
    def build():
        m = Model(name)
        body = RED if look == "crimson" else WHITE
        plate = GOLD if look == "crimson" else RED
        mats = {"skin": body, "chest": plate, "abs": body, "pelvis": plate, "neck": body, "deltoid": plate,
                "upper_arm": body, "forearm": plate, "hand": body, "finger": body, "thigh": body, "knee": plate,
                "shin": body, "calf": body, "foot": plate, "toe": plate}
        a = humanoid(m, mats, bulk=1.0, arm_bulk=1.05, leg_bulk=1.05, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.0, 60.4, plate, cut=1)
        m.box(hd, -1.8, 56.6, -3.7, 1.8, 57.4, -3.5, solid(P, "eye", glow=True))
        if look == "x":
            for i in range(5):                                                     # spray of crimson crest blades
                spike(m, hd, (0, 60.0, -1.0), ((i - 2) * 0.4, 1.0, 0.6), 1.0, 8.0 - abs(i - 2), RED, tip=0.25)
        else:
            spike(m, hd, (0, 59.6, -2.0), (0, 1, 0.3), 1.4, 6.0, body, tip=0.3)    # white crest-blade
            for sx in (-1, 1):                                                     # trailing antennae
                pts = [(sx * 1.6, 60.0, 1.0), (sx * 5.0, 68.0, 6.0), (sx * 10.0, 70.0, 14.0), (sx * 14.0, 64.0, 20.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, hd, p0, p1, 1, SILVER, extend=0.3)
        for sx in (-1, 1):
            dome(m, bd, (sx * 8.0, 49.0, 0), 4.0, 3.4, plate)
        if look != "crimson":
            cape(m, bd, 52.0, 16.0, 46.0, fabric(P, "red", "red_dark"), z=4.0, flare=1.0)
        ar = a["arm_right"]                                                        # lance
        hx, hy, hz = ar["hand"]
        lance = solid(P, "teal", glow=True) if look == "x" else solid(P, "light", glow=True) if look == "crimson" \
            else SILVER
        m.round_box(ar["bone"], hx, hz, 2.4, 2.4, hy - 2.0, hy + 1.0, plate, cut=1)
        d = (0.0, -0.55, -0.83)                                                    # pointing forward and down
        start = (hx, hy, hz - 1.0)
        for j, (r, L) in enumerate(((3, 10.0), (2, 12.0), (1, 12.0))):
            s0 = sum(l for _, l in ((3, 10.0), (2, 12.0), (1, 12.0))[:j])
            p0 = tuple(c + u * s0 for c, u in zip(start, d))
            p1 = tuple(c + u * (s0 + L) for c, u in zip(start, d))
            rod(m, ar["bone"], p0, p1, r, lance, extend=0.4)
        al = a["arm_left"]                                                         # shield
        hx, hy, hz = al["hand"]
        sx = 1 if hx > 0 else -1
        R = 9.0
        sh = aegisf if look == "base" else gem(P, "blue", "blue_light") if look == "x" else solid(P, "light", glow=True)
        cx, cy = hx + sx * 2.0, hy + 4.0                                           # octagonal round shield
        m.box(al["bone"], cx - R, cy - R * 0.45, hz - 3.6, cx + R, cy + R * 0.45, hz - 2.4, sh)
        m.box(al["bone"], cx - R * 0.45, cy - R, hz - 3.7, cx + R * 0.45, cy + R, hz - 2.5, sh)
        m.box(al["bone"], cx - R * 0.78, cy - R * 0.78, hz - 3.5, cx + R * 0.78, cy + R * 0.78, hz - 2.3, sh)
        if look == "x":
            for i in range(12):                                                    # gold sun ring
                ang = 2 * math.pi * i / 12
                spike(m, al["bone"], (hx + sx * 2.0 + R * math.cos(ang), hy + 4.0 + R * math.sin(ang), hz - 3.0),
                      (math.cos(ang), math.sin(ang), 0), 2.0, 3.0, GOLD, tip=0.5)
        if look == "crimson":                                                      # ten wings of light
            for side in (1, -1):
                for j in range(5):
                    wb = m.bone("wing_%s_%d" % ("left" if side > 0 else "right", j), bd, (side * 2.6, 50.0, 3.6))
                    feather_wing(m, wb, (side * 2.6, 50.0 - j * 2.0, 3.6 + j * 0.4), 22.0 - j * 2.0, 8.0, 1,
                                 feathers(P, "white", "white_dark", size=(1.4, 3.0)), side=side, sweep=20 + j * 8,
                                 droop=-10.0 + j * 5.0, layers=1)
        return m
    return build
