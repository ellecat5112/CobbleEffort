"""Hopple, the Den Rabbit Pokémon (Normal), after the Sundor Region's art (#102, name kept): a cute grey bunny with a
big round head, huge ears with pale insides (one cocked to the side), big red eyes, a little fang in its grin, a fluffy
white collar, a pale belly, little arms and long hopping feet. Alone it's timid; with its family it's something else.

Shiny: a sandy-brown bunny with blue eyes.

Front is -z, y is up. 21 units tall; baseScale 0.36 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _den import palette, tone

SHINY = {"fur": (196, 160, 116), "fur_dark": (150, 116, 80), "fur_light": (222, 196, 156), "eye": (70, 130, 220),
         "eye_light": (160, 210, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.36
HITBOX = [0.6, 1.3]
KIND = "biped"
K = 6
HEIGHT = 21
LOOK = "a cute grey bunny with a big round head, huge ears, big red eyes, a fang in its grin and a fluffy white collar"


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.5, y - 10.6
            if dx * dx / 1.1 + dy * dy / 1.4 < 1:
                if (dx + 0.3 * sx) ** 2 + (dy - 0.4) ** 2 < 0.12:
                    return p["white"], None                                   # the highlight
                return (p["eye"] if dx * dx + dy * dy > 0.25 else p["pupil"]), None
        if abs(x) < 0.3 and abs(y - 9.4) < 0.25:
            return p["pupil"], None                                           # little nose
        if abs(y - 8.6 - 0.35 * abs(x)) < 0.2 and abs(x) < 1.0:
            return p["pupil"], None                                           # the grin
        if 0.2 < x < 0.7 and 7.9 < y < 8.5:
            return p["white"], None                                           # its fang
    return tone(p["fur_light"] if face == "up" else p["fur"], face), None


def earf(x, y, z, face, variant, box=None, **k):
    """Grey ears with big pale insides (on the front face, inset from the edges)."""
    p = P(variant)
    if face == "north":
        (x0, y0, _), (w, h, _) = box.lo, box.size
        if x0 + 0.7 < x < x0 + w - 0.7 and y0 + 0.7 < y < y0 + h - 0.6:
            return p["inner"], None
    return tone(p["fur"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.2:
        return p["belly"], None
    return tone(p["fur"], face), None


def build() -> Model:
    m = Model("hopple")
    top = m.bone("hopple", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 1.8, 1.6, 2.4, 6.4, bodyf, cut=0.6)
    for i, (x, y) in enumerate(((-1.6, 6.6), (0.0, 6.4), (1.6, 6.6), (-0.8, 6.0), (0.8, 6.0))):
        m.round_box(bd, x, -0.6, 1.0, 1.4, y - 0.8, y + 0.6, solid("fluff"), cut=0.4)   # the fluffy collar
    hd = m.bone("head", bd, (0, 7, 0))
    m.round_box(hd, 0, 0, 3.4, 3.0, 7.0, 13.4, headf, cut=1.2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.2, 10.0, 0.4), (sx * 1, -0.2, 0.2), 1.2, 1.6, solid("fur"))      # cheek tufts
    er = m.bone("ear_right", hd, (1.4, 13, 0))
    m.box(er, -0.2, 12.6, -0.4, 3.4, 21.6, 0.6, earf, rotation=(0, 0, -12), pivot=(1.4, 13.0, 0))  # a big upright ear
    el = m.bone("ear_left", hd, (-1.6, 12, 0))
    m.box(el, -10.6, 10.4, -0.4, -1.6, 14.0, 0.6, earf, rotation=(0, 0, 18), pivot=(-1.6, 12.0, 0))  # one cocked sideways
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 1.6, 5.6, -0.6))
        rod(m, ar, (sx * 1.6, 5.6, -0.6), (sx * 1.0, 4.2, -2.0), 0.9, solid("fur"), extend=0.2)
        lb = m.bone(f"leg_{side}", top, (sx * 1.0, 2.6, 0))
        rod(m, lb, (sx * 1.0, 2.8, 0.0), (sx * 1.2, 0.6, 0.2), 1.2, solid("fur"), extend=0.3)
        m.box(lb, sx * 1.2 - 0.7, 0.0, -3.6, sx * 1.2 + 0.7, 0.8, 0.8, solid("fur_dark"))       # long feet
        m.box(lb, sx * 1.2 - 0.5, 0.0, -3.62, sx * 1.2 + 0.5, 0.6, -3.62, solid("inner"))
    tl = m.bone("tail", bd, (0, 3, 1.6))
    m.round_box(tl, 0, 1.9, 0.8, 0.6, 2.6, 4.0, solid("fluff"), cut=0.3)
    return m
