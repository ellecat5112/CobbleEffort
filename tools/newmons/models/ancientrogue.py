"""Ancient Rogue (Fire/Dragon), the ancient paradox Rayquaza, built from boxes after sub_arashii's art
(@MadZygardeCore; the art's own name).

A primeval Rayquaza: a long sage-grey serpent body outlined in red, coiling in an S, set with glowing green orbs
along its flanks. Plumes of fiery feathers, red at the root, orange and gold at the tips, burst from the back of its
head, its shoulders and the middle of its body. Its head gapes on a pink mouth below a red eye and swept horns, its
little arms end in dark claws, and its tail ends in a red-edged fin.

Shiny: charcoal body with blue-white fire.

Front is -z, y is up. 42 units tall; about 5.5 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, tri
from _regi import ellipsoid
from _route import mix, pal, tone
from _serpent import at, serpent, tangent

HEIGHT = 42
SCALE = round(5.0 * 16 / HEIGHT, 3)
HITBOX = [2.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a primeval sage-grey Rayquaza outlined in red, coiled in an S, with glowing green orbs and plumes of fiery "
        "feathers bursting from its head, shoulders and back")

BASE = {"sage": (150, 160, 140), "sage_dark": (108, 116, 100), "sage_light": (188, 198, 176), "red": (196, 48, 46),
        "flame_red": (236, 70, 50), "flame_orange": (250, 150, 60), "flame_gold": (255, 222, 120), "orb": (160, 230, 90),
        "orb_light": (220, 255, 170), "mouth": (220, 110, 130), "eye": (220, 40, 40), "claw": (50, 50, 56)}
SHINY = {"sage": (70, 72, 80), "sage_dark": (44, 46, 52), "sage_light": (104, 108, 118), "flame_red": (60, 110, 240),
         "flame_orange": (110, 180, 255), "flame_gold": (220, 244, 255), "orb": (90, 210, 255), "orb_light": (200, 244, 255)}
CTRL = [(0, 36.0, -6.0), (5, 30.0, -2.0), (8, 22.0, 4.0), (1, 15.0, 8.0), (-7, 11.0, 4.0), (-10, 6.0, -3.0),
        (-5, 2.4, -9.0), (2, 2.0, -12.0)]


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, box=None, **k):
    """Sage grey with a red line along each side (rods: x and y across the rod, centred on its middle)."""
    p = P(variant)
    cy = box.lo[1] + box.size[1] / 2
    if face in ("east", "west") and abs(y - cy) < max(0.35, box.size[1] * 0.08):
        return p["red"], None
    if face == "up":
        return p["sage_light"], None
    return tone(p["sage"] if face != "down" else p["sage_dark"], face), None


def flamef(x, y, z, face, variant, box=None, **k):
    """A feather of fire: red at its root, orange, then gold at its tip (rods: z runs from the root)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    c = p["flame_red"] if d < 0.35 else (p["flame_orange"] if d < 0.72 else p["flame_gold"])
    return c, c


def plume(m, bone, root, n, spread, up, length, lean=(0.0, 0.0, 1.0)):
    """A burst of flame feathers from root: n feathers fanned over `spread` degrees round an up-and-back direction."""
    for i in range(n):
        a = math.radians(-spread / 2 + spread * i / max(1, n - 1))
        d = (math.sin(a) * 0.9 + lean[0], up + 0.3 * math.cos(a * 2), math.cos(a) * 0.8 + lean[2])
        L = length * (0.75 + 0.25 * tri(i / 2.0 + 0.5))
        nrm = math.sqrt(sum(v * v for v in d))
        u = tuple(v / nrm for v in d)
        mid = tuple(r + q * L * 0.55 for r, q in zip(root, u))
        end = tuple(r + q * L for r, q in zip(root, u))
        rod(m, bone, root, mid, 3.0, flamef, extend=0.4)
        rod(m, bone, mid, end, 2.0, flamef, extend=0.4)


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 9.6, y - 37.8) < 0.6:
        return p["eye"], p["eye"]
    if face in ("east", "west") and abs(y - (37.0 - 0.2 * (z + 8))) < 0.3 and z < -7:
        return p["red"], None
    return tone(p["sage"], face), None


def build() -> Model:
    m = Model("ancientrogue")
    top = m.bone("ancientrogue", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    tl = m.bone("tail", bd, (-7, 11, 4))
    pts = serpent(m, [(0.0, bd), (0.62, tl)], CTRL, 30, 6.2, 2.2, bodyf)       # the coiling body
    for f in (0.2, 0.42, 0.62, 0.8):                                            # glowing green orbs on its flanks
        q = at(pts, f)
        for sx in (-1, 1):
            ellipsoid(m, bd if f < 0.62 else tl, q[0] + sx * 2.6 * (1 - f * 0.4), q[1], q[2], 1.4, 1.4, 1.4,
                      solid("orb", True), step=1)
    end, d = at(pts, 1.0), tangent(pts, 0.97)                                  # red-edged tail fin
    for side in (-1, 1):
        spike(m, tl, end, (d[0] + side * 0.6, d[1] + 0.5, d[2]), 2.0, 4.6, solid("red"), tip=0.8)
    hd = m.bone("head", bd, (0, 36.0, -6.0))
    m.round_box(hd, 0, -8.0, 2.8, 4.2, 35.0, 39.4, headf, cut=1)                 # long head
    m.box(hd, -1.8, 35.4, -14.4, 1.8, 37.8, -11.4, solid("sage"))                # snout
    jw = m.bone("jaw", hd, (0, 35.0, -6.0))
    m.box(jw, -1.6, 33.4, -13.4, 1.6, 34.8, -7.0, solid("sage_dark"), rotation=(18, 0, 0), pivot=(0, 35.0, -6.0))
    m.box(hd, -1.2, 34.6, -12.4, 1.2, 35.4, -7.4, solid("mouth"))
    for sx in (-1, 1):                                                          # swept horns
        rod(m, hd, (sx * 1.6, 39.0, -6.0), (sx * 2.6, 41.6, 0.0), 1.0, solid("sage_dark"), extend=0.3)
        rod(m, hd, (sx * 2.6, 41.6, 0.0), (sx * 3.0, 41.0, 4.0), 0.8, solid("red"), extend=0.3)
    plume(m, hd, (0, 38.6, -4.0), 7, 120, 0.5, 12.0)                             # flame plumes
    neck_q = at(pts, 0.12)
    plume(m, bd, (neck_q[0], neck_q[1] + 2.0, neck_q[2]), 8, 160, 0.5, 15.0)
    mid_q = at(pts, 0.4)
    plume(m, bd, (mid_q[0], mid_q[1] + 2.2, mid_q[2]), 7, 140, 0.6, 13.0, lean=(0.5, 0, 0.6))
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                         # little clawed arms
        q = at(pts, 0.1)
        ar = m.bone(nm, bd, (q[0] + sx * 2.4, q[1] - 1.0, q[2] - 1.0))
        a0 = (q[0] + sx * 2.4, q[1] - 1.0, q[2] - 1.0)
        a1 = (q[0] + sx * 4.6, q[1] - 3.6, q[2] - 3.4)
        rod(m, ar, a0, a1, 1.4, bodyf, extend=0.3)
        for cl in (-0.4, 0.0, 0.4):
            spike(m, ar, a1, (sx * 0.3 + cl, -0.8, -0.6), 0.6, 1.6, solid("claw"))
    return m
