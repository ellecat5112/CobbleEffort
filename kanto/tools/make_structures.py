#!/usr/bin/env python3
"""
Overworld landmarks of the first three generations (CobbleEffort: Kanto 0.14.0, the user's request). Original
Minecraft builds inspired by those places (not replicas of the games' maps), generated in the overworld like the
region landmarks, each with its own loot and its own Pokémon (spawn pools limited to the structure):

  Gen 1  Bill's Sea Cottage (a seaside cottage with the Cell Separation System and a gift Eevee), the S.S. Anne (a
         liner at sea), the Lavender Town Tower (seven floors of graves), the Celadon Rocket Hideout (a game corner
         over a three-floor basement), the Cinnabar Pokémon Lab (nearly every machine of Cobblemon, Mega Showdown and
         CobbleEffort: Distortion)
  Gen 2  the Ruins of Alph (Unown chambers), the Lake of Rage (a shrine on the dock calls the red Gyarados), the
         Mahogany Rocket HQ (a souvenir shop over a two-floor base)
  Gen 3  Meteor Falls (a waterfall cavern), Mt. Chimney (a volcano with a lava crater), Mt. Pyre (graves in the
         mountain; the Red and Blue Orbs at its summit), Sky Pillar (Rayquaza at the top), the Temple of Jirachi
         (Jirachi wakes at night) and the Deoxys meteorite (Mega Showdown's meteorites change Deoxys's forme; the
         shrine calls Deoxys)

Shrines (Shrines.java) carry their config in the template. Written here: templates, template pools, structures,
structure sets, biome tags, loot tables, spawn pools, the shrine block's assets and the names. Run standalone
(merges its names into en_us.json) or from make_assets.py.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from make_assets import A, D, MOD, h, save, write_json
from make_regions import S, pick

LANG: dict[str, str] = {}
FACE = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


# --- helpers ----------------------------------------------------------------------------------------------------------
def chest(t, x, y, z, facing, table):
    t.set(x, y, z, "minecraft:chest", {"facing": facing, "type": "single", "waterlogged": "false"},
          {"LootTable": f"{MOD}:chests/landmark/{table}"})


def barrel(t, x, y, z, table, facing="up"):
    t.set(x, y, z, "minecraft:barrel", {"facing": facing, "open": "false"}, {"LootTable": f"{MOD}:chests/landmark/{table}"})


def shrine(t, x, y, z, look="altar", **config):
    t.set(x, y, z, f"{MOD}:shrine", {"look": look, "facing": "north"}, {"config": config})


def two(t, x, y, z, name, facing, key="part", lo="bottom", hi="top", **extra):
    """A two-block-tall machine (Cobblemon's PC, restoration tank, pasture; DNA machine; reassembly unit)."""
    t.put(x, y, z, name, {"facing": facing, key: lo, **extra})
    t.put(x, y + 1, z, name, {"facing": facing, key: hi, **extra})


def candle(t, x, y, z, colour="", n=1, lit=True):
    t.put(x, y, z, f"{colour + '_' if colour else ''}candle", {"candles": str(n), "lit": str(lit).lower(), "waterlogged": "false"})


def ladder(t, x, y0, y1, z, facing):
    for y in range(y0, y1 + 1):
        t.put(x, y, z, "ladder", {"facing": facing, "waterlogged": "false"})


def pane(t, x, y, z, name="glass_pane", axis="x"):
    """A glass pane (or iron bars) joined along x or z."""
    p = {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"}
    if axis == "x":
        p.update(east="true", west="true")
    else:
        p.update(north="true", south="true")
    t.put(x, y, z, name, p)


def trapdoor(t, x, y, z, name, facing="north", half="top", open_=False):
    t.put(x, y, z, name, {"facing": facing, "half": half, "open": str(open_).lower(), "powered": "false", "waterlogged": "false"})


def lamp(t, x, y, z):
    t.put(x, y, z, "redstone_lamp", {"lit": "true"})


def table(t, x, y, z, top="spruce"):
    t.put(x, y, z, f"{top}_fence", {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"})
    t.put(x, y + 1, z, "minecraft:spruce_pressure_plate" if top == "spruce" else f"{top}_pressure_plate", {"powered": "false"})


def stairs_up(t, x0, y0, z, dx, n, mat, clear=3):
    """A straight flight of n stairs climbing along x (dx = +1 or -1) from (x0, y0, z), headroom cleared."""
    for i in range(n):
        x, y = x0 + dx * i, y0 + i
        t.stair(x, y, z, mat, "east" if dx > 0 else "west")
        for k in range(1, clear + 1):
            t.put(x, y + k, z, "air")


def disc(t, cx, y, cz, r, name, props=None, hollow=False):
    for x in range(int(cx - r - 1), int(cx + r + 2)):
        for z in range(int(cz - r - 1), int(cz + r + 2)):
            d = math.hypot(x - cx, z - cz)
            if d <= r and (not hollow or d > r - 1.2):
                t.put(x, y, z, name, props)


def noise(x, z, seed, cell=6.0):
    """Smooth value noise in [0, 1)."""
    gx, gz = x / cell, z / cell
    x0, z0 = math.floor(gx), math.floor(gz)
    fx, fz = gx - x0, gz - z0
    fx, fz = fx * fx * (3 - 2 * fx), fz * fz * (3 - 2 * fz)
    a, b = h(x0, z0, seed), h(x0 + 1, z0, seed)
    c, d = h(x0, z0 + 1, seed), h(x0 + 1, z0 + 1, seed)
    return (a * (1 - fx) + b * fx) * (1 - fz) + (c * (1 - fx) + d * fx) * fz


def ground_fill(t, w, d, y_top, top="grass_block", under="dirt", depth=3):
    """A layer of ground (top block over a few of under) across the template's footprint, for builds that sit on
    their own terrace."""
    for x in range(w):
        for z in range(d):
            t.put(x, y_top, z, top, {"snowy": "false"} if top == "grass_block" else None)
            for k in range(1, depth + 1):
                t.put(x, y_top - k, z, under)


def clear_above(t, x0, z0, x1, z1, y0):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(y0, t.size[1]):
                if t.get(x, y, z) is None:
                    t.put(x, y, z, "air")


# --- Gen 1: Bill's Sea Cottage ---------------------------------------------------------------------------------------
def bills_sea_cottage():
    """A cottage on a stone terrace by the sea: pale blue walls with birch corners, a teal prismarine roof and a brick
    chimney; inside, Bill's desk with a PC and a monitor, a bed, bookshelves, and the Cell Separation System, two
    copper-and-glass pods with a console between them (a shrine: Bill gives each visitor an Eevee). A pier runs out
    front and flower beds line the path."""
    W, H, Dp = 25, 16, 23
    t = S((W, H, Dp))
    g = 2
    ground_fill(t, W, Dp, g, "grass_block", "dirt", 2)
    for x in range(W):                                               # stone terrace edge and the path
        for z in range(Dp):
            if x in (0, W - 1) or z in (0, Dp - 1):
                t.put(x, g, z, "stone_bricks")
    for z in range(0, 6):
        for x in (11, 12, 13):
            t.put(x, g, z, "gravel" if z < 5 else "stone_bricks")
    for x in (8, 9, 15, 16):                                         # flower beds
        for z in (2, 3, 4):
            t.put(x, g + 1, z, pick([("poppy", 2), ("cornflower", 2), ("oxeye_daisy", 2), ("allium", 1)], x, z, 3))
    x0, x1, z0, z1 = 5, 19, 6, 17
    t.box(x0, g, z0, x1, g, z1, "spruce_planks")
    for y in range(g + 1, g + 6):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                wall = x in (x0, x1) or z in (z0, z1)
                corner = x in (x0, x1) and z in (z0, z1)
                if corner:
                    t.log(x, y, z, "birch_log")
                elif wall:
                    t.put(x, y, z, "light_blue_concrete" if y == g + 5 else "calcite")
                else:
                    t.put(x, y, z, "air")
    for x in (7, 8, 16, 17):                                         # windows
        for y in (g + 2, g + 3):
            pane(t, x, y, z0, axis="x")
            pane(t, x, y, z1, axis="x")
    for z in (9, 10, 13, 14):
        for y in (g + 2, g + 3):
            pane(t, x0, y, z, axis="z")
            pane(t, x1, y, z, axis="z")
    t.door(12, g + 1, z0, "birch_door", "south")
    t.put(12, g + 3, z0 - 1, "lantern", {"hanging": "false", "waterlogged": "false"})
    # the teal roof: a gable along x
    for k in range(0, 7):
        y = g + 6 + k
        za, zb = z0 - 1 + k, z1 + 1 - k
        if za > zb:
            break
        for x in range(x0 - 1, x1 + 2):
            if za == zb:
                t.put(x, y, za, "prismarine_bricks")
            else:
                t.stair(x, y, za, "prismarine_brick", "south")
                t.stair(x, y, zb, "prismarine_brick", "north")
                for z in range(za + 1, zb):
                    if x in (x0 - 1, x1 + 1):
                        continue
                    if x in (x0, x1):
                        t.put(x, y, z, "white_concrete")
    t.box(17, g + 6, 15, 18, g + 13, 16, "bricks")                   # the chimney
    t.put(17, g + 14, 15, "campfire", {"facing": "north", "lit": "true", "signal_fire": "false", "waterlogged": "false"})
    # inside: Bill's desk, PC, monitor, bed, bookshelves, a rug
    two(t, 7, g + 1, 16, "cobblemon:pc", "north", on="false")
    for x in (8, 9, 10):
        t.slab(x, g + 1, 16, "spruce", "top")
    t.put(9, g + 2, 16, "cobblemon:monitor", {"facing": "north", "screen": "porygon_grid"})
    t.put(10, g + 2, 16, "cobblemon:monitor", {"facing": "north", "screen": "music"})
    for z in (12, 13, 14, 15):
        t.put(6, g + 1, z, "bookshelf")
        t.put(6, g + 2, z, "bookshelf")
    t.put(6, g + 1, 7, "blue_bed", {"facing": "south", "part": "foot", "occupied": "false"})
    t.put(7, g + 1, 7, "blue_bed", {"facing": "west", "part": "foot", "occupied": "false"})
    t.put(6, g + 1, 7, "blue_bed", {"facing": "west", "part": "head", "occupied": "false"})
    chest(t, 6, g + 1, 9, "east", "bills_sea_cottage")
    for x in range(10, 15):
        for z in range(10, 14):
            t.put(x, g + 1, z, "light_blue_carpet")
    for x, z in ((12, 9), (12, 14)):
        t.put(x, g + 5, z, "lantern", {"hanging": "true", "waterlogged": "false"})
    # the Cell Separation System: two pods and a console between them
    for px in (15, 18):
        pz = 15
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                t.put(px + dx, g + 1, pz + dz, "waxed_copper_block")
                t.put(px + dx, g + 4, pz + dz, "waxed_copper_block")
                for y in (g + 2, g + 3):
                    if dx == 0 and dz == 0:
                        t.put(px, y, pz, "air")
                    elif dx == 0 or dz == 0:
                        t.put(px + dx, y, pz + dz, "glass")
                    else:
                        t.put(px + dx, y, pz + dz, "waxed_cut_copper")
        t.put(px, g + 4, pz, "end_rod", {"facing": "down"})
        t.put(px, g + 2, pz - 1, "air")                                 # step in from the front
        t.put(px, g + 3, pz - 1, "air")
    shrine(t, 16, g + 1, 12, "terminal", key="bills_eevee", mode="pokemon", props="eevee level=5",
           label=f"{MOD}.shrine.bills_eevee")
    t.put(17, g + 1, 12, "cobblemon:monitor", {"facing": "north", "screen": "green_progress_9"})
    # the pier out front
    for z in range(0, 5):
        for x in (19, 20, 21):
            t.put(x, g, z, "spruce_planks")
        if z % 2 == 0:
            t.fence(19, g + 1, z, "spruce_fence")
            t.fence(21, g + 1, z, "spruce_fence")
    t.put(21, g + 2, 0, "lantern", {"hanging": "false", "waterlogged": "false"})
    clear_above(t, 0, 0, W - 1, Dp - 1, g + 1)
    return t


# --- Gen 1: the S.S. Anne ----------------------------------------------------------------------------------------------
SHIP_WATER = 7                       # template y of the sea surface (sea level 63 -> start_height 56)


def ss_anne():
    """A white ocean liner afloat: a red-bottomed hull with a black waterline stripe and portholes, a planked deck with
    railings, a three-deck white superstructure banded with windows (a dining hall with chandeliers below, cabins
    above, the bridge on top), two funnels and two masts. Inside the hull: a cabin deck and, below it, the engine
    room. The hull is open air inside (the sea stays outside)."""
    L, W, H = 67, 21, 34
    t = S((W, H, L))
    cx = W // 2
    deck = 11

    def half(z, y):
        if z < 16:
            w = 1 + (z / 16) ** 0.7 * 8.5
        elif z > 58:
            w = 9.5 - ((z - 58) / 8) ** 1.6 * 3.5
        else:
            w = 9.5
        if y < 4:
            w -= (4 - y) * 0.9
        return w

    inside = set()
    for z in range(L):
        for y in range(0, deck + 1):
            w = half(z, y)
            if w < 0.5:
                continue
            for x in range(W):
                d = abs(x - cx)
                if d > w:
                    continue
                edge = d > w - 1.0 or z == 0 or z == L - 1 or y == 0 or half(z - 1, y) < d or half(z + 1, y) < d
                if edge:
                    c = "red_concrete" if y < 6 else "black_concrete" if y == 6 else "white_concrete"
                    if y == 9 and z % 3 == 0 and 16 <= z <= 58:
                        c = "glass"                                              # portholes
                    if y == deck:
                        c = "white_concrete"
                    t.put(x, y, z, c)
                else:
                    inside.add((x, y, z))
                    if y == deck:
                        t.put(x, y, z, "spruce_planks")                        # the main deck
                    elif y in (3, 7):
                        t.put(x, y, z, "dark_oak_planks" if y == 3 else "spruce_planks")
                    else:
                        t.put(x, y, z, "air")
    # railings round the deck
    for z in range(L):
        w = half(z, deck)
        for x in range(W):
            d = abs(x - cx)
            if w - 1.0 < d <= w:
                t.fence(x, deck + 1, z, "birch_fence")
    # cabins on the cabin deck (y 8..10): beds and chests either side of a corridor
    for z in range(18, 56, 4):
        for side in (-1, 1):
            xa = cx + side * 3
            xb = cx + side * 8
            for x in range(min(xa, xb), max(xa, xb) + 1):
                for y in (8, 9, 10):
                    if (x, y, z) in inside:
                        t.put(x, y, z, "white_terracotta")
            bx = cx + side * 6
            if (bx, 8, z + 2) in inside:
                t.put(bx, 8, z + 1, "red_bed", {"facing": "south", "part": "foot", "occupied": "false"})
                t.put(bx, 8, z + 2, "red_bed", {"facing": "south", "part": "head", "occupied": "false"})
                if (z // 4) % 2 == 0:
                    chest(t, cx + side * 7, 8, z + 3, "north", "ss_anne_cabin")
                t.put(cx + side * 3, 8, z + 2, "air")                        # cabin door gap
                t.put(cx + side * 3, 9, z + 2, "air")
                t.put(bx, 10, z + 2, "lantern", {"hanging": "true", "waterlogged": "false"})
    # the engine room (y 4..6)
    for z in range(40, 56):
        for x in range(cx - 3, cx + 4):
            if (x, 4, z) in inside and (z % 4 in (0, 1)) and abs(x - cx) in (2, 3):
                t.put(x, 4, z, "blast_furnace", {"facing": "east" if x < cx else "west", "lit": "true"})
                t.put(x, 5, z, "iron_block")
    for z in range(42, 54, 3):
        t.put(cx, 4, z, "piston", {"facing": "up", "extended": "false"})
        t.put(cx, 6, z, "lantern", {"hanging": "true", "waterlogged": "false"})
    barrel(t, cx - 1, 4, 56, "ss_anne_engine")
    # ladders between decks
    for z in (20, 50):
        ladder(t, cx, 4, deck, z, "north")
        for y in (7, deck):
            t.put(cx, y, z, "ladder", {"facing": "north", "waterlogged": "false"})
    # the superstructure: three white decks banded with windows
    tiers = [(16, 52, 7, deck + 1, deck + 4), (20, 48, 6, deck + 5, deck + 8), (18, 26, 5, deck + 9, deck + 12)]
    for (za, zb, hw, ya, yb) in tiers:
        for y in range(ya, yb + 1):
            for z in range(za, zb + 1):
                for x in range(cx - hw, cx + hw + 1):
                    edge = x in (cx - hw, cx + hw) or z in (za, zb)
                    if y == yb:
                        t.put(x, y, z, "smooth_quartz")
                    elif edge:
                        t.put(x, y, z, "light_blue_stained_glass" if y == ya + 1 and (z + x) % 2 else "white_concrete")
                    else:
                        t.put(x, y, z, "air")
    t.door(cx, deck + 1, 16, "birch_door", "north")
    # the dining hall (first tier): tables with cakes, red carpet, chandeliers
    for z in range(18, 51):
        for x in range(cx - 6, cx + 7):
            if t.get(x, deck + 1, z) == "minecraft:air":
                t.put(x, deck + 1, z, "red_carpet")
    for z in range(20, 50, 5):
        for x in (cx - 3, cx + 3):
            t.put(x, deck + 1, z, "dark_oak_fence", {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"})
            t.put(x, deck + 2, z, "cake", {"bites": "0"})
        t.put(cx, deck + 3, z, "lantern", {"hanging": "true", "waterlogged": "false"})
    chest(t, cx + 6, deck + 1, 50, "west", "ss_anne_galley")
    # cabins (second tier) and the bridge (third)
    for z in range(22, 47, 4):
        for x in (cx - 4, cx + 4):
            t.put(x, deck + 5, z, "white_bed", {"facing": "south", "part": "foot", "occupied": "false"})
            t.put(x, deck + 5, z + 1, "white_bed", {"facing": "south", "part": "head", "occupied": "false"})
    ladder(t, cx + 5, deck + 1, deck + 4, 30, "west")
    t.put(cx + 5, deck + 4, 30, "ladder", {"facing": "west", "waterlogged": "false"})
    ladder(t, cx + 4, deck + 5, deck + 8, 22, "west")
    t.put(cx - 2, deck + 9, 19, "cobblemon:lectern", {"facing": "south"})
    t.put(cx, deck + 9, 19, "cobblemon:monitor", {"facing": "south", "screen": "blue_progress_5"})
    chest(t, cx + 2, deck + 9, 19, "south", "ss_anne_captain")
    for x in range(cx - 4, cx + 5):
        pane(t, x, deck + 10, 18, axis="x")
    # two funnels and two masts
    for fz in (31, 40):
        for y in range(deck + 9, deck + 20):
            disc(t, cx, y, fz, 2.4, "black_concrete" if y >= deck + 17 else "red_concrete" if y in (deck + 14, deck + 15) else "white_concrete", hollow=True)
    for mz, top in ((6, deck + 18), (62, deck + 14)):
        for y in range(deck + 1, top):
            t.put(cx, y, mz, "spruce_fence", {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"})
        t.put(cx, top, mz, "lantern", {"hanging": "false", "waterlogged": "false"})
    t.put(cx - 1, deck + 1, 3, "chain", {"axis": "y", "waterlogged": "false"})
    return t


# --- Gen 1: the Lavender Town Tower -----------------------------------------------------------------------------------
def lavender_tower():
    """A seven-floor tower of dark blackstone bricks banded in purple terracotta with tall violet windows and tiered
    purple roofs. Every floor holds rows of gravestones (candles, dead bushes and wither roses in pots), cobwebs and
    soul lanterns; stairs climb round the walls; the top floor is a candlelit memorial with a chest."""
    W, H, Dp = 19, 49, 19
    t = S((W, H, Dp))
    g = 1
    ground_fill(t, W, Dp, g - 1 if g > 0 else 0, "grass_block", "dirt", 1)
    x0, x1, z0, z1 = 2, 16, 2, 16
    floors = 7
    for f in range(floors):
        fy = g + f * 5
        t.box(x0, fy, z0, x1, fy, z1, "polished_blackstone_bricks" if f == 0 else "dark_oak_planks")
        for y in range(fy + 1, fy + 5):
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    wall = x in (x0, x1) or z in (z0, z1)
                    if wall:
                        band = y == fy + 4
                        corner = x in (x0, x1) and z in (z0, z1)
                        t.put(x, y, z, "purple_terracotta" if band else "polished_blackstone" if corner else "polished_blackstone_bricks")
                    else:
                        t.put(x, y, z, "air")
        for c in (6, 9, 12):                                           # tall violet windows
            for y in (fy + 2, fy + 3):
                pane(t, c, y, z0, "purple_stained_glass_pane", "x")
                pane(t, c, y, z1, "purple_stained_glass_pane", "x")
                pane(t, x0, y, c, "purple_stained_glass_pane", "z")
                pane(t, x1, y, c, "purple_stained_glass_pane", "z")
        # gravestones
        if f < floors - 1:
            for z in (6, 9, 12):
                for x in range(5, 14, 2):
                    if (f, x, z) in ((0, 9, 6), (0, 9, 9)):
                        continue
                    t.put(x, fy + 1, z, pick([("cobblestone_wall", 3), ("mossy_cobblestone_wall", 2), ("stone_brick_wall", 2)], x, z, f))
                    r = h(x, z, f, 7)
                    if r < 0.25:
                        candle(t, x, fy + 2, z, "white", 1 + int(r * 8) % 3)
                    elif r < 0.4:
                        t.put(x, fy + 1, z + 1, "potted_wither_rose")
                    elif r < 0.55:
                        t.put(x, fy + 1, z + 1, "potted_dead_bush")
            for x, z in ((x0 + 1, z0 + 1), (x1 - 1, z0 + 1), (x0 + 1, z1 - 1), (x1 - 1, z1 - 1)):
                t.put(x, fy + 4, z, "cobweb")
            t.put(9, fy + 4, 9, "soul_lantern", {"hanging": "true", "waterlogged": "false"})
        # the stairs up (alternating sides along the back wall)
        if f < floors - 1:
            if f % 2 == 0:
                stairs_up(t, 4, fy + 1, 15, +1, 5, "polished_blackstone_brick", 4)
            else:
                stairs_up(t, 14, fy + 1, 15, -1, 5, "polished_blackstone_brick", 4)
        if f in (2, 4):
            chest(t, x1 - 1, fy + 1, 9, "west", "lavender_tower")
    t.door(9, g + 1, z0, "dark_oak_door", "south")
    candle(t, 8, g + 1, z0 + 1, "purple", 3)
    candle(t, 10, g + 1, z0 + 1, "purple", 3)
    # the top floor memorial
    fy = g + (floors - 1) * 5
    t.box(7, fy + 1, 7, 11, fy + 1, 11, "chiseled_stone_bricks")
    t.put(9, fy + 2, 9, "chiseled_stone_bricks")
    for x, z in ((7, 7), (11, 7), (7, 11), (11, 11)):
        candle(t, x, fy + 2, z, "white", 4)
    for x, z in ((8, 7), (10, 7), (8, 11), (10, 11)):
        t.put(x, fy + 2, z, "potted_lily_of_the_valley")
    chest(t, 9, fy + 2, 10, "north", "lavender_tower_top")
    t.put(9, fy + 4, 9, "soul_lantern", {"hanging": "true", "waterlogged": "false"})
    # the tiered roofs
    ry = g + floors * 5
    for k, r in enumerate((9, 7, 5, 3, 1)):
        for x in range(9 - r, 10 + r):
            for z in range(9 - r, 10 + r):
                if max(abs(x - 9), abs(z - 9)) == r:
                    t.put(x, ry + k * 2, z, "purple_terracotta")
                    t.put(x, ry + k * 2 + 1, z, "purpur_slab" if r > 1 else "amethyst_block", {"type": "bottom", "waterlogged": "false"} if r > 1 else None)
                elif max(abs(x - 9), abs(z - 9)) < r:
                    t.put(x, ry + k * 2, z, "purple_terracotta" if k == 0 else "polished_blackstone_bricks")
    t.put(9, ry + 10, 9, "lightning_rod", {"facing": "up", "powered": "false", "waterlogged": "false"})
    clear_above(t, 0, 0, W - 1, Dp - 1, g)
    return t


# --- Gen 1: the Celadon Rocket Hideout ---------------------------------------------------------------------------------
def rocket_hideout():
    """A flashy game corner (red and gold facade, a glowing marquee, rows of jukebox slot machines) over a three-floor
    basement reached by a hidden hatch behind the prize counter: grey concrete corridors lit by lamps, arrow-tile
    spinner floors, a storeroom, a lab with brewing stands and monitors, and the boss's office with the best chest."""
    W, Dp = 25, 23
    G = 18                                          # template y of ground level (start_height -18)
    H = G + 11
    t = S((W, H, Dp))
    t.box(0, 0, 0, W - 1, G - 1, Dp - 1, "stone")
    ground_fill(t, W, Dp, G - 1, "grass_block", "dirt", 0)
    # the game corner
    x0, x1, z0, z1 = 2, 22, 3, 19
    t.box(x0, G - 1, z0, x1, G - 1, z1, "red_concrete")
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            t.put(x, G - 1, z, "black_concrete" if (x + z) % 2 else "red_concrete")
    for y in range(G, G + 7):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                wall = x in (x0, x1) or z in (z0, z1)
                if wall:
                    c = "yellow_terracotta" if y in (G + 5,) else "red_terracotta"
                    if z == z0 and y == G + 6:
                        c = "glowstone" if x % 2 else "gold_block"
                    t.put(x, y, z, c)
                else:
                    t.put(x, y, z, "air")
    t.box(x0, G + 7, z0, x1, G + 7, z1, "smooth_stone")
    for x in range(x0 + 2, x1 - 1, 3):                               # front windows
        for y in (G + 1, G + 2, G + 3):
            if x not in (11, 12, 13):
                pane(t, x, y, z0, "orange_stained_glass_pane", "x")
    for x in (11, 13):
        t.door(x, G, z0, "iron_door", "south", "left" if x == 11 else "right")
    for y in (G, G + 1):
        t.put(12, y, z0, "air")
    # slot machine rows
    for z in range(7, 16, 3):
        for x in range(5, 20):
            if x in (11, 12, 13):
                continue
            t.put(x, G, z, "jukebox", {"has_record": "false"})
            t.put(x, G + 1, z, "redstone_lamp", {"lit": "true"} if x % 2 else {"lit": "false"})
    # the prize counter and the hidden hatch
    for x in range(15, 21):
        t.put(x, G, 17, "polished_andesite")
    t.put(20, G + 1, 17, "cobblemon:display_case", {"facing": "north"})
    trapdoor(t, 21, G - 1, 18, "spruce_trapdoor", "north", "top")
    ladder(t, 21, 3, G - 2, 18, "north")
    # the basement: three floors, 4 blocks tall each
    for fl, fy in enumerate((13, 8, 3)):
        for x in range(3, 22):
            for z in range(3, 20):
                t.put(x, fy - 1, z, "polished_andesite")
                for y in range(fy, fy + 4):
                    t.put(x, y, z, "gray_concrete" if (x in (3, 21) or z in (3, 19)) else "air")
        # internal walls: a cross of corridors with rooms
        for x in range(4, 21):
            for y in range(fy, fy + 3):
                if x not in (7, 8, 16, 17):
                    t.put(x, y, 11, "light_gray_concrete")
        for z in range(4, 19):
            for y in range(fy, fy + 3):
                if z not in (7, 15):
                    t.put(12, y, z, "light_gray_concrete")
        for x in range(5, 20, 3):
            for z in range(5, 19, 3):
                lamp(t, x, fy + 3, z)
        # arrow-tile spinner patches
        for x in range(13, 21):
            for z in range(4, 11):
                if (x + z + fl) % 3 == 0:
                    t.put(x, fy - 1, z, "magenta_glazed_terracotta", {"facing": ["north", "east", "south", "west"][(x * 7 + z + fl) % 4]})
    ladder(t, 21, 3, G - 2, 18, "north")
    for fy in (13, 8, 3):
        for y in range(fy, fy + 4):
            t.put(21, y, 18, "ladder", {"facing": "north", "waterlogged": "false"})
        t.put(20, fy, 18, "air")
    for fy in (13, 8):
        t.put(21, fy - 1, 18, "ladder", {"facing": "north", "waterlogged": "false"})
    # B1 storeroom, B2 lab, B3 the boss's office
    for x in range(4, 11):
        if x % 3 == 1:
            barrel(t, x, 13, 4, "rocket_hideout")
        else:
            t.put(x, 13, 4, "barrel", {"facing": "up", "open": "false"})
    chest(t, 5, 13, 10, "north", "rocket_hideout")
    for x in (4, 6, 8, 10):
        t.put(x, 8, 4, "brewing_stand", {"has_bottle_0": "false", "has_bottle_1": "false", "has_bottle_2": "false"})
        t.put(x, 8, 18, "cauldron")
    t.put(5, 9, 4, "cobblemon:monitor", {"facing": "south", "screen": "porygon_glitching"})
    t.put(9, 9, 4, "cobblemon:monitor", {"facing": "south", "screen": "blue_progress_7"})
    chest(t, 18, 8, 18, "north", "rocket_hideout")
    for x in range(4, 12):
        for z in range(12, 19):
            t.put(x, 3, z, "red_carpet")
    for x in (6, 7, 8, 9):
        t.slab(x, 3, 16, "dark_oak", "top")
    chest(t, 7, 3, 18, "north", "rocket_boss")
    t.put(8, 3, 18, "cobblemon:pc", {"facing": "north", "part": "bottom", "on": "false"})
    t.put(8, 4, 18, "cobblemon:pc", {"facing": "north", "part": "top", "on": "false"})
    clear_above(t, 0, 0, W - 1, Dp - 1, G)
    return t


# --- Gen 1: the Cinnabar Pokémon Lab -----------------------------------------------------------------------------------
def cinnabar_lab():
    """A two-storey white research lab with grey bands, wide windows and a rooftop dish. Nearly every machine of
    Cobblemon, Mega Showdown and CobbleEffort: Distortion works inside: healing machines and PCs in the lobby; two
    fossil restoration stations (analyzer, monitor, restoration tank); the DNA lab (DNA machine, analyzer, purifier)
    where Mewtwo was made; the Rotom appliance lab (all five units); a reassembly unit, pedestals and a power spot;
    upstairs the TM machines, display cases, a disc shelf and a lectern, a kitchen with campfire pots, gilded chests
    and the glitchy PC; a pasture in the fenced yard behind."""
    W, H, Dp = 35, 14, 33
    t = S((W, H, Dp))
    g = 1
    ground_fill(t, W, Dp, g - 1, "grass_block", "dirt", 0)
    x0, x1, z0, z1 = 2, 32, 2, 24
    for y in range(g, g + 11):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                wall = x in (x0, x1) or z in (z0, z1)
                if y in (g, g + 5):
                    t.put(x, y, z, "light_gray_concrete" if wall else ("smooth_quartz" if (x + z) % 2 else "white_concrete"))
                elif y == g + 10:
                    t.put(x, y, z, "light_gray_concrete")
                elif wall:
                    band = y in (g + 4, g + 9)
                    win = y in (g + 2, g + 3, g + 7, g + 8) and ((x % 4 in (1, 2) and z in (z0, z1)) or (z % 4 in (1, 2) and x in (x0, x1)))
                    t.put(x, y, z, "light_gray_concrete" if band else "light_blue_stained_glass" if win else "white_concrete")
                else:
                    t.put(x, y, z, "air")
    for y in (g + 1, g + 2):                                       # the entrance
        for x in (16, 17, 18):
            t.put(x, y, z0, "air")
    t.box(15, g + 3, z0 - 1, 19, g + 3, z0 - 1, "smooth_quartz_slab", {"type": "bottom", "waterlogged": "false"})
    # inner walls (ground floor): lobby in the middle, fossil room west, Rotom lab east, DNA lab at the back
    for z in range(z0 + 1, z1):
        for y in range(g + 1, g + 5):
            if z not in (8, 9, 18, 19):
                t.put(11, y, z, "white_concrete")
                t.put(23, y, z, "white_concrete")
    for x in range(x0 + 1, x1):
        for y in range(g + 1, g + 5):
            if x not in (16, 17, 18):
                t.put(x, y, 15, "white_concrete")
    for x in range(4, 31, 3):
        for z in range(4, 24, 4):
            t.put(x, g + 4, z, "sea_lantern")
            t.put(x, g + 9, z, "sea_lantern")
    # lobby: healing machines, PCs, a reception desk
    for x in (13, 14):
        t.put(x, g + 1, 13, "cobblemon:healing_machine", {"facing": "south", "charge": "6", "natural": "true"})
    two(t, 20, g + 1, 13, "cobblemon:pc", "south", on="false")
    two(t, 21, g + 1, 13, "cobblemon:pc", "south", on="false")
    for x in range(15, 20):
        t.put(x, g + 1, 10, "quartz_bricks")
    t.put(17, g + 2, 10, "cobblemon:monitor", {"facing": "north", "screen": "porygon_grid"})
    # fossil room (west): two restoration stations
    for z in (5, 10):
        t.put(4, g + 1, z, "cobblemon:fossil_analyzer", {"facing": "east", "on": "false"})
        t.put(4, g + 2, z, "cobblemon:monitor", {"facing": "east", "screen": "off"})
        two(t, 4, g + 1, z + 1, "cobblemon:restoration_tank", "east", on="false", triggered="false")
    for z in (4, 12):
        t.put(9, g + 1, z, "cobblemon:display_case", {"facing": "west"})
    chest(t, 9, g + 1, 7, "west", "cinnabar_fossils")
    # Rotom appliance lab (east): the five units, a reassembly unit, pedestals, a power spot
    for i, unit in enumerate(("rotom_fan", "rotom_fridge", "rotom_mow", "rotom_oven", "rotom_washing_machine")):
        t.put(30, g + 1, 4 + i * 2, f"mega_showdown:{unit}", {"facing": "west"})
    two(t, 26, g + 1, 13, "mega_showdown:reassembly_unit", "north", key="half", lo="lower", hi="upper", reassemble_stage="idle")
    for x in (25, 27):
        t.put(x, g + 1, 5, "mega_showdown:pedestal", {"facing": "south"})
    t.put(26, g + 1, 9, "mega_showdown:power_spot")
    # DNA lab (back): Distortion's DNA machine with its analyzer and purifier
    two(t, 17, g + 1, 22, "cobbleeffort_distortion:dna_machine", "north", key="half", lo="lower", hi="upper")
    t.put(15, g + 1, 22, "cobbleeffort_distortion:dna_analyzer", {"facing": "north"})
    t.put(19, g + 1, 22, "cobbleeffort_distortion:dna_purifier", {"facing": "north"})
    t.put(13, g + 1, 23, "cobblemon:damaged_monitor", {"facing": "north", "screen": "glitching"})
    chest(t, 21, g + 1, 23, "north", "cinnabar_lab")
    for x in range(4, 11):
        t.put(x, g + 1, 23, "bookshelf")
    for x in range(24, 31):
        t.put(x, g + 1, 23, "bookshelf")
    # stairs to the upper floor
    stairs_up(t, 25, g + 1, 17, +1, 5, "quartz", 3)
    for x in range(25, 31):
        t.put(x, g + 5, 17, "air")
        t.put(x, g + 5, 18, "air")
    # upstairs: TM room, displays, kitchen, gilded chests, the glitchy PC
    for x in (4, 6):
        t.put(x, g + 6, 4, "cobblemon:tm_machine", {"facing": "south", "empty": "true", "open": "false", "active": "false", "dispensed": "false"})
    for x, screen in ((8, "tm_fire"), (9, "tm_water"), (10, "tm_grass")):
        t.put(x, g + 6, 4, "cobblemon:monitor", {"facing": "south", "screen": screen})
    for x in range(13, 22, 2):
        t.put(x, g + 6, 12, "cobblemon:display_case", {"facing": "south"})
    t.put(23, g + 6, 4, "cobblemon:disc_shelf", {"facing": "south"})
    t.put(25, g + 6, 4, "cobblemon:lectern", {"facing": "south"})
    for x, colour in ((5, "red"), (7, "blue"), (9, "yellow")):
        t.put(x, g + 6, 22, f"cobblemon:campfire_pot_{colour}", {"facing": "north", "open": "false", "occupied": "false"})
    for x, colour in ((28, ""), (29, "blue_"), (30, "green_")):
        t.put(x, g + 6, 22, f"cobblemon:{colour}gilded_chest")
    t.put(17, g + 6, 23, f"{MOD}:glitchy_pc")
    chest(t, 30, g + 6, 12, "west", "cinnabar_lab")
    # the rooftop dish
    for y in range(g + 11, g + 13):
        t.put(28, y, 6, "iron_bars", {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"})
    for x in range(26, 31):
        for z in range(4, 9):
            if math.hypot(x - 28, z - 6) <= 2.3:
                t.put(x, g + 13, z, "iron_block" if math.hypot(x - 28, z - 6) > 1 else "lightning_rod",
                      None if math.hypot(x - 28, z - 6) > 1 else {"facing": "up", "powered": "false", "waterlogged": "false"})
    # the pasture yard behind
    for x in range(8, 27):
        for z in (26, 31):
            t.fence(x, g, z, "birch_fence")
    for z in range(26, 32):
        for x in (8, 26):
            t.fence(x, g, z, "birch_fence")
    two(t, 17, g, 28, "cobblemon:pasture", "north", on="false")
    t.put(17, g, 26, "birch_fence_gate", {"facing": "north", "in_wall": "false", "open": "false", "powered": "false"})
    clear_above(t, 0, 0, W - 1, Dp - 1, g)
    return t


# --- shared terrain helpers -------------------------------------------------------------------------------------------
FONT = {"A": ["010", "101", "111", "101", "101"], "L": ["100", "100", "100", "100", "111"],
        "P": ["110", "101", "110", "100", "100"], "H": ["101", "101", "111", "101", "101"]}


def glyph(t, letter, x0, y0, z, ink, ground, dx=1):
    """A 3x5 letter in the plane z (x0 is its left as you face it from -z; dx=-1 draws it mirrored for a back wall
    seen from inside)."""
    for r, row in enumerate(FONT[letter]):
        for c, ch in enumerate(row):
            t.put(x0 + dx * c, y0 + 4 - r, z, ink if ch == "1" else ground)


def mound(t, cx, cz, radius, peak, base_y, seed, rough=3.0, mats=("stone",), top=None, cell=6.0):
    """A rough hill or mountain: height falls off with distance, plus noise; returns the height map {(x, z): y}."""
    hm = {}
    W, _, Dp = t.size
    for x in range(W):
        for z in range(Dp):
            r = math.hypot(x - cx, z - cz) / radius
            if r > 1:
                continue
            hgt = base_y + peak * (1 - r ** 1.6) + (noise(x, z, seed, cell) - 0.5) * rough * 2 * (1 - r * 0.5)
            hy = int(hgt)
            hm[(x, z)] = hy
            for y in range(base_y, hy + 1):
                m = mats[int(h(x, y, z, seed) * len(mats))]
                if y == hy and top:
                    m = top
                t.put(x, y, z, m)
    return hm


def spiral_stairs(t, cx, cz, r, y0, y1, mat, solid):
    """A stair climbing round a square shaft (radius r, open centre) from y0 to y1; the shaft walls are `solid`."""
    ring = []
    for x in range(cx - r, cx + r + 1):
        ring.append((x, cz - r))
    for z in range(cz - r + 1, cz + r + 1):
        ring.append((cx + r, z))
    for x in range(cx + r - 1, cx - r - 1, -1):
        ring.append((x, cz + r))
    for z in range(cz + r - 1, cz - r, -1):
        ring.append((cx - r, z))
    for y in range(y0, y1 + 4):
        for x in range(cx - r - 1, cx + r + 2):
            for z in range(cz - r - 1, cz + r + 2):
                edge = max(abs(x - cx), abs(z - cz)) == r + 1
                t.put(x, y, z, solid if edge else "air")
        t.put(cx, y, cz, solid)
    i = 0
    for y in range(y0, y1 + 1):
        x, z = ring[i % len(ring)]
        nx, nz = ring[(i + 1) % len(ring)]
        facing = "east" if nx > x else "west" if nx < x else "south" if nz > z else "north"
        t.stair(x, y, z, mat, facing)
        if y > y0:
            px, pz = ring[(i - 1) % len(ring)]
            t.put(px, y, pz, solid)
        i += 1


# --- Gen 2: the Ruins of Alph ---------------------------------------------------------------------------------------
def ruins_of_alph():
    """Grass-grown ruins: crumbling mossy walls and broken pillars round four stone chambers, each half sunk in the
    ground, carved inside with tuff glyphs, a puzzle panel of coloured tiles on its back wall and one great letter of
    A-L-P-H; in the middle a researchers' tent with a lectern, a monitor and their notes. Unown live in the chambers."""
    W, H, Dp = 43, 14, 43
    t = S((W, H, Dp))
    g = 3
    ground_fill(t, W, Dp, g, "grass_block", "dirt", 3)
    for x in range(W):
        for z in range(Dp):
            if noise(x, z, 11, 5) > 0.66:
                t.put(x, g, z, pick([("coarse_dirt", 3), ("gravel", 2), ("mossy_cobblestone", 1)], x, z, 1))
    stones = [("stone_bricks", 3), ("mossy_stone_bricks", 3), ("cracked_stone_bricks", 2)]
    for i, (cx, cz, letter) in enumerate(((10, 10, "A"), (32, 10, "L"), (10, 32, "P"), (32, 32, "H"))):
        x0, x1, z0, z1 = cx - 5, cx + 5, cz - 5, cz + 5
        fy = g - 2                                              # half sunk
        t.box(x0, fy - 1, z0, x1, fy - 1, z1, "chiseled_stone_bricks")
        for y in range(fy, g + 5):
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    wall = x in (x0, x1) or z in (z0, z1)
                    if y >= g + 4 - (1 if h(x, z, i) < 0.4 else 0) and wall and not (x in (x0, x1) and z in (z0, z1)):
                        t.put(x, y, z, "air" if h(x, y, z) < 0.5 else pick(stones, x, y, z))
                    elif wall:
                        inner = "chiseled_tuff" if (x + y + z) % 3 == 0 else "tuff_bricks"
                        t.put(x, y, z, inner if y < g + 2 else pick(stones, x, y, z))
                    else:
                        t.put(x, y, z, "air")
        t.box(x0, g + 4, z0, x1, g + 4, z1, "stone_brick_slab", {"type": "bottom", "waterlogged": "false"})
        for x in range(x0 + 1, x1):
            for z in range(z0 + 1, z1):
                if h(x, z, i, 3) < 0.35:
                    t.put(x, g + 4, z, "air")                      # a broken roof lets the light in
        door = (cx, z1) if cz < 20 else (cx, z0)
        for y in (fy, fy + 1, fy + 2):
            t.put(door[0], y, door[1], "air")
        step_dz = 1 if cz < 20 else -1
        for k in range(1, 3):
            t.stair(door[0], fy + k - 1, door[1] + step_dz * k, "stone_brick", "north" if cz < 20 else "south")
            t.put(door[0], fy + k, door[1] + step_dz * k, "air")
        back = z0 if cz < 20 else z1
        colours = ["orange_terracotta", "yellow_terracotta", "brown_terracotta", "white_terracotta"]
        for a in range(4):
            for b in range(4):
                t.put(cx - 2 + a, fy + 1 + b, back, colours[(a * 3 + b * 7 + i) % 4])
        side = x0 if cx < 20 else x1
        for r_, row in enumerate(FONT[letter]):
            for c_, ch in enumerate(row):
                t.put(side, fy + 4 - r_, cz - 1 + c_, "polished_blackstone" if ch == "1" else "calcite")
        if i in (0, 3):
            chest(t, x1 - 1, fy, cz, "west", "ruins_of_alph")
    # broken walls and pillars about the field
    for k in range(18):
        x = 4 + int(h(k, 1, 7) * (W - 8))
        z = 4 + int(h(k, 2, 7) * (Dp - 8))
        if any(abs(x - cx) < 8 and abs(z - cz) < 8 for cx, cz in ((10, 10), (32, 10), (10, 32), (32, 32), (21, 21))):
            continue
        hgt = 1 + int(h(k, 3, 7) * 4)
        if k % 3 == 0:
            for y in range(g + 1, g + 1 + hgt):
                t.put(x, y, z, "chiseled_stone_bricks" if y == g + hgt else pick(stones, x, y, z))
        else:
            for j in range(3 + k % 3):
                for y in range(g + 1, g + 1 + max(1, hgt - j)):
                    t.put(x + j, y, z, pick(stones, x + j, y, z))
    # the researchers' tent
    for x in range(18, 25):
        for z in range(18, 25):
            t.put(x, g, z, "spruce_planks")
    for x in range(18, 25):
        for k, z in enumerate(range(18, 25)):
            hy = g + 1 + min(k, 6 - k)
            for y in range(g + 1, hy + 1):
                if x in (18, 24) and y < hy:
                    if z not in (21,):
                        t.put(x, y, z, "air")
                t.put(x, hy, z, "white_wool")
    t.put(21, g + 1, 23, "cobblemon:lectern", {"facing": "north"})
    t.put(20, g + 1, 23, "crafting_table")
    t.put(22, g + 1, 23, "cobblemon:monitor", {"facing": "north", "screen": "blue_progress_3"})
    chest(t, 19, g + 1, 23, "north", "ruins_of_alph_camp")
    t.put(21, g + 3, 21, "lantern", {"hanging": "true", "waterlogged": "false"})
    clear_above(t, 0, 0, W - 1, Dp - 1, g + 1)
    return t


# --- Gen 2: the Lake of Rage ------------------------------------------------------------------------------------------
def lake_of_rage():
    """A round lake in the woods, deepest in the middle, ringed by sand, reeds and lily pads, with spruces round it.
    A fisherman's hut stands on the shore and a dock runs out over the water to a shrine: it calls the red Gyarados
    up from the depths (once for each trainer, until caught)."""
    W, H, Dp = 49, 16, 49
    t = S((W, H, Dp))
    g = 6
    cx, cz, R = 24, 22, 17.5
    ground_fill(t, W, Dp, g, "grass_block", "dirt", 5)
    for x in range(W):
        for z in range(Dp):
            d = math.hypot(x - cx, z - cz) + (noise(x, z, 5, 5) - 0.5) * 3
            if d < R:
                depth = 1 + int((1 - d / R) * 5)
                for y in range(g - depth + 1, g + 1):
                    t.put(x, y, z, "water", {"level": "0"})
                t.put(x, g - depth, z, "sand" if depth < 3 else "gravel" if depth < 5 else "clay")
                if d > R - 2.5 and h(x, z, 9) < 0.18:
                    t.put(x, g + 1, z, "lily_pad")
            elif d < R + 2.2:
                t.put(x, g, z, "sand")
                if h(x, z, 4) < 0.12:
                    for y in (g + 1, g + 2):
                        t.put(x, y, z, "sugar_cane", {"age": "0"})
    # the dock and the shrine at its end
    for z in range(int(cz + R) + 2, int(cz + R) - 10, -1):
        for x in (23, 24, 25):
            t.put(x, g + 1, z, "spruce_planks")
        if z % 3 == 0:
            for x in (23, 25):
                t.log(x, g, z, "spruce_log")
                t.fence(x, g + 2, z, "spruce_fence")
    end = int(cz + R) - 9
    shrine(t, 24, g + 2, end, "altar", key="red_gyarados", mode="encounter", props="gyarados shiny=yes level=30",
           dx=0, dy=-1, dz=-5, label=f"{MOD}.shrine.red_gyarados")
    for x in (23, 25):
        t.put(x, g + 2, end, "lantern", {"hanging": "false", "waterlogged": "false"})
    # the fisherman's hut
    hx0, hx1, hz0, hz1 = 36, 42, 38, 44
    t.box(hx0, g, hz0, hx1, g, hz1, "spruce_planks")
    for y in range(g + 1, g + 5):
        for x in range(hx0, hx1 + 1):
            for z in range(hz0, hz1 + 1):
                wall = x in (hx0, hx1) or z in (hz0, hz1)
                t.put(x, y, z, ("spruce_log" if x in (hx0, hx1) and z in (hz0, hz1) else "spruce_planks") if wall else "air")
    t.box(hx0 - 1, g + 5, hz0 - 1, hx1 + 1, g + 5, hz1 + 1, "spruce_slab", {"type": "bottom", "waterlogged": "false"})
    t.door(39, g + 1, hz0, "spruce_door", "north")
    pane(t, hx0, g + 2, 41, axis="z")
    chest(t, 41, g + 1, 43, "north", "lake_of_rage")
    barrel(t, 37, g + 1, 43, "lake_of_rage")
    t.put(39, g + 4, 41, "lantern", {"hanging": "true", "waterlogged": "false"})
    # spruces round the lake
    for k in range(14):
        a = k / 14 * 2 * math.pi + 0.3
        x, z = int(cx + math.cos(a) * (R + 5)), int(cz + math.sin(a) * (R + 5))
        if not (0 < x < W - 1 and 0 < z < Dp - 1) or (20 < x < 28 and z > 36) or (34 < x < 44 and 36 < z < 46):
            continue
        hgt = 5 + int(h(k, 5) * 3)
        for y in range(g + 1, g + 1 + hgt):
            t.log(x, y, z, "spruce_log")
        for y in range(g + 3, g + 2 + hgt):
            r = 2 if y < g + hgt - 1 else 1
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if (dx or dz) and abs(dx) + abs(dz) <= r + 1:
                        t.leaves(x + dx, y, z + dz, "spruce_leaves")
        t.leaves(x, g + 1 + hgt, z, "spruce_leaves")
    clear_above(t, 0, 0, W - 1, Dp - 1, g + 1)
    return t


# --- Gen 2: the Mahogany Rocket HQ --------------------------------------------------------------------------------------
def rocket_hq_mahogany():
    """A little snow-roofed souvenir shop (shelves of barrels, display cases, a counter) whose back room hides a stair
    down to a two-floor base: corridors watched by target-block 'Electrode traps', a warehouse, a lab, the radio
    transmitter room (an antenna mast of iron bars and lightning rods, lamps and note blocks) and the boss's office."""
    W, Dp = 29, 27
    G = 14
    H = G + 10
    t = S((W, H, Dp))
    t.box(0, 0, 0, W - 1, G - 1, Dp - 1, "stone")
    ground_fill(t, W, Dp, G - 1, "grass_block", "dirt", 0)
    # the shop
    x0, x1, z0, z1 = 8, 20, 3, 13
    t.box(x0, G - 1, z0, x1, G - 1, z1, "spruce_planks")
    for y in range(G, G + 5):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                wall = x in (x0, x1) or z in (z0, z1)
                corner = x in (x0, x1) and z in (z0, z1)
                t.put(x, y, z, ("spruce_log" if corner else "birch_planks") if wall else "air")
    for k in range(0, 7):
        y = G + 5 + k
        za, zb = z0 - 1 + k, z1 + 1 - k
        if za > zb:
            break
        for x in range(x0 - 1, x1 + 2):
            if za == zb:
                t.put(x, y, za, "snow_block")
            else:
                t.stair(x, y, za, "spruce", "south")
                t.stair(x, y, zb, "spruce", "north")
                t.put(x, y + 1, za, "snow", {"layers": "1"})
                t.put(x, y + 1, zb, "snow", {"layers": "1"})
                for z in range(za + 1, zb):
                    if x in (x0, x1):
                        t.put(x, y, z, "birch_planks")
    t.door(14, G, z0, "spruce_door", "south")
    for x in (10, 11, 17, 18):
        pane(t, x, G + 1, z0, axis="x")
    for x in range(10, 19):
        if x in (13, 14, 15):
            continue
        t.put(x, G, 7, "barrel", {"facing": "up", "open": "false"})
        t.put(x, G + 1, 7, "cobblemon:display_case", {"facing": "south"})
    for x in range(10, 19):
        t.put(x, G, 10, "spruce_planks")
    chest(t, 10, G, 12, "south", "rocket_hq_shop")
    # the hidden stair down (behind the counter, in the back corner)
    ladder(t, 19, 4, G - 1, 12, "north")
    trapdoor(t, 19, G - 1, 12, "spruce_trapdoor", "north", "top")
    # two basement floors
    for fl, fy in enumerate((9, 4)):
        for x in range(2, 27):
            for z in range(2, 25):
                t.put(x, fy - 1, z, "polished_andesite" if (x + z) % 2 else "andesite")
                for y in range(fy, fy + 4):
                    t.put(x, y, z, "gray_concrete" if x in (2, 26) or z in (2, 24) else "air")
        for z in range(3, 24):
            for y in range(fy, fy + 3):
                if z not in (6, 7, 17, 18):
                    t.put(10, y, z, "light_gray_concrete")
                    t.put(18, y, z, "light_gray_concrete")
        for x in range(3, 26):
            for y in range(fy, fy + 3):
                if x not in (6, 14, 22):
                    t.put(x, y, 12, "light_gray_concrete")
        for x in range(4, 26, 4):
            for z in range(4, 24, 4):
                lamp(t, x, fy + 3, z)
        for x, z in ((14, 5), (14, 20), (6, 15), (22, 9)):
            t.put(x, fy, z, "target", {"power": "0"})               # 'Electrode traps'
    for fy in (9, 4):
        for y in range(fy, fy + 4):
            t.put(19, y, 12, "ladder", {"facing": "north", "waterlogged": "false"})
    # B1: warehouse and lab; B2: radio room and the boss's office
    for x in range(3, 10):
        for z in range(13, 24):
            if (x + z) % 3 == 0:
                t.put(x, 9, z, "barrel", {"facing": "up", "open": "false"})
    chest(t, 4, 9, 23, "north", "rocket_hq")
    for x in (20, 22, 24):
        t.put(x, 9, 3, "brewing_stand", {"has_bottle_0": "false", "has_bottle_1": "false", "has_bottle_2": "false"})
    t.put(21, 10, 3, "cobblemon:monitor", {"facing": "south", "screen": "blue_progress_9"})
    for y in range(4, 8):
        t.put(14, y, 21, "iron_bars", {"north": "false", "south": "false", "east": "false", "west": "false", "waterlogged": "false"})
    t.put(14, 8, 21, "lightning_rod", {"facing": "up", "powered": "false", "waterlogged": "false"})
    for x in (12, 16):
        for y in (4, 5):
            t.put(x, y, 21, "note_block", {"instrument": "harp", "note": "0", "powered": "false"})
        t.put(x, 6, 21, "redstone_lamp", {"lit": "true"})
    for x in (13, 15):
        t.put(x, 4, 21, "waxed_copper_block")
    for x in range(20, 26):
        for z in range(13, 24):
            t.put(x, 4, z, "red_carpet")
    chest(t, 23, 4, 23, "north", "rocket_boss")
    clear_above(t, 0, 0, W - 1, Dp - 1, G)
    return t


# --- Gen 3: Meteor Falls ---------------------------------------------------------------------------------------------
def meteor_falls():
    """A craggy hill of stone, tuff and andesite with a cave mouth. Inside, a great cavern: a waterfall pours from a
    high ledge into a clear pool, meteorite chunks (obsidian, crying obsidian, Mega Showdown's meteorite blocks) are
    sunk in the walls, dripstone hangs from the roof, glowstone glints, and a dragon's den hides at the back."""
    W, H, Dp = 47, 36, 43
    t = S((W, H, Dp))
    cx, cz = 23, 23
    hm = mound(t, cx, cz, 23, 28, 1, 21, 4.0, ("stone", "stone", "tuff", "andesite", "cobblestone"), None, 7)
    for (x, z), y in hm.items():
        if y > 3:
            t.put(x, y, z, "grass_block" if y < 18 else "stone", {"snowy": "false"} if y < 18 else None)
    # the cavern
    for x in range(W):
        for y in range(2, H):
            for z in range(Dp):
                e = ((x - cx) / 15) ** 2 + ((y - 9) / 8) ** 2 + ((z - cz) / 13) ** 2
                if e < 1 + (noise(x + y, z, 3, 4) - 0.5) * 0.25 and hm.get((x, z), 0) > y + 2:
                    t.put(x, y, z, "air")
    for x in range(cx - 2, cx + 3):                              # the cave mouth and tunnel
        for z in range(0, cz - 10):
            for y in range(2, 7 - abs(x - cx) // 2):
                t.put(x, y, z, "air")
            t.put(x, 1, z, "gravel")
    # floor, the high ledge with the waterfall, the pool
    for x in range(W):
        for z in range(Dp):
            if t.get(x, 2, z) == "minecraft:air":
                t.put(x, 1, z, pick([("stone", 3), ("gravel", 1), ("tuff", 1)], x, z, 2))
    for x in range(cx - 5, cx + 6):
        for z in range(cz + 6, cz + 12):
            for y in range(2, 12):
                t.put(x, y, z, pick([("stone", 2), ("tuff", 1)], x, y, z))
    t.put(cx, 12, cz + 6, "water", {"level": "0"})
    for dx, dz in ((-1, 0), (1, 0), (0, 1)):
        t.put(cx + dx, 12, cz + 6 + dz, "stone")
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 1, cz + 6):
            if math.hypot(x - cx, (z - cz - 3) * 1.3) < 4.2:
                t.put(x, 1, z, "water", {"level": "0"})
                t.put(x, 0, z, "sand")
    # meteorite chunks in the walls, dripstone, glowstone
    for k in range(60):
        x, y, z = int(h(k, 1, 4) * W), 2 + int(h(k, 2, 4) * 14), int(h(k, 3, 4) * Dp)
        if t.get(x, y, z) in ("minecraft:stone", "minecraft:tuff", "minecraft:andesite"):
            for dx, dy, dz in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)):
                if t.get(x + dx, y + dy, z + dz) not in (None, "minecraft:air", "minecraft:water"):
                    t.put(x + dx, y + dy, z + dz, pick([("obsidian", 3), ("crying_obsidian", 2), ("mega_showdown:mega_meteorid_block", 2),
                                                        ("mega_showdown:mega_meteorid_radiated_block", 1)], k, dx, dy, dz))
    for x in range(W):
        for z in range(Dp):
            for y in range(H - 1, 3, -1):
                if t.get(x, y, z) == "minecraft:air" and t.get(x, y + 1, z) not in (None, "minecraft:air", "minecraft:water"):
                    r = h(x, y, z, 6)
                    if r < 0.05:
                        t.put(x, y, z, "pointed_dripstone", {"thickness": "tip", "vertical_direction": "down", "waterlogged": "false"})
                    elif r < 0.08:
                        t.put(x, y + 1, z, "glowstone")
                    break
    # the dragon's den at the back
    for x in range(cx - 3, cx + 4):
        for z in range(cz + 12, cz + 17):
            for y in range(2, 6):
                t.put(x, y, z, "air")
            t.put(x, 1, z, "mossy_cobblestone")
    for y in range(2, 5):
        for x in (cx - 1, cx, cx + 1):
            t.put(x, y, cz + 11, "air")
    chest(t, cx, 2, cz + 16, "north", "meteor_falls")
    t.put(cx - 2, 2, cz + 16, "bone_block", {"axis": "y"})
    t.put(cx + 2, 2, cz + 15, "bone_block", {"axis": "x"})
    return t


# --- Gen 3: Mt. Chimney ---------------------------------------------------------------------------------------------
def mt_chimney():
    """A volcano of basalt, blackstone and tuff, magma near the top, ash-grey coarse slopes below, and a lava lake in
    its smoking crater. A carved stair climbs the north face to a lookout on the rim with a strange machine of iron,
    copper and lamps (someone wanted to stir the volcano up) and a chest; a little ropeway station waits at the foot."""
    W, H, Dp = 63, 44, 63
    t = S((W, H, Dp))
    cx, cz = 31, 31
    base = 1

    def cone(r):
        """Height of the slope at radius r: the rim (38) at r = 7, the foot at r = 30; inside, the crater's bowl."""
        return base + 38 - (r - 7) * 1.6 if r >= 7 else base + 38 - (7 - r) * 1.2

    for x in range(W):
        for z in range(Dp):
            r = math.hypot(x - cx, z - cz)
            if r > 30:
                continue
            hy = int(cone(r) + ((noise(x, z, 8, 6) - 0.5) * 4 if r > 8 else 0))
            for y in range(base, hy + 1):
                if y > base + 26:
                    m = pick([("basalt", 3), ("blackstone", 2), ("magma_block", 1)], x, y, z)
                elif y > base + 12:
                    m = pick([("tuff", 2), ("basalt", 2), ("smooth_basalt", 1)], x, y, z)
                else:
                    m = pick([("stone", 2), ("tuff", 1), ("andesite", 1)], x, y, z)
                t.put(x, y, z, m, {"axis": "y"} if m == "basalt" else None)
            if y < base + 12 and r > 6:
                t.put(x, hy, z, pick([("coarse_dirt", 3), ("gravel", 1), ("grass_block", 1)], x, z, 4))
    # the lava lake
    for x in range(cx - 6, cx + 7):
        for z in range(cz - 6, cz + 7):
            if math.hypot(x - cx, z - cz) < 5:
                for y in range(base + 30, base + 33):
                    t.put(x, y, z, "lava", {"level": "0"})
                for y in range(base + 33, H):
                    t.put(x, y, z, "air")
                t.put(x, base + 29, z, "magma_block")
    # the stair up the north face
    for z in range(1, cz - 6):
        r = cz - z
        y = int(cone(r))
        for x in (cx - 1, cx, cx + 1):
            t.stair(x, y, z, "polished_blackstone_brick", "south")
            for k in range(1, 4):
                t.put(x, y + k, z, "air")
            t.put(x, y - 1, z, "polished_blackstone_bricks")
    # the lookout and the machine on the rim
    ry = int(cone(7))
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 9, cz - 6):
            t.put(x, ry, z, "polished_blackstone_bricks")
            for k in range(1, 5):
                t.put(x, ry + k, z, "air")
    for x in (cx - 4, cx + 4):
        t.fence(x, ry + 1, cz - 9, "nether_brick_fence")
    t.put(cx - 2, ry + 1, cz - 8, "iron_block")
    t.put(cx - 2, ry + 2, cz - 8, "lightning_rod", {"facing": "up", "powered": "false", "waterlogged": "false"})
    t.put(cx - 1, ry + 1, cz - 8, "waxed_copper_block")
    t.put(cx - 1, ry + 2, cz - 8, "redstone_lamp", {"lit": "true"})
    t.put(cx, ry + 1, cz - 8, "cobblemon:monitor", {"facing": "north", "screen": "blue_progress_8"})
    chest(t, cx + 2, ry + 1, cz - 8, "north", "mt_chimney")
    t.put(cx + 1, ry + 1, cz - 7, "campfire", {"facing": "north", "lit": "true", "signal_fire": "true", "waterlogged": "false"})
    # the ropeway station at the foot
    for x in range(cx + 6, cx + 13):
        for z in range(1, 6):
            t.put(x, base, z, "spruce_planks")
            for y in range(base + 1, base + 4):
                t.put(x, y, z, "air")
        t.put(x, base + 4, 1, "spruce_slab", {"type": "bottom", "waterlogged": "false"})
        t.put(x, base + 4, 5, "spruce_slab", {"type": "bottom", "waterlogged": "false"})
    for x, z in ((cx + 6, 1), (cx + 12, 1), (cx + 6, 5), (cx + 12, 5)):
        for y in range(base + 1, base + 4):
            t.log(x, y, z, "spruce_log")
    t.box(cx + 6, base + 4, 2, cx + 12, base + 4, 4, "spruce_planks")
    for y in range(base + 5, base + 12):
        t.put(cx + 9, y, 3, "chain", {"axis": "y", "waterlogged": "false"})
    return t


# --- Gen 3: Mt. Pyre ----------------------------------------------------------------------------------------------------
def mt_pyre():
    """A tall misty-grey mountain of stone, diorite and calcite. A doorway at its foot opens on a hall of graves
    lit by candles; a spiral stair climbs inside the mountain to its summit, where a little stone shrine keeps the Red
    and Blue Orbs (each trainer may take a pair) between two pedestals."""
    W, H, Dp = 53, 50, 53
    t = S((W, H, Dp))
    cx, cz = 26, 26
    hm = mound(t, cx, cz, 25, 40, 1, 31, 4.0, ("stone", "stone", "stone", "andesite", "diorite"), None, 6)
    for (x, z), y in hm.items():
        if y < 14:
            t.put(x, y, z, "grass_block", {"snowy": "false"})
    # the hall of graves
    for x in range(14, 39):
        for z in range(10, 30):
            t.put(x, 1, z, "polished_andesite")
            for y in range(2, 9):
                t.put(x, y, z, "air")
    for x in range(cx - 1, cx + 2):
        for z in range(0, 10):
            for y in range(2, 6):
                t.put(x, y, z, "air")
            t.put(x, 1, z, "stone_bricks")
    for z in range(13, 29, 3):
        for x in range(16, 37, 2):
            if abs(x - cx) <= 1:
                continue
            t.put(x, 2, z, pick([("stone_brick_wall", 2), ("cobblestone_wall", 1), ("mossy_stone_brick_wall", 1)], x, z, 5))
            r = h(x, z, 13)
            if r < 0.3:
                candle(t, x, 3, z, "white", 1 + int(r * 10) % 4)
            elif r < 0.45:
                t.put(x, 2, z + 1, "potted_lily_of_the_valley")
    for x in range(16, 37, 5):
        t.put(x, 8, 20, "soul_lantern", {"hanging": "true", "waterlogged": "false"})
    chest(t, 37, 2, 28, "west", "mt_pyre")
    # the spiral stair to the summit
    top = max(hm.values())
    spiral_stairs(t, cx, 31, 2, 2, top - 1, "stone_brick", "stone_bricks")
    for z in range(29, 31):
        for x in range(cx - 1, cx + 2):
            for y in range(2, 5):
                t.put(x, y, z, "air")
    # the summit shrine
    sy = top
    for x in range(cx - 5, cx + 6):
        for z in range(26, 37):
            t.put(x, sy, z, "stone_bricks" if (x + z) % 2 else "polished_andesite")
            for y in range(sy + 1, sy + 7):
                t.put(x, y, z, "air")
    for x, z in ((cx - 3, 28), (cx + 3, 28), (cx - 3, 34), (cx + 3, 34)):
        for y in range(sy + 1, sy + 5):
            t.put(x, y, z, "stone_brick_wall")
    for x in range(cx - 4, cx + 5):
        for z in range(27, 36):
            t.put(x, sy + 5, z, "deepslate_tile_slab", {"type": "bottom", "waterlogged": "false"})
    t.put(cx - 2, sy + 1, 33, "mega_showdown:pedestal", {"facing": "north"})
    t.put(cx + 2, sy + 1, 33, "mega_showdown:pedestal", {"facing": "north"})
    shrine(t, cx, sy + 1, 33, "altar", key="mt_pyre_orbs", mode="gift",
           items=["mega_showdown:red_orb", "mega_showdown:blue_orb"], label=f"{MOD}.shrine.mt_pyre_orbs")
    for x in (cx - 2, cx + 2):
        candle(t, x, sy + 1, 29, "red" if x < cx else "blue", 3)
    return t


# --- Gen 3: Sky Pillar --------------------------------------------------------------------------------------------------
def sky_pillar():
    """A crumbling round tower of mossy and cracked stone bricks on a rocky islet, banded with weathered copper and
    pierced by window slits. A stair winds up inside past six floors (holes worn in them) to the open, broken-walled
    summit, where Rayquaza answers the shrine."""
    W, H, Dp = 31, 106, 31
    t = S((W, H, Dp))
    cx, cz = 15, 15
    for x in range(W):
        for z in range(Dp):
            d = math.hypot(x - cx, z - cz) + (noise(x, z, 9, 4) - 0.5) * 3
            if d < 15:
                hy = 2 + int((15 - d) / 3)
                for y in range(0, hy + 1):
                    t.put(x, y, z, pick([("stone", 3), ("mossy_cobblestone", 1), ("cobblestone", 1)], x, y, z))
                if d > 12:
                    t.put(x, hy, z, "sand")
    R, base, top = 9, 6, 94
    bricks = [("mossy_stone_bricks", 4), ("stone_bricks", 3), ("cracked_stone_bricks", 2)]
    floors = list(range(base, top, 15)) + [top]
    for y in range(base, top + 1):
        for x in range(cx - R - 1, cx + R + 2):
            for z in range(cz - R - 1, cz + R + 2):
                d = math.hypot(x - cx, z - cz)
                if d <= R:
                    if d > R - 2:
                        c = pick(bricks, x, y, z)
                        if y % 15 == 9:
                            c = "weathered_cut_copper"
                        if y % 15 in (4, 5, 6) and (int(math.degrees(math.atan2(z - cz, x - cx))) // 30) % 3 == 0 and d > R - 1:
                            c = "air"                                   # window slits
                        if h(x, y, z, 12) < 0.02 and y > base + 10:
                            c = "air"                                   # crumbled gaps
                        t.put(x, y, z, c)
                    elif y in floors:
                        t.put(x, y, z, "air" if (y != top and h(x, z, y) < 0.06) else pick(bricks, x, y, z))
                    else:
                        t.put(x, y, z, "air")
    # the broken top wall
    for x in range(cx - R, cx + R + 1):
        for z in range(cz - R, cz + R + 1):
            d = math.hypot(x - cx, z - cz)
            if R - 2 < d <= R:
                for y in range(top + 1, top + 1 + int(noise(x, z, 4, 3) * 5)):
                    t.put(x, y, z, pick(bricks, x, y, z))
    # the winding stair (one turn every two floors) hugging the inner wall
    steps = []
    a = 0.0
    y = base + 1
    rr = R - 2.5
    while y <= top:
        x, z = int(round(cx + math.cos(a) * rr)), int(round(cz + math.sin(a) * rr))
        steps.append((x, y, z, a))
        a += 1.0 / rr
        y += 1
    for x, y, z, a in steps:
        tx, tz = -math.sin(a), math.cos(a)
        facing = ("east" if tx > 0 else "west") if abs(tx) > abs(tz) else ("south" if tz > 0 else "north")
        t.stair(x, y, z, "mossy_stone_brick", facing)
        for k in range(1, 4):
            if y + k <= top + 4:
                t.put(x, y + k, z, "air")
        if t.get(x, y - 1, z) in (None, "minecraft:air"):
            t.put(x, y - 1, z, "mossy_stone_bricks")
    for x in range(cx - 1, cx + 2):                              # the door
        for y in range(base + 1, base + 4):
            t.put(x, y, cz - R, "air")
            t.put(x, y, cz - R + 1, "air")
    t.door(cx, base + 1, cz - R, "spruce_door", "south")
    # the summit altar
    t.box(cx - 2, top + 1, cz - 2, cx + 2, top + 1, cz + 2, "chiseled_stone_bricks")
    shrine(t, cx, top + 2, cz, "altar", key="rayquaza", mode="encounter", props="rayquaza level=70",
           dx=0, dy=4, dz=0, label=f"{MOD}.shrine.rayquaza")
    for x, z in ((cx - 2, cz - 2), (cx + 2, cz - 2), (cx - 2, cz + 2), (cx + 2, cz + 2)):
        t.put(x, top + 2, z, "lantern", {"hanging": "false", "waterlogged": "false"})
    chest(t, cx + 6, base + 1, cz, "west", "sky_pillar")
    chest(t, cx - 5, top + 1, cz + 4, "east", "sky_pillar_top")
    return t


# --- Gen 3: the Temple of Jirachi -------------------------------------------------------------------------------------
def temple_of_jirachi():
    """A round white temple of calcite and quartz trimmed with gold, on a plaza round a star-shaped pool. Gold-capped
    pillars hold a glass dome with an open oculus over the dais where Jirachi sleeps: at night the shrine wakes it.
    End rods and Mega Showdown's wishing-star crystals sparkle round the dais; cherry trees and lilies fill the
    garden."""
    W, H, Dp = 39, 24, 39
    t = S((W, H, Dp))
    g = 1
    cx, cz = 19, 19
    ground_fill(t, W, Dp, g, "grass_block", "dirt", 1)
    disc(t, cx, g, cz, 18, "calcite")
    disc(t, cx, g, cz, 17, "smooth_quartz")
    for k in range(5):                                         # the star pool (five points)
        a = -math.pi / 2 + k * 2 * math.pi / 5
        for s in range(30):
            f = s / 30
            px = cx + math.cos(a) * (6 + f * 9)
            pz = cz + math.sin(a) * (6 + f * 9)
            w = (1 - f) * 2.2
            for x in range(int(px - w - 1), int(px + w + 2)):
                for z in range(int(pz - w - 1), int(pz + w + 2)):
                    if math.hypot(x - px, z - pz) <= w:
                        t.put(x, g, z, "water", {"level": "0"})
                        t.put(x, g - 1, z, "prismarine")
    disc(t, cx, g, cz, 7, "smooth_quartz")
    # pillars, the dome and the oculus
    for k in range(8):
        a = k * math.pi / 4
        px, pz = int(round(cx + math.cos(a) * 6)), int(round(cz + math.sin(a) * 6))
        for y in range(g + 1, g + 7):
            t.put(px, y, pz, "quartz_pillar", {"axis": "y"})
        t.put(px, g + 7, pz, "gold_block")
    for y in range(g + 8, g + 14):
        r = 7 * math.sqrt(max(0, 1 - ((y - g - 8) / 6) ** 2))
        for x in range(cx - 8, cx + 9):
            for z in range(cz - 8, cz + 9):
                d = math.hypot(x - cx, z - cz)
                if r - 1.1 < d <= r and d > 1.6:
                    t.put(x, y, z, "white_stained_glass" if (x + z + y) % 4 else "yellow_stained_glass")
    disc(t, cx, g + 7, cz, 7, "chiseled_quartz_block", hollow=True)
    # the dais and the shrine
    disc(t, cx, g + 1, cz, 2.5, "gold_block")
    t.put(cx, g + 2, cz, "chiseled_quartz_block")
    shrine(t, cx, g + 3, cz, "altar", key="jirachi", mode="encounter", props="jirachi level=50", time="night",
           dx=0, dy=2, dz=-3, label=f"{MOD}.shrine.jirachi", hint=f"{MOD}.shrine.jirachi_day")
    for k in range(6):
        a = k * math.pi / 3 + 0.5
        x, z = int(round(cx + math.cos(a) * 4)), int(round(cz + math.sin(a) * 4))
        t.put(x, g + 1, z, "mega_showdown:wishing_star_crystal" if k % 2 else "end_rod", None if k % 2 else {"facing": "up"})
    # cherry trees and lilies round the plaza
    for k in range(10):
        a = k / 10 * 2 * math.pi + 0.15
        x, z = int(cx + math.cos(a) * 15.5), int(cz + math.sin(a) * 15.5)
        if k % 2 == 0:
            for y in range(g + 1, g + 5):
                t.log(x, y, z, "cherry_log")
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    for dy in (4, 5):
                        if abs(dx) + abs(dz) <= (3 if dy == 4 else 2):
                            t.leaves(x + dx, g + dy, z + dz, "cherry_leaves")
        else:
            t.put(x, g + 1, z, "lily_of_the_valley")
            t.put(x + 1, g + 1, z, "azure_bluet")
    chest(t, cx + 3, g + 1, cz + 5, "north", "temple_of_jirachi")
    clear_above(t, 0, 0, W - 1, Dp - 1, g + 1)
    return t


# --- Gen 3: the Deoxys meteorite ------------------------------------------------------------------------------------
def deoxys_meteorite():
    """A scorched crater (coarse dirt, blackstone, basalt and smouldering magma) round a meteorite of Mega Showdown's
    meteorite stone veined with crying obsidian and amethyst. Four of Mega Showdown's Deoxys meteorites are set in
    its sides (use one to change your Deoxys's forme), and a shrine on its face calls Deoxys down."""
    W, H, Dp = 35, 18, 35
    t = S((W, H, Dp))
    g = 7
    cx, cz = 17, 17
    ground_fill(t, W, Dp, g, "grass_block", "dirt", 6)
    for x in range(W):
        for z in range(Dp):
            d = math.hypot(x - cx, z - cz) + (noise(x, z, 6, 4) - 0.5) * 2
            if d < 13:
                y = g - int((1 - (d / 13) ** 2) * 6)
                for k in range(y + 1, g + 1):
                    t.put(x, k, z, "air")
                m = pick([("coarse_dirt", 3), ("blackstone", 2), ("basalt", 2), ("magma_block", 1)], x, z, 8)
                t.put(x, y, z, m, {"axis": "y"} if m == "basalt" else None)
            elif d < 15:
                t.put(x, g + 1, z, pick([("coarse_dirt", 2), ("gravel", 1)], x, z, 3))
    # the meteorite
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            for y in range(g - 6, g + 1):
                e = ((x - cx) / 4.2) ** 2 + ((y - (g - 4)) / 4.0) ** 2 + ((z - cz) / 3.8) ** 2
                if e < 1 + (h(x, y, z, 3) - 0.5) * 0.4:
                    t.put(x, y, z, pick([("mega_showdown:mega_meteorid_block", 4), ("mega_showdown:polished_mega_meteorid_block", 1),
                                         ("crying_obsidian", 1), ("amethyst_block", 1), ("mega_showdown:mega_meteorid_radiated_block", 1)], x, y, z))
    for x, z in ((cx - 4, cz), (cx + 4, cz), (cx, cz - 4), (cx, cz + 4)):
        t.put(x, g - 4, z, "mega_showdown:deoxys_meteorite")
    shrine(t, cx, g - 3, cz - 4, "altar", key="deoxys", mode="encounter", props="deoxys level=50",
           dx=0, dy=1, dz=-4, label=f"{MOD}.shrine.deoxys")
    barrel(t, cx + 8, g - 2, cz + 5, "deoxys_meteorite")
    clear_above(t, 0, 0, W - 1, Dp - 1, g + 2)
    return t


# --- registry: builders, placement, loot, spawns -------------------------------------------------------------------
OCEANS = ["ocean", "deep_ocean", "lukewarm_ocean", "deep_lukewarm_ocean", "warm_ocean", "cold_ocean", "deep_cold_ocean"]

# id: (name, builder, biomes, spacing, separation, start_height, heightmap or None, terrain adaptation)
STRUCTURES = {
    "bills_sea_cottage": ("Bill's Sea Cottage", bills_sea_cottage, ["beach", "stony_shore", "snowy_beach"], 40, 14, 0, "WORLD_SURFACE_WG", "beard_thin"),
    "ss_anne": ("S.S. Anne", ss_anne, OCEANS, 48, 18, 63 - SHIP_WATER, None, "none"),
    "lavender_tower": ("Lavender Town Tower", lavender_tower, ["plains", "meadow", "taiga", "sunflower_plains"], 48, 16, 0, "WORLD_SURFACE_WG", "beard_thin"),
    "rocket_hideout": ("Celadon Rocket Hideout", rocket_hideout, ["plains", "savanna", "sunflower_plains", "forest"], 48, 16, -18, "WORLD_SURFACE_WG", "beard_thin"),
    "cinnabar_lab": ("Cinnabar Pokémon Lab", cinnabar_lab, ["beach", "savanna", "badlands", "windswept_savanna", "desert"], 48, 16, 0, "WORLD_SURFACE_WG", "beard_thin"),
    "ruins_of_alph": ("Ruins of Alph", ruins_of_alph, ["plains", "savanna", "meadow", "sunflower_plains"], 44, 14, -3, "WORLD_SURFACE_WG", "beard_thin"),
    "lake_of_rage": ("Lake of Rage", lake_of_rage, ["forest", "birch_forest", "taiga", "flower_forest", "old_growth_birch_forest"], 44, 14, -6, "WORLD_SURFACE_WG", "beard_thin"),
    "rocket_hq_mahogany": ("Mahogany Rocket HQ", rocket_hq_mahogany, ["taiga", "snowy_taiga", "snowy_plains", "grove"], 48, 16, -14, "WORLD_SURFACE_WG", "beard_thin"),
    "meteor_falls": ("Meteor Falls", meteor_falls, ["windswept_hills", "windswept_gravelly_hills", "windswept_forest", "meadow", "stony_shore"], 48, 16, -1, "WORLD_SURFACE_WG", "beard_thin"),
    "mt_chimney": ("Mt. Chimney", mt_chimney, ["badlands", "eroded_badlands", "wooded_badlands", "savanna_plateau", "windswept_savanna"], 56, 20, -1, "WORLD_SURFACE_WG", "beard_thin"),
    "mt_pyre": ("Mt. Pyre", mt_pyre, ["meadow", "windswept_hills", "old_growth_spruce_taiga", "grove"], 56, 20, -1, "WORLD_SURFACE_WG", "beard_thin"),
    "sky_pillar": ("Sky Pillar", sky_pillar, ["beach", "stony_shore"], 60, 22, -1, "WORLD_SURFACE_WG", "beard_thin"),
    "temple_of_jirachi": ("Temple of Jirachi", temple_of_jirachi, ["cherry_grove", "flower_forest", "meadow", "sunflower_plains"], 52, 18, -1, "WORLD_SURFACE_WG", "beard_thin"),
    "deoxys_meteorite": ("Deoxys Meteorite", deoxys_meteorite, ["plains", "desert", "savanna", "snowy_plains", "badlands"], 48, 16, -7, "WORLD_SURFACE_WG", "beard_thin"),
}

TABLES = {
    "bills_sea_cottage": [("cobblemon:poke_ball", 4, 8), ("cobblemon:great_ball", 2, 4), ("cobblemon:potion", 2, 4),
                          ("cobblemon:exp_share", 1, 1), ("cobblemon:exp_candy_s", 2, 5), ("minecraft:book", 1, 3)],
    "ss_anne_cabin": [("cobblemon:great_ball", 1, 4), ("cobblemon:super_potion", 1, 3), ("cobblemon:revive", 1, 2),
                      ("cobblemon:exp_candy_s", 1, 4), ("minecraft:emerald", 1, 3), ("cobblemon:mystic_water", 1, 1)],
    "ss_anne_galley": [("minecraft:cake", 1, 2), ("minecraft:cooked_cod", 3, 8), ("minecraft:bread", 3, 8),
                       ("cobblemon:berry_juice", 1, 3), ("cobblemon:lava_cookie", 1, 2)],
    "ss_anne_captain": [("cobblemon:ultra_ball", 2, 5), ("cobblemon:rare_candy", 1, 2), ("cobblemon:hyper_potion", 1, 3),
                        ("minecraft:compass", 1, 1), ("minecraft:map", 1, 1), ("minecraft:diamond", 1, 2)],
    "ss_anne_engine": [("minecraft:coal", 4, 12), ("minecraft:iron_ingot", 2, 6), ("cobblemon:magnet", 1, 1),
                       ("minecraft:redstone", 3, 9)],
    "lavender_tower": [("cobblemon:spell_tag", 1, 1), ("cobblemon:cleanse_tag", 1, 1), ("cobblemon:revive", 1, 2),
                       ("minecraft:candle", 2, 6), ("cobblemon:dusk_ball", 1, 3), ("minecraft:bone", 2, 6)],
    "lavender_tower_top": [("cobblemon:max_revive", 1, 1), ("cobblemon:cleanse_tag", 1, 1), ("cobblemon:dusk_stone", 1, 1),
                           ("cobblemon:spell_tag", 1, 1), ("cobblemon:rare_candy", 1, 2)],
    "rocket_hideout": [("cobblemon:poke_ball", 3, 8), ("cobblemon:great_ball", 2, 5), ("cobblemon:smoke_ball", 1, 1),
                       ("cobblemon:super_potion", 1, 3), ("minecraft:gold_ingot", 1, 4), ("cobblemon:exp_candy_m", 1, 2)],
    "rocket_boss": [("cobblemon:ultra_ball", 2, 6), ("cobblemon:rare_candy", 2, 4), ("cobblemon:master_ball", 1, 1),
                    ("cobblemon:max_potion", 1, 3), ("minecraft:diamond", 2, 5), ("cobblemon:kings_rock", 1, 1)],
    "cinnabar_fossils": [("cobblemon:helix_fossil", 1, 1), ("cobblemon:dome_fossil", 1, 1), ("cobblemon:old_amber_fossil", 1, 1),
                         ("cobblemon:root_fossil", 1, 1), ("cobblemon:claw_fossil", 1, 1), ("cobblemon:skull_fossil", 1, 1),
                         ("cobblemon:armor_fossil", 1, 1)],
    "ruins_of_alph": [("cobblemon:relic_coin", 1, 4), ("cobblemon:old_amber_fossil", 1, 1), ("cobblemon:rare_candy", 1, 1),
                      ("cobblemon:moon_stone", 1, 1), ("cobblemon:sun_stone", 1, 1), ("minecraft:gold_nugget", 3, 9)],
    "ruins_of_alph_camp": [("minecraft:paper", 3, 8), ("minecraft:book", 1, 3), ("cobblemon:poke_ball", 3, 6),
                           ("cobblemon:potion", 1, 3), ("minecraft:bread", 2, 5)],
    "lake_of_rage": [("cobblemon:poke_rod", 1, 1), ("cobblemon:net_ball", 2, 5),
                     ("cobblemon:dive_ball", 1, 3), ("cobblemon:mystic_water", 1, 1), ("minecraft:cod", 2, 6)],
    "rocket_hq_shop": [("cobblemon:rage_candy_bar", 2, 5), ("cobblemon:berry_juice", 1, 3), ("cobblemon:poke_ball", 2, 5),
                       ("minecraft:emerald", 1, 3)],
    "rocket_hq": [("cobblemon:great_ball", 2, 5), ("cobblemon:hyper_potion", 1, 2), ("cobblemon:magnet", 1, 1),
                  ("minecraft:redstone", 4, 12), ("minecraft:copper_ingot", 2, 6), ("cobblemon:exp_candy_m", 1, 2)],
    "meteor_falls": [("cobblemon:dragon_fang", 1, 1), ("cobblemon:dragon_scale", 1, 1), ("cobblemon:moon_stone", 1, 2),
                     ("cobblemon:sun_stone", 1, 1), ("mega_showdown:keystone", 1, 1), ("minecraft:obsidian", 2, 5)],
    "mt_chimney": [("cobblemon:fire_stone", 1, 2), ("cobblemon:charcoal_stick", 1, 1), ("cobblemon:heat_rock", 1, 1),
                   ("cobblemon:lava_cookie", 2, 5), ("cobblemon:flame_orb", 1, 1), ("minecraft:magma_cream", 2, 5)],
    "mt_pyre": [("cobblemon:spell_tag", 1, 1), ("cobblemon:cleanse_tag", 1, 1), ("cobblemon:dusk_stone", 1, 1),
                ("cobblemon:revive", 1, 3), ("minecraft:candle", 2, 6)],
    "sky_pillar": [("cobblemon:ultra_ball", 2, 4), ("cobblemon:max_potion", 1, 2), ("cobblemon:dragon_scale", 1, 1),
                   ("cobblemon:full_heal", 1, 3)],
    "sky_pillar_top": [("cobblemon:master_ball", 1, 1), ("cobblemon:rare_candy", 2, 4), ("cobblemon:dragon_fang", 1, 1),
                       ("cobblemon:max_revive", 1, 2), ("minecraft:diamond", 2, 4)],
    "temple_of_jirachi": [("cobblemon:shiny_stone", 1, 1), ("cobblemon:moon_stone", 1, 1), ("cobblemon:soothe_bell", 1, 1),
                          ("cobblemon:luxury_ball", 1, 3), ("minecraft:glowstone_dust", 3, 8)],
    "deoxys_meteorite": [("cobblemon:moon_stone", 1, 2), ("mega_showdown:keystone", 1, 1), ("minecraft:amethyst_shard", 3, 8),
                         ("cobblemon:quick_ball", 2, 4), ("minecraft:obsidian", 2, 4)],
    "cinnabar_lab": [("cobblemon:upgrade", 1, 1), ("cobblemon:dubious_disc", 1, 1), ("cobblemon:metal_coat", 1, 1),
                     ("cobblemon:fire_stone", 1, 1), ("cobblemon:rare_candy", 1, 2), ("cobblemon:exp_candy_l", 1, 1),
                     ("cobblemon:ultra_ball", 1, 4)],
}

# id: [(species, bucket, level, weight, position[, extra condition])]
SPAWNS = {
    "bills_sea_cottage": [("eevee", "rare", "5-15", 1.0, "grounded"), ("clefairy", "uncommon", "5-15", 3.0, "grounded"),
                          ("pidgey", "common", "3-12", 8.0, "grounded")],
    "ss_anne": [("tentacool", "common", "10-25", 10.0, "submerged"), ("machop", "uncommon", "12-24", 4.0, "grounded"),
                ("shellder", "uncommon", "10-22", 4.0, "grounded"), ("wingull", "common", "10-22", 6.0, "grounded")],
    "lavender_tower": [("gastly", "common", "15-30", 10.0, "grounded"), ("haunter", "uncommon", "25-35", 3.0, "grounded"),
                       ("cubone", "uncommon", "15-30", 4.0, "grounded"), ("gengar", "ultra-rare", "35-45", 0.5, "grounded")],
    "rocket_hideout": [("koffing", "common", "15-30", 8.0, "grounded"), ("grimer", "common", "15-30", 6.0, "grounded"),
                       ("rattata", "common", "12-25", 8.0, "grounded"), ("ekans", "uncommon", "15-28", 3.0, "grounded")],
    "ruins_of_alph": [("unown", "common", "5-35", 12.0, "grounded"), ("natu", "uncommon", "8-25", 3.0, "grounded"),
                      ("smeargle", "rare", "10-30", 1.0, "grounded")],
    "lake_of_rage": [("magikarp", "common", "5-30", 14.0, "submerged"), ("gyarados", "rare", "25-40", 1.0, "submerged"),
                     ("psyduck", "uncommon", "10-25", 3.0, "grounded")],
    "rocket_hq_mahogany": [("voltorb", "common", "15-30", 8.0, "grounded"), ("electrode", "uncommon", "25-35", 3.0, "grounded"),
                           ("koffing", "common", "15-30", 6.0, "grounded"), ("rattata", "common", "12-25", 6.0, "grounded")],
    "meteor_falls": [("bagon", "rare", "15-30", 1.5, "grounded"), ("solrock", "uncommon", "20-35", 4.0, "grounded"),
                     ("lunatone", "uncommon", "20-35", 4.0, "grounded"), ("zubat", "common", "10-25", 8.0, "grounded"),
                     ("golbat", "uncommon", "22-35", 3.0, "grounded"), ("absol", "rare", "25-40", 1.0, "grounded")],
    "mt_chimney": [("numel", "common", "15-30", 10.0, "grounded"), ("slugma", "common", "15-30", 8.0, "grounded"),
                   ("torkoal", "uncommon", "20-35", 4.0, "grounded"), ("magcargo", "rare", "35-45", 1.0, "grounded")],
    "mt_pyre": [("shuppet", "common", "20-35", 10.0, "grounded"), ("duskull", "common", "20-35", 8.0, "grounded"),
                ("vulpix", "uncommon", "18-30", 3.0, "grounded"), ("chimecho", "rare", "25-40", 1.0, "grounded")],
    "sky_pillar": [("sableye", "common", "35-50", 6.0, "grounded"), ("claydol", "uncommon", "40-50", 4.0, "grounded"),
                   ("banette", "uncommon", "38-50", 4.0, "grounded"), ("altaria", "rare", "40-55", 2.0, "grounded")],
    "temple_of_jirachi": [("clefairy", "common", "15-30", 8.0, "grounded"), ("cleffa", "uncommon", "5-15", 3.0, "grounded"),
                          ("chimecho", "rare", "20-35", 1.0, "grounded"), ("togepi", "rare", "5-15", 1.0, "grounded")],
    "deoxys_meteorite": [("lunatone", "uncommon", "20-35", 4.0, "grounded"), ("solrock", "uncommon", "20-35", 4.0, "grounded"),
                         ("clefairy", "common", "15-30", 6.0, "grounded", {"timeRange": "night"})],
    "cinnabar_lab": [("porygon", "rare", "20-35", 1.0, "grounded"), ("ditto", "uncommon", "20-35", 3.0, "grounded"),
                     ("magnemite", "common", "15-30", 8.0, "grounded"), ("voltorb", "common", "15-30", 6.0, "grounded")],
}


def loot_table(rows):
    return {"type": "minecraft:chest", "pools": [{"rolls": {"type": "minecraft:uniform", "min": 3, "max": 6}, "entries": [
        {"type": "minecraft:item", "name": item, "weight": 2 if hi > 1 else 1,
         "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]}
        for item, lo, hi in rows]}]}


def worldgen():
    for n, (sid, (label, builder, biomes, spacing, sep, start, hmap, adapt)) in enumerate(STRUCTURES.items()):
        t = builder()
        p = D / "structure" / "landmark" / f"{sid}.nbt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(t.nbt())
        write_json(D / "worldgen" / "template_pool" / "landmark" / f"{sid}.json", {
            "fallback": "minecraft:empty", "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element", "location": f"{MOD}:landmark/{sid}",
                "processors": "minecraft:empty", "projection": "rigid"}}]})
        st = {"type": "minecraft:jigsaw", "biomes": f"#{MOD}:has_structure/{sid}", "step": "surface_structures",
              "spawn_overrides": {}, "terrain_adaptation": adapt, "start_pool": f"{MOD}:landmark/{sid}", "size": 1,
              "start_height": {"absolute": start}, "max_distance_from_center": 80, "use_expansion_hack": False}
        if hmap:
            st["project_start_to_heightmap"] = hmap
        write_json(D / "worldgen" / "structure" / f"{sid}.json", st)
        write_json(D / "worldgen" / "structure_set" / f"{sid}.json", {
            "structures": [{"structure": f"{MOD}:{sid}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": sep, "salt": 31337 + 131 * n}})
        write_json(D / "tags" / "worldgen" / "biome" / "has_structure" / f"{sid}.json",
                   {"replace": False, "values": [f"minecraft:{b}" for b in biomes]})
        LANG[f"structure.{MOD}.{sid}"] = label
        print(f"  {sid}: {t.size}, {len(t.blocks)} blocks, {p.stat().st_size // 1024} KB")
    for name, rows in TABLES.items():
        write_json(D / "loot_table" / "chests" / "landmark" / f"{name}.json", loot_table(rows))
    for sid, rows in SPAWNS.items():
        spawns = []
        for i, row in enumerate(rows):
            species, bucket, level, weight, position = row[:5]
            cond = {"structures": [f"{MOD}:{sid}"]}
            if len(row) > 5:
                cond.update(row[5])
            spawns.append({"id": f"{MOD}-{sid}-{i}", "pokemon": species, "presets": ["water" if position == "submerged" else "natural"],
                           "type": "pokemon", "spawnablePositionType": position, "bucket": bucket, "level": level,
                           "weight": weight, "condition": cond})
        write_json(D / "spawn_pool_world" / f"landmark_{sid}.json",
                   {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": spawns})


# --- the shrine block's look -----------------------------------------------------------------------------------------
def shrine_assets():
    tex = A / "textures" / "block"
    tex.mkdir(parents=True, exist_ok=True)

    def stone(seed):
        im = Image.new("RGBA", (16, 16))
        for x in range(16):
            for y in range(16):
                v = 92 + int(h(x, y, seed) * 26)
                im.putpixel((x, y), (v, v - 4, v + 10, 255))
        return im

    top = stone(1)
    d = ImageDraw.Draw(top)
    d.ellipse((2, 2, 13, 13), outline=(120, 230, 255, 255))
    d.ellipse((5, 5, 10, 10), outline=(250, 220, 120, 255))
    d.point([(7, 7), (8, 8), (7, 8), (8, 7)], fill=(255, 255, 230, 255))
    side = stone(2)
    d = ImageDraw.Draw(side)
    d.rectangle((0, 0, 15, 1), fill=(70, 66, 82, 255))
    d.rectangle((0, 14, 15, 15), fill=(70, 66, 82, 255))
    for i, x in enumerate((3, 7, 11)):
        d.line((x, 5, x + 1, 10), fill=(120, 230, 255, 255) if i != 1 else (250, 220, 120, 255))
    save(top, tex / "shrine_altar_top.png")
    save(side, tex / "shrine_altar_side.png")
    case = Image.new("RGBA", (16, 16), (200, 204, 212, 255))
    d = ImageDraw.Draw(case)
    d.rectangle((0, 0, 15, 15), outline=(120, 124, 134, 255))
    front = case.copy()
    d = ImageDraw.Draw(front)
    d.rectangle((2, 2, 13, 9), fill=(30, 40, 60, 255))
    d.rectangle((3, 3, 12, 8), fill=(60, 200, 150, 255))
    d.line((4, 6, 11, 6), fill=(220, 255, 240, 255))
    d.rectangle((3, 11, 5, 13), fill=(220, 60, 60, 255))
    d.rectangle((7, 11, 9, 13), fill=(60, 120, 220, 255))
    save(case, tex / "shrine_terminal_side.png")
    save(front, tex / "shrine_terminal_front.png")
    models = A / "models" / "block"
    write_json(models / "shrine_altar.json", {"parent": "minecraft:block/cube_bottom_top", "textures": {
        "top": f"{MOD}:block/shrine_altar_top", "bottom": f"{MOD}:block/shrine_altar_side", "side": f"{MOD}:block/shrine_altar_side"}})
    write_json(models / "shrine_terminal.json", {"parent": "minecraft:block/cube_bottom_top", "textures": {
        "top": f"{MOD}:block/shrine_terminal_side", "bottom": f"{MOD}:block/shrine_terminal_side", "side": f"{MOD}:block/shrine_terminal_front"}})
    write_json(A / "blockstates" / "shrine.json", {"variants": {
        f"facing={f},look={look}": {"model": f"{MOD}:block/shrine_{look}"}
        for f in ("north", "south", "east", "west") for look in ("altar", "terminal")}})
    write_json(A / "models" / "item" / "shrine.json", {"parent": f"{MOD}:block/shrine_altar"})
    m = f"{MOD}.shrine."
    LANG.update({
        f"block.{MOD}.shrine": "Shrine",
        m + "done.encounter": "It's quiet here now.",
        m + "done.gift": "There's nothing more here for you.",
        m + "done.pokemon": "You've already been given a Pokémon here.",
        m + "here": "It's still here! Go and meet it.",
        m + "resting": "The shrine is resting. Try again in about %s minute(s).",
        m + "bills_eevee": "Bill's console whirs: \"Take good care of this one!\" You received %s!",
        m + "red_gyarados": "The lake churns red... a raging %s surges out of the water!",
        m + "rayquaza": "A roar splits the sky: %s descends on the pillar's summit!",
        m + "jirachi": "A star twinkles over the dais, and %s wakes from its thousand-year sleep!",
        m + "jirachi_day": "The temple is quiet. Jirachi only wakes under the night stars.",
        m + "deoxys": "The meteorite pulses with light... %s takes shape from the stone!",
        m + "mt_pyre_orbs": "You take the Red Orb and the Blue Orb from the shrine. Keep them safe.",
    })


def lang():
    path = A / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.update(LANG)
    path.write_text(json.dumps(dict(sorted(data.items())), indent=2, ensure_ascii=False) + "\n")


def build():
    shrine_assets()
    worldgen()


if __name__ == "__main__":
    build()
    lang()
