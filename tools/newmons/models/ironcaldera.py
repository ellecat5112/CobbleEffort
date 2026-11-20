"""Iron Caldera (Fire/Ground), the future paradox Entei, built from boxes after the art the user shared (artist not
named, no name given; our name).

A heavy robot Entei: banded brown armour with glowing orange vents on its chest, grey disc joints at the hips and
shoulders, and legs ringed with black cuffs over glowing orange bands, ending in slotted grey hooves. Its head is a
grey skull-like mask with a glowing yellow eye under crimson crest plates and a swept gold crown, with grey blades
hanging from its chest like Entei's beard. A fan of grey blades rises from its back into a mane of glowing yellow
flame under a pall of black smoke, and thin orange laser beams lance out from it in every direction.

Shiny: steel-blue armour and blue-white fire.

Front is -z, y is up. 46 units tall (to the smoke); about 2.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _pgen1 import CLEAR, stars
from _regi import ellipsoid
from _route import pal, tone

HEIGHT = 46
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [2.6, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a heavy robot Entei of banded brown armour with glowing vents, a grey skull mask under crimson and gold crests, "
        "a fan of grey blades, a mane of glowing flame under black smoke and orange laser beams")

BASE = {"brown": (132, 74, 44), "brown_dark": (96, 52, 30), "brown_light": (166, 100, 62), "grey": (190, 192, 200),
        "grey_dark": (130, 132, 142), "black": (34, 32, 36), "glow": (255, 160, 40), "glow_light": (255, 230, 120),
        "red": (178, 36, 40), "red_dark": (128, 22, 28), "gold": (220, 186, 96), "gold_dark": (176, 140, 62),
        "flame": (255, 196, 40), "flame_light": (255, 240, 120), "flame_edge": (244, 120, 30), "smoke": (54, 54, 58, 230),
        "smoke_dark": (24, 24, 26, 230), "laser": (255, 140, 40), "spark": (255, 255, 255)}
SHINY = {"brown": (70, 92, 128), "brown_dark": (46, 62, 92), "brown_light": (100, 124, 160), "glow": (110, 200, 255),
         "glow_light": (210, 240, 255), "flame": (120, 200, 255), "flame_light": (220, 246, 255),
         "flame_edge": (60, 120, 230), "laser": (110, 190, 255)}
CLOUD = [(-9, 33, 5.0), (-4, 35, 5.5), (2, 35, 6.0), (8, 33, 5.5), (13, 30, 5.0), (17, 27, 4.0), (-11, 28, 4.0),
         (5, 29, 6.0), (-3, 30, 6.0)]
SMOKE = [(-6, 41, 3.6), (-1, 42, 4.0), (4, 41.5, 3.8), (9, 40, 3.4), (13, 38, 3.0), (17, 38, 2.4), (-10, 39, 2.6)]


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def armourf(x, y, z, face, variant, **k):
    """Banded brown plates; glowing orange vents on the chest."""
    p = P(variant)
    if face == "north" and z < -13:
        for vx in (-1.4, 1.4):
            if abs(x - vx) < 0.45 and 13.5 < y < 19.5:
                return p["glow"], p["glow"]
    if (z % 4.0) < 0.45 and face in ("east", "west", "up"):
        return tone(p["brown_dark"], face), None
    return tone(p["brown_light"] if face == "up" else p["brown"], face), None


def legf(x, y, z, face, variant, box=None, **k):
    """Brown legs ringed by a black cuff over a glowing orange band near the hoof (rods: z runs from the knee)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    if 0.5 < d < 0.66:
        return tone(p["black"], face), None
    if d >= 0.66:
        return p["glow"], p["glow"]
    return tone(p["brown"], face), None


def hooff(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and (x % 1.4) < 0.3:
        return tone(p["grey_dark"], face), None
    return tone(p["grey"], face), None


def maskf(eye_y, eye_z):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west") and math.hypot(z - eye_z, (y - eye_y) * 1.4) < 0.7:
            return p["flame_light"], p["flame_light"]
        if face == "north" and abs(y - eye_y) < 0.45 and abs(x) > 1.0:
            return p["flame_light"], p["flame_light"]
        return tone(p["grey"], face), None
    return s


def blobs(circles, key, edge, glowy=True, sparks=True):
    """A cloud on a zy plane: the union of circles (z, y, r), with a rim colour round its edge."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        best = -1e9
        for cz, cy, r in circles:
            best = max(best, r - math.hypot(z - cz, y - cy))
        if best < 0:
            return CLEAR
        if sparks and stars(x, y, z, face, cell=1.8, r=0.3, prob=0.25):
            return p["spark"], (p["spark"] if glowy else None)
        c = p[edge] if best < 0.7 else p[key]
        return c, (c[:3] if glowy else None)
    return s


def blobs_xy(circles, key, edge):
    """The same cloud seen from behind, on an xy plane (x from z's role)."""
    base = blobs(circles, key, edge)

    def s(x, y, z, face, variant, **k):
        return base(x, y, x * 1.2, face, variant, **k)
    return s


def build() -> Model:
    m = Model("ironcaldera")
    neck = ((0, 25.0, -14.0), (0, 28.0, -17.5))
    head_len, head_w, head_h = 9.5, 4.0, 5.0
    hx, hy, hz = neck[-1]
    eye_y, eye_z = hy + head_h * 0.25, hz - head_len * 0.35
    mats = {"skin": armourf, "belly": solid("brown_dark"), "neck": armourf, "head": maskf(eye_y, eye_z),
            "snout": solid("grey"), "jaw": solid("grey_dark"), "mouth": solid("black"), "tooth": solid("grey"),
            "tongue": solid("red_dark"), "leg_upper": armourf, "leg_lower": legf, "paw": hooff,
            "claw": solid("grey_dark"), "tail": armourf}
    a = quadruped(m, mats, "ironcaldera", length=30.0, body_y=18.0, body_rx=6.4, body_ry=6.2, chest_bulk=1.2,
                  neck=neck, head_len=head_len, head_w=head_w, head_h=head_h, snout=0.45, mouth_open=6, teeth=0,
                  leg_bulk=1.35, tail=((0, 21.0, 16.0), (0, 20.0, 19.0)), tail_r=(2.0, 1.4), toes=3, claws=False)
    bd, hd, nk = a["body"], a["head"], a["neck"]
    for sx in (-1, 1):                                                              # grey disc joints
        for zz in (-10.0, 10.0):
            x0, x1 = sorted((sx * 8.0, sx * 9.0))
            m.box(bd, x0, 13.0, zz - 2.4, x1, 18.6, zz + 2.4, solid("grey"))
            m.box(bd, x0 + 0.05 * sx, 13.8, zz - 2.9, x1 - 0.05 * sx, 17.8, zz + 2.9, solid("grey_dark"))
    top = a["skull_top"]
    for sx in (-1, 1):                                                              # crimson crest plates
        x0, x1 = sorted((sx * 2.6, sx * 4.6))
        m.box(hd, x0, hy - 0.6, hz - 4.0, x1, top + 1.4, hz + 1.6, solid("red"),
              rotation=(0, 0, sx * 14), pivot=(sx * 2.6, hy, hz))
    for i, (h, lean, w) in enumerate(((7.0, 0.9, 3.0), (5.6, 1.4, 2.4), (4.4, 2.0, 1.8))):   # the gold crown
        spike(m, hd, (0, top + 0.4, hz - 2.6 + i * 1.4), (0, 1, lean), w, h, solid("gold"), tip=max(0.8, w * 0.4))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, top + 0.2, hz - 1.0), (sx * 0.6, 1, 1.2), 1.6, 4.6, solid("gold_dark"), tip=0.7)
    for i, bx in enumerate((-2.4, -0.8, 0.8, 2.4)):                                 # grey beard blades on the chest
        rod(m, nk, (bx, 22.0, -15.4), (bx * 1.3, 13.0 - abs(bx) * 0.6, -16.4), 1.4, solid("grey"), extend=0.3,
            t2=0.6)
    # the back: a fan of grey blades, a mane of glowing flame, black smoke and orange laser beams
    mane = m.bone("mane", bd, (0, 24.0, -4.0))
    for i in range(6):
        ang = -50 + i * 20
        d = (math.sin(math.radians(ang)) * 0.8, 0.55, 0.8)
        spike(m, mane, (d[0] * 2.0, 24.0, -6.0 + i * 0.8), d, 1.6, 12.0 - abs(i - 2.5) * 1.2, solid("grey"), tip=0.6)
    m.box(mane, 0, 20.0, -16.0, 0, 42.0, 22.0, blobs(CLOUD, "flame", "flame_edge"))
    m.box(mane, -14.0, 22.0, 6.0, 14.0, 40.0, 6.0, blobs_xy([(x, y, r * 0.8) for x, y, r in CLOUD[:6]], "flame",
                                                             "flame_edge"))
    m.box(mane, 0.4, 34.0, -14.0, 0.4, 46.0, 21.0, blobs(SMOKE, "smoke", "smoke_dark", glowy=False, sparks=False))
    for ang, el, L in ((-60, 30, 22), (-25, 55, 24), (10, 65, 26), (40, 45, 24), (70, 20, 22), (-80, 5, 18),
                       (85, -5, 18), (150, 35, 20)):
        a_, e_ = math.radians(ang), math.radians(el)
        d = (math.sin(a_) * math.cos(e_), math.sin(e_), math.cos(a_) * math.cos(e_))
        start = (d[0] * 4.0, 26.0 + d[1] * 2.0, 2.0 + d[2] * 4.0)
        rod(m, mane, start, tuple(s_ + v * L for s_, v in zip(start, d)), 0.6, solid("laser", True), extend=0.2)
    return m
