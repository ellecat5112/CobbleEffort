"""Genesis One (Psychic/Normal), the ancient paradox Mew, built from boxes after @amalryart's art (the art's own name;
Brasto region).

A small curled Mew of translucent-looking salmon pink with darker rib-like bands round its body, limbs and tail, as
if its skeleton showed through, and a big almond eye of grey-green under a heavy lid. It floats curled inside a ring of
pink tube, banded at its joints, and from the ring three DNA double helices spiral out to one side in glowing
rainbow colours.

Shiny: a sky-blue body and ring.

Front is -z, y is up. 35 units tall; about 1.3 blocks (the helices reach out about 1.6 blocks to its left).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import helix, rainbow, ribbon, smooth_path
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 35
SCALE = round(1.3 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("a curled translucent-pink Mew with rib-like bands and a heavy-lidded grey-green eye, floating inside a banded "
        "pink ring from which three glowing rainbow DNA helices spiral out")

BASE = {"pink": (252, 172, 180), "pink_light": (255, 206, 206), "rib": (230, 120, 144), "rib_dark": (190, 80, 110),
        "eye": (150, 160, 140), "eye_dark": (70, 76, 70), "lid": (196, 110, 120), "ring": (232, 120, 140),
        "ring_dark": (184, 74, 104), "rung": (246, 242, 250)}
SHINY = {"pink": (150, 200, 244), "pink_light": (196, 228, 252), "rib": (96, 146, 214), "rib_dark": (60, 104, 176),
         "lid": (110, 150, 200), "ring": (120, 170, 236), "ring_dark": (70, 120, 196), "eye": (170, 150, 200),
         "eye_dark": (80, 60, 110)}
RC = (0.0, 14.0, 0.0)       # the ring's centre
RR = 10.0                   # the ring's radius
HELIX_BASES = []


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def ribbed(axis="y", period=1.5, share=0.32, cy=14.0, ry=6.0):
    """Salmon pink with darker rib bands (axis y: horizontal bands; axis z: rings round a rod)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        w = y if axis == "y" else z
        if (w % period) < period * share and face not in ("up", "down"):
            return lit(p["rib"], face, y, cy, ry), None
        return lit(p["pink"], face, y, cy, ry), None
    return s


def headf(x, y, z, face, variant, **k):
    """A big almond eye of grey-green under a heavy lid on each side of the face; a rib band over the crown."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.8, y - 18.6
            e = (dx / 1.5) ** 2 + (dy / 1.0) ** 2
            if e < 1.0:
                if dy > 0.35:
                    return p["lid"], None
                return (p["eye_dark"] if dx * sx > 0.5 else p["eye"]), None
            if e < 1.35:
                return p["eye_dark"], None
    if face == "up" and abs(z) < 0.6:
        return p["rib"], None
    return lit(p["pink"], face, y, 18.0, 4), None


def ringf(x, y, z, face, variant, **k):
    p = P(variant)
    if (z % 2.4) < 0.45:
        return tone(p["ring_dark"], face), None
    return tone(p["ring"], face), None


def helix_shader(base, d, length, strand=True):
    """Rainbow by distance along the helix from its base."""
    L = math.sqrt(sum(v * v for v in d))
    u = tuple(v / L for v in d)

    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not strand:
            c = p["rung"]
            return c, c
        c0 = box.pivot or box.lo
        t = sum((cc - bb) * uu for cc, bb, uu in zip(c0, base, u)) / length
        c = rainbow(0.0 + 0.8 * max(0.0, min(1.0, t)), s=0.62)
        return c, c
    return s


def build() -> Model:
    m = Model("genesisone")
    top = m.bone("genesisone", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    # the ring of pink tube round it
    n = 20
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p0 = (RC[0] + RR * math.cos(a0), RC[1] + RR * math.sin(a0), 0.0)
        p1 = (RC[0] + RR * math.cos(a1), RC[1] + RR * math.sin(a1), 0.0)
        rod(m, bd, p0, p1, 1.8, ringf, extend=0.6)
    # the curled Mew
    ellipsoid(m, bd, 0, 13.0, 0.4, 2.6, 3.4, 2.4, ribbed(cy=13, ry=3.4), step=1)       # body
    hd = m.bone("head", bd, (0, 16, 0))
    ellipsoid(m, hd, 0, 18.4, 0, 3.8, 3.4, 3.4, headf, step=1)                        # big head
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 21.0, 0.4), (sx * 0.5, 1, 0.1), 1.8, 2.6, solid("pink"), tip=0.9)   # ears
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        ar = m.bone(nm, bd, (sx * 2.0, 14.6, -1.0))
        rod(m, ar, (sx * 2.0, 14.6, -1.0), (sx * 2.6, 12.6, -3.0), 1.2, ribbed("z", 1.0, 0.35), extend=0.4)
        ellipsoid(m, ar, sx * 2.6, 12.4, -3.2, 0.8, 0.8, 0.8, solid("pink_light"), step=1)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                                # legs tucked up
        lg = m.bone(nm, bd, (sx * 1.6, 10.6, 0))
        rod(m, lg, (sx * 1.6, 10.8, 0.2), (sx * 2.6, 9.0, -2.6), 2.0, ribbed("z", 1.2, 0.35), extend=0.5)
        rod(m, lg, (sx * 2.6, 9.0, -2.6), (sx * 2.2, 7.4, -0.8), 1.6, ribbed("z", 1.2, 0.35), extend=0.4)
        ellipsoid(m, lg, sx * 2.2, 7.0, -1.2, 1.1, 0.8, 1.6, solid("pink_light"), step=1)
    tl = m.bone("tail", bd, (0, 11, 2.0))                                              # long thin tail
    path = smooth_path([(0, 11.0, 2.2), (2.6, 9.0, 3.6), (5.4, 6.4, 3.0), (6.4, 3.4, 1.0), (4.4, 1.6, -0.6)], 12)
    ribbon(m, tl, path, [1.0] * len(path), ribbed("z", 1.0, 0.35), extend=0.3)
    ellipsoid(m, tl, 4.0, 1.6, -0.8, 1.2, 1.2, 1.2, ribbed(cy=1.6, ry=1.2), step=1)
    # three rainbow DNA helices spiralling out from the ring to its left (+x)
    dn = m.bone("dna", bd, (RR, RC[1], 0))
    for ang, d, length, ph in ((35, (1, 0.95, 0.1), 21.0, 0.0), (0, (1, 0.05, -0.1), 19.0, 1.3),
                               (-35, (1, -0.5, 0.1), 13.0, 2.4)):
        a = math.radians(ang)
        base = (RC[0] + RR * math.cos(a), RC[1] + RR * math.sin(a), 0.0)
        helix(m, dn, base, d, length, 2.2, 2.0, helix_shader(base, d, length),
              helix_shader(base, d, length, strand=False), w=0.9, phase=ph)
    return m
