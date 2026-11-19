"""Iron Freeze (Ice/Electric), the paradox Regice, built from boxes after @Alex_LR04's art (the art's own name).

A tall faceted crystal column with a pencil-point top, pale ice blue, a black visor shaped like a downward pentagon
showing Regice's cross of dots in glowing yellow, and a little steel latch on its side. The ice ends in a jagged
fringe over a black machine skirt. Huge blocky crystal arms hang from black ball joints, each ending in two glowing
yellow crystal claws (two more short ones under the arm), four glowing crystal spikes fan out behind it like wings,
and it hovers on two crystal foot slabs, each with a steel thruster dome and a glowing crystal point below.

Shiny: violet ice with cyan energy.

Front is -z, y is up. 41 units tall; about 1.8 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _regi import CROSS, dot_at, glowing
from _route import pal, tone

HEIGHT = 41
SCALE = round(1.8 * 16 / HEIGHT, 3)
HITBOX = [1.2, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a faceted ice crystal column with a black visor of glowing yellow dots, huge blocky crystal arms with glowing "
        "claws, glowing crystal wings and hovering crystal feet")

BASE = {"ice": (176, 224, 255), "ice_light": (212, 242, 255), "ice_shade": (140, 196, 242), "ice_line": (104, 156, 214),
        "skirt": (44, 44, 50), "skirt_line": (70, 70, 78), "visor": (26, 26, 30), "steel": (198, 200, 208),
        "steel_dark": (130, 132, 140), "glow": (255, 212, 40), "glow_light": (255, 236, 140), "fleck": (255, 255, 236)}
SHINY = {"ice": (216, 204, 255), "ice_light": (240, 234, 255), "ice_shade": (184, 168, 240), "ice_line": (136, 118, 206),
         "glow": (70, 230, 250), "glow_light": (170, 248, 255), "fleck": (236, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GLOW = glowing(P, "glow", light="glow_light")


def zig(u):
    """The jagged lower edge of the ice: points down to y 12, notches up to 15.6 (period 7 units)."""
    t = (u / 7.0) % 1.0
    return 12 + 3.6 * (1 - abs(2 * t - 1))


def icef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return (0, 0, 0, 0)
    if face in ("north", "south", "east", "west") and y < zig(x if face in ("north", "south") else z + 3.5):
        return (0, 0, 0, 0)                                                  # the jagged fringe over the skirt
    if face == "north":
        dx, dy = -x, y - 30.6
        if abs(x) <= 6.6 and 27.2 - (6.6 - abs(x)) * 0.48 <= y <= 34.6:   # the black pentagon visor
            if dot_at(dx, dy, CROSS, 0.8):
                return p["glow"], p["glow"]
            return p["visor"], None
        if abs(x) < 0.25 and y < 24.0:
            return p["ice_line"], None                                       # the facet ridge down its front
        if abs(x) > 7.4:
            return tone(p["ice_shade"], face), None                          # the bevelled corners
        return tone(p["ice_light"] if x > 0 else p["ice"], face), None
    if face == "up":
        return p["ice_light"], None
    if face == "south":
        return tone(p["ice_shade"], face), None
    return tone(p["ice"] if abs(z) < 3.5 else p["ice_shade"], face), None


def blockf(x, y, z, face, variant, **k):
    """Plain faceted ice (arms, roof, feet)."""
    p = P(variant)
    c = {"up": p["ice_light"], "north": p["ice"], "south": p["ice_shade"], "down": p["ice_shade"]}.get(face, p["ice_shade"])
    return tone(c, face), None


def skirtf(x, y, z, face, variant, **k):
    p = P(variant)
    u = x if face in ("north", "south") else z
    if face in ("north", "south", "east", "west") and abs(abs(u) - 3.4) < 0.22:
        return p["skirt_line"], None                                         # panel seams
    return tone(p["skirt"], face), None


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def build() -> Model:
    m = Model("ironfreeze")
    top = m.bone("ironfreeze", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 0))
    m.round_box(bd, 0, 0, 10.5, 7, 12, 35, icef, cut=3)                      # the crystal column
    m.round_box(bd, 0, 0, 9.5, 5.5, 7, 19, skirtf, cut=2)                    # the black machine skirt
    for (rx, rz, y0, y1, c) in ((9.5, 6, 35, 36, 3), (8, 5, 36, 37, 2), (6.5, 4, 37, 38, 2), (5, 3, 38, 39, 1),
                                (3.5, 2, 39, 40, 1), (2, 1, 40, 41, 0.5)):
        m.round_box(bd, 0, 0, rx, rz, y0, y1, blockf, cut=c)                 # the pencil-point top
    m.box(bd, -7.4, 20, -7.6, -6.6, 24, -7.0, solid("steel"))                # the steel latch on its side
    for sx in (-1, 1):
        m.round_box(bd, sx * 11, 0, 2, 2, 27.5, 31.5, solid("visor"), cut=1)  # black ball joints
        m.round_box(bd, sx * 6.5, -1, 4.5, 5.5, 5, 8, blockf, cut=2)         # crystal foot slabs
        m.round_box(bd, sx * 6.5, -1, 2.5, 2.5, 3, 5, solid("steel"), cut=1)  # thruster domes
        m.round_box(bd, sx * 6.5, -1, 1.5, 1.5, 2, 3, solid("steel_dark"), cut=0.5)
        spike(m, bd, (sx * 6.5, 2.4, -1), (0, -1, 0), 2.0, 2.4, GLOW, tip=1.0)  # glowing points below
    # huge blocky crystal arms with glowing claws
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        arm = m.bone(nm, bd, (sx * 11, 29.5, 0))
        a, b = (sx * 12.0, 29.5, 0), (sx * 22.5, 18.0, -1.0)
        rod(m, arm, a, b, 11, blockf, extend=1.5, t2=8)
        rod(m, arm, a, b, 8, blockf, extend=1.5, t2=11)
        for d, L in (((sx * 0.95, -0.05, -0.1), 10), ((sx * 0.5, -0.9, -0.1), 9)):
            spike(m, arm, (sx * 22.5, 18.5, -1.0), d, 3.8, L, GLOW, tip=2.0)
        for f in (0.3, 0.55):                                                # two short claws under the arm
            px, py = sx * (12.0 + 10.5 * f), 29.5 - 11.5 * f - 4.6
            spike(m, arm, (px, py, -1.0), (sx * 0.3, -1, -0.15), 2.0, 5.0, GLOW, tip=1.0)
    # four glowing crystal spikes fanning out behind it
    for nm, sx in (("wing_left", -1), ("wing_right", 1)):
        w = m.bone(nm, bd, (sx * 4, 30, 6))
        spike(m, w, (sx * 4.5, 31, 6.5), (sx * 0.75, 1, 0.25), 4.4, 14, GLOW, tip=2.4)
        spike(m, w, (sx * 6.0, 27, 6.5), (sx * 1, 0.42, 0.25), 4.0, 12, GLOW, tip=2.2)
    return m
