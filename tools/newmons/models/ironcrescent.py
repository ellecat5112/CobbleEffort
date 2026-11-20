"""Iron Crescent (Psychic/Steel), the future paradox Cresselia, built from boxes after the art the user shared
(artist and name not given; our name).

A sleek robot Cresselia: a lilac pod flecked with sparkles, its lower front a dome of pale blue glass, rising into a
long swan neck banded in dark segments. Its small head wears a dark visor and swept dark plates under a tall cream
crescent blade. Three lilac orbit rings, each slotted down its length, cross round its body, and a glowing violet
ring hovers beneath it.

Shiny: a pale gold body with rose rings.

Front is -z, y is up. 48 units tall (to the crescent); about 2.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import smooth_path, stars
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 48
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a sleek robot Cresselia: a sparkling lilac pod with a pale blue glass dome, a long banded swan neck, a dark "
        "visor under a tall cream crescent, three slotted orbit rings and a glowing hover ring")

BASE = {"lilac": (196, 150, 230), "lilac_dark": (150, 106, 190), "lilac_light": (224, 196, 246), "dark": (40, 36, 50),
        "glass": (176, 206, 240), "glass_light": (220, 236, 255), "cream": (238, 220, 170), "cream_dark": (200, 176, 120),
        "ring": (200, 140, 236), "ring_slot": (120, 70, 170), "hover": (210, 110, 240), "star": (255, 255, 255)}
SHINY = {"lilac": (236, 210, 140), "lilac_dark": (196, 166, 96), "lilac_light": (250, 236, 190), "ring": (240, 150, 180),
         "ring_slot": (170, 80, 110), "hover": (250, 140, 180)}
CY = 11.0


def P(v):
    return pal(BASE, SHINY, v)


def podf(x, y, z, face, variant, **k):
    """The pod: lilac with sparkles; its lower front a dome of pale blue glass."""
    p = P(variant)
    if z < -0.5 and y < CY + 0.5 and face in ("north", "east", "west", "down"):
        return (p["glass_light"] if y > CY - 1.5 and face == "north" else p["glass"]), None
    if stars(x, y, z, face, cell=1.5, r=0.2, prob=0.25):
        return p["star"], p["star"]
    return lit(p["lilac"], face, y, CY, 5), None


def neckf(x, y, z, face, variant, box=None, **k):
    """The neck: lilac banded in dark segments (rods: z runs back from the start)."""
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    if d % 2.6 < 0.7:
        return tone(p["dark"], face), None
    if stars(x, y, z, face, cell=1.5, r=0.2, prob=0.2):
        return p["star"], p["star"]
    return tone(p["lilac"], face), None


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def ringf(x, y, z, face, variant, box=None, **k):
    """An orbit ring's segment: lilac with a dark slot down its middle (rods: x across)."""
    p = P(variant)
    cx = box.lo[0] + box.size[0] / 2
    if face in ("up", "down") and abs(x - cx) < box.size[0] * 0.18:
        return p["ring_slot"], None
    return p["ring"], p["ring"]


def orbit(m, bone, c, rx, rz, tilt, yaw, n=28, w=1.6):
    """An elliptical ring of short rods round centre c, tipped `tilt` degrees about x then turned `yaw` about y."""
    ct, st = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))

    def pt(a):
        x, z = rx * math.cos(a), rz * math.sin(a)
        y, z = -z * st, z * ct
        x, z = x * cy_ + z * sy_, -x * sy_ + z * cy_
        return (c[0] + x, c[1] + y, c[2] + z)
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        rod(m, bone, pt(a0), pt(a1), w, ringf, extend=0.4, t2=0.6)


def build() -> Model:
    m = Model("ironcrescent")
    top = m.bone("ironcrescent", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.0, 6.0, 6.8, 6.0, podf, step=1)                       # the pod
    nk = m.bone("neck", bd, (0, CY + 4.6, 1.0))
    pts = smooth_path([(0, CY + 3.0, 1.0), (0, CY + 11.0, 2.4), (0, CY + 18.0, 1.6), (0, CY + 22.0, -0.4)], 10)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, nk, a, b, round((6.0 - 2.6 * i / (len(pts) - 2)) * 2) / 2, neckf, extend=0.8)
    wing = m.bone("wing_left", bd, (4.0, CY + 3.0, 2.0))                            # the crescent loop at its side
    wp = smooth_path([(4.4, CY + 2.0, 2.4), (10.0, CY + 6.0, 4.0), (12.4, CY + 13.0, 4.4), (10.0, CY + 18.0, 3.6),
                      (6.0, CY + 17.0, 2.6)], 12)
    for i, (a, b) in enumerate(zip(wp, wp[1:])):
        w = 4.6 - 3.0 * abs(i - 4) / 8
        rod(m, wing, a, b, 1.8, podf, extend=0.6, t2=max(1.5, round(w * 2) / 2))
    hy = CY + 23.6
    hd = m.bone("head", nk, (0, hy, -0.6))
    ellipsoid(m, hd, 0, hy, -0.8, 2.6, 2.4, 2.8, solid("lilac"), step=1)              # small head
    m.box(hd, -2.0, hy - 1.2, -4.6, 2.0, hy + 0.6, -2.0, solid("dark"))              # dark visor beak
    for sx in (-1, 1):                                                           # swept dark plates
        rod(m, hd, (sx * 1.8, hy - 0.6, -2.4), (sx * 4.2, hy - 2.4, 1.6), 1.6, solid("dark"), extend=0.4, t2=1.0)
    cres = m.bone("cap", hd, (0, hy + 2.0, -0.4))                                   # the tall cream crescent
    cp = smooth_path([(0, hy + 1.6, -1.2), (0, hy + 5.6, -2.8), (0, hy + 9.6, -2.4), (0, hy + 13.0, 0.6)], 8)
    for i, (a, b) in enumerate(zip(cp, cp[1:])):
        w = 6.0 - 4.6 * i / (len(cp) - 2)
        rod(m, cres, a, b, 1.2, solid("cream"), extend=0.6, t2=max(1.0, round(w * 2) / 2))
    for j, (tilt, yaw) in enumerate(((18, 20), (-24, -35), (60, 80))):          # three orbit rings
        rg = m.bone(f"ring_{'abc'[j]}", bd, (0, CY + 2.0, 0))
        orbit(m, rg, (0, CY + 2.0 + j * 1.2, 0), 15.0 - j, 4.2, tilt, yaw)
    hv = m.bone("ring_hover", top, (0, 1.0, 0))                                     # the hover ring beneath
    orbit(m, hv, (0, 1.0, 0), 4.6, 4.6, 0, 0, n=16, w=1.2)
    for i in range(16):
        a = 2 * math.pi * i / 16
        m.box(hv, math.cos(a) * 4.6 - 0.5, 0.4, math.sin(a) * 4.6 - 0.5, math.cos(a) * 4.6 + 0.5, 1.4,
              math.sin(a) * 4.6 + 0.5, solid("hover", True))
    return m
