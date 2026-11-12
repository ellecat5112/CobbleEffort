#!/usr/bin/env python3
"""
The regions after Kanto (CobbleEffort: Kanto 0.3.0): a dimension each for Johto, Hoenn, Sinnoh, Unova, Kalos, Alola,
Galar and Paldea (their own biome mixes and terrain; only that generation's Pokémon spawn, see KantoEvents), and a
landmark for each, generated in the overworld (and any dimension with its biomes) holding the region's portal:

  Johto   a three-storey wooden pagoda with a swaying central pillar; the portal is the bell in its belfry
  Hoenn   a granite cave in a hill, a giant stone Groudon statue inside; the statue is the portal
  Sinnoh  an old haunted manor; the portal is a boarded-up doorway hidden in the basement
  Unova   a white-and-gold castle; the portal is a golden wardrobe engraved with Magearna in the throne room
  Kalos   a Poké Ball factory beside a MASSIVE Poké Ball; the ball is the portal
  Alola   a hilltop observatory; the portal is its telescope
  Galar   a snowy shrine before a giant Dynamax tree, 300 blocks from root tip to crown; a bark block engraved with a
          Poké Ball at the base of the trunk, on the gate side, is the portal
  Paldea  a grand academy; the portal is the PC on the front desk in the entrance hall

The buildings are original designs inspired by those places (not replicas of the games' maps). Everything is written
here: structure templates, worldgen (jigsaw structures, structure sets, biome tags), the dimensions, the portal
blocks' textures/models/loot and names. Run by make_assets.py.
"""
from __future__ import annotations

import io
import json
import math
import zipfile
from pathlib import Path

from PIL import Image

from make_assets import A, D, MOD, RES, Nbt, Template, h, save, write_json

LANG: dict[str, str] = {}
LOOM = Path.home() / ".gradle" / "caches" / "fabric-loom" / "1.21.1" / "minecraft-merged.jar"


# --- building helpers -------------------------------------------------------------------------------------------------
class S(Template):
    """A template with shape helpers. x right, y up, z back; the entrance is at the front (z = 0, facing north)."""

    def inb(self, x, y, z):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]

    def put(self, x, y, z, name, props=None):
        if self.inb(x, y, z):
            if ":" not in name:
                name = "minecraft:" + name
            self.set(x, y, z, name, props)

    def get(self, x, y, z):
        b = self.blocks.get((x, y, z))
        return b[0] if b else None

    def box(self, x0, y0, z0, x1, y1, z1, name, props=None):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.put(x, y, z, name, props)

    def ring(self, x0, y, z0, x1, z1, name, props=None):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    self.put(x, y, z, name, props)

    def walls(self, x0, y0, z0, x1, y1, z1, name, props=None):
        for y in range(y0, y1 + 1):
            self.ring(x0, y, z0, x1, z1, name, props)

    def stair(self, x, y, z, mat, facing, half="bottom"):
        self.put(x, y, z, f"{mat}_stairs", {"facing": facing, "half": half, "shape": "straight", "waterlogged": "false"})

    def slab(self, x, y, z, mat, kind="bottom"):
        self.put(x, y, z, f"{mat}_slab", {"type": kind, "waterlogged": "false"})

    def log(self, x, y, z, name, axis="y"):
        self.put(x, y, z, name, {"axis": axis})

    def leaves(self, x, y, z, name):
        self.put(x, y, z, name, {"distance": "7", "persistent": "true", "waterlogged": "false"})

    def lantern(self, x, y, z, hanging=False, soul=False):
        self.put(x, y, z, "soul_lantern" if soul else "lantern", {"hanging": str(hanging).lower(), "waterlogged": "false"})

    def door(self, x, y, z, name, facing, hinge="left"):
        for half, dy in (("lower", 0), ("upper", 1)):
            self.put(x, y + dy, z, name, {"facing": facing, "half": half, "hinge": hinge, "open": "false", "powered": "false"})

    def fence(self, x, y, z, name):
        self.put(x, y, z, name, {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"})

    def roof_square(self, cx, cz, y, r, mat, solid="planks"):
        """One layer of a pyramid roof: a solid square of radius r-1 and stairs round its edge (high side inward)."""
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                dx, dz = x - cx, z - cz
                if max(abs(dx), abs(dz)) < r:
                    self.put(x, y, z, f"{mat}_{solid}" if solid else mat)
                elif abs(dz) >= abs(dx):
                    self.stair(x, y, z, mat, "south" if dz < 0 else "north")
                else:
                    self.stair(x, y, z, mat, "east" if dx < 0 else "west")

    def nbt(self):
        return Nbt.file(self.data())


def pick(options, *key):
    """A weighted pick, stable per position: options = [(name, weight), ...]."""
    total = sum(w for _, w in options)
    v = h(*key) * total
    for name, w in options:
        v -= w
        if v <= 0:
            return name
    return options[-1][0]


# --- Johto: the pagoda ------------------------------------------------------------------------------------------------
def johto_pagoda():
    """Three storeys of dark wood stepping in, flared eaves with hanging lanterns at each floor, a central pillar running
    up through every floor (a ladder on it), and an open belfry at the top where the bell hangs under a stepped roof."""
    W, H = 25, 36
    c = W // 2
    t = S((W, H, W))
    t.box(0, 0, 0, W - 1, 0, W - 1, "stone_bricks")
    for x in range(W):
        for z in range(W):
            if h(x, z, 1) > 0.8:
                t.put(x, 0, z, "mossy_stone_bricks")
    t.box(2, 1, 2, W - 3, 1, W - 3, "polished_andesite")
    for x in range(c - 2, c + 3):
        t.stair(x, 1, 1, "stone_brick", "south")
    # storeys: (floor y, half-width, wall height)
    storeys = [(2, 8, 5), (8, 7, 5), (14, 6, 5)]
    for fy, r, wh in storeys:
        t.box(c - r, fy, c - r, c + r, fy, c + r, "spruce_planks")
        for y in range(fy + 1, fy + wh + 1):
            for x in range(c - r, c + r + 1):
                for z in range(c - r, c + r + 1):
                    edge = x in (c - r, c + r) or z in (c - r, c + r)
                    corner = x in (c - r, c + r) and z in (c - r, c + r)
                    if corner:
                        t.log(x, y, z, "stripped_dark_oak_log")
                    elif edge:
                        side = x - c if z in (c - r, c + r) else z - c
                        window = y in (fy + 2, fy + 3) and abs(side) % 3 == 1
                        t.put(x, y, z, "white_stained_glass" if window else "dark_oak_planks")
                    else:
                        t.put(x, y, z, "air")
        # eave above this storey: solid square, stairs round it, slabs hanging lower, lanterns under the corners
        ey = fy + wh + 1
        t.roof_square(c, c, ey, r + 2, "dark_oak")
        for x in range(c - r - 3, c + r + 4):
            for z in range(c - r - 3, c + r + 4):
                if max(abs(x - c), abs(z - c)) == r + 3:
                    t.slab(x, ey - 1, z, "dark_oak", "top")
        for sx in (-1, 1):
            for sz in (-1, 1):
                t.lantern(c + sx * (r + 2), ey - 1, c + sz * (r + 2), hanging=True)
                t.fence(c + sx * (r + 3), ey, c + sz * (r + 3), "dark_oak_fence")
        # lanterns and a little furniture inside
        for sx in (-1, 1):
            for sz in (-1, 1):
                t.lantern(c + sx * (r - 1), fy + 1, c + sz * (r - 1))
        t.put(c - r + 1, fy + 1, c + r - 1, "potted_bamboo")
        t.put(c + r - 1, fy + 1, c + r - 1, "potted_bamboo")
    # the front door of the first storey
    r0 = storeys[0][1]
    t.door(c, 3, c - r0, "dark_oak_door", "south")
    for x in range(c - r0 + 1, c + r0):
        t.box(x, 3, c + r0 - 1, x, 4, c + r0 - 1, "bookshelf")
    # the belfry: floor = the top eave (y 20); posts, rails, the bell under the roof
    by = storeys[-1][0] + storeys[-1][2] + 1
    for sx in (-2, 2):
        for sz in (-2, 2):
            for y in range(by + 1, by + 5):
                t.log(c + sx, y, c + sz, "stripped_dark_oak_log")
    for x in range(c - 1, c + 2):
        for z in (c - 2, c + 2):
            if z == c + 2 or x != c:
                t.fence(x, by + 1, z, "dark_oak_fence")
    for z in range(c - 1, c + 2):
        t.fence(c - 2, by + 1, z, "dark_oak_fence")
        t.fence(c + 2, by + 1, z, "dark_oak_fence")
    for x in range(c - 1, c + 2):
        for z in range(c - 1, c + 2):
            for y in range(by + 1, by + 5):
                if t.get(x, y, z) is None:
                    t.put(x, y, z, "air")
    t.put(c, by + 4, c, "dark_oak_planks")                           # the beam
    t.put(c, by + 3, c, f"{MOD}:johto_bell")                          # THE PORTAL
    roof = by + 5
    for i, r in enumerate((5, 4, 3, 2, 1)):
        t.roof_square(c, c, roof + i, r, "dark_oak")
    t.put(c, roof + 5, c, "dark_oak_planks")
    for y in range(roof + 6, roof + 9):
        t.fence(c, y, c, "dark_oak_fence")
    t.put(c, roof + 9, c, "gold_block")
    # the central pillar (it sways in the stories; here it stands) and the ladder on it, through every floor
    for y in range(3, by):
        t.log(c, y, c, "stripped_oak_log")
    for y in range(3, by + 1):
        t.put(c, y, c + 1, "ladder", {"facing": "south", "waterlogged": "false"})
    t.put(c, by, c, "dark_oak_planks")
    return t


# --- Hoenn: the granite cave and the statue ---------------------------------------------------------------------------
def groudon_statue():
    """A Groudon statue as voxels (relative x, y, z; front = -z): built from ellipsoids for the bulky body, the thick
    legs and arms with claws, the head and snout, the plates on its back and shoulders, and a tail curling on the
    ground. Returns (voxels, eyes)."""
    parts = [  # (centre, radii)
        ((0, 8.5, 0.5), (5, 5.5, 4.5)), ((0, 6.5, -1.8), (4, 4, 3)),                     # torso, belly
        ((0, 13.4, -2.4), (3, 2.6, 3.2)), ((0, 12.5, -5.0), (2.3, 1.7, 2.1)),            # head, snout
        ((0, 11.6, -1.0), (3.2, 2.2, 2.6)),                                              # neck
    ]
    for sx in (-1, 1):
        parts += [((sx * 3.3, 4.0, 0.5), (2.4, 3.0, 2.8)), ((sx * 3.5, 1.0, -1.0), (2.3, 1.1, 3.2)),   # thigh, foot
                  ((sx * 5.8, 9.6, -0.5), (1.9, 2.8, 1.9)), ((sx * 6.4, 6.8, -2.5), (1.7, 2.3, 1.7)),  # upper arm, forearm
                  ((sx * 6.5, 4.7, -3.4), (1.4, 1.0, 1.4)),                                           # claw
                  ((sx * 4.2, 13.0, 1.5), (1.3, 1.9, 1.9)), ((sx * 7.6, 10.0, -0.3), (1.0, 1.9, 1.5)),  # plates
                  ((sx * 1.6, 15.4, -2.0), (0.9, 1.0, 1.4))]                                          # brow ridges
    for i, (z, y, r) in enumerate(((5, 5.0, 3.2), (7.4, 3.8, 2.6), (9.4, 2.6, 2.0), (11.0, 1.6, 1.5), (12.2, 1.0, 1.1))):
        parts.append(((0, y, z), (r, r, r * 1.1)))
    parts += [((0, 11.5, 4.3), (1.6, 1.8, 1.4)), ((0, 8.0, 5.0), (1.4, 1.6, 1.3))]          # back plates
    vox = set()
    for x in range(-10, 11):
        for y in range(0, 18):
            for z in range(-9, 15):
                p = (x, y + 0.5, z)
                for c, r in parts:
                    if sum(((p[i] - c[i]) / r[i]) ** 2 for i in range(3)) <= 1:
                        vox.add((x, y, z))
                        break
    for sx in (-1, 1):                                                                   # toe claws
        for dx in (-1, 0, 1):
            vox.add((int(round(sx * 3.5)) + dx, 0, -5))
    eyes = []
    for ex in (-1, 1):
        zs = [z for (x, y, z) in vox if x == ex and y == 14]
        if zs:
            eyes.append((ex, 14, min(zs)))
    return vox, eyes


def hoenn_cave():
    """A hill of granite and stone with grass on top, a tunnel in, and a cavern lit by glowstone and lanterns with
    dripstone hanging from the roof; the statue stands on a granite pedestal facing the entrance."""
    W, H = 47, 27
    c = W // 2
    t = S((W, H, W))
    RO, RI = (22, 25, 22), (18.5, 22, 18.5)
    for x in range(W):
        for z in range(W):
            for y in range(H):
                dx, dy, dz = (x + 0.5 - c - 0.5) / RO[0], y / RO[1], (z + 0.5 - c - 0.5) / RO[2]
                n = (h(x // 3, y // 3, z // 3, 7) - 0.5) * 0.12
                d = math.sqrt(dx * dx + dy * dy + dz * dz) + n
                if d > 1:
                    continue
                di = math.sqrt(((x - c) / RI[0]) ** 2 + (y / RI[1]) ** 2 + ((z - c) / RI[2]) ** 2) + n * 0.5
                if di < 1 and y >= 1:
                    t.put(x, y, z, "air")
                    continue
                above_out = math.sqrt(dx * dx + ((y + 1) / RO[1]) ** 2 + dz * dz) + n > 1
                if above_out and y > 2:
                    t.put(x, y, z, "grass_block")
                elif math.sqrt(dx * dx + ((y + 3) / RO[1]) ** 2 + dz * dz) + n > 1 and y > 2:
                    t.put(x, y, z, "dirt")
                else:
                    t.put(x, y, z, pick([("granite", 5), ("stone", 3), ("andesite", 1), ("tuff", 1), ("polished_granite", 0.4)],
                                        x // 2, y // 2, z // 2, 11))
    # the cavern floor
    for x in range(W):
        for z in range(W):
            if t.get(x, 1, z) == "minecraft:air":
                t.put(x, 0, z, pick([("coarse_dirt", 3), ("granite", 3), ("gravel", 2), ("packed_mud", 1)], x, z, 5))
    # the tunnel
    for z in range(0, c):
        for x in range(c - 2, c + 3):
            for y in range(1, 6):
                if y == 5 and abs(x - c) == 2:
                    continue
                if t.get(x, y, z) is not None:
                    t.put(x, y, z, "air")
            if t.get(x, 0, z) is not None:
                t.put(x, 0, z, "coarse_dirt")
    for z in (3, 9, 15):
        t.lantern(c - 2, 1, z)
        t.lantern(c + 2, 1, z)
    # dripstone and glowstone in the roof
    for x in range(W):
        for z in range(W):
            for y in range(2, H - 1):
                if t.get(x, y, z) == "minecraft:air" and t.get(x, y + 1, z) not in (None, "minecraft:air"):
                    if "statue" in t.get(x, y + 1, z):
                        break
                    v = h(x, y, z, 21)
                    if v > 0.93:
                        t.put(x, y + 1, z, "glowstone")
                    elif v > 0.86 and y > 6:
                        t.put(x, y, z, "pointed_dripstone", {"thickness": "tip", "vertical_direction": "down", "waterlogged": "false"})
                    break
    # the pedestal and the statue (THE PORTAL), facing the entrance
    sz = c + 2
    for x in range(W):
        for z in range(W):
            d = math.hypot(x - c, z - sz)
            if d <= 7.5:
                t.put(x, 1, z, "polished_granite")
                t.put(x, 2, z, "polished_granite" if d <= 6.5 else "air")
            if 7.5 < d <= 8.5 and t.get(x, 1, z) == "minecraft:air":
                t.stair(x, 1, z, "granite", "south" if abs(z - sz) >= abs(x - c) and z < sz else
                        "north" if abs(z - sz) >= abs(x - c) else ("east" if x < c else "west"))
    vox, eyes = groudon_statue()
    for (x, y, z) in vox:
        t.put(c + x, 3 + y, sz + z, f"{MOD}:hoenn_statue_stone")
    for (x, y, z) in eyes:
        t.put(c + x, 3 + y, sz + z, "magma_block")
    for dx in (-5, 5):
        t.lantern(c + dx, 3, sz - 6)
    return t


# --- Sinnoh: the old manor --------------------------------------------------------------------------------------------
def sinnoh_manor():
    """A gloomy two-storey manor (dark oak frame, deepslate footing, grey glass, broken windows and cobwebs) with a porch,
    a dining hall, a grand staircase up, stairs down to a stone basement, and in the basement's back wall a doorway
    boarded shut (the portal). The template starts 6 below ground so the basement is buried."""
    W, H, Dp = 25, 30, 22
    G = 6                                            # ground floor level
    t = S((W, H, Dp))
    z0, z1 = 3, Dp - 1                               # the house
    # buried ground outside the house (so the terrain stays) and the porch
    t.box(0, 0, 0, W - 1, G - 1, z0 - 1, "dirt")
    t.box(0, G, 0, W - 1, G, z0 - 1, "grass_block")
    for x in range(9, 16):
        for z in range(0, z0):
            t.slab(x, G, z, "dark_oak", "top")
    for x in (9, 15):
        for y in range(G + 1, G + 5):
            t.fence(x, y, 0, "dark_oak_fence")
    for x in range(8, 17):
        for z in range(0, z0):
            t.slab(x, G + 5, z, "dark_oak", "bottom")
    # the basement
    for x in range(W):
        for z in range(z0, z1 + 1):
            for y in range(0, G):
                wall = x in (0, W - 1) or z in (z0, z1) or y == 0
                if wall:
                    t.put(x, y, z, pick([("stone_bricks", 4), ("cracked_stone_bricks", 2), ("mossy_stone_bricks", 2), ("cobblestone", 1)], x, y, z, 3))
                else:
                    t.put(x, y, z, "air")
    # floors, walls, windows
    for fy in (G, G + 6):
        t.box(0, fy, z0, W - 1, fy, z1, "dark_oak_planks")
    for y in range(G + 1, G + 12):
        for x in range(W):
            for z in range(z0, z1 + 1):
                edge = x in (0, W - 1) or z in (z0, z1)
                if not edge:
                    if y != G + 6:
                        t.put(x, y, z, "air")
                    continue
                post = (x in (0, W - 1) and z in (z0, z1, z0 + 6, z1 - 6)) or (z in (z0, z1) and x % 6 == 0)
                if post:
                    t.log(x, y, z, "dark_oak_log")
                elif y == G + 6:
                    t.log(x, y, z, "stripped_dark_oak_log", "x" if z in (z0, z1) else "z")
                elif y == G + 1:
                    t.put(x, y, z, "deepslate_bricks")
                else:
                    along = x if z in (z0, z1) else z
                    window = (y - G) % 6 in (2, 3) and along % 3 == 1
                    if window:
                        broken = h(x, y, z, 9) > 0.7
                        t.put(x, y, z, "cobweb" if broken else "gray_stained_glass")
                    else:
                        t.put(x, y, z, "dark_oak_planks")
    # the gabled roof (ridge along x)
    for k in range(0, 11):
        y = G + 12 + k
        za, zb = z0 - 1 + k, z1 + 1 - k
        if za > zb:
            break
        for x in range(-1, W + 1):
            if za == zb:
                t.slab(x, y, za, "deepslate_tile", "bottom")
                continue
            t.stair(x, y, za, "deepslate_tile", "south")
            t.stair(x, y, zb, "deepslate_tile", "north")
            if x in (0, W - 1):
                for z in range(za + 1, zb):
                    t.put(x, y, z, "dark_oak_planks")
    for x in range(1, W - 1):
        for y in range(G + 12, G + 22):
            for z in range(z0 + 1, z1):
                if t.get(x, y, z) is None:
                    t.put(x, y, z, "air")
    for x in range(W):
        for z in range(z0, z1 + 1):
            t.put(x, G + 12, z, "spruce_planks" if 0 < x < W - 1 and z0 < z < z1 else t.get(x, G + 12, z) or "dark_oak_planks")
    # the front door
    t.door(12, G + 1, z0, "dark_oak_door", "north")
    # inside: carpet, dining table and chairs, chandeliers, bookshelves, cobwebs
    for z in range(z0 + 1, z0 + 10):
        t.put(12, G + 1, z, "red_carpet")
    for x in range(15, 21):
        for z in range(z0 + 7, z0 + 10):
            t.slab(x, G + 1, z, "dark_oak", "top")
        t.stair(x, G + 1, z0 + 6, "dark_oak", "north")
        t.stair(x, G + 1, z0 + 10, "dark_oak", "south")
    for (x, z) in ((12, z0 + 5), (17, z0 + 8), (6, z0 + 12)):
        t.put(x, G + 5, z, "chain", {"axis": "y", "waterlogged": "false"})
        t.lantern(x, G + 4, z, hanging=True)
    for z in range(z0 + 13, z1):
        t.box(1, G + 1, z, 1, G + 3, z, "bookshelf")
    for i in range(30):
        x, y, z = 1 + int(h(i, 1) * (W - 2)), G + 1 + int(h(i, 2) * 10), z0 + 1 + int(h(i, 3) * (z1 - z0 - 1))
        if t.get(x, y, z) == "minecraft:air" and t.get(x, y + 1, z) not in (None, "minecraft:air"):
            t.put(x, y, z, "cobweb")
    # the grand staircase up (right side) and the stairs down to the basement (left side)
    for i in range(6):
        for x in (W - 3, W - 2):
            t.stair(x, G + 1 + i, z0 + 3 + i, "dark_oak", "south")
            for y in range(G + 2 + i, G + 5 + i):
                if y != G + 6 or i < 5:
                    t.put(x, y, z0 + 3 + i, "air")
    for i in range(6):
        for x in (1, 2):
            t.stair(x, G - i, z0 + 2 + i, "stone_brick", "north")
            for y in range(G - i + 1, G - i + 4):
                t.put(x, y, z0 + 2 + i, "air")
    for z in range(z0 + 2, z0 + 9):
        t.fence(3, G + 1, z, "dark_oak_fence")
    # the basement: barrels, chains, soul lanterns, cobwebs, and the boarded doorway (THE PORTAL)
    for x in range(4, W - 4, 4):
        t.put(x, 1, z0 + 1, "barrel", {"facing": "up", "open": "false"})
    for (x, z) in ((8, z0 + 9), (16, z0 + 9)):
        t.put(x, G - 1, z, "chain", {"axis": "y", "waterlogged": "false"})
        t.lantern(x, G - 2, z, hanging=True, soul=True)
    for i in range(14):
        x, y, z = 3 + int(h(i, 11) * (W - 6)), 1 + int(h(i, 12) * 4), z0 + 1 + int(h(i, 13) * (z1 - z0 - 2))
        if t.get(x, y, z) == "minecraft:air":
            t.put(x, y, z, "cobweb")
    cx = W // 2
    for y in (1, 2, 3):
        t.log(cx - 1, y, z1, "dark_oak_log")
        t.log(cx + 1, y, z1, "dark_oak_log")
    t.log(cx, 3, z1, "dark_oak_log", "x")
    for half, y in (("lower", 1), ("upper", 2)):
        t.put(cx, y, z1, f"{MOD}:sinnoh_boarded_doorway", {"facing": "north", "half": half})
    return t


# --- Unova: the castle ------------------------------------------------------------------------------------------------
def unova_castle():
    """A white-and-gold castle: a crenellated curtain wall with four round towers under dark spires, a gate, a courtyard
    and a central keep with a spire; inside the keep a pillared throne room down a red carpet, and beside the throne
    against the back wall the golden wardrobe engraved with Magearna (the portal)."""
    W, H = 47, 40
    c = W // 2
    t = S((W, H, W))
    t.box(0, 0, 0, W - 1, 0, W - 1, "grass_block")
    for z in range(0, 16):
        for x in range(c - 2, c + 3):
            t.put(x, 0, z, "smooth_stone")
    wallmat = lambda x, y, z: "quartz_bricks" if h(x, y, z, 4) > 0.25 else "calcite"
    # the curtain wall
    for y in range(1, 11):
        for x in range(1, W - 1):
            for z in range(1, W - 1):
                if x in (1, 2, W - 3, W - 2) or z in (1, 2, W - 3, W - 2):
                    t.put(x, y, z, "gold_block" if y == 10 else wallmat(x, y, z))
    for x in range(1, W - 1):
        for z in range(1, W - 1):
            if (x in (1, W - 2) or z in (1, W - 2)) and (x + z) % 2 == 0:
                t.put(x, 11, z, "quartz_bricks")
    # the gate
    for x in range(c - 2, c + 3):
        for y in range(1, 8):
            if y == 7 and abs(x - c) == 2:
                continue
            for z in (1, 2):
                t.put(x, y, z, "air")
    for sx in (-4, 4):
        for y in range(1, 15):
            for x in (c + sx - 1, c + sx, c + sx + 1):
                for z in (0, 1, 2, 3):
                    t.put(x, y, z, "gold_block" if y in (9, 14) else wallmat(x, y, z))
        t.lantern(c + sx, 15, 1)
    # the corner towers
    for tx, tz in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5)):
        for y in range(1, 20):
            for x in range(tx - 5, tx + 6):
                for z in range(tz - 5, tz + 6):
                    d = math.hypot(x - tx, z - tz)
                    if d <= 4.6:
                        if d > 3.4 or y == 1:
                            window = y % 5 == 3 and d > 3.4 and (abs(x - tx) <= 0 or abs(z - tz) <= 0)
                            t.put(x, y, z, "white_stained_glass" if window else ("gold_block" if y == 19 else wallmat(x, y, z)))
                        else:
                            t.put(x, y, z, "air")
        for k in range(0, 10):
            r = 5.2 - k * 0.55
            for x in range(tx - 6, tx + 7):
                for z in range(tz - 6, tz + 7):
                    d = math.hypot(x - tx, z - tz)
                    if r - 1.2 < d <= r or (k == 9 and d <= r):
                        t.put(x, 20 + k, z, "deepslate_tiles")
        t.put(tx, 30, tz, "gold_block")
        t.put(tx, 31, tz, "lightning_rod", {"facing": "up", "powered": "false", "waterlogged": "false"})
    # the keep
    kx0, kx1, kz0, kz1 = 13, 33, 16, 41
    for y in range(1, 19):
        for x in range(kx0, kx1 + 1):
            for z in range(kz0, kz1 + 1):
                edge = x in (kx0, kx1) or z in (kz0, kz1)
                if edge:
                    along = x if z in (kz0, kz1) else z
                    window = 4 <= y <= 11 and along % 4 == 2
                    t.put(x, y, z, "white_stained_glass" if window else ("gold_block" if y in (12, 18) else wallmat(x, y, z)))
                else:
                    t.put(x, y, z, "air")
    t.box(kx0 + 1, 0, kz0 + 1, kx1 - 1, 0, kz1 - 1, "polished_diorite")
    t.box(kx0, 19, kz0, kx1, 19, kz1, "smooth_quartz")
    for x in range(kx0, kx1 + 1):
        for z in range(kz0, kz1 + 1):
            if (x in (kx0, kx1) or z in (kz0, kz1)) and (x + z) % 2 == 0:
                t.put(x, 20, z, "quartz_bricks")
    for x in range(c - 1, c + 2):
        for y in range(1, 7):
            t.put(x, y, kz0, "air")
    # throne room: carpet, pillars, chandeliers, the throne, the wardrobe
    for z in range(kz0 + 1, kz1 - 3):
        t.put(c, 1, z, "red_carpet")
    for z in range(kz0 + 3, kz1 - 3, 4):
        for x in (kx0 + 4, kx1 - 4):
            for y in range(1, 18):
                t.log(x, y, z, "quartz_pillar")
            t.put(x, 18, z, "gold_block")
    for z in range(kz0 + 5, kz1 - 3, 8):
        t.put(c, 18, z, "chain", {"axis": "y", "waterlogged": "false"})
        t.lantern(c, 17, z, hanging=True)
    tz = kz1 - 4
    t.box(c - 2, 1, tz - 1, c + 2, 1, kz1 - 1, "gold_block")
    t.stair(c, 2, tz, "quartz", "south")
    t.box(c, 2, tz + 1, c, 5, tz + 1, "gold_block")
    t.put(c - 1, 2, tz, "gold_block")
    t.put(c + 1, 2, tz, "gold_block")
    for half, y in (("lower", 2), ("upper", 3)):
        t.put(c + 4, y, kz1 - 1, f"{MOD}:unova_wardrobe", {"facing": "north", "half": half})
    t.put(c + 4, 1, kz1 - 1, "gold_block")
    # the keep's spire
    sx, sz = c, (kz0 + kz1) // 2
    for y in range(20, 31):
        for x in range(sx - 4, sx + 5):
            for z in range(sz - 4, sz + 5):
                d = math.hypot(x - sx, z - sz)
                if 2.4 < d <= 3.6:
                    t.put(x, y, z, "gold_block" if y == 30 else wallmat(x, y, z))
    for k in range(0, 8):
        r = 4.2 - k * 0.55
        for x in range(sx - 5, sx + 6):
            for z in range(sz - 5, sz + 6):
                d = math.hypot(x - sx, z - sz)
                if r - 1.2 < d <= r or (k == 7 and d <= r):
                    t.put(x, 31 + k, z, "deepslate_tiles")
    t.put(sx, 39, sz, "gold_block")
    return t


# --- Kalos: the ball factory and the giant Poké Ball -----------------------------------------------------------------
def kalos_factory():
    """A white factory hall (grey footing, blue glass bands, a skylight, two brick smokestacks with red bands, conveyor
    lines and machines inside) and beside it on a stone plinth a MASSIVE Poké Ball, 25 blocks across, its button facing
    the front: every block of its shell is the portal."""
    W, H, Dp = 66, 30, 36
    t = S((W, H, Dp))
    t.box(0, 0, 0, W - 1, 0, Dp - 1, "grass_block")
    fx0, fx1, fz0, fz1 = 1, 34, 6, 30
    t.box(fx0, 0, fz0, fx1, 0, fz1, "smooth_stone")
    for y in range(1, 13):
        for x in range(fx0, fx1 + 1):
            for z in range(fz0, fz1 + 1):
                edge = x in (fx0, fx1) or z in (fz0, fz1)
                if not edge:
                    t.put(x, y, z, "air")
                    continue
                along = x if z in (fz0, fz1) else z
                if y <= 2:
                    t.put(x, y, z, "light_gray_concrete")
                elif 6 <= y <= 8 and along % 5 != 0:
                    t.put(x, y, z, "light_blue_stained_glass")
                elif along % 5 == 0:
                    t.put(x, y, z, "iron_block")
                else:
                    t.put(x, y, z, "white_concrete")
    for x in range(fx0, fx1 + 1):
        for z in range(fz0, fz1 + 1):
            t.put(x, 13, z, "glass" if 15 <= z <= 21 and fx0 < x < fx1 else "light_gray_concrete")
    # loading bay door, a sign band of red and white over it
    for x in range(15, 21):
        for y in range(1, 6):
            t.put(x, y, fz0, "air")
    for x in range(13, 23):
        t.put(x, 10, fz0, "red_concrete" if x < 18 else "white_concrete")
    t.put(18, 10, fz0, "black_concrete")
    # smokestacks
    for sx in (6, 12):
        for y in range(14, 29):
            for x in range(sx - 3, sx + 4):
                for z in range(23, 30):
                    d = math.hypot(x - sx, z - 26)
                    if 1.2 < d <= 2.4:
                        t.put(x, y, z, "red_concrete" if y in (24, 25) else "bricks")
                    elif d <= 1.2:
                        t.put(x, y, z, "air")
    # inside: conveyors and machines
    for z in (11, 17, 23):
        for x in range(4, 31):
            t.slab(x, 1, z, "smooth_stone")
        t.put(3, 1, z, "blast_furnace", {"facing": "east", "lit": "true"})
        t.put(31, 1, z, "piston", {"facing": "west", "extended": "false"})
        for x in range(6, 30, 6):
            t.put(x, 2, z, "observer", {"facing": "down", "powered": "false"})
            t.put(x, 3, z, "iron_block")
    for x in range(5, 31, 8):
        t.put(x, 12, 14, "sea_lantern")
        t.put(x, 12, 22, "sea_lantern")
    # the giant Poké Ball (THE PORTAL)
    R, cx, cy, cz = 12.5, 50, 13, 18
    for x in range(int(cx - R - 1), int(cx + R + 2)):
        for z in range(int(cz - R - 2), int(cz + R + 2)):
            if math.hypot(x - cx, z - cz) <= 6.5:
                t.put(x, 0, z, "polished_andesite")
                t.put(x, 1, z, "polished_andesite" if math.hypot(x - cx, z - cz) <= 5.5 else "air")
    for x in range(int(cx - R - 1), int(cx + R + 2)):
        for y in range(1, int(cy + R + 2)):
            for z in range(int(cz - R - 2), int(cz + R + 2)):
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
                if not (R - 1.7 < d <= R):
                    continue
                part = "red" if y > cy + 1 else "white" if y < cy - 1 else "black"
                ring = math.hypot(x - cx, y - cy)
                if z < cz and ring <= 4.6:
                    part = "black" if ring > 3.0 else "button"
                t.put(x, y, z, f"{MOD}:kalos_ball_shell", {"part": part})
    for x in range(cx - 2, cx + 3):                                   # the button stands out
        for y in range(cy - 2, cy + 3):
            if math.hypot(x - cx, y - cy) <= 2.6:
                t.put(x, y, int(cz - R) - 1, f"{MOD}:kalos_ball_shell", {"part": "button"})
    for z in range(0, 6):                                             # paths
        for x in range(16, 20):
            t.put(x, 0, z, "smooth_stone")
    for x in range(36, 46):
        for z in range(2, 6):
            t.put(x, 0, z, "smooth_stone")
    return t


# --- Alola: the observatory -------------------------------------------------------------------------------------------
def alola_observatory():
    """On a round stone platform: a white observatory with a domed roof (panelled white and light grey), its shutter
    slit open to the sky, and inside on an iron mount a long telescope pointing out through the slit: every block of the
    telescope is the portal. A little solar array stands behind it."""
    W, H = 35, 32
    c = W // 2
    t = S((W, H, W))
    for x in range(W):
        for z in range(W):
            d = math.hypot(x - c, z - c)
            if d <= 17:
                t.put(x, 0, z, pick([("stone", 3), ("andesite", 2), ("cobblestone", 1)], x, z, 2))
            if d <= 15:
                t.put(x, 1, z, "polished_andesite" if (x + z) % 2 else "smooth_stone")
            if 14 < d <= 15:
                t.fence(x, 2, z, "spruce_fence")
    for x in range(c - 1, c + 2):
        for z in range(0, 3):
            t.stair(x, 1, z, "stone_brick", "south")
            t.put(x, 2, z, "air")
    # the round building and its dome
    for y in range(2, 10):
        for x in range(W):
            for z in range(W):
                d = math.hypot(x - c, z - c)
                if 7.6 < d <= 8.8:
                    t.put(x, y, z, "light_gray_concrete" if y in (2, 9) else "white_concrete")
                elif d <= 7.6:
                    t.put(x, y, z, "air")
    for y in range(2, 5):
        for x in range(c - 1, c + 2):
            for z in range(c - 9, c - 7):
                t.put(x, y, z, "air")
    for x in range(W):
        for y in range(10, 21):
            for z in range(W):
                d = math.sqrt((x - c) ** 2 + (y - 10) ** 2 + (z - c) ** 2)
                if d <= 9.6:
                    slit = abs(x - c) <= 1 and z <= c + 1
                    if d > 8.4 and not slit:
                        ang = math.atan2(z - c, x - c)
                        t.put(x, y, z, "white_concrete" if int((ang + math.pi) / (math.pi / 6)) % 2 else "light_gray_concrete")
                    else:
                        t.put(x, y, z, "air")
    # the telescope (THE PORTAL) on its mount, aimed up through the slit
    for y in range(2, 6):
        t.put(c, y, c + 1, "iron_block")
    ang = math.radians(48)
    dx, dy, dz = 0.0, math.sin(ang), -math.cos(ang)
    base = (c + 0.5, 6.5, c + 1.5)
    for i in range(-30, 140):
        s_ = i / 10.0
        px, py, pz = base[0] + dx * s_, base[1] + dy * s_, base[2] + dz * s_
        r = 1.6 if s_ > 1 else 1.1
        for x in range(int(px - 2), int(px + 3)):
            for y in range(int(py - 2), int(py + 3)):
                for z in range(int(pz - 2), int(pz + 3)):
                    # distance from the tube's axis
                    vx, vy, vz = x + 0.5 - base[0], y + 0.5 - base[1], z + 0.5 - base[2]
                    along = vx * dx + vy * dy + vz * dz
                    ox, oy, oz = vx - along * dx, vy - along * dy, vz - along * dz
                    if math.sqrt(ox * ox + oy * oy + oz * oz) <= r and -3 <= along <= 14:
                        t.put(x, y, z, f"{MOD}:alola_telescope")
    # inside: a desk, lanterns; outside: a little solar array
    for x in range(c - 5, c - 2):
        t.slab(x, 2, c + 5, "spruce", "top")
    t.lantern(c + 5, 2, c + 4)
    t.lantern(c - 5, 2, c - 4)
    for x in range(c - 6, c + 7):
        for z in range(c + 11, c + 14):
            t.put(x, 2, z, "daylight_detector", {"inverted": "false", "power": "0"})
    return t


# --- Galar: the giant tree and the shrine -----------------------------------------------------------------------------
GALAR_GROUND = 60                    # template layer at ground level (the structure starts 60 below the surface)


def galar_tree():
    """A giant Dynamax tree: roots reaching 60 blocks down, a flared trunk tapering up to a huge crown (300 blocks from
    root tip to crown top), big branches with leaf clusters glowing with red Dynamax light. In front of it, a snowy
    shrine: a path, a gate, stone lanterns and a little pavilion. At the base of the trunk, on the gate side, one bark
    block engraved with a Poké Ball is the portal."""
    W, H, Dp = 125, 300, 150
    G = GALAR_GROUND
    t = S((W, H, Dp))
    cx, cz = 62, 88

    def centre(y):
        return cx + 2.5 * math.sin(y / 37.0), cz + 2.0 * math.sin(y / 53.0 + 1.0)

    wood = lambda x, y, z: "mangrove_log" if h(int(math.atan2(z - cz, x - cx) * 4), y // 23, 3) > 0.82 else "dark_oak_log"
    # the trunk
    top = G + 195
    for y in range(G - 12, top + 1):
        tt = max(0.0, (y - G) / (top - G))
        r = 11.5 - 6.5 * tt + 6.0 * math.exp(-max(0, y - G) / 6.0)
        ccx, ccz = centre(y)
        for x in range(int(ccx - r - 1), int(ccx + r + 2)):
            for z in range(int(ccz - r - 1), int(ccz + r + 2)):
                if math.hypot(x + 0.5 - ccx, z + 0.5 - ccz) <= r:
                    t.log(x, y, z, wood(x, y, z))
    # roots: down and out, never across the gate side
    for i in range(11):
        a = math.radians(-60 + i * 330 / 11 + 15 * h(i, 1))
        if abs(((math.degrees(a) - 270) + 180) % 360 - 180) < 35:     # keep the front (-z) clear
            a += math.radians(45)
        steps = 90
        for k in range(steps):
            s_ = k / steps
            R = 8 + 34 * s_
            depth = -3 + 62 * s_ ** 1.6 - 5 * math.sin(math.pi * min(1, s_ * 3)) * (s_ < 0.34)
            px, pz, py = cx + math.cos(a) * R, cz + math.sin(a) * R, G - depth
            r = 4.6 * (1 - s_) + 0.9
            for x in range(int(px - r), int(px + r + 1)):
                for y in range(int(py - r), int(py + r + 1)):
                    for z in range(int(pz - r), int(pz + r + 1)):
                        if (x + 0.5 - px) ** 2 + (y + 0.5 - py) ** 2 + (z + 0.5 - pz) ** 2 <= r * r and y >= 0:
                            t.put(x, y, z, "dark_oak_wood", {"axis": "y"})

    def cluster(px, py, pz, rx, ry, rz, seed):
        for x in range(int(px - rx), int(px + rx + 1)):
            for y in range(int(py - ry), int(py + ry + 1)):
                for z in range(int(pz - rz), int(pz + rz + 1)):
                    d = math.sqrt(((x - px) / rx) ** 2 + ((y - py) / ry) ** 2 + ((z - pz) / rz) ** 2)
                    lump = 0.16 * (h(x // 3, y // 3, z // 3, seed) - 0.5)
                    if 0.72 < d + lump <= 1.0 and t.get(x, y, z) is None:
                        v = h(x, y, z, seed + 1)
                        if v > 0.975:
                            t.put(x, y, z, "shroomlight")
                        elif v > 0.92:
                            t.put(x, y, z, "nether_wart_block")
                        else:
                            t.leaves(x, y, z, "cherry_leaves" if h(x // 4, y // 4, z // 4, seed + 2) > 0.7 else "mangrove_leaves")
    # branches with leaf clusters
    for i in range(22):
        a = math.radians(i * 137.5 + 20)
        by = G + 70 + i * 6
        L = 42 - i * 0.9
        dirx, diry, dirz = math.cos(a) * 0.82, 0.55, math.sin(a) * 0.82
        bx, bz = centre(by)
        end = None
        for k in range(int(L * 2)):
            s_ = k / (L * 2)
            px, py, pz = bx + dirx * L * s_, by + diry * L * s_ + 4 * s_ * s_, bz + dirz * L * s_
            r = 3.6 * (1 - s_) + 1.2
            for x in range(int(px - r), int(px + r + 1)):
                for y in range(int(py - r), int(py + r + 1)):
                    for z in range(int(pz - r), int(pz + r + 1)):
                        if (x + 0.5 - px) ** 2 + (y + 0.5 - py) ** 2 + (z + 0.5 - pz) ** 2 <= r * r:
                            t.put(x, y, z, "dark_oak_wood", {"axis": "y"})
            end = (px, py, pz)
        cluster(end[0], end[1] + 3, end[2], 14, 9, 14, 40 + i)
    # the crown: to the top of the template (300 blocks from the deepest root)
    tx, tz = centre(top)
    cluster(tx, H - 26, tz, 36, 25.5, 36, 99)
    cluster(tx, H - 50, tz, 28, 12, 28, 98)
    # the engraved bark (THE PORTAL): the trunk's front-most block on the centre line, at the base
    bx, bz = centre(G + 1)
    x = int(round(bx - 0.5))
    zs = [z for z in range(Dp) if t.get(x, G + 1, z) and "dark_oak" in t.get(x, G + 1, z)]
    front = min(zs)
    t.put(x, G + 1, front, f"{MOD}:galar_engraved_bark", {"facing": "north"})
    # the shrine in front: path, gate, lanterns, pavilion; snow on the ground
    for z in range(0, front):
        for xx in range(x - 1, x + 2):
            t.put(xx, G, z, "polished_andesite" if (xx + z) % 3 else "stone_bricks")
            for y in range(G + 1, G + 4):
                if t.get(xx, y, z) is None:
                    t.put(xx, y, z, "air")
    gz = 12
    for sx in (-4, 4):
        for y in range(G + 1, G + 9):
            t.log(x + sx, y, gz, "dark_oak_log")
        for y in range(G - 5, G + 1):
            t.put(x + sx, y, gz, "stone_bricks")
    for xx in range(x - 5, x + 6):
        t.log(xx, G + 7, gz, "dark_oak_log", "x")
    for xx in range(x - 6, x + 7):
        t.put(xx, G + 9, gz, "dark_oak_planks")
    t.stair(x - 7, G + 9, gz, "dark_oak", "east", "top")
    t.stair(x + 7, G + 9, gz, "dark_oak", "west", "top")
    for xx in range(x - 6, x + 7):
        t.put(xx, G + 10, gz, "snow", {"layers": "2"})
    for z in (20, 28, 36):
        for sx in (-3, 3):
            t.put(x + sx, G + 1, z, "stone_brick_wall", {"east": "none", "west": "none", "north": "none", "south": "none",
                                                         "up": "true", "waterlogged": "false"})
            t.lantern(x + sx, G + 2, z)
    px0, pz0 = x + 8, 18
    for xx in range(px0, px0 + 7):
        for z in range(pz0, pz0 + 7):
            for y in range(G - 4, G + 1):
                t.put(xx, y, z, "stone_bricks")
            t.put(xx, G + 1, z, "spruce_planks")
    for (xx, z) in ((px0, pz0), (px0 + 6, pz0), (px0, pz0 + 6), (px0 + 6, pz0 + 6)):
        for y in range(G + 2, G + 6):
            t.log(xx, y, z, "dark_oak_log")
    for k, r in enumerate((4, 3, 2, 1)):
        t.roof_square(px0 + 3, pz0 + 3, G + 6 + k, r, "dark_oak")
    t.put(px0 + 3, G + 2, pz0 + 3, "lectern", {"facing": "north", "has_book": "false", "powered": "false"})
    return t


# --- Paldea: the academy ----------------------------------------------------------------------------------------------
def paldea_academy():
    """A grand academy on a stone terrace up a wide flight of steps: a long three-storey hall (cream walls, orange
    pilasters, blue windows, an orange hipped roof) with a clock tower over the entrance; in the entrance hall a front
    desk with the academy PC on it (the portal), facing the doors."""
    W, H, Dp = 53, 48, 47
    c = W // 2
    t = S((W, H, Dp))
    T = 6                                                            # terrace level
    t.box(0, 0, 9, W - 1, T - 1, Dp - 1, "stone_bricks")
    t.box(0, T, 9, W - 1, T, Dp - 1, "smooth_stone")
    for x in range(0, W):
        for z in range(9, Dp):
            if (x // 3 + z // 3) % 2 == 0:
                t.put(x, T, z, "polished_andesite")
    for i in range(9):                                              # the steps (one up per block, 15 wide)
        y = min(T, i + 1) if i < 6 else T
        for x in range(c - 7, c + 8):
            if i < 6:
                t.box(x, 0, i, x, y - 1, i, "stone_bricks")
                t.stair(x, y, i, "stone_brick", "south")
            else:
                t.box(x, 0, i, x, T - 1, i, "stone_bricks")
                t.put(x, T, i, "smooth_stone")
    bx0, bx1, bz0, bz1 = 5, W - 6, 16, Dp - 6
    top = T + 16
    for y in range(T + 1, top):
        for x in range(bx0, bx1 + 1):
            for z in range(bz0, bz1 + 1):
                edge = x in (bx0, bx1) or z in (bz0, bz1)
                if not edge:
                    floor = y in (T + 6, T + 11)
                    atrium = c - 8 <= x <= c + 8 and z <= bz0 + 10
                    t.put(x, y, z, "smooth_quartz" if floor and not atrium else "air")
                    continue
                along = x if z in (bz0, bz1) else z
                if along % 4 == 0:
                    t.put(x, y, z, "orange_terracotta")
                elif (y - T) % 5 in (2, 3):
                    t.put(x, y, z, "light_blue_stained_glass")
                else:
                    t.put(x, y, z, "white_concrete" if (y - T) % 5 else "smooth_sandstone")
    for k in range(0, 14):                                           # the hipped roof
        x0, x1, z0, z1 = bx0 - 1 + k, bx1 + 1 - k, bz0 - 1 + k, bz1 + 1 - k
        if x0 > x1 or z0 > z1:
            break
        y = top + k
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    if z == z0 and x0 < x < x1:
                        t.stair(x, y, z, "red_sandstone", "south")
                    elif z == z1 and x0 < x < x1:
                        t.stair(x, y, z, "red_sandstone", "north")
                    elif x == x0:
                        t.stair(x, y, z, "red_sandstone", "east")
                    else:
                        t.stair(x, y, z, "red_sandstone", "west")
                elif k == 0 or z0 + 1 == z1 or x0 + 1 == x1:
                    t.put(x, y, z, "cut_red_sandstone")
    # the clock tower over the entrance
    tx0, tx1, tz0, tz1 = c - 4, c + 4, 11, 19
    for y in range(T + 1, T + 33):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                edge = x in (tx0, tx1) or z in (tz0, tz1)
                if edge:
                    t.put(x, y, z, "orange_terracotta" if x in (tx0, tx1) and z in (tz0, tz1) else "white_concrete")
                elif y > top:
                    t.put(x, y, z, "air")
    cy = T + 26
    for x in range(tx0 + 1, tx1):
        for y in range(cy - 3, cy + 4):
            d = math.hypot(x - c, y - cy)
            if d <= 3.6:
                t.put(x, y, tz0, "black_concrete" if d > 2.6 else "white_concrete")
    for y in range(cy, cy + 3):
        t.put(c, y, tz0, "gold_block")
    for x in range(c, c + 2):
        t.put(x, cy, tz0, "gold_block")
    for k, r in enumerate((5, 4, 3, 2, 1)):
        t.roof_square(c, (tz0 + tz1) // 2, T + 33 + k, r, "red_sandstone", solid="")
        for x in range(c - r + 1, c + r):
            for z in range((tz0 + tz1) // 2 - r + 1, (tz0 + tz1) // 2 + r):
                t.put(x, T + 33 + k, z, "cut_red_sandstone")
    t.put(c, T + 38, (tz0 + tz1) // 2, "gold_block")
    t.put(c, T + 39, (tz0 + tz1) // 2, "lightning_rod", {"facing": "up", "powered": "false", "waterlogged": "false"})
    # the entrance and the hall
    for x in range(c - 2, c + 3):
        for y in range(T + 1, T + 6):
            if y == T + 5 and abs(x - c) == 2:
                continue
            t.put(x, y, tz0, "air")
    for z in range(tz0 + 1, bz0 + 1):
        for x in range(tx0 + 1, tx1):
            for y in range(T + 1, T + 6):
                t.put(x, y, z, "air")
    for x in range(c - 2, c + 3):
        for y in range(T + 1, T + 6):
            t.put(x, y, bz0, "air")
    for z in range(tz0 + 1, bz0 + 6):
        t.put(c, T + 1, z, "orange_carpet")
    for z in range(bz0 + 3, bz0 + 10, 3):
        for x in (c - 7, c + 7):
            for y in range(T + 1, T + 11):
                t.log(x, y, z, "quartz_pillar")
    for (x, z) in ((c - 4, bz0 + 4), (c + 4, bz0 + 4), (c, bz0 + 9)):
        t.put(x, T + 15, z, "chain", {"axis": "y", "waterlogged": "false"})
        t.lantern(x, T + 14, z, hanging=True)
    dz = bz0 + 6
    for x in range(c - 3, c + 4):
        t.put(x, T + 1, dz, "quartz_block")
    t.put(c - 3, T + 1, dz - 1, "quartz_block")
    t.put(c + 3, T + 1, dz - 1, "quartz_block")
    t.put(c, T + 2, dz, f"{MOD}:paldea_pc", {"facing": "north"})            # THE PORTAL
    t.stair(c, T + 1, dz + 1, "quartz", "south")
    t.put(c + 2, T + 2, dz, "potted_azure_bluet")
    t.put(c - 2, T + 2, dz, "lantern", {"hanging": "false", "waterlogged": "false"})
    return t


# --- Hisui: the great mountain ---------------------------------------------------------------------------------------
def arceus_statue():
    """An Arceus sculpture as voxels (relative x, y, z; front = -z), stone with a gold cross-wheel: a deep-chested
    quadruped body, a long arched neck, a head with a swept-back crest, slender legs ending in pointed hooves, a
    flowing tail, and the wheel standing round its middle. Returns (stone voxels, gold voxels)."""
    parts = [((0, 9.0, 1.0), (3.6, 3.4, 6.0)), ((0, 9.6, -3.6), (3.4, 3.6, 3.0)),             # body, chest
             ((0, 13.0, -5.6), (1.9, 3.4, 1.9)), ((0, 16.2, -6.6), (2.2, 2.1, 2.8)),            # neck, head
             ((0, 15.6, -9.2), (1.1, 1.0, 1.6)),                                                 # muzzle
             ((0, 18.0, -5.4), (1.6, 1.4, 1.8)), ((0, 18.6, -3.4), (1.1, 1.2, 2.2)),            # crest sweeping back
             ((0, 10.6, 7.4), (1.6, 1.6, 2.6)), ((0, 9.0, 9.6), (1.3, 2.4, 1.3))]               # tail
    for sx in (-1, 1):
        for zc in (-3.2, 4.2):
            parts += [((sx * 2.2, 5.4, zc), (1.2, 3.6, 1.2)), ((sx * 2.3, 1.8, zc - 0.3), (0.9, 2.2, 0.9)),
                      ((sx * 2.3, 0.4, zc - 0.9), (0.8, 0.5, 1.4))]                              # thigh, shin, hoof
        parts.append(((sx * 1.6, 16.2, -2.6), (0.7, 0.9, 1.8)))                                 # crest wings
    stone, gold = set(), set()
    for x in range(-9, 10):
        for y in range(0, 21):
            for z in range(-12, 13):
                p = (x, y + 0.5, z)
                if any(sum(((p[i] - c[i]) / r[i]) ** 2 for i in range(3)) <= 1 for c, r in parts):
                    stone.add((x, y, z))
    # the cross-wheel: a ring standing across the body (in the x-y plane), centred on the middle
    cy, cz = 9.5, 0
    for x in range(-9, 10):
        for y in range(0, 21):
            d = math.hypot(x, y + 0.5 - cy)
            if 6.4 <= d <= 7.6:
                for z in (cz - 1, cz, cz + 1):
                    gold.add((x, y, z))
            # four jewels at the wheel's quarters
            for jx, jy in ((7, cy), (-7, cy), (0, cy + 7), (0, cy - 7)):
                if math.hypot(x - jx, y + 0.5 - jy) <= 1.3:
                    gold.add((x, y, cz - 2))
    stone -= gold
    return stone, gold


def hisui_mountain():
    """A great snow-capped mountain (an original landmark inspired by the great mountain of Hisui): a rugged peak
    of stone, andesite and tuff, grass round its foot and snow toward the top, a path spiralling up its flanks to a
    flattened summit where ruined white pillars ring a pedestal, and on it a stone Arceus sculpture: every block of
    the sculpture is the portal. Its core is a great cavern, reached by a tunnel at the foot, lit by glowing lichen."""
    R, HMAX = 96, 150
    W = 2 * R + 3
    H = HMAX + 26
    c = W // 2
    t = S((W, H, W))
    rng_cells = {}

    def bump(x, z, cell, seed):
        key = (x // cell, z // cell, seed)
        if key not in rng_cells:
            rng_cells[key] = h(*key)
        return rng_cells[key]

    def smooth(x, z, cell, seed):
        gx, gz = x / cell, z / cell
        x0, z0 = int(math.floor(gx)), int(math.floor(gz))
        fx, fz = gx - x0, gz - z0
        v = [[h(x0 + i, z0 + j, seed) for j in (0, 1)] for i in (0, 1)]
        top = v[0][0] * (1 - fx) + v[1][0] * fx
        bot = v[0][1] * (1 - fx) + v[1][1] * fx
        return top * (1 - fz) + bot * fz

    summit_r = 16
    height = {}
    for x in range(W):
        for z in range(W):
            r = math.hypot(x - c, z - c)
            if r > R:
                continue
            k = 1 - r / R
            ridge = 0.6 * smooth(x, z, 22, 3) + 0.4 * smooth(x, z, 9, 4)
            hgt = HMAX * (k ** 1.35) * (0.82 + 0.3 * ridge)
            if r <= summit_r:
                hgt = HMAX * ((1 - summit_r / R) ** 1.35) * 0.98
            height[(x, z)] = max(1, int(hgt))
    summit = max(v for (x, z), v in height.items() if math.hypot(x - c, z - c) <= summit_r)
    for (x, z), top in height.items():
        r = math.hypot(x - c, z - c)
        if r <= summit_r:
            top = summit
            height[(x, z)] = top
        thick = 7
        for y in range(max(0, top - thick), top + 1):
            frac = y / HMAX
            if y == top:
                b = "snow_block" if frac > 0.62 else ("stone" if frac > 0.38 else ("grass_block" if frac < 0.2 else
                     pick([("stone", 2), ("coarse_dirt", 1), ("grass_block", 1)], x, z, 8)))
            else:
                b = pick([("stone", 5), ("andesite", 2), ("tuff", 1), ("granite", 0.5)] if frac > 0.15 else
                         [("dirt", 2), ("stone", 3), ("andesite", 1)], x // 2, y // 2, z // 2, 9)
                if frac > 0.62 and y >= top - 1:
                    b = "packed_ice" if h(x, z, 11) > 0.8 else "snow_block"
            t.put(x, y, z, b)
    # the cavern inside, and the tunnel to it from the south foot
    for (x, z), top in height.items():
        r = math.hypot(x - c, z - c)
        if r < R * 0.55:
            ceil = min(top - 8, int(46 * (1 - r / (R * 0.55)) ** 0.5) + 2)
            for y in range(1, max(1, ceil)):
                t.put(x, y, z, "air")
            if ceil > 3:
                t.put(x, 0, z, pick([("stone", 4), ("gravel", 1), ("tuff", 1)], x, z, 13))
                if h(x, z, 14) > 0.985:
                    t.put(x, ceil, z, "glowstone")
                elif h(x, z, 15) > 0.97:
                    t.put(x, ceil, z, "glow_lichen", {"down": "false", "up": "true", "north": "false", "south": "false",
                                                    "east": "false", "west": "false", "waterlogged": "false"})
    for z in range(c + int(R * 0.5), W):
        for x in range(c - 2, c + 3):
            for y in range(1, 5):
                if (x, z) in height and t.get(x, y, z) is not None:
                    t.put(x, y, z, "air")
    # the spiral path up the flanks (three turns), a carved ledge three blocks wide
    turns, steps = 3.0, 6000
    for i in range(steps):
        f = i / steps
        ang = f * turns * 2 * math.pi + math.pi / 2
        r = (R - 6) * (1 - f) + (summit_r - 1) * f
        x0, z0 = c + math.cos(ang) * r, c + math.sin(ang) * r
        xi, zi = int(round(x0)), int(round(z0))
        if (xi, zi) not in height:
            continue
        y = height[(xi, zi)] if f < 0.98 else summit
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                xx, zz = xi + dx, zi + dz
                if (xx, zz) not in height:
                    continue
                py = min(y, height[(xx, zz)])
                t.put(xx, py, zz, "gravel" if (xx + zz) % 3 else "cobblestone")
                for yy in range(py + 1, py + 4):
                    if t.get(xx, yy, zz) is not None:
                        t.put(xx, yy, zz, "air")
    # the summit: a ring of ruined pillars round a stepped pedestal, the sculpture on it
    for x in range(c - summit_r, c + summit_r + 1):
        for z in range(c - summit_r, c + summit_r + 1):
            if math.hypot(x - c, z - c) <= summit_r:
                t.put(x, summit, z, "polished_diorite" if (x + z) % 4 else "calcite")
                for y in range(summit + 1, H):
                    t.put(x, y, z, "air")
    for k in range(12):
        a = k / 12 * 2 * math.pi
        px, pz = int(round(c + math.cos(a) * (summit_r - 2))), int(round(c + math.sin(a) * (summit_r - 2)))
        ph = 3 + int(h(k, 21) * 7)
        for y in range(summit + 1, summit + 1 + ph):
            t.put(px, y, pz, "quartz_pillar", {"axis": "y"})
        if ph > 7:
            t.put(px, summit + 1 + ph, pz, "chiseled_quartz_block")
    for rr, y in ((6, 1), (5, 2), (4, 3)):
        for x in range(c - rr, c + rr + 1):
            for z in range(c - rr, c + rr + 1):
                t.put(x, summit + y, z, "smooth_quartz" if max(abs(x - c), abs(z - c)) < rr else "quartz_bricks")
    base = summit + 4
    stone, gold = arceus_statue()
    for (x, y, z) in stone:
        t.put(c + x, base + y, c + z, f"{MOD}:hisui_arceus_statue")
    for (x, y, z) in gold:
        t.put(c + x, base + y, c + z, "gold_block")
    return t


# --- the portal blocks' art ---------------------------------------------------------------------------------------------
def rgba(c, a=255):
    return tuple(max(0, min(255, int(round(v)))) for v in c[:3]) + (a,)


def shade(c, k):
    return tuple(v * k for v in c)


def tex(fn, w=16, hh=16):
    im = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
    for y in range(hh):
        for x in range(w):
            c = fn(x, y)
            if c is not None:
                im.putpixel((x, y), rgba(c) if len(c) == 3 else c)
    return im


def bronze(x, y):
    base = (176, 120, 52)
    k = 0.75 + 0.5 * (1 - abs(x - 6.5) / 8)                         # a rounded sheen
    if y in (3, 4) or y == 12:
        k *= 0.7                                                    # engraved bands
    if y == 8 and x % 3 == 0:
        k *= 0.75
    return shade(base, k * (0.96 + 0.08 * h(x, y, 5)))


def statue_stone(x, y):
    base = (138, 92, 78)                                            # a dark red granite
    k = 0.86 + 0.22 * h(x // 2, y // 2, 8) + 0.06 * (h(x, y, 9) - 0.5)
    if (x + 2 * y) % 11 == 0 or (y == 7 and 3 < x < 13):            # chisel lines
        k *= 0.72
    return shade(base, k)


def arceus_stone(x, y):
    """Pale carved stone with faint gold veins (the Arceus sculpture)."""
    base = (214, 210, 196)
    k = 0.9 + 0.14 * h(x // 2, y // 2, 31) + 0.04 * (h(x, y, 32) - 0.5)
    if (x * 3 + y * 2) % 13 == 0:
        return (200, 170, 90)
    if (x + 2 * y) % 9 == 0:
        k *= 0.84                                             # chisel strokes
    return shade(base, k)


def boarded(lower):
    """A dark doorway behind diagonal-free horizontal boards (the doorway of the lower/upper block)."""
    def f(x, y):
        frame = x in (0, 15)
        if frame:
            return shade((60, 40, 26), 0.9 + 0.1 * h(x, y, 1))
        yy = y + (16 if lower else 0)
        board = (yy % 8) in (2, 3, 4)
        if board:
            k = 0.85 + 0.25 * h(x // 4, yy // 8, 2) + 0.05 * (h(x, yy, 3) - 0.5)
            if x in (3, 12) and (yy % 8) == 3:
                return (40, 40, 44)                                 # nails
            return shade((122, 88, 56), k)
        return shade((22, 16, 14), 0.8 + 0.3 * h(x, yy, 4))           # darkness behind
    return f


GOLD = [(120, 84, 20), (190, 140, 40), (240, 196, 70), (255, 236, 150)]


def wardrobe(lower):
    """Golden wardrobe doors (two blocks tall) with a Magearna engraving: up top a gear-ring round a round face with two
    eyes, below the Soul-Heart and the skirt-like lower body."""
    def f(x, y):
        yy = y + (16 if lower else 0)                               # 0..31 down the two blocks
        k = 2
        if x in (0, 15) or yy in (0, 31):
            k = 0
        elif x in (7, 8):
            k = 1                                                   # the doors' seam
        elif x in (1, 14) or yy in (1, 30):
            k = 3
        # the engraving (darker lines)
        cx, cy = 7.5, 9.0
        d = math.hypot(x - cx, yy - cy)
        ang = math.atan2(yy - cy, x - cx)
        teeth = 6.2 + 0.9 * (math.cos(ang * 10) > 0.3)
        line = False
        if 5.4 <= d <= teeth:
            line = d > 6.0 or abs(d - 5.6) < 0.5
        if 2.4 <= d <= 3.4:
            line = True                                             # the face
        if yy == 9 and x in (6, 9):
            line = True                                             # the eyes
        # the heart
        hy = 20.0
        hx = abs(x - 7.5)
        heart = (hx - 1.6) ** 2 + (yy - hy + 0.6) ** 2 <= 2.6 or (yy >= hy and hx <= 3.6 - (yy - hy) * 0.9)
        heart_edge = heart and not ((hx - 1.6) ** 2 + (yy - hy + 0.6) ** 2 <= 1.0 or (yy >= hy + 0.5 and hx <= 2.2 - (yy - hy) * 0.9))
        if heart_edge:
            line = True
        if heart and not heart_edge:
            return (230, 70, 90)                                    # the Soul-Heart, enamelled red
        if 25 <= yy <= 28 and abs(x - 7.5) <= 2 + (yy - 25) and abs(x - 7.5) >= 1 + (yy - 25):
            line = True                                             # the skirt
        if line and k >= 2:
            k = 1
        return shade(GOLD[k], 0.95 + 0.1 * h(x, yy, 7))
    return f


def ball(part):
    def f(x, y):
        hi = (x + y) < 9                                            # a glossy highlight top-left
        if part == "red":
            c = (214, 40, 40)
        elif part == "white":
            c = (238, 238, 240)
        elif part == "black":
            c = (30, 30, 34)
        else:
            d = math.hypot(x - 7.5, y - 7.5)
            c = (30, 30, 34) if d > 6.5 else (200, 200, 205) if d > 5.2 else (248, 248, 250)
        k = 1.08 if hi else 0.94
        return shade(c, k + 0.03 * (h(x, y, 2) - 0.5))
    return f


def telescope(x, y):
    c = (236, 238, 242)
    if y in (0, 15) or x in (0, 15):
        c = (150, 156, 168)
    if y in (5, 10):
        c = (64, 70, 84)                                            # rings
    return shade(c, 0.95 + 0.08 * h(x, y, 4))


def engraved_bark(x, y):
    bark = (60, 46, 30)
    k = 0.8 + 0.35 * h(x, y // 3, 1) if x % 4 else 0.7               # vertical bark grain
    c = shade(bark, k)
    d = math.hypot(x - 7.5, y - 7.5)
    if 5.0 <= d <= 6.2 or (abs(y - 7.5) <= 0.6 and d <= 6.2) or 1.6 <= d <= 2.6:
        return shade((26, 18, 12), 1.0)                             # the carved ball: outline, band, button ring
    if d < 5.0 and y < 7:
        return shade((140, 40, 40), 0.9 + 0.2 * h(x, y, 3))        # a hint of red rubbed into the top half
    return c


def pc_screen(x, y):
    if x in (0, 15) or y in (0, 15):
        return (34, 34, 40)
    c = (255, 150, 60) if y < 4 else (70, 40, 120)                  # an orange title bar over a violet desktop
    if 6 <= y <= 12 and 2 <= x <= 13 and (x % 4 == 1 or y == 9):
        c = (240, 220, 255)                                         # icons and a line of text
    return shade(c, 0.95 + 0.08 * h(x, y, 6))


def pc_body(x, y):
    return shade((52, 54, 62), 0.9 + 0.15 * h(x, y, 8))


PORTALS = {
    "johto_bell": "Johto Bell", "hoenn_statue_stone": "Groudon Statue Stone", "sinnoh_boarded_doorway": "Boarded Doorway",
    "unova_wardrobe": "Golden Wardrobe", "kalos_ball_shell": "Giant Poké Ball Shell", "alola_telescope": "Observatory Telescope",
    "galar_engraved_bark": "Engraved Giant Bark", "paldea_pc": "Academy PC", "hisui_arceus_statue": "Arceus Sculpture Stone",
}


def portal_assets():
    B = A / "textures" / "block"
    save(tex(bronze), B / "johto_bell.png")
    save(tex(statue_stone), B / "hoenn_statue_stone.png")
    save(tex(arceus_stone), B / "hisui_arceus_statue.png")
    for half in ("lower", "upper"):
        save(tex(boarded(half == "lower")), B / f"sinnoh_boarded_doorway_{half}.png")
        save(tex(wardrobe(half == "lower")), B / f"unova_wardrobe_{half}.png")
    save(tex(lambda x, y: shade(GOLD[2 if 0 < x < 15 and 0 < y < 15 else 1], 0.95 + 0.1 * h(x, y, 2))), B / "unova_wardrobe_side.png")
    for part in ("red", "white", "black", "button"):
        save(tex(ball(part)), B / f"kalos_ball_shell_{part}.png")
    save(tex(telescope), B / "alola_telescope.png")
    save(tex(engraved_bark), B / "galar_engraved_bark.png")
    save(tex(pc_screen), B / "paldea_pc_screen.png")
    save(tex(pc_body), B / "paldea_pc_body.png")
    M, BS = A / "models" / "block", A / "blockstates"
    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    # the bell: a lip, a body, a crown and the hanger
    write_json(M / "johto_bell.json", {"parent": "minecraft:block/block", "textures": {"all": f"{MOD}:block/johto_bell", "particle": f"{MOD}:block/johto_bell"},
                                      "elements": [{"from": f, "to": t_, "faces": {d: {"texture": "#all"} for d in ("north", "south", "east", "west", "up", "down")}}
                                                   for f, t_ in (([3, 0, 3], [13, 3, 13]), ([4, 3, 4], [12, 12, 12]), ([5, 12, 5], [11, 13, 11]),
                                                                 ([7, 13, 7], [9, 16, 9]))]})
    write_json(BS / "johto_bell.json", {"variants": {"": {"model": f"{MOD}:block/johto_bell"}}})
    for name in ("hoenn_statue_stone", "alola_telescope", "hisui_arceus_statue"):
        write_json(M / f"{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/{name}"}})
        write_json(BS / f"{name}.json", {"variants": {"": {"model": f"{MOD}:block/{name}"}}})
    # tall ones: a front texture per half, plain sides
    for name, side, top in (("sinnoh_boarded_doorway", "minecraft:block/dark_oak_planks", "minecraft:block/dark_oak_planks"),
                            ("unova_wardrobe", f"{MOD}:block/unova_wardrobe_side", f"{MOD}:block/unova_wardrobe_side")):
        for half in ("lower", "upper"):
            write_json(M / f"{name}_{half}.json", {"parent": "minecraft:block/orientable", "textures": {
                "front": f"{MOD}:block/{name}_{half}", "side": side, "top": top}})
        write_json(BS / f"{name}.json", {"variants": {f"facing={f},half={hf}": dict({"model": f"{MOD}:block/{name}_{hf}"}, **({"y": r} if r else {}))
                                                      for f, r in rot.items() for hf in ("lower", "upper")}})
    write_json(M / "galar_engraved_bark.json", {"parent": "minecraft:block/orientable", "textures": {
        "front": f"{MOD}:block/galar_engraved_bark", "side": "minecraft:block/dark_oak_log", "top": "minecraft:block/dark_oak_log_top"}})
    write_json(BS / "galar_engraved_bark.json", {"variants": {f"facing={f}": dict({"model": f"{MOD}:block/galar_engraved_bark"}, **({"y": r} if r else {}))
                                                             for f, r in rot.items()}})
    for part in ("red", "white", "black", "button"):
        write_json(M / f"kalos_ball_shell_{part}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/kalos_ball_shell_{part}"}})
    write_json(BS / "kalos_ball_shell.json", {"variants": {f"part={p}": {"model": f"{MOD}:block/kalos_ball_shell_{p}"} for p in ("red", "white", "black", "button")}})
    # the PC: base plate, a keyboard, a stand and the monitor (screen on the north face)
    allf = lambda tx: {d: {"texture": tx} for d in ("north", "south", "east", "west", "up", "down")}
    screen = allf("#body")
    screen["north"] = {"texture": "#screen", "uv": [1, 2, 15, 14]}
    write_json(M / "paldea_pc.json", {"parent": "minecraft:block/block", "textures": {"body": f"{MOD}:block/paldea_pc_body",
                                                                                   "screen": f"{MOD}:block/paldea_pc_screen", "particle": f"{MOD}:block/paldea_pc_body"},
                                     "elements": [{"from": [5, 0, 8], "to": [11, 1, 12], "faces": allf("#body")},
                                                  {"from": [3, 0, 2], "to": [13, 1, 6], "faces": allf("#body")},
                                                  {"from": [7, 1, 9], "to": [9, 4, 10], "faces": allf("#body")},
                                                  {"from": [1, 2, 8], "to": [15, 14, 9], "faces": screen}]})
    write_json(BS / "paldea_pc.json", {"variants": {f"facing={f}": dict({"model": f"{MOD}:block/paldea_pc"}, **({"y": r} if r else {}))
                                                   for f, r in rot.items()}})
    # item models, loot tables, names
    item_model = {"hisui_arceus_statue": "hisui_arceus_statue", "johto_bell": "johto_bell", "hoenn_statue_stone": "hoenn_statue_stone", "sinnoh_boarded_doorway": "sinnoh_boarded_doorway_lower",
                  "unova_wardrobe": "unova_wardrobe_lower", "kalos_ball_shell": "kalos_ball_shell_button", "alola_telescope": "alola_telescope",
                  "galar_engraved_bark": "galar_engraved_bark", "paldea_pc": "paldea_pc"}
    for name, label in PORTALS.items():
        write_json(A / "models" / "item" / f"{name}.json", {"parent": f"{MOD}:block/{item_model[name]}"})
        entry = {"type": "minecraft:item", "name": f"{MOD}:{name}"}
        cond = [{"condition": "minecraft:survives_explosion"}]
        if name in ("sinnoh_boarded_doorway", "unova_wardrobe"):
            cond.append({"condition": "minecraft:block_state_property", "block": f"{MOD}:{name}", "properties": {"half": "lower"}})
        write_json(D / "loot_table" / "blocks" / f"{name}.json", {"type": "minecraft:block", "pools": [{"rolls": 1, "entries": [entry], "conditions": cond}]})
        LANG[f"block.{MOD}.{name}"] = label
    tags = RES / "data" / "minecraft" / "tags" / "block"
    for tool, names in (("pickaxe", ["hisui_arceus_statue", "hoenn_statue_stone", "kalos_ball_shell", "alola_telescope", "paldea_pc", "johto_bell", "unova_wardrobe"]),
                        ("axe", ["sinnoh_boarded_doorway", "galar_engraved_bark"])):
        path = tags / "mineable" / f"{tool}.json"
        cur = json.loads(path.read_text()) if path.exists() else {"replace": False, "values": []}
        cur["values"] = sorted(set(cur["values"]) | {f"{MOD}:{n}" for n in names})
        write_json(path, cur)


# --- worldgen: landmarks and dimensions -----------------------------------------------------------------------------
# region -> (structure id, label, builder, biomes it generates in, spacing, separation, start height, adaptation, arrival)
LANDMARKS = {
    "johto": ("johto_pagoda", "Johto Pagoda", johto_pagoda,
              ["forest", "birch_forest", "cherry_grove", "plains", "flower_forest", "old_growth_birch_forest", "meadow"], 40, 14, 0, "beard_thin",
              "Welcome to Johto. Ring the bell to go home."),
    "hoenn": ("hoenn_granite_cave", "Hoenn Granite Cave", hoenn_cave,
              ["badlands", "wooded_badlands", "savanna", "savanna_plateau", "windswept_hills", "stony_shore", "desert", "beach"], 40, 14, 0, "beard_thin",
              "Welcome to Hoenn. Touch a statue stone to go home."),
    "sinnoh": ("sinnoh_old_manor", "Sinnoh Old Manor", sinnoh_manor,
               ["dark_forest", "old_growth_spruce_taiga", "old_growth_pine_taiga", "taiga", "swamp", "snowy_taiga"], 32, 10, -6, "beard_thin",
               "Welcome to Sinnoh. Open the boarded doorway to go home."),
    "unova": ("unova_castle", "Unova Castle", unova_castle,
              ["plains", "sunflower_plains", "meadow", "savanna", "windswept_hills"], 44, 16, 0, "beard_thin",
              "Welcome to Unova. Open the golden wardrobe to go home."),
    "kalos": ("kalos_ball_factory", "Kalos Ball Factory", kalos_factory,
              ["plains", "sunflower_plains", "flower_forest", "meadow", "forest"], 44, 16, 0, "beard_thin",
              "Welcome to Kalos. Touch the Poké Ball to go home."),
    "alola": ("alola_observatory", "Alola Observatory", alola_observatory,
              ["meadow", "grove", "stony_peaks", "windswept_hills", "windswept_gravelly_hills", "jagged_peaks", "snowy_slopes", "cherry_grove"], 32, 10, 0, "beard_thin",
              "Welcome to Alola. Look through the telescope to go home."),
    "galar": ("galar_giant_tree", "Galar Giant Tree", galar_tree,
              ["snowy_plains", "snowy_taiga", "ice_spikes", "grove", "snowy_slopes", "frozen_river"], 40, 14, -GALAR_GROUND, "none",
              "Welcome to Galar. Touch the engraved bark to go home."),
    "hisui": ("hisui_great_mountain", "Hisui Great Mountain", hisui_mountain,
              ["plains", "meadow", "taiga", "snowy_taiga", "snowy_plains", "old_growth_spruce_taiga", "windswept_forest"], 64, 24, 0, "none",
              "Welcome to Hisui. Touch the Arceus sculpture to go home."),
    "paldea": ("paldea_academy", "Paldea Academy", paldea_academy,
               ["plains", "savanna", "meadow", "sunflower_plains", "desert", "cherry_grove"], 44, 16, 0, "beard_thin",
               "Welcome to Paldea. Use the academy PC to go home."),
}

# each region's biome mix: (oceans, beach, river, peaks, [(biome, temperature range, humidity range)]), noise settings
OCEAN = (-1.2, -0.19)
BIOMES = {
    "johto": (["ocean", "deep_ocean"], "beach", "river", "stony_peaks",
              [("plains", (-0.45, 0.2), (-1, -0.1)), ("forest", (-0.45, 0.55), (-0.1, 0.3)), ("birch_forest", (-0.15, 0.2), (0.1, 0.3)),
               ("cherry_grove", (0.2, 0.55), (-1, 0.1)), ("taiga", (-1, -0.45), (-1, 1)), ("dark_forest", (-0.15, 0.55), (0.3, 1)),
               ("meadow", (0.55, 1), (-1, 1))], "minecraft:overworld"),
    "hoenn": (["warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean"], "beach", "river", "badlands",
              [("jungle", (0.2, 1), (0.3, 1)), ("sparse_jungle", (0.2, 1), (0, 0.3)), ("savanna", (0.2, 1), (-0.35, 0)),
               ("desert", (0.55, 1), (-1, -0.35)), ("bamboo_jungle", (-0.45, 0.2), (0.3, 1)), ("mangrove_swamp", (-0.45, 0.2), (0, 0.3)),
               ("plains", (-1, 0.2), (-1, 0)), ("wooded_badlands", (0.2, 0.55), (-1, -0.35))], f"{MOD}:hoenn"),
    "sinnoh": (["cold_ocean", "deep_cold_ocean", "frozen_ocean"], "snowy_beach", "frozen_river", "frozen_peaks",
               [("taiga", (-0.45, 0.2), (-1, 0.3)), ("snowy_taiga", (-1, -0.45), (0, 1)), ("snowy_plains", (-1, -0.45), (-1, 0)),
                ("old_growth_spruce_taiga", (-0.45, 0.2), (0.3, 1)), ("grove", (-1, -0.15), (-0.3, 0.3)), ("forest", (0.2, 1), (-1, 1))],
               "minecraft:amplified"),
    "unova": (["ocean", "deep_ocean"], "beach", "river", "windswept_hills",
              [("plains", (-0.45, 0.2), (-1, 0)), ("sunflower_plains", (-0.15, 0.2), (-0.35, 0)), ("desert", (0.55, 1), (-1, 0)),
               ("savanna", (0.2, 0.55), (-1, 0)), ("dark_forest", (-0.45, 0.55), (0.3, 1)), ("swamp", (0.2, 1), (0.3, 1)),
               ("forest", (-0.45, 0.55), (0, 0.3)), ("snowy_plains", (-1, -0.45), (-1, 1))], "minecraft:overworld"),
    "kalos": (["lukewarm_ocean", "ocean", "deep_ocean"], "beach", "river", "snowy_slopes",
              [("flower_forest", (-0.15, 0.55), (0, 0.3)), ("sunflower_plains", (0.2, 1), (-1, 0)), ("meadow", (-0.45, 0.2), (-1, 0)),
               ("birch_forest", (-0.45, -0.15), (0, 1)), ("cherry_grove", (0.2, 1), (0, 1)), ("forest", (-0.15, 0.2), (0.3, 1)),
               ("plains", (-1, -0.45), (-1, 1))], "minecraft:overworld"),
    "alola": (["warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean"], "beach", "river", "snowy_slopes",
              [("jungle", (0.2, 1), (0.3, 1)), ("sparse_jungle", (0.2, 1), (-0.1, 0.3)), ("bamboo_jungle", (-0.45, 0.2), (0.3, 1)),
               ("savanna", (0.2, 1), (-1, -0.1)), ("desert", (0.55, 1), (-1, -0.35)), ("plains", (-1, 0.2), (-1, 0.3))], f"{MOD}:alola"),
    "galar": (["cold_ocean", "ocean", "deep_cold_ocean"], "stony_shore", "river", "frozen_peaks",
              [("plains", (-0.15, 0.55), (-1, 0)), ("meadow", (0.2, 1), (-1, 0)), ("windswept_hills", (-0.45, -0.15), (-1, 0)),
               ("forest", (-0.15, 1), (0, 0.3)), ("dark_forest", (-0.15, 1), (0.3, 1)), ("snowy_plains", (-1, -0.45), (-1, 0)),
               ("snowy_taiga", (-1, -0.45), (0, 1)), ("taiga", (-0.45, -0.15), (0, 1))], "minecraft:large_biomes"),
    "paldea": (["ocean", "lukewarm_ocean", "deep_ocean"], "beach", "river", "jagged_peaks",
               [("plains", (-0.15, 0.2), (-1, 0)), ("savanna", (0.2, 0.55), (-1, 0)), ("desert", (0.55, 1), (-1, -0.35)),
                ("badlands", (0.55, 1), (-0.35, 0.3)), ("cherry_grove", (-0.15, 0.55), (0, 0.3)), ("swamp", (0.2, 1), (0.3, 1)),
                ("snowy_taiga", (-1, -0.45), (-1, 1)), ("meadow", (-0.45, -0.15), (-1, 1)), ("bamboo_jungle", (-0.15, 0.2), (0.3, 1))],
               "minecraft:large_biomes"),
}
BIOMES["hisui"] = (["cold_ocean", "ocean", "deep_cold_ocean"], "stony_shore", "river", "jagged_peaks",
                   [("plains", (-0.15, 0.55), (-1, 0)), ("forest", (-0.15, 0.55), (0, 0.3)), ("swamp", (0.2, 1), (0.3, 1)),
                    ("mangrove_swamp", (0.55, 1), (0, 0.3)), ("badlands", (0.55, 1), (-1, 0)), ("meadow", (-0.45, -0.15), (-1, 0)),
                    ("windswept_hills", (-0.45, -0.15), (0, 1)), ("snowy_plains", (-1, -0.45), (-1, 0)),
                    ("snowy_taiga", (-1, -0.45), (0, 1)), ("dark_forest", (-0.15, 0.2), (0.3, 1))], "minecraft:large_biomes")
SEA_LEVEL = {"hoenn": 70, "alola": 90}                        # more sea: Hoenn's islands, Alola's archipelago


def multi_noise(region):
    oceans, beach, river, peaks, land, _ = BIOMES[region]
    out = []

    def add(biome, t, hum, cont, ero=(-1, 1), weird=(-1, 1), offset=0.0):
        out.append({"biome": f"minecraft:{biome}", "parameters": {"temperature": list(t), "humidity": list(hum), "continentalness": list(cont),
                                                                 "erosion": list(ero), "weirdness": list(weird), "depth": 0, "offset": offset}})
    # oceans: the shallow ones split by temperature, coldest to warmest; deep ones further out at their temperature
    warmth = lambda o: next((i for i, k in enumerate(("frozen", "cold", "ocean", "lukewarm", "warm")) if o.replace("deep_", "").startswith(k)), 2)
    shallow = sorted((o for o in oceans if not o.startswith("deep_")), key=warmth)
    deep = [o for o in oceans if o.startswith("deep_")]
    for i, o in enumerate(shallow):
        lo = -1 + 2 * i / len(shallow)
        add(o, (lo, lo + 2 / len(shallow)), (-1, 1), OCEAN)
    for o in deep:
        t = next(((-1 + 2 * i / len(shallow), -1 + 2 * (i + 1) / len(shallow)) for i, so in enumerate(shallow) if so == o[5:]), (-1, 1))
        add(o, t, (-1, 1), (-1.2, -0.455))
    add(beach, (-1, 1), (-1, 1), (-0.19, -0.11))
    # rivers and peaks overlap the land boxes: the land's small offset makes them win where they apply
    add(river, (-1, 1), (-1, 1), (-0.11, 0.55), (-0.2, 1), (-0.05, 0.05))
    add(peaks, (-1, 1), (-1, 1), (0.3, 1), (-1, -0.55), (-1, 1))
    for biome, t, hum in land:
        add(biome, t, hum, (-0.11, 1), offset=0.08)
    return {"type": "minecraft:multi_noise", "biomes": out}


def worldgen():
    for region, (sid, label, builder, biomes, spacing, sep, start, adapt, arrival) in LANDMARKS.items():
        t = builder()
        p = D / "structure" / "region" / f"{sid}.nbt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(t.nbt())
        write_json(D / "worldgen" / "template_pool" / "region" / f"{sid}.json", {
            "fallback": "minecraft:empty", "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element", "location": f"{MOD}:region/{sid}",
                "processors": "minecraft:empty", "projection": "rigid"}}]})
        write_json(D / "worldgen" / "structure" / f"{sid}.json", {
            "type": "minecraft:jigsaw", "biomes": f"#{MOD}:has_structure/{sid}", "step": "surface_structures",
            "spawn_overrides": {}, "terrain_adaptation": adapt, "start_pool": f"{MOD}:region/{sid}", "size": 1,
            "start_height": {"absolute": start}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "max_distance_from_center": 116 if adapt == "none" else 100, "use_expansion_hack": False})
        write_json(D / "worldgen" / "structure_set" / f"{sid}.json", {
            "structures": [{"structure": f"{MOD}:{sid}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": sep,
                          "salt": 20651 + 97 * list(LANDMARKS).index(region)}})
        write_json(D / "tags" / "worldgen" / "biome" / "has_structure" / f"{sid}.json",
                   {"replace": False, "values": [f"minecraft:{b}" for b in biomes]})
        LANG[f"{MOD}.arrived.{region}"] = arrival
        LANG[f"structure.{MOD}.{sid}"] = label
        print(f"  {sid}: {t.size}, {len(t.blocks)} blocks, {p.stat().st_size // 1024} KB")
    # the dimensions (Kanto's dimension type: overworld-like)
    vanilla = json.loads(zipfile.ZipFile(LOOM).read("data/minecraft/worldgen/noise_settings/overworld.json"))
    for region, sea in SEA_LEVEL.items():
        ns = json.loads(json.dumps(vanilla))
        ns["sea_level"] = sea
        write_json(D / "worldgen" / "noise_settings" / f"{region}.json", ns)
    for region in LANDMARKS:
        write_json(D / "dimension" / f"{region}.json", {"type": f"{MOD}:kanto", "generator": {
            "type": "minecraft:noise", "settings": BIOMES[region][5], "biome_source": multi_noise(region)}})


def build():
    portal_assets()
    worldgen()


if __name__ == "__main__":
    build()
