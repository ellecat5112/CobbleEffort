"""Lesbeon, the Devotion Pokémon (Fairy/Fighting), a new Eevee evolution after the meme art the user shared (the art's
own name; artist not named): a pink, slender Eeveelution with a fierce red-eyed glare, a rainbow mohawk swept over one
eye with a dark shaved undercut, tall pointed ears with darker insides, two pink Venus-symbol earrings hanging on long
chains (one each side, together the lesbian double-Venus), and a short pink tail with a spiky darker tip.

Shiny: a lilac coat, with a mohawk in the colours of the lesbian pride flag.

Front is -z, y is up. 23 units tall to the ear tips; baseScale 0.65 (0.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod
from _route import pal, tone

SCALE = 0.65
HITBOX = [1.3, 1.4]
KIND = "quadruped"
K = 5
HEIGHT = 23
LOOK = ("a pink Eeveelution with a fierce red-eyed glare, a rainbow mohawk swept over one eye, tall pointed ears, two "
        "pink Venus-symbol earrings and a short spiky-tipped tail")

BASE = {"coat": (246, 196, 210), "coat_light": (252, 224, 232), "coat_dark": (226, 150, 176), "inner": (232, 120, 150),
        "eye": (200, 30, 50), "eye_dark": (90, 10, 24), "brow": (120, 40, 60), "nose": (130, 60, 70),
        "undercut": (110, 112, 124), "earring": (240, 120, 168), "earring_dark": (200, 80, 130)}
SHINY = {"coat": (210, 182, 236), "coat_light": (230, 214, 248), "coat_dark": (170, 138, 210), "inner": (176, 110, 210),
         "earring": (250, 160, 200), "earring_dark": (214, 110, 160)}
RAINBOW = [(228, 30, 30), (255, 140, 0), (250, 220, 0), (0, 150, 60), (30, 90, 230), (130, 40, 160)]
LESBIAN = [(214, 41, 0), (255, 155, 86), (255, 255, 255), (212, 98, 166), (164, 0, 98), (120, 20, 80)]


def P(v):
    return pal(BASE, SHINY, v)


def stripes(variant):
    return LESBIAN if variant and "shiny" in variant else RAINBOW


def coatf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return p["coat_light"], None
    return tone(p["coat"], face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["coat_light"] if y < 2.4 else p["coat"], face), None                 # pale paws


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            ex, ey = sx * 1.45, 13.6
            dx, dy = x - ex, y - ey
            if (dx / 1.05) ** 2 + (dy / 0.8) ** 2 < 1:
                if dy > 0.25 + 0.45 * dx * sx:                                    # a fierce, angled brow
                    return p["brow"], None
                if math.hypot(dx + sx * 0.25, dy + 0.1) < 0.42:
                    return p["eye_dark"], None
                return p["eye"], None
        if abs(x) < 0.3 and 12.0 < y < 12.5:
            return p["nose"], None
    if face == "west" and y > 14.6:
        return tone(p["undercut"], face), None                                    # the shaved undercut
    return coatf(x, y, z, face, variant)


def earf(cx, y0, y1, w):
    """A tall pointed ear on a plane (pre-rotation): cut to a triangle, darker pink inside on its front."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        t = min(1.0, max(0.0, (y - y0) / (y1 - y0)))
        half = w / 2 * (1 - t) ** 0.85
        if abs(x - cx) > half:
            return (0, 0, 0, 0), None
        if face == "north" and abs(x - cx) < half * 0.55 and 0.08 < t < 0.85:
            return p["inner"], None
        return tone(p["coat"], face), None
    return s


def hairf(i):
    """One stripe of the mohawk (rainbow; the lesbian flag on a shiny)."""
    def s(x, y, z, face, variant, **k):
        c = stripes(variant)[i]
        return tone(c, face), None
    return s


def tipf(x, y, z, face, variant, **k):
    return tone(P(variant)["coat_dark"], face), None


def ringf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["earring"] if face in ("north", "south", "up") else p["earring_dark"], face), None


def venus(m, bone, cx, top_y, cz):
    """A Venus-symbol earring hanging from a chain: the cross on top, the ring below (parts at least a unit thick, or
    they would round to nothing)."""
    m.box(bone, cx - 0.5, top_y - 5.0, cz - 0.5, cx + 0.5, top_y, cz + 0.5, ringf)          # chain and stem
    m.box(bone, cx - 1.5, top_y - 4.2, cz - 0.5, cx + 1.5, top_y - 3.2, cz + 0.5, ringf)    # the cross bar
    r, n, cy = 1.8, 8, top_y - 6.9
    for i in range(n):                                                                # the ring
        t = 2 * math.pi * (i + 0.5) / n
        x, y = cx + r * math.sin(t), cy + r * math.cos(t)
        w = 2 * r * math.sin(math.pi / n) + 0.6
        m.box(bone, x - w / 2, y - 0.5, cz - 0.5, x + w / 2, y + 0.5, cz + 0.5, ringf,
              rotation=(0, 0, math.degrees(t)), pivot=(x, y, cz))


def build() -> Model:
    m = Model("lesbeon")
    top = m.bone("lesbeon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0.5, 2.6, 6.0, 7.0, 11.6, coatf, cut=1.2)                   # slender body
    m.round_box(bd, 0, -4.6, 2.4, 2.0, 8.6, 13.0, coatf, cut=0.9)                  # chest and neck
    tl = m.bone("tail", bd, (0, 10.8, 6.2))
    rod(m, tl, (0, 10.8, 6.0), (0, 13.6, 8.6), 2.0, coatf, extend=0.3, t2=1.4)      # short tail
    for dx, dz in ((0, 0), (-0.7, 0.4), (0.7, 0.4)):                                # its spiky darker tip
        rod(m, tl, (0, 13.4, 8.4), (dx, 15.4, 9.4 + dz), 0.9, tipf, extend=0.1)
    hd = m.bone("head", bd, (0, 12.5, -5.0))
    m.round_box(hd, 0, -5.4, 2.9, 2.6, 10.8, 16.0, headf, cut=1.1)                 # head
    m.round_box(hd, 0, -8.2, 1.3, 0.8, 11.2, 13.0, coatf, cut=0.4)                  # little muzzle
    for sx in (-1, 1):                                                              # tall pointed ears, tilted out
        cx = sx * 1.9
        m.box(hd, cx - 1.8, 15.4, -4.4, cx + 1.8, 23.0, -4.4, earf(cx, 15.4, 23.0, 3.6),
              rotation=(-8, 0, sx * 22), pivot=(cx, 15.6, -4.4))
    # the rainbow mohawk: stripes from front (red) to back (violet), and a fringe swept over one eye
    for i in range(6):
        z0 = -7.6 + i * 0.95
        m.box(hd, -1.6, 15.6, z0, 1.6, 17.6 - abs(i - 2) * 0.25, z0 + 1.0, hairf(i),
              rotation=(0, 0, 10), pivot=(0, 16, z0 + 0.5))
    for i in range(3):                                                              # the fringe over its right eye
        m.box(hd, 0.2 + i * 0.75, 13.8 - i * 0.3, -8.2, 0.95 + i * 0.75, 16.2, -7.7, hairf(i))
    for nm, sx in (("earring_left", 1), ("earring_right", -1)):                     # Venus-symbol earrings
        er = m.bone(nm, hd, (sx * 3.4, 13.4, -5.6))
        venus(m, er, sx * 3.6, 13.4, -6.0)
    for nm, lx, lz in (("leg_front_left", -1.4, -4.4), ("leg_front_right", 1.4, -4.4),
                       ("leg_back_left", -1.5, 4.6), ("leg_back_right", 1.5, 4.6)):
        lg = m.bone(nm, top, (lx, 8, lz))
        rod(m, lg, (lx, 8.4, lz), (lx, 0.9, lz - 0.2), 1.6, legf, extend=0.3)       # slim legs
        m.round_box(lg, lx, lz - 0.5, 0.95, 1.2, 0, 1.2, legf, cut=0.3)            # pale paws
    return m
