"""Darumamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the daruma demon. A great red lacquered daruma egg painted with gold swirls and a gold glyph, a wide
grinning maw full of white fangs with glowing yellow eyes, four golden flames dancing at its sides, and underneath it a
crouching green dragon whose scaly clawed hands grip the egg and whose long tail ends in a violet fin. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, flame_inside, local, scales, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a red lacquered daruma egg with gold swirls, a grinning fanged maw and glowing eyes, golden flames at its sides "
        "and a green dragon with a violet tail fin crouching beneath it")
BASE = {"red": (220, 40, 40), "red_dark": (130, 14, 18), "red_light": (255, 140, 120), "gold": (250, 210, 60),
        "black": (24, 20, 24), "tooth": (250, 250, 246), "eye": (255, 240, 60), "green": (90, 160, 120),
        "green_dark": (40, 90, 60), "green_light": (170, 220, 180), "violet": (160, 90, 200), "claw": (240, 236, 226),
        "flame": (255, 200, 40, 230), "flame_core": (255, 250, 200, 240)}
SHINY = {"red": (40, 60, 70), "red_dark": (14, 20, 26), "red_light": (110, 130, 140), "green": (190, 150, 80),
         "green_dark": (120, 80, 30)}


def P(v):
    return pal(BASE, SHINY, v)


LACQUER = skin(P, "red", dark="red_dark", light="red_light", var=0.02)
SCALE_ = scales(P, "green", "green_dark", size=1.2, light="green_light", rim_mix=0.4)


def eggf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        mx = abs(x)
        if 17.0 < y < 23.0 and mx < 7.0 - (y - 20.0) ** 2 * 0.2:                            # the grinning maw
            ty = 23.0 - abs(((x + 0.7) % 1.4) - 0.7) * 3.0
            by = 17.0 + abs(((x) % 1.4) - 0.7) * 3.0
            if y > ty - 1.4 or y < by + 1.4:
                return tone(p["tooth"], face), None
            return tone(p["black"], face), None
        for sx in (-1, 1):
            if math.hypot((x - sx * 2.6) * 0.8, y - 24.6) < 1.1:
                return p["eye"], p["eye"]
            if abs(y - 26.4 - (abs(x) - 2.6) ** 2 * -0.2) < 0.3 and 1.0 < abs(x) < 4.4 and x * sx > 0:
                return tone(p["gold"], face), None                                          # brows
        if abs(x) < 0.4 and 9.0 < y < 15.0 or abs(y - 12.0) < 0.3 and abs(x) < 1.6:
            return tone(p["gold"], face), None                                              # glyph
    if face in ("east", "west", "up", "south"):
        ang = math.atan2(y - 22.0, x if face != "south" else -x)
        r = math.hypot(x, y - 22.0)
        if abs((r - ang * 1.2) % 4.0 - 2.0) < 0.35:
            return tone(p["gold"], face), None                                              # swirls
    return LACQUER(x, y, z, face, variant, box=box, **k)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
    return c, c[:3]


def build():
    m = Model("darumamon")
    top = m.bone("darumamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 21.0, 0), 11.0, eggf, layers=10, squash=0.9, ry=13.0)              # the daruma egg
    hd = m.bone("head", bd, (0, 32, 0))
    for sx, sy in ((1, 30.0), (-1, 30.0), (1, 14.0), (-1, 14.0)):                       # golden flames
        fb = m.bone("flame_%s_%d" % ("l" if sx > 0 else "r", int(sy)), bd, (sx * 11.0, sy, 0))
        for ang in (0, 90):
            m.box(fb, sx * 11.0 - 3.6, sy, -0.0, sx * 11.0 + 3.6, sy + 9.0, 0.0,
                  cutout(flame_inside(4, sx * 0.2, int(sy)), flamef), rotation=(0, ang, sx * -15),
                  pivot=(sx * 11.0, sy, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # the dragon's gripping hands
        lg = m.bone(nm, top, (sx * 5.0, 8.0, -4.0))
        rod(m, lg, (sx * 8.0, 9.0, 2.0), (sx * 6.0, 5.0, -8.0), 3, SCALE_, extend=0.6)
        m.round_box(lg, sx * 5.0, -9.6, 3.0, 2.4, 3.0, 7.0, SCALE_, cut=1)
        for j in range(4):
            p0 = (sx * 5.0 + (j - 1.5) * 1.4, 5.0, -11.6)
            spike(m, lg, p0, (0, -0.6, -0.4), 1.0, 2.4, solid(P, "claw"), tip=0.25)
        m.round_box(lg, sx * 7.0, 1.0, 3.0, 5.0, 0.0, 6.0, SCALE_, cut=1)                # haunch
    tl = m.bone("tail", bd, (-4, 8, 6))                                                  # long dragon tail
    pts = [(-4.0, 8.0, 6.0), (-12.0, 6.0, 8.0), (-19.0, 7.0, 6.0), (-24.0, 10.0, 2.0), (-26.0, 14.0, -2.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 4 - j), SCALE_, extend=0.6)
    for j in range(5):                                                                   # violet tail fin
        spike(m, tl, pts[-1], (-0.4 + j * 0.2, 1.0, -0.6 + j * 0.3), 1.0, 5.0 + j % 2 * 2, solid(P, "violet"), tip=0.2)
    return m
