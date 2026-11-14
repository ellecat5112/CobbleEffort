"""Arctosaur, the Dino Fossil Pokémon (Ice/Water; the art the user shared, name kept): the Fossilized Dino as it really
was, a plesiosaur with a shark's head: a deep-blue head with a wide toothy jaw and yellow eyes, a long rounded body of
pale icy shell plates on a blue underside, a tall blue dorsal fin, a tail fin, and four paddle flippers with white
tips and pale spots.

Shiny: violet with a frosty white shell.

Front is -z, y is up. 15 units tall; baseScale 1.1 (2.2 m long). Swims.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _purefossil import body_along, eye_at, palette, toned
from _route import tone

BASE = {"blue": (54, 120, 196), "blue_dark": (36, 82, 150), "shell": (190, 206, 232), "shell_dark": (150, 168, 204),
        "white": (250, 250, 250), "tooth": (250, 248, 236), "gum": (190, 70, 90), "eye": (240, 200, 60),
        "pupil": (24, 24, 30), "spot": (200, 230, 250)}
SHINY = {"blue": (130, 90, 200), "blue_dark": (94, 60, 160), "shell": (236, 240, 252), "shell_dark": (204, 210, 236)}
P, solid, ramp = palette(BASE, SHINY)
SCALE = 1.1
HITBOX = [1.6, 0.95]
KIND = "floater"
K = 3
HEIGHT = 15
LOOK = ("a plesiosaur with a shark's head: a deep-blue toothy head, a long body of pale icy shell plates, a tall dorsal "
        "fin and four white-tipped paddle flippers")


def shell(x, y, z, face, variant, **k):
    p = P(variant)
    if y < 6.4 or face == "down":
        return tone(p["blue"], face), None                              # the blue underside
    if abs(((z + 30) * 0.32) % 2 - 1) < 0.12 or abs(x) < 0.2:
        return tone(p["shell_dark"], face), None                        # seams between the shell plates
    return tone(p["shell"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = eye_at(p, z + 11.0, y - 9.6, 0.65)
        if e:
            return e, None
        if abs(y - 7.6) < 0.5 and z < -10.0:
            return (p["tooth"] if int((z + 30) * 1.6) % 2 == 0 else p["gum"]), None   # a toothy grin
    if face == "north" and abs(y - 7.6) < 0.55:
        return (p["tooth"] if int((x + 10) * 1.6) % 2 == 0 else p["gum"]), None
    return tone(p["blue"] if y > 7.4 else p["shell"], face), None


def flipper(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(1e-6, box.size[2]) if box is not None else 0
    if t > 0.75:
        return tone(p["white"], face), None                             # white tips
    if face == "up" and math.sin(z * 2.2) * math.cos(x * 2.0) > 0.6:
        return tone(p["spot"], face), None
    return tone(p["blue"], face), None


def build() -> Model:
    m = Model("arctosaur")
    top = m.bone("arctosaur", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    body_along(m, bd, [(-7, -3, 7.6, 3.4, 3.0), (-3, 4, 8.2, 4.4, 3.8), (4, 8, 7.6, 3.4, 3.0), (8, 11, 7.2, 2.2, 2.0)],
               shell)
    spike(m, bd, (0, 11.6, 3.0), (0, 1, 0.9), 1.4, 4.6, toned(P, "blue_dark"), tip=0.6)   # the dorsal fin
    hd = m.bone("head", bd, (0, 8, -7))
    body_along(m, hd, [(-11.0, -6.4, 8.6, 2.6, 2.4), (-13.0, -11.0, 8.2, 2.0, 1.8)], head)   # the shark head
    tl = m.bone("tail", bd, (0, 7.2, 11))
    rod(m, tl, (0, 7.2, 11.0), (0, 7.6, 14.0), 1.8, toned(P, "blue"))
    for d in ((0, 1, 0.6), (0, -0.7, 0.8)):                                           # the tail fin
        spike(m, tl, (0, 7.6, 14.0), d, 1.2, 3.4, toned(P, "blue_dark"), tip=0.5)
    for lz, nm in ((-3.0, "front"), (5.0, "back")):                                   # four paddle flippers
        for sx, side in ((1, "left"), (-1, "right")):
            fl = m.bone(f"leg_{nm}_{side}", top, (sx * 4.0, 6.6, lz))
            rod(m, fl, (sx * 4.0, 6.6, lz), (sx * 8.4, 4.4, lz + 1.6), 2.4, flipper, t2=1.0)
    return m
