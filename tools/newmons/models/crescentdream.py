"""Crescent Dream (Psychic/Fairy), the ancient paradox Cresselia, built from boxes after @Alex_LR04's art (the art's
own name).

A pterosaur Cresselia. Two immense wings rise from its shoulders as long curved crescents of pink, banded lighter
along their length, with little clawed pink hands at their joints. Its body is wrapped in a shaggy cream mane tipped
with green; its head is a long pointed tan beak under a pink cap, swept back into a tan crest, with a red eye. Its
legs and tail are blue and fluffy above tan clawed feet, and crescent ribbons of gold light swirl round behind it.

Shiny: lilac wings and a teal body.

Front is -z, y is up. 48 units tall (to the wing tips); about 3.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, smooth_path
from _regi import _hash, ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 48
SCALE = round(3.0 * 16 / HEIGHT, 3)
HITBOX = [1.6, 30 / 16]
KIND = "floater"
K = 3
LOOK = ("a pterosaur Cresselia with immense curved pink crescent wings, a shaggy cream mane tipped with green, a long "
        "tan beak and crest under a pink cap, fluffy blue legs and swirling gold crescent ribbons behind it")

BASE = {"pink": (214, 120, 170), "pink_light": (240, 178, 206), "pink_dark": (170, 84, 134), "cream": (246, 238, 214),
        "cream_dark": (214, 200, 170), "green": (150, 190, 90), "tan": (226, 196, 130), "tan_dark": (186, 150, 90),
        "blue": (90, 130, 200), "blue_light": (140, 176, 232), "eye": (210, 40, 40), "gold": (246, 210, 80),
        "gold_light": (255, 236, 150), "claw": (240, 226, 196)}
SHINY = {"pink": (176, 140, 226), "pink_light": (210, 190, 246), "pink_dark": (130, 100, 190), "blue": (60, 160, 160),
         "blue_light": (110, 210, 200)}
GC = (0.0, 22.0, 7.0)      # the gold swirl's centre


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def wingf(x, y, z, face, variant, box=None, **k):
    """A crescent wing: pink, banded lighter along its length (rods: y across the broad face)."""
    p = P(variant)
    cy = box.lo[1] + box.size[1] / 2
    v = (y - cy) / (box.size[1] / 2)
    if -0.1 < v < 0.35:
        return tone(p["pink_light"], face), None
    if v < -0.65:
        return tone(p["pink_dark"], face), None
    return tone(p["pink"], face), None


def manef(x, y, z, face, variant, box=None, **k):
    """A tuft of the shaggy mane: cream, green at its tip (rods: z runs back from the root)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    if d > 0.7:
        return tone(p["green"], face), None
    return tone(p["cream"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if y < 14.0:
        return lit(p["blue"], face, y, 14, 4), None
    return lit(p["cream"], face, y, 18, 5), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 6.0, y - 24.0) < 0.7:
        return p["eye"], p["eye"]
    if y > 25.4:
        return tone(p["pink"], face), None
    return lit(p["tan"], face, y, 24, 2.4), None


def swirlf(x, y, z, face, variant, **k):
    """Crescent ribbons of gold light swirling round (an xy plane)."""
    p = P(variant)
    dx, dy = x - GC[0], y - GC[1]
    r = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    for i in range(5):
        a0 = i * 2 * math.pi / 5
        t = ((a - a0) % (2 * math.pi)) / 2.0                   # 0..1 along a ribbon spanning 2 radians
        if t > 1.0:
            continue
        rr = 12.0 + 4.0 * t + 1.2 * (i % 2)
        w = 1.6 * math.sin(math.pi * t)
        if abs(r - rr) < w:
            c = p["gold_light"] if abs(r - rr) < w * 0.4 else p["gold"]
            return c, c
    return CLEAR


def build() -> Model:
    m = Model("crescentdream")
    top = m.bone("crescentdream", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 17.0, 0))
    ellipsoid(m, bd, 0, 17.0, 0.6, 3.6, 5.4, 4.0, bodyf, step=1)                  # body
    for i in range(14):                                                          # the shaggy mane
        a = math.radians(i * 360 / 14)
        root = (math.cos(a) * 3.4, 20.0 + 1.2 * math.sin(a * 2), 0.6 + math.sin(a) * 3.6)
        d = (math.cos(a) * 0.8, -1.0, math.sin(a) * 0.8 - 0.2)
        spike(m, bd, root, d, 2.0, 5.0 + 1.6 * _hash(i, 1), manef, tip=1.0)
    hd = m.bone("head", bd, (0, 22.0, -2.0))
    m.round_box(hd, 0, -4.6, 2.2, 2.6, 21.6, 26.6, headf, cut=1)                    # skull
    spike(m, hd, (0, 23.0, -6.6), (0, -0.25, -1), 2.6, 12.0, solid("tan"), tip=1.2)  # long beak
    spike(m, hd, (0, 25.6, -3.0), (0, 0.55, 1), 2.2, 9.0, solid("tan"), tip=1.0)     # swept crest
    m.round_box(hd, 0, -4.4, 2.4, 2.4, 25.4, 27.2, solid("pink"), cut=1)            # pink cap
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # immense crescent wings
        wg = m.bone(nm, bd, (sx * 3.0, 21.0, 1.0))
        pts = smooth_path([(sx * 3.0, 21.0, 1.0), (sx * 7.0, 25.0, 1.6), (sx * 11.0, 32.0, 2.6), (sx * 14.0, 39.0, 3.6),
                           (sx * 18.0, 45.0, 4.6), (sx * 23.0, 48.0, 5.0)], 12)
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            w = 6.0 - 4.8 * i / (len(pts) - 2)
            rod(m, wg, a, b, 1.6, wingf, extend=0.8, t2=max(1.2, round(w * 2) / 2))
        hand = pts[2]                                                            # little clawed hand at its joint
        for c in (-1, 0, 1):
            spike(m, wg, hand, (sx * 1.0, -0.2 + c * 0.6, -0.6), 0.9, 3.0, solid("pink"), tip=0.5)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                          # fluffy blue legs, tan claws
        lg = m.bone(nm, bd, (sx * 2.0, 13.0, 1.0))
        rod(m, lg, (sx * 2.0, 13.0, 1.0), (sx * 2.6, 6.0, -0.6), 2.6, solid("blue"), extend=0.6)
        ellipsoid(m, lg, sx * 2.6, 6.6, -0.6, 2.0, 1.6, 2.0, solid("blue_light"), step=1)
        for c in (-1, 0, 1):
            spike(m, lg, (sx * 2.6 + c * 0.8, 5.0, -0.8), (c * 0.3, -1, -0.5), 0.9, 3.2, solid("claw"), tip=0.5)
    tl = m.bone("tail", bd, (0, 13.0, 3.6))
    spike(m, tl, (0, 13.0, 3.6), (0, -0.6, 1), 2.4, 7.0, solid("blue"), tip=1.0)
    sw = m.bone("ring_swirl", top, GC)                                             # gold crescent ribbons
    R = 18.0
    m.box(sw, GC[0] - R, max(0.0, GC[1] - R), GC[2], GC[0] + R, GC[1] + R, GC[2], swirlf)
    return m
