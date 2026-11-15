"""Shared parts for the velvet worm line (Squirmlet, Nozzlurm, Onychydra; after the art of the user's friend on
r/fakemon, signed "sno", shared with permission; our names): segmented worms on stubby lobed legs. Red-orange rings
joined by glossy cyan jelly bands, yellow spots along the back, cyan water sacs speckled blue, a blue throat, grey and
black undersides, dark-red toe pads, round orange eye discs.

Shiny: jade-green rings with magenta jelly."""
from __future__ import annotations

import math

from _afake import solid_of
from _boxmodel import spike
from _route import pal, tone

BASE = {"red": (212, 66, 28), "red_dark": (164, 44, 22), "orange": (242, 130, 34), "yellow": (250, 196, 56),
        "jelly": (84, 226, 228), "jelly_light": (214, 252, 250), "jelly_spot": (46, 132, 214), "blue": (44, 96, 206),
        "blue_dark": (30, 66, 156), "grey": (150, 150, 158), "grey_dark": (96, 96, 104), "black": (44, 42, 48),
        "toe": (132, 22, 22), "eye": (250, 184, 40), "eye_red": (214, 44, 30), "pupil": (24, 18, 18),
        "white": (250, 250, 246), "beak": (112, 112, 118), "tongue": (84, 226, 228)}
SHINY = {"red": (44, 170, 110), "red_dark": (28, 124, 80), "orange": (120, 214, 120), "yellow": (250, 240, 140),
         "jelly": (236, 96, 200), "jelly_light": (255, 214, 246), "jelly_spot": (150, 40, 150), "blue": (120, 50, 170),
         "blue_dark": (84, 32, 126), "tongue": (236, 96, 200)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)


def coords(x, y, z, face):
    return {"up": (x, z), "down": (x, z), "north": (x, y), "south": (-x, y), "east": (z, y), "west": (-z, y)}[face]


def _hash(i, j, seed):
    h = math.sin(i * 12.9898 + j * 78.233 + seed) * 43758.5453
    return h - math.floor(h)


def spots(a, b, spacing, size, seed=0.0, density=0.5):
    i, j = math.floor(a / spacing), math.floor(b / spacing)
    h = _hash(i, j, seed)
    if h > density:
        return False
    ca = (i + 0.3 + 0.4 * h) * spacing
    cb = (j + 0.3 + 0.4 * _hash(i, j, seed + 1)) * spacing
    return math.hypot(a - ca, b - cb) < size


def segf(key="red", band=1.1, spotted=True, belly=None, seed=0.0):
    """A body ring (a box running along z): a glossy cyan jelly band at its front end, yellow spots on top, a darker
    (or `belly`-coloured) underside."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        lo, hi = box.lo[2], box.lo[2] + box.size[2]
        if face not in ("north", "south", "down") and box.size[2] > 2.5 and z - lo < band:
            return tone(p["jelly"], face), None
        if face == "down":
            return tone(p[belly] if belly else p[key + "_dark"] if key + "_dark" in p else p[key], face), None
        if spotted and face == "up" and spots(x, z, 2.8, 0.95, seed, 0.6):
            return tone(p["yellow"], face), None
        return tone(p[key], face), None
    return s


def jelly(x, y, z, face, variant, box=None, **k):
    """A glossy cyan water sac speckled blue, with a highlight near its top."""
    p = P(variant)
    a, b = coords(x, y, z, face)
    lo = [box.lo[i] for i in range(3)]
    sz = [max(box.size[i], 1e-6) for i in range(3)]
    u = {"north": (x - lo[0]) / sz[0], "south": (x - lo[0]) / sz[0], "east": (z - lo[2]) / sz[2],
         "west": (z - lo[2]) / sz[2], "up": (x - lo[0]) / sz[0], "down": (x - lo[0]) / sz[0]}[face]
    v = (y - lo[1]) / sz[1] if face not in ("up", "down") else (z - lo[2]) / sz[2]
    if face not in ("down",) and (u - 0.32) ** 2 + (v - 0.74) ** 2 < 0.018:
        return p["jelly_light"], None
    if spots(a, b, 1.9, 0.55, 3.3, 0.4):
        return tone(p["jelly_spot"], face), None
    return tone(p["jelly"], face), None


def toes(m, bone, x, y, z, n=3, w=1.4, spread=1.3, length=1.6, key="toe"):
    """Velvet-worm toe pads: dark-red lobes pointing forward and out round a foot at (x, y, z)."""
    for k in range(n):
        dx = (k - (n - 1) / 2) * spread
        m.box(bone, x + dx - w / 2, y, z - length, x + dx + w / 2, y + w * 0.8, z + 0.4, solid(key))


def eye_disc(p, du, dv, r, iris="eye", slit=False):
    """A round orange eye disc: an iris ring and a dark pupil (or a white slit)."""
    d = math.hypot(du, dv)
    if d > r:
        return None
    if d > r * 0.72:
        return p["orange"]
    if slit:
        return p["white"] if abs(dv) < r * 0.16 and abs(du) < r * 0.45 else p[iris]
    if d < r * 0.38:
        return p["pupil"]
    return p[iris]


def tip_spike(m, bone, base, d, w, h):
    spike(m, bone, base, d, w, h, solid("grey_dark"), tip=max(0.6, w * 0.3))
