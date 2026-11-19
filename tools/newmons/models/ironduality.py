"""Iron Duality (Dragon/Electric), the paradox Regieleki and Regidrago in one, built from boxes after @Alex_LR04's art
(the art's own name).

Its core is Regieleki's: a black sphere under a silver crown that bites down over its face in zigzag teeth, with a tall
silver spike banded in glowing cyan and smaller crown points round it, Regieleki's dots in glowing pink, navy discs on
its sides, a black ribbed neck, a white crescent below with cyan points, and two glowing cyan lightning bolts for legs.
Arcs of cyan energy curve out from its crown. On either side hangs one of Regidrago's dragon heads, huge, dark slate
and angular, with spiked ridges and back horns, a slanted glowing cyan eye slit, and gaping jaws lined with glowing cyan
zigzag teeth, the lower jaw banded with a cyan zigzag.

Shiny: crimson heads with gold energy.

Front is -z, y is up. 43 units tall; about 2.1 blocks (about 3.4 blocks across the heads).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _regi import dot_at, ellipsoid, glowing, lit, speck
from _route import pal, tone

HEIGHT = 43
SCALE = round(2.1 * 16 / HEIGHT, 3)
HITBOX = [2.2, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a black core sphere under a zigzag silver crown with glowing pink dots and cyan lightning-bolt legs, flanked "
        "by two huge dark dragon heads with gaping jaws of glowing cyan teeth")

BASE = {"silver": (228, 230, 236), "silver_shade": (184, 188, 198), "black": (26, 26, 32), "black_light": (52, 52, 62),
        "navy": (52, 62, 140), "navy_light": (86, 98, 186), "white": (240, 240, 244), "slate": (66, 88, 92),
        "slate_light": (96, 120, 124), "slate_dark": (40, 54, 58), "glow": (40, 214, 232), "glow_light": (160, 246, 252),
        "fleck": (240, 255, 255), "pink": (255, 120, 196)}
SHINY = {"slate": (120, 40, 52), "slate_light": (156, 64, 76), "slate_dark": (80, 24, 34), "glow": (255, 196, 54),
         "glow_light": (255, 232, 150), "fleck": (255, 252, 230), "navy": (92, 40, 120), "navy_light": (130, 70, 170)}

CY = 26.7                                     # the core sphere's centre
DOTS = [(0, 2.8), (-3.4, 1.0), (-1.7, 1.0), (0, 1.0), (1.7, 1.0), (3.4, 1.0), (0, -0.8), (0, -2.6)]


def P(v):
    return pal(BASE, SHINY, v)


GLOW = glowing(P, "glow", light="glow_light")


def cyan(x, y, z, face, p):
    c = p["fleck"] if speck(x, y, z, face) else p["glow"]
    return c, c


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def tri(t):
    """A triangle wave, 0 at whole numbers, 1 at halves."""
    return 1 - abs(2 * (t % 1.0) - 1)


def coref(x, y, z, face, variant, **k):
    """The black core under the silver crown, whose lower edge bites down over the face in zigzag teeth."""
    p = P(variant)
    edge = 29.9 - 2.0 * tri(x / 2.4 + 0.5)
    if y > edge or (face == "up" and y > 28.5):
        return lit(p["silver"], face, y, CY, 8), None
    if face == "north" and dot_at(-x, y - 25.4, DOTS, 0.68):
        return p["pink"], p["pink"]
    return lit(p["black"], face, y, CY, 8), None


def neckf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["black_light"] if (y % 1.4) < 0.45 else p["black"], face), None


def spikef(base_z, lo, hi):
    """Silver, with a glowing cyan band from lo to hi along the rod (rods: z runs from base_z back along it)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        d = base_z - z
        if lo <= d <= hi:
            return cyan(x, y, z, face, p)
        return tone(p["silver"] if face != "down" else p["silver_shade"], face), None
    return s


def snoutf(base, t2):
    """The upper jaw: dark slate, a slanted glowing cyan eye slit near the top of each side. (Shaders get the rod box's
    own unrotated coordinates: z runs back from base z along it, y is centred on base y.)"""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        d, yy = base[2] - z, y - base[1]
        if face in ("east", "west") and 5 < d < 15.5:
            line = t2 / 2 - 1.4 - 0.12 * (d - 5)
            y = yy
            if abs(y - line) < 0.55:
                return cyan(x, y, z, face, p)
        if face == "up":
            return p["slate_light"], None
        return tone(p["slate"], face), None
    return s


def teethf(base, h, up):
    """A strip of glowing cyan zigzag teeth along a jaw (rods: z along the jaw, y across it). up: teeth point up."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("up", "down"):
            return (0, 0, 0, 0)
        d, yy = base[2] - z, y - base[1]
        reach = h * tri(d / 2.8)
        hy = (yy + h / 2) if up else (h / 2 - yy)        # distance from the jaw edge the teeth grow from
        if face in ("east", "west") and hy > reach:
            return (0, 0, 0, 0)
        return cyan(x, y, z, face, p)
    return s


def jawf(base, t2):
    """The lower jaw: dark slate banded with a glowing cyan zigzag; its top (inside the mouth) glows."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        d, yy = base[2] - z, y - base[1]
        if face == "up":
            return cyan(x, y, z, face, p)
        if face in ("east", "west") and abs(yy - (-0.6 + 2.2 * (tri(d / 3.2) - 0.5))) < 0.8:
            return cyan(x, y, z, face, p)
        return tone(p["slate"], face), None
    return s


def plate_zigf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south") and abs(y - (16.0 + 3.0 * (tri(x / 3.0) - 0.5))) < 1.0:
        return cyan(x, y, z, face, p)
    return tone(p["slate"], face), None


def head(m, bone, sx):
    """One of Regidrago's dragon heads, gaping outward (sx = side)."""
    x0, x1 = sorted((sx * 9.0, sx * 20.0))
    m.box(bone, x0, 33, -5, x1, 42, 5, solid("slate"))                                            # the skull
    a, b = (sx * 17.0, 37.5, 0), (sx * 36.0, 34.5, -0.5)
    rod(m, bone, a, b, 9, snoutf(a, 7), extend=0.5, t2=7)                                       # the upper jaw
    ta, tb = (sx * 12.5, 32.2, 0), (sx * 35.5, 29.6, -0.5)
    rod(m, bone, ta, tb, 8, teethf(ta, 4, up=False), extend=0.3, t2=4)                       # upper teeth
    for i, f in enumerate((0.0, 0.28, 0.56, 0.82)):                                                # ridge spikes
        px = a[0] + (b[0] - a[0]) * f
        py = a[1] + (b[1] - a[1]) * f + 3.4 + (1.2 if i == 0 else 0)
        spike(m, bone, (px, py, -0.5), (-sx * 0.5, 1, 0), 3.0 - 0.4 * i, 4.4 - 0.5 * i, solid("slate_dark"), tip=1.2)
    for dz in (-2.8, 2.8):                                                                         # back horns
        spike(m, bone, (sx * 12.0, 41.5, dz), (-sx * 0.6, 1, dz * 0.12), 3.0, 6.0, solid("slate_dark"), tip=1.4)
    jw = m.bone(f"jaw_{'left' if sx < 0 else 'right'}", bone, (sx * 14, 24, 0))
    x0, x1 = sorted((sx * 12.0, sx * 22.5))
    m.box(jw, x0, 11, -4, x1, 22, 4, plate_zigf)                                                    # jaw's deep back
    ja, jb = (sx * 15.0, 20.0, 0), (sx * 33.5, 21.5, -0.5)
    rod(m, jw, ja, jb, 8, jawf(ja, 6), extend=0.5, t2=6)                                         # the lower jaw
    la, lb = (sx * 14.0, 24.6, 0), (sx * 33.0, 26.1, -0.5)
    rod(m, jw, la, lb, 7, teethf(la, 4, up=True), extend=0.3, t2=4)                          # lower teeth


def build() -> Model:
    m = Model("ironduality")
    top = m.bone("ironduality", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ellipsoid(m, bd, 0, CY, 0, 8.0, 8.0, 7.5, coref, step=1)                                       # the core
    m.round_box(bd, 0, 0, 2.2, 2.2, 13.5, 19.5, neckf, cut=1)                                      # ribbed neck
    for sx in (-1, 1):                                                                             # navy side discs
        x0, x1 = sorted((sx * 7.4, sx * 9.6))
        m.box(bd, x0, CY - 3.5, -5.0, x1, CY + 3.5, 5.0, solid("navy"))
        m.box(bd, x0 + 0.05 * sx, CY - 5.0, -3.5, x1 - 0.05 * sx, CY + 5.0, 3.5, solid("navy"))
    # the silver crown: a tall spike banded in cyan and smaller crown points
    for i, (w, y0, y1) in enumerate(((4.0, 33.0, 36.0), (3.0, 35.6, 38.4), (2.0, 38.0, 40.4), (1.0, 40.0, 42.0))):
        rod(m, bd, (0, y0, 0), (0, y1, 0), w, spikef(0, 3.4 - (y0 - 33.0), 4.4 - (y0 - 33.0)), extend=0.2)
    for sx in (-1, 1):
        spike(m, bd, (sx * 3.6, 32.4, -1.0), (sx * 0.5, 1, -0.1), 3.0, 5.6, solid("silver"), tip=1.4)
        spike(m, bd, (sx * 6.6, 30.4, -1.0), (sx * 1, 0.7, -0.1), 2.8, 4.6, solid("silver"), tip=1.2)
        chain(m, bd, [(sx * 4, 33.5, 2.5), (sx * 9, 37, 3.5), (sx * 14, 37, 3.5), (sx * 17.5, 34.5, 3.0)],
              [1.4, 1.4, 1.4], GLOW)                                                               # cyan arcs
    # the white crescent below the neck, with cyan points, and two lightning-bolt legs
    for i in range(9):
        xa, xb = -8.4 + i * 2.1, -8.4 + (i + 1) * 2.1
        ya, yb = 12.4 + 0.045 * xa * xa, 12.4 + 0.045 * xb * xb
        xm, ym = (xa + xb) / 2, (ya + yb) / 2
        ang = math.degrees(math.atan2(yb - ya, xb - xa))
        m.box(bd, xm - 1.4, ym - 1, -2.5, xm + 1.4, ym + 1, 2.5, solid("white"), rotation=(0, 0, ang), pivot=(xm, ym, 0))
    for sx in (-1, 1):
        spike(m, bd, (sx * 8.6, 14.8, 0), (sx * 0.55, -1, 0), 1.8, 3.4, GLOW, tip=0.9)
        spike(m, bd, (sx * 3.4, 11.6, -0.5), (sx * 0.25, -1, 0), 1.4, 2.4, GLOW)
        chain(m, bd, [(sx * 2.2, 11.0, 0), (sx * 4.4, 7.0, 0), (sx * 1.8, 5.8, 0), (sx * 3.8, 0.0, 0)],
              [2.2, 1.8, 1.6], GLOW)                                                               # lightning legs
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        head(m, m.bone(nm, bd, (sx * 9.5, 30, 0)), sx)
    return m
