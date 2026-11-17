"""Shared builder for Demon, the Demon Lord of Wrath (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). make(name, look):

- "base": a tall fallen angel in a long dark-red coat trimmed with white fur, silver horns curling from a head of
  white hair, a cruel blue-grey face, a gold pentagram badge, violet clawed hands and feet with red claws, and two
  huge violet bat wings with red-tipped finger claws.
- "x": the X-Antibody form, hulking in crimson crystal armour: giant crystal-studded gauntlet claws, red horns, a
  violet-masked face, purple bat wings and a burning golden ring of flame behind its head.
- "super": Demon Super Ultimate, a lean black figure with a narrow horned head, a green band round its waist, black
  trousers, violet clawed feet and an enormous cloak of violet wings with great grasping claws at their tops.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, fur, gem, local, metal, noise2, skin, solid, strands
from _route import pal, tone

BASE = {"coat": (140, 20, 30), "coat_dark": (60, 6, 10), "fur": (240, 240, 244), "fur_dark": (180, 180, 190),
        "skin": (110, 120, 170), "skin_dark": (50, 56, 90), "skin_light": (170, 180, 220), "hair": (230, 230, 240),
        "hair_dark": (160, 160, 180), "horn": (200, 204, 216), "horn_dark": (110, 114, 128), "gold": (240, 200, 70),
        "claw": (210, 30, 40), "wing": (110, 60, 150), "wing_dark": (50, 20, 80), "red": (210, 30, 40),
        "crystal": (230, 50, 70), "crystal_light": (255, 170, 180), "black": (30, 28, 34), "black_dark": (8, 8, 12),
        "black_light": (90, 90, 104), "green": (100, 230, 100), "flame": (255, 210, 60, 220),
        "flame_core": (255, 250, 200, 240), "eye": (250, 220, 60), "mouth": (40, 10, 20)}
SHINY = {"coat": (40, 40, 140), "coat_dark": (10, 10, 60), "wing": (60, 150, 110), "wing_dark": (20, 70, 50),
         "crystal": (60, 160, 240), "crystal_light": (180, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark", light="skin_light")
COAT = fabric(P, "coat", "coat_dark", axis="y")
FUR = fur(P, "fur", "fur_dark", length=1.2)
HORN = metal(P, "horn", dark="horn_dark")
CLAW = solid(P, "claw")
BLACK = skin(P, "black", dark="black_dark", light="black_light")
CRYSTAL = gem(P, "crystal", "crystal_light", glow=False)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["wing"] if noise2(u * 0.3, v * 0.3, 4) < 0.6 else p["wing_dark"], face), None


def wing_in(x, y, z, face, box):
    return True


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(y - (58.6 + (abs(x) - 1.2) * 0.4)) < 0.35 and 0.4 < abs(x) < 2.0 and x * sx > 0:
                return p["eye"], p["eye"]
        if abs(y - 55.8) < 0.4 and abs(x) < 1.6:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def badgef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x - 2.6, y - 47.0)
        a = math.atan2(y - 47.0, x - 2.6)
        if abs(r - 1.6) < 0.2 or (r < 1.6 and abs(math.sin(2.5 * a + 0.3)) < 0.15):
            return tone(p["gold"], face), None
    return COAT(x, y, z, face, variant, box=box, **k)


def make(name, look="base"):
    def build():
        m = Model(name)
        if look == "base":
            mats = {"skin": SKIN, "chest": badgef, "abs": COAT, "pelvis": COAT, "neck": SKIN, "deltoid": FUR,
                    "upper_arm": COAT, "forearm": FUR, "hand": SKIN, "finger": SKIN, "claw": CLAW, "thigh": COAT,
                    "knee": COAT, "shin": SKIN, "calf": SKIN, "foot": SKIN, "talon": CLAW}
            a = humanoid(m, mats, bulk=1.05, arm_bulk=1.1, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                         name=name)
        elif look == "x":
            mats = {"skin": CRYSTAL, "chest": armour(P, "coat", "coat_dark", trim="gold"), "abs": BLACK,
                    "pelvis": CRYSTAL, "neck": BLACK, "deltoid": CRYSTAL, "upper_arm": FUR, "forearm": CRYSTAL,
                    "hand": HORN, "finger": HORN, "claw": HORN, "thigh": CRYSTAL, "knee": HORN, "shin": FUR,
                    "calf": FUR, "foot": HORN, "talon": HORN}
            a = humanoid(m, mats, bulk=1.4, arm_bulk=1.6, leg_bulk=1.4, claws=True, talons=True, digitigrade=True,
                         name=name)
        else:
            mats = {"skin": BLACK, "chest": BLACK, "abs": solid(P, "green", glow=True), "pelvis": BLACK,
                    "neck": BLACK, "deltoid": BLACK, "upper_arm": BLACK, "forearm": BLACK, "hand": SKIN,
                    "finger": SKIN, "claw": HORN, "thigh": fabric(P, "black", "black_dark"), "knee": BLACK,
                    "shin": SKIN, "calf": SKIN, "foot": SKIN, "talon": HORN}
            a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                         name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, facef if look != "super" else BLACK, cut=1)
        horn = HORN if look != "x" else solid(P, "red")
        for sx in (-1, 1):                                                    # curling horns
            pts = [(sx * 2.4, 59.6, 0.0), (sx * 4.6, 61.6, 1.0), (sx * 5.6, 64.4, 0.0), (sx * 4.4, 67.0, -1.0)]
            if look == "super":
                pts = [(sx * 1.6, 60.0, 0.0), (sx * 2.4, 64.0, 1.0), (sx * 2.0, 68.0, 2.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, hd, p0, p1, 2 if j < 1 else 1, horn, extend=0.4)
        if look == "base":
            for i in range(9):                                                # white hair
                ang = math.radians(-100 + i * 25)
                rod(m, hd, (2.4 * math.sin(ang), 60.0, 1.0 + math.cos(ang)), (3.6 * math.sin(ang), 52.0, 4.0), 2,
                    strands(P, "hair", "hair_dark"), extend=0.3, t2=1)
            for sx in (-1, 1):                                                # long coat tails
                x0, x1 = sorted((sx * 1.0, sx * 5.0))
                m.box(bd, x0, 12.0, 3.0, x1, 32.0, 3.6, COAT, rotation=(10, 0, sx * 4), pivot=(sx * 3.0, 32.0, 3.0))
        if look == "x":                                                       # giant crystal claws + flame halo
            for nm in ("arm_left", "arm_right"):
                ar = a[nm]
                hx, hy, hz = ar["hand"]
                m.round_box(ar["bone"], hx, hz, 4.6, 4.6, hy - 2.0, hy + 6.0, CRYSTAL, cut=2)
                for j in range(4):
                    spike(m, ar["bone"], (hx + (j - 1.5) * 2.0, hy - 2.0, hz - 2.0), (0, -1, -0.6), 1.4, 7.0, HORN,
                          tip=0.5)
            hb = m.bone("ring_halo", bd, (0, 62, 5))
            for i in range(16):
                ang = 2 * math.pi * i / 16
                p0 = (9.0 * math.cos(ang), 62.0 + 9.0 * math.sin(ang), 6.0)
                p1 = (9.0 * math.cos(ang + math.pi / 8), 62.0 + 9.0 * math.sin(ang + math.pi / 8), 6.0)
                rod(m, hb, p0, p1, 2, solid(P, "flame", glow=True), extend=0.4)
        span, height = (30.0, 30.0) if look != "super" else (34.0, 44.0)
        for side in (1, -1):                                                  # huge bat wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.6))
            bat_wing(m, wb, (side * 3.0, 50.0, 3.6), span, height, 4, BLACK if look == "super" else SKIN,
                     cutout(wing_in, wingf), side=side, sweep=20)
            tipp = (side * (3.0 + span * 0.45 + span * 0.55 * math.cos(math.radians(10))), 50.0 + height * 0.85, 3.6)
            for j in range(3):                                                # finger claws on top
                spike(m, wb, tipp, (side * (0.4 - j * 0.4), 1.0, -0.2), 1.2 if look != "super" else 2.4,
                      4.0 if look != "super" else 9.0, CLAW if look != "super" else HORN, tip=0.4)
        return m
    return build
