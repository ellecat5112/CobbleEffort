"""Waddical, the Surfer Pokémon (Ice/Water; the user's art, artist not named, name kept), Awkwaddle evolved at level 33:
a tall, sleek navy penguin with a white belly, olive-gold bands on its long flippers and legs, a long hooked beak and its
goggles pushed up on its forehead, a see-through surfboard tucked under one flipper.

Front is -z, y is up. 38 units tall; baseScale 0.75 (1.8 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _penguin import P, lens, penguin, solid
from _route import tone

SCALE = 0.75
HITBOX = [1.3, 2.1]
KIND = "biped"
K = 4
HEIGHT = 38
LOOK = ("a tall sleek navy penguin with a white belly, olive-gold bands on its flippers and legs, a long hooked beak, "
        "goggles pushed up on its forehead and a see-through surfboard under one flipper")


def head_extra(x, y, z, face, p):
    if face == "north":
        for sx in (-1, 1):
            c = lens(p, x - sx * 1.5, y - 35.0, 1.3, eye=False)
            if c is not None:
                return c, None
            if abs(x - sx * 1.6) < 0.6 and abs(y - 32.4) < 0.6:
                return (p["white"] if x * sx > 1.7 else p["eye"]), None   # sharp eyes under the goggles
    if face in ("east", "west", "south") and abs(y - 35.0) < 0.5:
        return tone(p["rim"], face), None
    return None


def banded(at, axis="y"):
    """A navy limb with an olive-gold band at `at`."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
        if abs(t - at) < 0.12 and face not in ("up", "down"):
            return tone(p["band"], face), None
        return tone(p["navy"], face), None
    return s


def boardf(x, y, z, face, variant, box=None, **k):
    """The surfboard: a long see-through oval, its rim and a stripe stronger."""
    p = P(variant)
    cy, cz = box.lo[1] + box.size[1] / 2, box.lo[2] + box.size[2] / 2
    u, v = (z - cz) / (box.size[2] / 2), (y - cy) / (box.size[1] / 2)
    d = (u * u + v ** 4) ** 0.5
    if d > 1:
        return (0, 0, 0, 0), None
    if d > 0.86 or abs(u) < 0.08:
        return p["board_rim"], None
    return p["board"], None


def build() -> Model:
    m = Model("waddical")
    top = m.bone("waddical", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    body = penguin((9, 30), 4.0, 19.5, 10.5, head_extra)
    for y0, y1, rx, rz, cut in ((8.0, 12.2, 5.0, 4.4, 1.8), (12.0, 26.2, 5.8, 5.0, 2.0), (26.0, 30.2, 4.8, 4.3, 1.8),
                                (30.0, 36.4, 3.8, 3.6, 1.4), (36.2, 37.6, 2.8, 2.6, 1.0)):
        m.round_box(bd, 0, 0, rx, rz, y0, y1, body, cut=cut)
    rod(m, bd, (0, 32.6, -3.4), (0, 31.4, -9.0), 1.6, solid("beak"), extend=0.3, t2=1.4)   # a long beak
    rod(m, bd, (0, 31.4, -9.0), (0, 30.4, -9.6), 1.2, solid("navy_light"), extend=0.2)       # hooked tip
    m.box(bd, -1.4, 8.0, 4.0, 1.4, 9.4, 6.4, solid("navy"))                                  # a stubby tail
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                      # long flippers
        a = m.bone(nm, bd, (sx * 5.4, 27.0, 0))
        tip = (sx * 8.8, 15.0, -0.8) if sx > 0 else (sx * 8.0, 17.0, 1.0)
        rod(m, a, (sx * 5.4, 27.0, 0), tip, 3.6, banded(0.72), extend=0.4, t2=1.2)
    arm_r = "arm_right"
    m.box(arm_r, -10.4, 2.0, -4.6, -10.4, 36.0, 5.4, boardf, rotation=(0, 0, 6), pivot=(-10.4, 18, 0))   # the board
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.8, 10.5, 0))
        rod(m, lg, (sx * 2.8, 10.5, 0), (sx * 3.2, 2.0, -0.4), 2.8, banded(0.5), extend=0.4)
        m.box(lg, sx * 3.2 - 2.0, 0, -4.4, sx * 3.2 + 2.0, 1.4, 1.2, solid("feet_dark"))     # big webbed feet
    return m
