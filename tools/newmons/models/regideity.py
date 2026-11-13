"""Regideity, the Colossus Pokémon (Normal), Regigigas evolved, built from boxes after the fakemon art by @trainer_matz
that the user shared (the art's own name), with the user's idea: titanic, its legs each the size of a huge Onix.

Two immense white legs banded in black stride out from a glowing green orb at its hips, each leg rising into a flared
gold cuff. Above the orb a banded white neck climbs to its head, a white dome dotted like Regigigas's face, set in the
foot of a great upright gold ring: two tall gold horns crown the ring, dark spikes line its inner edge and Regigigas's
coloured gems stud its face. Round it turn two concentric halos of light (one inside the ring, one behind it), and six
arms radiate from the ring like the spokes of a wheel, each a banded white forearm ending in a huge gold cup with three
white fingers.

Shiny: rose gold, blue halos and a blue orb.

Front is -z, y is up. 85 units tall to the horn tips; baseScale 4.4 (about 23 m: each leg is about 8 m long).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import pal, tone

SCALE = 4.4
HITBOX = [1.36, 3.64]                 # x baseScale: about 6 blocks wide and 16 tall, so it can still move about
KIND = "biped"
K = 2
HEIGHT = 85
LOOK = ("a titanic colossus: two immense black-banded white legs from a glowing green orb, a great gold ring with two "
        "horns, gems and dark spikes round a dotted white head, two turning halos, and six arms ending in gold cups "
        "with white fingers")

BASE = {"white": (236, 238, 240), "white_shade": (196, 200, 208), "band": (34, 34, 42), "gold": (238, 192, 58),
        "gold_light": (252, 226, 124), "gold_shade": (196, 146, 36), "dark": (28, 28, 34), "halo": (255, 236, 150),
        "halo_core": (255, 250, 220), "orb": (40, 164, 84), "orb_light": (130, 226, 150), "dot": (30, 30, 36)}
SHINY = {"gold": (224, 138, 118), "gold_light": (246, 190, 168), "gold_shade": (170, 92, 80), "halo": (130, 200, 255),
         "halo_core": (220, 240, 255), "orb": (40, 110, 210), "orb_light": (140, 200, 255)}
GEMS = [(230, 56, 56), (176, 80, 206), (250, 226, 70), (60, 190, 92), (60, 200, 206), (192, 198, 206)]

RC = (0, 57, 1)                       # the great ring's centre
RX, RY = 9.5, 14.0                    # its half-width and half-height (to the middle of the band)


def P(v):
    return pal(BASE, SHINY, v)


def whitef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["white"] if face in ("up", "north", "east", "west") else p["white_shade"], face), None


def bandf(x, y, z, face, variant, **k):
    """White banded in black (rods: z runs along the rod, so the bands ring it)."""
    p = P(variant)
    if face not in ("north", "south") and (z % 4.2) < 1.2:
        return tone(p["band"], face), None
    return whitef(x, y, z, face, variant)


def goldf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return p["gold_light"], None
    return tone(p["gold"] if face != "down" else p["gold_shade"], face), None


def darkf(x, y, z, face, variant, **k):
    return tone(P(variant)["dark"], face), None


def halof(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["halo_core"] if face in ("north", "south") else p["halo"]
    return c, c


def orbf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "up") and math.hypot(x + 0.8, y - 35.2) < 1.0:
        return p["orb_light"], p["orb_light"]                              # the shine on the orb
    return p["orb"], p["orb"]


def gemf(i):
    def s(x, y, z, face, variant, **k):
        c = GEMS[i]
        return c, (c if face == "north" else None)
    return s


def headf(x, y, z, face, variant, **k):
    """A white dome dotted like Regigigas's face: six black dots in an arc round a centre dot."""
    p = P(variant)
    if face == "north":
        dots = [(0, 47.2)] + [(2.5 * math.sin(a), 47.2 + 2.3 * math.cos(a)) for a in
                              (math.radians(d) for d in (-120, -72, -24, 24, 72, 120))]
        if any(math.hypot(x - dx, y - dy) < 0.8 for dx, dy in dots):
            return p["dot"], None
    return whitef(x, y, z, face, variant)


def ellipse_ring(m, bone, cx, cy, z0, z1, rx, ry, thick, shader, n):
    """An upright ring in the xy plane: n slabs placed round an ellipse, each turned along its tangent."""
    for i in range(n):
        t = 2 * math.pi * (i + 0.5) / n
        x, y = cx + rx * math.sin(t), cy + ry * math.cos(t)
        t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        seg = math.hypot(rx * (math.sin(t1) - math.sin(t0)), ry * (math.cos(t1) - math.cos(t0)))
        phi = math.degrees(math.atan2(ry * math.sin(t), rx * math.cos(t)))
        w = seg + thick * 0.35
        m.box(bone, x - w / 2, y - thick / 2, z0, x + w / 2, y + thick / 2, z1, shader,
              rotation=(0, 0, phi), pivot=(x, y, (z0 + z1) / 2))


def on_ring(t, grow=0.0):
    """A point on the great ring at angle t (0 = top, clockwise to the right), pushed outward by grow."""
    return (RC[0] + (RX + grow) * math.sin(t), RC[1] + (RY + grow) * math.cos(t))


def arm(m, bone, t):
    """One of the six arms: a black stalk, a banded white forearm and a huge gold cup with three white fingers."""
    bx, by = on_ring(t, 1.4)
    nx, ny = math.sin(t) * RY, math.cos(t) * RX                             # the ring's outward normal
    n = math.hypot(nx, ny)
    u = (nx / n, ny / n, -0.18)
    ul = math.sqrt(sum(c * c for c in u))
    u = tuple(c / ul for c in u)
    at = lambda d, off=(0, 0, 0): (bx + u[0] * d + off[0], by + u[1] * d + off[1], RC[2] + u[2] * d + off[2])
    rod(m, bone, at(-0.5), at(3.4), 1.8, darkf, extend=0.2)                 # stalk
    rod(m, bone, at(3.0), at(8.2), 4.4, bandf, extend=0.2)                  # banded forearm
    rod(m, bone, at(7.6), at(8.6), 5.2, goldf, extend=0)                    # collar
    rod(m, bone, at(8.4), at(11.4), 7.0, goldf, extend=0)                   # the great gold cup
    rod(m, bone, at(11.3), at(11.7), 5.8, darkf, extend=0)                  # the dark palm inside it
    side = (-u[1], u[0], 0)                                                 # across the arm, in the ring's plane
    for off, spread in (((side[0] * 1.7, side[1] * 1.7, 0.6), 1.25), ((-side[0] * 1.7, -side[1] * 1.7, 0.6), 1.25),
                        ((0, 0, -1.8), 1.3)):
        a = at(11.5, off)
        b = at(15.6, tuple(c * spread for c in off))
        rod(m, bone, a, b, 1.5, whitef, extend=0.2)                         # three white fingers
        rod(m, bone, b, at(16.6, tuple(c * spread * 1.15 for c in off)), 1.1, whitef, extend=0.1)


def build() -> Model:
    m = Model("regideity")
    top = m.bone("regideity", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 34, 0))
    m.round_box(bd, 0, -0.5, 2.7, 2.7, 31.6, 36.8, orbf, cut=0.9)          # the green orb at its hips
    for sx in (-1, 1):                                                      # flared gold cuffs on the hip joints
        rod(m, bd, (sx * 1.8, 34.2, -0.3), (sx * 4.6, 32.6, -0.4), 4.4, goldf, extend=0)
        rod(m, bd, (sx * 4.2, 32.8, -0.4), (sx * 6.6, 31.2, -0.5), 7.0, goldf, extend=0)
    rod(m, bd, (0, 36.4, 0.4), (0, 45.5, 0.2), 3.6, bandf, extend=0.3)       # the banded neck
    hd = m.bone("head", bd, (0, 46, -1))
    m.round_box(hd, 0, -1, 4.2, 3.4, 43.6, 51.4, headf, cut=1.5)            # the dotted white dome
    for sx in (-1, 1):                                                      # the gold blade, pointing down
        rod(m, hd, (sx * 4.4, 45.5, -2.4), (sx * 0.4, 37.6, -3.4), 2.4, goldf, extend=0.4, t2=1.4)
    # the great gold ring, two horns, dark spikes on its inner edge and the six gems on its face
    rg = m.bone("cap", bd, RC)
    ellipse_ring(m, rg, RC[0], RC[1], RC[2] - 1.4, RC[2] + 1.4, RX, RY, 3.0, goldf, 28)
    for sx in (-1, 1):
        x0, y0 = on_ring(sx * math.radians(10))
        spike(m, rg, (x0, y0 + 1, RC[2]), (sx * 0.1, 1, 0), 3.4, 13, goldf, tip=1.8)      # tall horns
    for i in range(10):
        t = 2 * math.pi * (i + 0.5) / 10
        if abs(math.cos(t)) > 0.92:
            continue                                                        # none at the top or behind the head
        x0, y0 = on_ring(t, -1.4)
        spike(m, rg, (x0, y0, RC[2]), (-math.sin(t) * RY, -math.cos(t) * RX, 0), 1.1, 2.2, darkf)
    for i, deg in enumerate((-58, -100, -138, 58, 100, 138)):
        x0, y0 = on_ring(math.radians(deg))
        m.box(rg, x0 - 0.7, y0 - 0.9, RC[2] - 1.9, x0 + 0.7, y0 + 0.9, RC[2] - 1.3, gemf(i))
    # two concentric halos of light that keep turning: one inside the ring, one behind it
    hi = m.bone("ring_inner", rg, RC)
    ellipse_ring(m, hi, RC[0], RC[1], RC[2] - 0.3, RC[2] + 0.3, 6.0, 6.0, 0.7, halof, 20)
    for a in range(4):
        th = a * math.pi / 2 + 0.4
        x0, y0 = RC[0] + 6 * math.sin(th), RC[1] + 6 * math.cos(th)
        m.box(hi, x0 - 0.6, y0 - 0.6, RC[2] - 0.6, x0 + 0.6, y0 + 0.6, RC[2] + 0.6, halof)
    ho = m.bone("ring_outer", rg, RC)
    ellipse_ring(m, ho, RC[0], RC[1], RC[2] + 2.4, RC[2] + 3.0, 19.0, 19.0, 0.8, halof, 36)
    for a in range(6):
        th = a * math.pi / 3
        x0, y0 = RC[0] + 19 * math.sin(th), RC[1] + 19 * math.cos(th)
        m.box(ho, x0 - 0.8, y0 - 0.8, RC[2] + 2.0, x0 + 0.8, y0 + 0.8, RC[2] + 3.4, halof)
    # six arms like the spokes of a wheel: the middle pair are its working arms
    for nm, deg in (("arm_upper_right", 40), ("arm_right", 82), ("arm_lower_right", 124),
                    ("arm_upper_left", -40), ("arm_left", -82), ("arm_lower_left", -124)):
        t = math.radians(deg)
        bx, by = on_ring(t, 1.4)
        arm(m, m.bone(nm, rg, (bx, by, RC[2])), t)
    # two immense legs, each as long as a huge Onix
    for nm, sx in (("leg_left", -1), ("leg_right", 1)):
        lg = m.bone(nm, top, (sx * 4.6, 32, 0))
        rod(m, lg, (sx * 4.6, 32.4, -0.4), (sx * 10.2, 18, -1.2), 5.6, bandf, extend=0.6)    # thigh
        m.round_box(lg, sx * 10.2, -1.2, 2.7, 2.7, 16.4, 19.8, whitef, cut=1)               # knee
        rod(m, lg, (sx * 10.2, 18, -1.2), (sx * 11.6, 4.6, -0.4), 5.0, bandf, extend=0.4)    # shin
        rod(m, lg, (sx * 11.6, 5.2, -0.4), (sx * 11.9, 1.4, -0.2), 3.6, whitef, extend=0.2)  # tapering foot
        rod(m, lg, (sx * 11.9, 1.8, -0.2), (sx * 12.0, 0, -0.1), 2.4, darkf, extend=0)      # its dark point
    return m
