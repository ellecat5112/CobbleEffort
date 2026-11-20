"""Iron Storm (Psychic/Electric), the future paradox Lugia, built from boxes after @CaligoMilites' art (the art's own
name).

A chunky armoured Lugia in white plating. Its head is a blocky helmet with a dark visor and a red eye and a pointed
snout, set on a neck of black rings. Round glowing peach panels shine from its chest, belly, thighs and its massive
wing-arms, which are great rounded cylinders of armour studded with spikes tipped in glowing peach. It stands on thick
white legs with black clawed feet, and its armoured tail carries more glowing spikes.

Shiny: steel-blue plating with violet panels.

Front is -z, y is up. 56 units tall; about 4.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 56
SCALE = round(4.4 * 16 / HEIGHT, 3)
HITBOX = [2.6, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a chunky white-armoured Lugia with a blocky visored helmet, glowing peach panels on its chest, thighs and "
        "massive cylinder wing-arms, peach-tipped spikes and thick legs on black clawed feet")

BASE = {"white": (236, 236, 242), "white_dark": (190, 192, 206), "black": (30, 30, 36), "black_light": (64, 64, 74),
        "peach": (255, 196, 164), "peach_light": (255, 236, 210), "peach_edge": (240, 150, 120), "red": (220, 40, 60)}
SHINY = {"white": (176, 196, 226), "white_dark": (128, 150, 190), "peach": (196, 150, 255), "peach_light": (232, 214, 255),
         "peach_edge": (150, 100, 230)}
CY = 33.0
PANELS = [(0.0, 37.0, 2.6), (0.0, 30.0, 2.2), (-2.6, 33.0, 1.3), (2.6, 33.0, 1.3)]       # chest/belly circles (x, y, r)


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def panel(p, d, r):
    """A glowing peach disc: brighter at its heart, a darker rim."""
    if d > r:
        return None
    c = p["peach_edge"] if d > r * 0.82 else (p["peach_light"] if d < r * 0.4 else p["peach"])
    return c, c


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for px, py, r in PANELS:
            hit = panel(p, math.hypot(x - px, y - py), r)
            if hit:
                return hit
    return lit(p["white"] if face != "south" else p["white_dark"], face, y, CY, 9), None


def podf(spots):
    """White armour with glowing peach discs at given (u, v) spots on its outward faces (rods: z along the pod)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west", "up", "north"):
            a = z - box.lo[2]
            b = (y - box.lo[1]) if face in ("east", "west", "north") else (x - box.lo[0])
            for su, sv, r in spots:
                hit = panel(p, math.hypot(a - su * box.size[2], b - sv * (box.size[1] if face != "up"
                                                                          else box.size[0])), r)
                if hit:
                    return hit
        return tone(p["white"] if face != "down" else p["white_dark"], face), None
    return s


def thighf(cx, cy, cz):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("north", "east", "west"):
            a = x - cx if face == "north" else z - cz
            hit = panel(p, math.hypot(a, y - cy), 2.0)
            if hit:
                return hit
        return lit(p["white"], face, y, cy, 5), None
    return s


def headf(x, y, z, face, variant, **k):
    """A blocky white helmet with a dark visor band and a red eye on each side."""
    p = P(variant)
    if 51.4 < y < 52.8 and face in ("east", "west", "north"):
        if face in ("east", "west") and abs(z + 2.6) < 0.7:
            return p["red"], p["red"]
        return p["black"], None
    return tone(p["white"] if face != "down" else p["white_dark"], face), None


def peachspike(m, bone, base, d, w, h):
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    mid = tuple(b + uu * h * 0.45 for b, uu in zip(base, u))
    rod(m, bone, base, mid, w, solid("white"), extend=0.2)
    spike(m, bone, mid, u, w * 0.8, h * 0.55, solid("peach", True), tip=max(0.6, w * 0.3))


def build() -> Model:
    m = Model("ironstorm")
    top = m.bone("ironstorm", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 6.0, 8.4, 5.2, bodyf, step=1)                     # the armoured torso
    for i in range(3):                                                             # neck of black rings
        y0 = 41.2 + i * 2.2
        m.round_box(bd, 0, -0.4 - i * 0.6, 2.4, 2.4, y0, y0 + 1.6, solid("black"), cut=1)
        m.round_box(bd, 0, -0.4 - i * 0.6, 1.8, 1.8, y0 + 1.4, y0 + 2.4, solid("black_light"), cut=0.6)
    hd = m.bone("head", bd, (0, 48.5, -1.6))
    m.box(hd, -3.2, 48.4, -6.0, 3.2, 55.6, 3.0, headf)                             # the blocky helmet
    m.box(hd, -2.2, 49.0, -10.6, 2.2, 52.8, -6.0, headf)                            # snout block
    spike(m, hd, (0, 50.6, -10.4), (0, -0.25, -1), 2.4, 2.6, solid("white"), tip=0.8)
    spike(m, hd, (0, 55.4, 1.0), (0, 0.5, 1), 2.4, 4.6, solid("white"), tip=0.9)    # swept crest
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 54.0, 2.0), (sx * 0.5, 0.3, 1), 1.4, 3.4, solid("white"), tip=0.6)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                           # massive wing-arms
        ar = m.bone(nm, bd, (sx * 6.0, 41.0, 0))
        sh, el, wr = (sx * 6.0, 41.5, 0.4), (sx * 15.0, 45.5, 1.0), (sx * 21.0, 32.0, -2.0)
        rod(m, ar, sh, el, 6.0, podf([(0.55, 0.5, 1.6)]), extend=1.2)
        rod(m, ar, sh, el, 4.6, podf([]), extend=1.0, t2=7.2)
        rod(m, ar, el, wr, 8.0, podf([(0.3, 0.5, 2.2), (0.72, 0.5, 2.0)]), extend=1.6)
        rod(m, ar, el, wr, 6.2, podf([]), extend=1.4, t2=9.6)
        ellipsoid(m, ar, wr[0], wr[1] - 1.0, wr[2], 4.2, 3.6, 4.2, bodyf, step=1)
        for f in (0.15, 0.45, 0.75):                                                # peach-tipped spikes along it
            q = tuple(a + (b - a) * f for a, b in zip(el, wr))
            peachspike(m, ar, (q[0] + sx * 3.2, q[1] + 1.0, q[2]), (sx * 1, 0.6, 0.2), 2.0, 5.0)
        peachspike(m, ar, (el[0], el[1] + 3.0, el[2]), (sx * 0.3, 1, 0.1), 2.2, 5.6)
        for cl in (-0.6, 0.0, 0.6):                                                 # black claws at the end
            spike(m, ar, (wr[0] + cl * 1.6, wr[1] - 4.2, wr[2] - 1.0), (cl * 0.3, -1, -0.4), 1.2, 2.6,
                  solid("black"), tip=0.5)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                           # thick legs, black clawed feet
        lg = m.bone(nm, bd, (sx * 4.0, 25.0, 0))
        ellipsoid(m, lg, sx * 4.6, 19.0, -0.2, 4.4, 6.4, 4.6, thighf(sx * 4.6, 19.0, -0.2), step=1)
        rod(m, lg, (sx * 4.6, 14.0, 0.4), (sx * 4.8, 6.0, 1.6), 4.6, solid("white"), extend=0.6)
        rod(m, lg, (sx * 4.8, 6.6, 1.6), (sx * 4.8, 2.0, 0.0), 4.0, solid("black"), extend=0.4)
        m.box(lg, sx * 4.8 - 2.8, 0, -2.6, sx * 4.8 + 2.8, 2.6, 2.6, solid("black"))
        for cl in (-0.7, 0.0, 0.7):
            spike(m, lg, (sx * 4.8 + cl * 1.8, 1.2, -2.6), (cl * 0.3, -0.35, -1), 1.8, 3.6, solid("black_light"),
                  tip=0.7)
    tl = m.bone("tail", bd, (0, 26.0, 4.0))                                        # armoured tail
    pts = [(0, 26.0, 4.2), (0, 20.0, 11.0), (0, 14.0, 17.0), (0, 9.0, 23.0), (0, 6.0, 28.0)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, a, b, 5.0 - i * 1.0, solid("white"), extend=0.8)
        peachspike(m, tl, (b[0], b[1] + 2.4 - i * 0.4, b[2] - 1.0), (0, 1, 0.6), 1.8 - i * 0.2, 4.0 - i * 0.4)
    return m
