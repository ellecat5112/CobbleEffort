"""Shared parts for CobbleEffort's extra Rotom forms (tools/newmons/rotom.py): Rotom's orange plasma body colours,
its white-rimmed lens eyes, the toothy grin, and the glowing plasma bolts that crackle round every form (the coloured
aura in the reference art). Each form module picks its own aura colour and extra palette keys.

Shiny: Rotom's shiny colours, orange turning pink-red (like the shiny Rotom forms), and the aura's hue turned.
"""
from __future__ import annotations

import math

from _boxmodel import hue_shift, mix
from _route import tone

BASE = {"orange": (238, 114, 46), "orange_light": (252, 164, 96), "orange_dark": (180, 72, 30), "black": (30, 30, 36),
        "charcoal": (58, 58, 66), "grey": (156, 160, 170), "grey_light": (210, 213, 220), "grey_dark": (96, 98, 108),
        "white": (246, 246, 246), "pupil": (24, 24, 30), "iris": (120, 210, 236), "mouth": (40, 18, 22),
        "aura": (110, 220, 255), "aura_light": (220, 250, 255)}
SHINY = {"orange": (232, 70, 96), "orange_light": (250, 126, 150), "orange_dark": (160, 36, 62)}


def palette(extra=None, shiny_extra=None, aura_turn=0.18):
    """-> P(variant): the form's palette (BASE + its own keys); the shiny one turns orange pink-red and the aura's hue."""
    base = {**BASE, **(extra or {})}
    shiny = {**SHINY, **(shiny_extra or {})}
    for k in ("aura", "aura_light"):
        shiny.setdefault(k, hue_shift(base[k], aura_turn)[:3])

    def P(variant):
        return base if variant != "shiny" else {**base, **shiny}
    return P


def solid(P, key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return tone(c, face), (c if glow else None)
    return s


def rotom_eye(dx, dy, r, p, iris="iris"):
    """Rotom's lens eye: a dark outline, a glowing white ring, a coloured iris and a dark pupil with a shine.
    -> (colour, glow) or None."""
    d = math.hypot(dx, dy)
    if d > r:
        return None
    if d > r * 0.9:
        return p["black"], None
    if d > r * 0.6:
        return p["white"], p["white"]
    if math.hypot(dx + r * 0.22, dy - r * 0.22) < r * 0.14:
        return p["white"], p["white"]
    if d > r * 0.3:
        return p[iris], p[iris]
    return p["pupil"], None


def grin(du, dv, w, h, p, teeth=6, gap=0.12):
    """A toothy grin in a w x h rectangle (du right, dv up from its centre): a dark mouth with white triangle teeth
    from the top and bottom lips. -> colour or None (outside)."""
    if abs(du) > w / 2 or abs(dv) > h / 2:
        return None
    u = (du + w / 2) / w * teeth
    f = u - math.floor(u)
    tri = 1 - abs(f - 0.5) * 2                              # 0 at a tooth's edge, 1 at its tip column
    top = (h / 2 - dv) / h                                  # 0 at the top lip
    bot = (dv + h / 2) / h
    if top < 0.62 * tri - gap / 2 or bot < 0.45 * tri - gap / 2:
        return p["white"]
    return p["mouth"]


def bolt_shape(u, v):
    """A zig-zag lightning bolt in the unit square (u right, v up): True inside."""
    pts = [(0.62, 1.0), (0.18, 0.46), (0.48, 0.46), (0.3, 0.0), (0.84, 0.6), (0.52, 0.6), (0.78, 1.0)]
    inside = False
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if (y0 > v) != (y1 > v) and u < x0 + (v - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


def bolt_plane(m, bone, x, y, z, w, h, P, key="aura", plane="xy", rotation=None, flip=False):
    """A glowing plasma bolt on a zero-thickness plane, w wide and h tall, its lower-left corner at (x, y, z); `plane`
    "xy" faces front/back, "zy" faces the sides. Everything outside the bolt is cut out."""
    def s(px, py, pz, face, variant, **k):
        u = ((pz - z) if plane == "zy" else (px - x)) / w
        v = (py - y) / h
        if flip:
            u = 1 - u
        if not (0 <= u <= 1 and 0 <= v <= 1) or not bolt_shape(u, v):
            return (0, 0, 0, 0)
        p = P(variant)
        c = p["aura_light"] if 0.4 < u < 0.62 else p[key]
        return c, c
    if plane == "zy":
        m.box(bone, x, y, z, x, y + h, z + w, s, rotation=rotation, pivot=(x, y, z) if rotation else None)
    else:
        m.box(bone, x, y, z, x + w, y + h, z, s, rotation=rotation, pivot=(x, y, z) if rotation else None)


def wheel(P, hub="orange", tyre="black", tread=True, axis="x", centre=(0, 0, 0), r=4.0):
    """A shader for a wheel box seen side-on (`axis` = the axle): a dark tyre with tread nicks, a coloured hub."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        side = face in (("east", "west") if axis == "x" else ("north", "south"))
        if side:
            a, b = ((z - centre[2], y - centre[1]) if axis == "x" else (x - centre[0], y - centre[1]))
            d = math.hypot(a, b)
            if d < r * 0.42:
                return tone(p[hub], face), None
            if d < r * 0.5:
                return p["charcoal"], None
            return tone(p[tyre], face), None
        if tread and int((y + z + x) * 1.5) % 2 == 0:
            return mix(p[tyre], (0, 0, 0), 0.35), None
        return tone(p[tyre], face), None
    return s


def face_on(P, centre, eyes=(), mouth=None, base="orange", plane="north", iris="iris", spike_y=None):
    """A shader painting Rotom's face on a box: `eyes` = [(dx, dy, r)] from `centre` (cx, cy, cz), `mouth` =
    (dx, dy, w, h, teeth); on the face named `plane` (north = front, -z). Other faces: the base colour."""
    cx, cy, cz = centre

    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == plane:
            u = (x - cx) if plane in ("north", "up", "down") else (z - cz) * (1 if plane == "east" else -1)
            if plane == "south":
                u = cx - x
            v = (y - cy) if plane not in ("up", "down") else (cz - z)
            for ex, ey, r in eyes:
                e = rotom_eye(u - ex, v - ey, r, p, iris)
                if e:
                    return e
            if mouth:
                mx, my, mw, mh, n = mouth
                g = grin(u - mx, v - my, mw, mh, p, n)
                if g:
                    return g, None
        return tone(p[base], face), None
    return s


def ball(m, bone, cx, cy, cz, r, shader, slices=3):
    """A roundish ball of radius r from stacked rounded slices (wide in the middle, narrower above and below)."""
    hs = 2 * r / slices
    for i in range(slices):
        y0 = cy - r + i * hs
        t = (y0 + hs / 2 - cy) / r
        rr = max(1.0, r * math.sqrt(max(0.0, 1 - t * t)) * 1.05)
        m.round_box(bone, cx, cz, rr, rr, y0, y0 + hs, shader, cut=max(0.6, rr * 0.38))


def tyre(m, bone, x0, x1, cy, cz, r, shader):
    """A wheel with a rounded silhouette seen side-on (axle along x): two crossed boxes."""
    c = max(1.0, round(r * 0.3))
    m.box(bone, x0, cy - r + c, cz - r, x1, cy + r - c, cz + r, shader)
    m.box(bone, x0 + 0.05, cy - r, cz - r + c, x1 - 0.05, cy + r, cz + r - c, shader)


def cone(m, bone, base, d, w, h, shader, steps=3):
    """A pointed cone (Rotom's horn) of stacked shrinking rods along d."""
    import math as _m
    n = _m.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    from _boxmodel import rod
    for i in range(steps):
        a = tuple(b + uu * h * i / steps for b, uu in zip(base, u))
        b_ = tuple(b + uu * h * (i + 1) / steps for b, uu in zip(base, u))
        rod(m, bone, a, b_, max(0.6, w * (1 - i / steps)), shader, extend=0.3)


# --- the Pokémon Abyss instrument forms (dark lacquer, pink inlay, an aura in the instrument's colour) ---------------

ABYSS = {"ink": (54, 48, 62), "ink_dark": (32, 28, 38), "ink_light": (86, 78, 96), "pink": (244, 176, 214),
         "pink_dark": (196, 112, 164), "silver": (200, 204, 214), "keywhite": (246, 240, 244)}
ABYSS_SHINY = {"ink": (232, 226, 238), "ink_dark": (176, 168, 186), "ink_light": (250, 248, 252), "pink": (90, 200, 220),
               "pink_dark": (40, 140, 170)}


def abyss_eye(dx, dy, rx, ry, p):
    """The Abyss forms' eye: an aura-coloured rim, a white oval with a dark slot in the middle. -> (colour, glow)."""
    if (dx / rx) ** 2 + (dy / ry) ** 2 > 1:
        return None
    if (dx / rx) ** 2 + (dy / ry) ** 2 > 0.55:
        return p["aura"], p["aura"]
    if abs(dx) < rx * 0.22 and abs(dy) < ry * 0.5:
        return p["ink_dark"], None
    return p["white"], p["white"]


def disc_z(m, bone, cx, cy, z0, z1, r, shader):
    """A round disc facing front (axis z), from z0 to z1: two crossed boxes."""
    c = max(1.0, round(r * 0.3))
    m.box(bone, cx - r, cy - r + c, z0, cx + r, cy + r - c, z1, shader)
    m.box(bone, cx - r + c, cy - r, z0 + 0.05, cx + r - c, cy + r, z1 - 0.05, shader)


def disc_x(m, bone, x0, x1, cy, cz, r, shader):
    """A round disc facing sideways (axis x)."""
    tyre(m, bone, x0, x1, cy, cz, r, shader)


def note_shape(u, v):
    """An eighth note in the unit square: an oval head bottom-left, a stem, a flag."""
    if ((u - 0.32) / 0.3) ** 2 + ((v - 0.18) / 0.17) ** 2 <= 1:
        return True
    if 0.52 <= u <= 0.64 and 0.18 <= v <= 1.0:
        return True
    return 0.64 <= u <= 0.95 and 0.62 + (u - 0.64) * 0.25 <= v <= 1.0 - (u - 0.64) * 0.6 and v >= 0.6


def note_plane(m, bone, x, y, z, w, h, P, key="aura", plane="xy"):
    """A glowing music note on a zero-thickness plane (lower-left corner at x, y, z)."""
    def s(px, py, pz, face, variant, **k):
        u = ((pz - z) if plane == "zy" else (px - x)) / w
        v = (py - y) / h
        if not (0 <= u <= 1 and 0 <= v <= 1) or not note_shape(u, v):
            return (0, 0, 0, 0)
        c = P(variant)[key]
        return c, c
    if plane == "zy":
        m.box(bone, x, y, z, x, y + h, z + w, s)
    else:
        m.box(bone, x, y, z, x + w, y + h, z, s)
