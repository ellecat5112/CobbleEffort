"""Petroil, the Oil Slick Pokémon (Poison/Fire; after @Kai_FakemonsR's art, name kept): CobbleEffortian Slugma grown
into a tar-black slug that hauls a rusty barrel on its back like a shell. Its edges burn with a glowing oil-slick
rainbow, a wavy drippy cap hangs over one fiery eye, it spills a yellow oil puddle wherever it goes, and it is never
without its entourage: a Trubbish rides in the barrel and another trails along behind.

Shiny: blue-black tar on a cyan puddle.

Front is -z, y is up. 19 units tall; baseScale 0.9 (1.1 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _petro import P, angle_t, sheen, solid, trubbish
from _route import tone

SCALE = 0.9
HITBOX = [1.7, 1.2]
KIND = "quadruped"
K = 3
HEIGHT = 19
LOOK = ("a tar-black slug hauling a rusty barrel like a shell, its edges burning with a glowing oil-slick rainbow, "
        "with a Trubbish riding in the barrel and another trailing behind")
HY = 12.5
HX, HZ = -4.6, -4.0                                                  # the head, front left


def tar(x, y, z, face, variant, **k):
    p = P(variant)
    if face not in ("up", "down") and abs(y - 3.0) < 0.6:
        return sheen(p, angle_t(x, z))                                 # the burning rainbow along its sides
    for sx, sy in ((-2.6, 6.0), (2.4, 9.0), (-1.0, 11.0)):
        if face in ("north", "east", "west") and math.hypot(x - sx, y - sy) < 0.6:
            return sheen(p, sx * 0.1 + 0.3)
    return tone(p["tar"] if y > 2.0 else p["tar_dark"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot((x - HX - 1.6) / 1.2, (y - HY - 0.4) / 0.9)
        if d < 1:
            if d < 0.35:
                return p["pupil"], None
            return sheen(p, 0.05 + 0.1 * d)                            # one fiery eye
        if math.hypot(x - HX + 1.8, y - HY + 0.2) < 0.7:
            return p["tar_light"], None
    if y < HY - 1.0 and face != "up":
        return sheen(p, angle_t(x, z, HX, HZ))
    return tone(p["tar"], face), None


def barrel(x, y, z, face, variant, **k):
    p = P(variant)
    if face not in ("up", "down") and any(abs(y - h) < 0.45 for h in (6.0, 10.0, 14.0)):
        return tone(p["hoop"], face), None
    if face in ("east", "west", "south", "north") and abs(((x + z) * 0.9) % 3.0 - 1.5) < 0.12:
        return tone(p["barrel_dark"], face), None                     # staves
    if math.sin(x * 1.3) + math.cos(y * 0.9 + z) > 1.4:
        return tone(p["tar"], face), None                             # tar stains
    return tone(p["barrel"], face), None


def build() -> Model:
    m = Model("petroil")
    top = m.bone("petroil", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, -1.0, 0.0, 8.0, 10.0, 0.0, 1.0, solid("tar_dark"), cut=3.0)          # the tar puddle
    m.round_box(bd, -4.5, -9.0, 3.6, 2.6, 0.0, 0.8, solid("puddle"), cut=1.0)             # a yellow oil spill
    m.round_box(bd, 0, 0.5, 4.6, 8.2, 0.8, 4.4, tar, cut=1.8)                            # the slug's foot
    m.round_box(bd, HX, HZ + 0.6, 2.6, 2.4, 3.6, HY - 2.0, tar, cut=1.0)                 # its neck, front left
    hd = m.bone("head", bd, (HX, HY - 2, HZ))
    for y0, y1, rx, rz in ((HY - 2.0, HY + 0.6, 4.2, 3.6), (HY + 0.6, HY + 2.2, 3.6, 3.2), (HY + 2.2, HY + 3.2, 2.4, 2.2)):
        m.round_box(hd, HX, HZ, rx, rz, y0, y1, head, cut=1.2)                           # its drippy cap
    for a in range(30, 360, 60):
        r = math.radians(a)
        m.round_box(hd, HX + 3.9 * math.sin(r), HZ - 3.2 * math.cos(r), 1.1, 1.1, HY - 1.6, HY + 1.0, head, cut=0.5)
    for dx, dz, ln in ((HX - 3.2, HZ - 1.6, 3.0), (HX + 2.2, HZ - 3.0, 2.2), (HX - 0.8, HZ - 3.4, 1.8)):   # tar drips
        rod(m, hd, (dx, HY - 1.8, dz), (dx, HY - 1.8 - ln, dz), 1.0, solid("tar"), extend=0.2)
    bb = m.bone("barrel", bd, (2.4, 4, 2))
    m.round_box(bb, 2.4, 2.0, 4.6, 4.6, 3.6, 13.6, barrel, cut=1.6)                     # the rusty barrel
    m.round_box(bb, 2.4, 2.0, 4.0, 4.0, 13.4, 14.0, solid("tar"), cut=1.4)               # tar sloshing at its rim
    for dx, dz, ln in ((6.8, 1.0, 5.0), (-1.6, 5.4, 3.2), (3.0, -2.6, 4.0)):             # tar running down its side
        rod(m, bb, (dx, 13.6, dz), (dx, 13.6 - ln, dz), 1.2, solid("tar"), extend=0.2)
    rider = m.bone("rider", bb, (2.4, 13, 2))
    trubbish(m, rider, (2.4, 11.6, 1.6), 1.0)                                            # a Trubbish in the barrel
    follower = m.bone("follower", bd, (6, 0, 10))
    trubbish(m, follower, (6.5, 0.0, 10.5), 0.75)                                         # and one trailing behind
    return m
