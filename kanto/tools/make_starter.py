#!/usr/bin/env python3
"""
The starter kit (the user's request): the Starter Bundle (given once, when you first join a new world) and the
Starter Base Token, which builds a furnished, stocked starter base where you use it.

Writes: the base's structure template (data/<mod>/structure/starter_base.nbt), the loot tables that stock its chests
and barrels (data/<mod>/loot_table/chests/starter/*.json), the two items' textures and models, and their English
names (merged into en_us.json). The Java side is StarterKit.java (it also grows the farm's apricorn trees from
Cobblemon's own tree features and ripens the berries).

The base (x right, y up, z away from you; the door faces you at z = 0):
  ground floor (y 10) on a stone-brick plinth: an entrance hall with a healing machine and a PC, a kitchen (furnace,
    smoker, barrel of food, cauldron), a dining table and a living corner with bookshelves;
  first floor: two bedrooms' worth of beds, wardrobes and nightstands, and an enchanting nook;
  second floor: the workshop (anvil, smithing table, grindstone, stonecutter, loom, brewing stand...);
  attic under the gable roof; a ladder shaft runs from the lowest basement to the attic;
  basement 1: the storage room, chests and barrels all round; basement 2: the forge (furnaces, blast furnace) and a
    starter mine tunnel running out under the farm;
  the farm (fenced, beside the house): wheat on watered farmland, twelve Cobblemon berry bushes on farmland either side
    of a channel, and seven apricorn trees (one of each colour), a composter and a chest of seeds.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from make_assets import A, D, MOD, Nbt, write_json
from make_regions import S

W, H, DEP = 34, 34, 27
G = 10                                   # the ground floor's slab (the surface you clicked)
FLOORS = [0, 5, 10, 15, 20, 25]          # B2, B1, ground, first, second, attic floor slabs
HX0, HX1, HZ0, HZ1 = 0, 16, 3, 17        # the house's outer walls
LAD_X, LAD_Z = (1,), (15, 16)            # the ladder shaft (against the west wall)
TREES = [("red", 20, 17), ("yellow", 24, 17), ("green", 28, 17), ("blue", 32, 17),
         ("pink", 22, 22), ("black", 26, 22), ("white", 30, 22)]    # apricorn trees (Java grows them here, y = G + 1)
BERRIES = ["oran", "pecha", "cheri", "chesto", "rawst", "aspear", "persim", "lum", "sitrus", "leppa", "figy", "wiki"]

LANG = {
    f"item.{MOD}.starter_bundle": "Starter Bundle",
    f"item.{MOD}.starter_bundle.tooltip": "Use it to open: 64 oak logs, 32 cobblestone, 32 Poké Balls, 16 Exp. Candy S, 64 cooked porkchops and a Starter Base Token.",
    f"item.{MOD}.starter_base_token": "Starter Base Token",
    f"item.{MOD}.starter_base_token.tooltip": "Use it on the ground: a furnished, stocked starter base (three floors, two basements, a storage room and a farm) is built right in front of you, its door facing you. Needs a 34 x 27 space.",
    f"{MOD}.starter.welcome": "Welcome! Here's a Starter Bundle to get you going. Use it to open it.",
    f"{MOD}.starter.opened": "You open the Starter Bundle. Use the Starter Base Token on the ground to build your base!",
    f"{MOD}.starter.built": "Your starter base is ready! Healing machine and PC by the door, storage in the basement, farm to the side.",
    f"{MOD}.starter.failed": "The base couldn't be built here.",
    f"{MOD}.starter.given": "Gave a Starter Bundle to %s.",
}


# --- loot tables ---------------------------------------------------------------------------------------------------------
def entry(item, count):
    e = {"type": "minecraft:item", "name": item}
    if count > 1:
        e["functions"] = [{"function": "minecraft:set_count", "count": count}]
    return {"rolls": 1, "entries": [e]}


LOOT = {
    "pokemon": [("cobblemon:poke_ball", 16), ("cobblemon:great_ball", 8), ("cobblemon:potion", 8),
                ("cobblemon:super_potion", 4), ("cobblemon:revive", 4), ("cobblemon:full_heal", 2),
                ("cobblemon:antidote", 4), ("cobblemon:poke_rod", 1), ("cobblemon:exp_candy_s", 8)],
    "kitchen": [("minecraft:bread", 16), ("minecraft:baked_potato", 16), ("minecraft:cooked_beef", 8),
                ("minecraft:cooked_chicken", 8), ("minecraft:apple", 16), ("minecraft:cake", 1),
                ("minecraft:pumpkin_pie", 4), ("minecraft:honey_bottle", 4)],
    "bedroom": [("minecraft:white_wool", 16), ("minecraft:book", 8), ("minecraft:writable_book", 1),
                ("minecraft:map", 2), ("minecraft:compass", 1), ("minecraft:clock", 1), ("minecraft:leather_helmet", 1),
                ("minecraft:leather_chestplate", 1), ("minecraft:leather_leggings", 1), ("minecraft:leather_boots", 1)],
    "workshop": [("minecraft:iron_ingot", 16), ("minecraft:stick", 32), ("minecraft:string", 16),
                 ("minecraft:leather", 8), ("minecraft:flint", 8), ("minecraft:feather", 16),
                 ("minecraft:lapis_lazuli", 16), ("minecraft:glass_bottle", 8), ("minecraft:nether_wart", 4),
                 ("minecraft:paper", 16)],
    "tools": [("minecraft:stone_pickaxe", 1), ("minecraft:stone_axe", 1), ("minecraft:stone_shovel", 1),
              ("minecraft:stone_hoe", 1), ("minecraft:stone_sword", 1), ("minecraft:iron_pickaxe", 1),
              ("minecraft:shield", 1), ("minecraft:bow", 1), ("minecraft:arrow", 32), ("minecraft:fishing_rod", 1),
              ("minecraft:shears", 1), ("minecraft:flint_and_steel", 1), ("minecraft:bucket", 2),
              ("minecraft:water_bucket", 1)],
    "building": [("minecraft:oak_planks", 64), ("minecraft:oak_planks", 64), ("minecraft:cobblestone", 64),
                 ("minecraft:stone_bricks", 64), ("minecraft:glass", 32), ("minecraft:oak_log", 32),
                 ("minecraft:oak_stairs", 32), ("minecraft:oak_slab", 32), ("minecraft:ladder", 16),
                 ("minecraft:oak_door", 4), ("minecraft:oak_fence", 32), ("minecraft:oak_fence_gate", 4)],
    "lighting": [("minecraft:torch", 64), ("minecraft:torch", 64), ("minecraft:lantern", 8), ("minecraft:chest", 4),
                 ("minecraft:barrel", 4), ("minecraft:crafting_table", 2), ("minecraft:furnace", 2),
                 ("minecraft:white_bed", 2), ("minecraft:campfire", 2)],
    "farming": [("minecraft:wheat_seeds", 32), ("minecraft:beetroot_seeds", 16), ("minecraft:carrot", 16),
                ("minecraft:potato", 16), ("minecraft:sugar_cane", 8), ("minecraft:pumpkin_seeds", 8),
                ("minecraft:melon_seeds", 8), ("minecraft:bone_meal", 32), ("minecraft:oak_sapling", 8),
                ("minecraft:birch_sapling", 4)],
    "berries": [(f"cobblemon:{b}_berry", 4) for b in BERRIES] +
               [("cobblemon:growth_mulch", 8), ("cobblemon:rich_mulch", 8)],
    "apricorns": [(f"cobblemon:{c}_apricorn", 4) for c, _, _ in TREES] +
                 [(f"cobblemon:{c}_apricorn_seed", 2) for c, _, _ in TREES],
    "food": [("minecraft:cooked_porkchop", 32), ("minecraft:bread", 32), ("minecraft:cooked_cod", 16),
             ("minecraft:carrot", 16), ("minecraft:sweet_berries", 16), ("minecraft:mushroom_stew", 4)],
    "forge": [("minecraft:coal", 64), ("minecraft:coal", 32), ("minecraft:raw_iron", 16),
              ("minecraft:raw_copper", 16), ("minecraft:iron_ingot", 8), ("minecraft:charcoal", 16),
              ("minecraft:torch", 32), ("minecraft:stone_pickaxe", 1)],
    "attic": [("minecraft:white_carpet", 16), ("minecraft:painting", 4), ("minecraft:flower_pot", 4),
              ("minecraft:item_frame", 4), ("minecraft:name_tag", 2), ("minecraft:lead", 2)],
}


def loot(name):
    return {"LootTable": f"{MOD}:chests/starter/{name}"}


# --- the base ------------------------------------------------------------------------------------------------------------
def chest(t, x, y, z, facing, table):
    t.set(x, y, z, "minecraft:chest", {"facing": facing, "type": "single", "waterlogged": "false"}, loot(table))


def barrel(t, x, y, z, facing, table):
    t.set(x, y, z, "minecraft:barrel", {"facing": facing, "open": "false"}, loot(table))


def bed(t, x, y, z, colour, facing="north"):
    """A bed whose head is toward `facing` from (x, z)."""
    dx, dz = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}[facing]
    t.put(x, y, z, f"{colour}_bed", {"facing": facing, "part": "foot", "occupied": "false"})
    t.put(x + dx, y, z + dz, f"{colour}_bed", {"facing": facing, "part": "head", "occupied": "false"})


def window_wall(t, y0):
    """Glass panes in the outer walls of the storey whose floor is y0 (rows 2-3 above it), every few blocks."""
    for y in (y0 + 2, y0 + 3):
        for x in (3, 4, 12, 13):
            t.put(x, y, HZ0, "glass_pane", {"north": "false", "south": "false", "east": "true", "west": "true", "waterlogged": "false"})
            t.put(x, y, HZ1, "glass_pane", {"north": "false", "south": "false", "east": "true", "west": "true", "waterlogged": "false"})
        for z in (6, 7, 11, 12):
            t.put(HX1, y, z, "glass_pane", {"north": "true", "south": "true", "east": "false", "west": "false", "waterlogged": "false"})
            if z not in LAD_Z:
                t.put(HX0, y, z, "glass_pane", {"north": "true", "south": "true", "east": "false", "west": "false", "waterlogged": "false"})


def storey_shell(t, y0, wall, frame="spruce_log", floor="spruce_planks"):
    """A floor slab at y0 and four walls up to y0 + 4 (the next slab), corner posts of logs, interior air."""
    t.box(HX0, y0, HZ0, HX1, y0, HZ1, floor)
    for y in range(y0 + 1, y0 + 5):
        for x in range(HX0, HX1 + 1):
            for z in range(HZ0, HZ1 + 1):
                if x in (HX0, HX1) or z in (HZ0, HZ1):
                    corner = x in (HX0, HX1) and z in (HZ0, HZ1)
                    t.put(x, y, z, frame if corner else wall, {"axis": "y"} if corner else None)
                else:
                    t.put(x, y, z, "air")


def ladder_shaft(t):
    for y in range(1, FLOORS[-1] + 2):
        for z in LAD_Z:
            t.put(LAD_X[0], y, z, "ladder", {"facing": "east", "waterlogged": "false"})


def hanging_lanterns(t, y, spots):
    for x, z in spots:
        t.lantern(x, y, z, hanging=True)


def base() -> S:
    t = S((W, H, DEP))
    # the ground layer: lawn everywhere, under it a dirt bed (Java fills any gaps below with dirt too)
    t.box(0, G, 0, W - 1, G, DEP - 1, "grass_block", {"snowy": "false"})
    t.box(0, G - 1, 0, W - 1, G - 3, DEP - 1, "dirt")

    # --- the basements: stone bricks dug into the ground
    t.box(HX0, 0, HZ0, HX1, 9, HZ1, "stone_bricks")
    t.box(HX0 + 1, 0, HZ0 + 1, HX1 - 1, 0, HZ1 - 1, "polished_deepslate")
    t.box(HX0 + 1, 1, HZ0 + 1, HX1 - 1, 4, HZ1 - 1, "air")                       # B2
    t.box(HX0 + 1, 5, HZ0 + 1, HX1 - 1, 5, HZ1 - 1, "spruce_planks")             # B1 floor
    t.box(HX0 + 1, 6, HZ0 + 1, HX1 - 1, 9, HZ1 - 1, "air")                       # B1
    for x in range(HX0 + 1, HX1, 4):                                              # support pillars in B2
        t.box(x, 1, 9, x, 4, 9, "spruce_log", {"axis": "y"})
    # B2: the forge and the start of a mine
    for x, kind in ((4, "furnace"), (5, "furnace"), (6, "blast_furnace"), (7, "smoker")):
        t.put(x, 1, HZ1 - 1, kind, {"facing": "north", "lit": "false"})
    chest(t, 9, 1, HZ1 - 1, "north", "forge")
    chest(t, 10, 1, HZ1 - 1, "north", "forge")
    t.put(12, 1, HZ1 - 1, "crafting_table")
    t.put(13, 1, HZ1 - 1, "anvil", {"facing": "east"})
    for x in range(HX1, 31):                                                      # the mine tunnel, under the farm
        t.box(x, 1, 9, x, 2, 10, "air")
        if (x - HX1) % 5 == 2:
            t.lantern(x, 1, 10)
    t.box(HX1, 1, 9, HX1, 2, 10, "air")
    hanging_lanterns(t, 4, [(4, 6), (12, 6), (4, 14), (12, 14), (8, 10)])
    chest(t, 3, 1, 5, "south", "tools")
    # B1: the storage room, chests and barrels all round
    tables = ["building", "building", "lighting", "farming", "berries", "apricorns", "food", "pokemon", "tools", "forge"]
    i = 0
    for x in range(3, 14, 1):
        if i < len(tables) and x % 2 == 1:
            chest(t, x, 6, HZ0 + 1, "south", tables[i])
            chest(t, x, 7, HZ0 + 1, "south", tables[(i + 3) % len(tables)])
            i += 1
    for z in range(6, 15, 2):
        barrel(t, HX1 - 1, 6, z, "west", ["food", "farming", "building", "lighting", "berries"][(z // 2) % 5])
    for z in (6, 8, 10):
        chest(t, 3, 6, z, "east", ["pokemon", "apricorns", "food"][(z // 2) % 3])
    hanging_lanterns(t, 9, [(5, 8), (11, 8), (5, 13), (11, 13)])
    t.put(8, 6, 12, "crafting_table")
    t.box(6, 6, 15, 10, 6, 15, "spruce_slab", {"type": "bottom", "waterlogged": "false"})

    # --- ground floor: stone brick walls, spruce floor
    storey_shell(t, G, "stone_bricks", "spruce_log", "spruce_planks")
    t.door(8, G + 1, HZ0, "spruce_door", "south")
    window_wall(t, G)
    # entrance hall: healing machine and PC either side of the door
    t.put(10, G + 1, HZ0 + 1, "cobblemon:healing_machine", {"facing": "south", "natural": "false", "charge": "6"})
    t.put(HX1 - 1, G + 1, 5, "cobblemon:pc", {"facing": "west", "part": "bottom", "on": "false"})
    t.put(HX1 - 1, G + 2, 5, "cobblemon:pc", {"facing": "west", "part": "top", "on": "false"})
    chest(t, HX1 - 1, G + 1, 7, "west", "pokemon")
    t.put(6, G + 1, HZ0 + 1, "potted_red_tulip")
    # kitchen (back right)
    for z, kind in ((12, "furnace"), (13, "smoker")):
        t.put(HX1 - 1, G + 1, z, kind, {"facing": "west", "lit": "false"})
    t.put(HX1 - 1, G + 1, 14, "crafting_table")
    barrel(t, HX1 - 1, G + 1, 15, "west", "kitchen")
    t.put(HX1 - 1, G + 1, 16, "water_cauldron", {"level": "3"})
    t.box(11, G + 1, 16, 13, G + 1, 16, "smooth_stone")
    t.put(12, G + 2, 16, "composter", {"level": "0"})
    # dining table and chairs
    for x in (7, 8, 9):
        t.fence(x, G + 1, 11, "spruce_fence")
        t.put(x, G + 2, 11, "white_carpet")
        t.stair(x, G + 1, 10, "spruce", "south")
        t.stair(x, G + 1, 12, "spruce", "north")
    # living corner (front left): bookshelves, a couch, a rug
    t.box(HX0 + 1, G + 1, 4, HX0 + 1, G + 3, 9, "bookshelf")
    for z in (5, 6, 7):
        t.stair(3, G + 1, z, "oak", "west")
    t.box(4, G + 1, 5, 6, G + 1, 7, "red_carpet")
    t.put(4, G + 1, 9, "potted_fern")
    hanging_lanterns(t, G + 4, [(4, 7), (12, 7), (8, 11), (4, 14), (12, 14)])
    # porch: a spruce deck, two lanterns on posts
    t.box(5, G, 0, 11, G, 2, "spruce_planks")
    for x in (5, 11):
        t.fence(x, G + 1, 0, "spruce_fence")
        t.lantern(x, G + 2, 0)
    t.stair(8, G, 0, "spruce", "south")
    # a dirt path round to the farm gate
    for x in range(8, 18):
        if not (5 <= x <= 11):
            t.put(x, G, 1, "dirt_path")
    for x in range(12, 18):
        t.put(x, G, 1, "dirt_path")

    # --- first floor: bedrooms, oak plank walls
    storey_shell(t, G + 5, "oak_planks", "spruce_log", "spruce_planks")
    window_wall(t, G + 5)
    y = G + 6
    bed(t, 4, y, 6, "red", "north")
    bed(t, 7, y, 6, "blue", "north")
    bed(t, 13, y, 6, "green", "north")
    for x in (3, 5, 8, 12, 14):
        barrel(t, x, y, HZ0 + 1, "south", "bedroom")
    t.box(10, y, 9, 10, y + 3, 9, "oak_planks")                                   # a partition
    t.box(10, y, 10, 10, y + 3, 16, "oak_planks")
    t.door(10, y, 12, "oak_door", "east")
    chest(t, HX1 - 1, y, 9, "west", "bedroom")
    chest(t, HX1 - 1, y, 10, "west", "bedroom")
    # enchanting nook behind the partition: the table with a ring of bookshelves
    t.put(13, y, 14, "enchanting_table")
    for z in (12, 13, 14, 15, 16):
        t.put(HX1 - 1, y, z, "bookshelf")
    for x in (11, 12):
        t.put(x, y, 16, "bookshelf")
    t.box(3, y, 10, 7, y, 13, "light_blue_carpet")
    hanging_lanterns(t, G + 9, [(5, 8), (13, 8), (13, 14), (5, 13)])

    # --- second floor: the workshop
    storey_shell(t, G + 10, "oak_planks", "spruce_log", "spruce_planks")
    window_wall(t, G + 10)
    y = G + 11
    t.put(3, y, HZ0 + 1, "anvil", {"facing": "east"})
    t.put(5, y, HZ0 + 1, "smithing_table")
    t.put(7, y, HZ0 + 1, "grindstone", {"face": "floor", "facing": "south"})
    t.put(9, y, HZ0 + 1, "stonecutter", {"facing": "south"})
    t.put(11, y, HZ0 + 1, "loom", {"facing": "south"})
    t.put(13, y, HZ0 + 1, "cartography_table")
    t.put(HX1 - 1, y, 8, "fletching_table")
    t.put(HX1 - 1, y, 10, "brewing_stand", {"has_bottle_0": "false", "has_bottle_1": "false", "has_bottle_2": "false"})
    t.put(HX1 - 1, y, 12, "crafting_table")
    chest(t, HX1 - 1, y, 14, "west", "workshop")
    chest(t, HX1 - 1, y, 15, "west", "tools")
    t.put(8, y, 12, "lectern", {"facing": "south", "has_book": "false", "powered": "false"})
    t.box(6, y, 15, 10, y, 16, "oak_slab", {"type": "bottom", "waterlogged": "false"})
    hanging_lanterns(t, G + 14, [(5, 8), (12, 8), (8, 13)])

    # --- attic and the gable roof (ridge along x)
    t.box(HX0, G + 15, HZ0, HX1, G + 15, HZ1, "spruce_planks")
    depth = HZ1 - HZ0 + 1
    for k in range(depth // 2 + 2):
        yy = G + 15 + k
        zf, zb = HZ0 - 1 + k, HZ1 + 1 - k
        if zf > zb:
            break
        for x in range(HX0 - 1, HX1 + 2):
            if zf == zb:
                t.put(x, yy, zf, "dark_oak_planks")
                continue
            t.stair(x, yy, zf, "dark_oak", "south")
            t.stair(x, yy, zb, "dark_oak", "north")
        for x in (HX0, HX1):                                                      # gable ends
            for z in range(zf + 1, zb):
                t.put(x, yy, z, "oak_planks" if yy > G + 15 else "spruce_planks")
        for x in range(HX0 + 1, HX1):
            for z in range(zf + 1, zb):
                if yy > G + 15:
                    t.put(x, yy, z, "air")
    for x in (HX0, HX1):                                                          # round attic windows
        t.put(x, G + 18, 10, "glass")
    t.box(5, G + 16, 8, 11, G + 16, 12, "white_carpet")
    chest(t, 8, G + 16, 10, "south", "attic")
    t.lantern(10, G + 16, 10)

    # ladder shaft from B2 to the attic: holes in every floor slab
    for y in FLOORS[1:]:
        for z in LAD_Z:
            t.put(LAD_X[0], y, z, "air")
    ladder_shaft(t)

    # --- the farm: fenced, beside the house
    fx0, fx1, fz0, fz1 = 18, 33, 0, 26
    for x in range(fx0, fx1 + 1):
        for z in range(fz0, fz1 + 1):
            if x in (fx0, fx1) or z in (fz0, fz1):
                t.fence(x, G + 1, z, "oak_fence")
    t.put(fx0, G + 1, 1, "oak_fence_gate", {"facing": "east", "in_wall": "false", "open": "false", "powered": "false"})
    for x, z in ((fx0, fz0), (fx1, fz0), (fx0, fz1), (fx1, fz1)):
        t.lantern(x, G + 2, z)
    for x in range(fx0 + 1, fx1):                                                 # the path just inside the gate
        t.put(x, G, 1, "dirt_path")
    # wheat: farmland either side of a water channel, ripe
    for x in range(20, 32):
        for z in range(3, 9):
            if z == 5:
                t.put(x, G, z, "water", {"level": "0"})
            else:
                t.put(x, G, z, "farmland", {"moisture": "7"})
                t.put(x, G + 1, z, "wheat", {"age": "7"})
    # berries: two rows of six on farmland either side of a channel (Java grows them until they fruit)
    for i, b in enumerate(BERRIES):
        x = 20 + 2 * (i % 6)
        z = 11 if i < 6 else 13
        t.put(x, G, z, "farmland", {"moisture": "7"})
        t.put(x, G + 1, z, f"cobblemon:{b}_berry", {"age": "0", "rooted": "false"})
    for x in range(19, 32):
        t.put(x, G, 12, "water", {"level": "0"})
    # apricorn trees: dirt under each spot (Java grows Cobblemon's own trees there)
    for _, x, z in TREES:
        t.put(x, G, z, "grass_block", {"snowy": "false"})
    t.put(19, G + 1, 3, "composter", {"level": "0"})
    chest(t, 19, G + 1, 8, "east", "farming")
    t.put(32, G + 1, 10, "hay_block", {"axis": "y"})                             # a scarecrow
    t.put(32, G + 2, 10, "carved_pumpkin", {"facing": "west"})
    return t


# --- items ---------------------------------------------------------------------------------------------------------------
def _bundle():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 18, 56, 60), fill=(122, 78, 44, 255))                          # the leather sack
    d.ellipse((12, 22, 52, 56), fill=(150, 98, 56, 255))
    d.polygon([(20, 22), (44, 22), (40, 10), (24, 10)], fill=(122, 78, 44, 255))  # its gathered neck
    d.rectangle((20, 18, 44, 24), fill=(214, 182, 96, 255))                       # a rope tie
    d.ellipse((24, 32, 40, 48), fill=(230, 48, 48, 255))                          # a Poké Ball clasp
    d.pieslice((24, 32, 40, 48), 0, 180, fill=(245, 245, 245, 255))
    d.line((24, 40, 40, 40), fill=(30, 30, 30, 255), width=2)
    d.ellipse((29, 37, 35, 43), fill=(245, 245, 245, 255), outline=(30, 30, 30, 255), width=1)
    return img.resize((16, 16), Image.LANCZOS)


def _token():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 60, 60), fill=(176, 130, 40, 255))                          # a gold coin
    d.ellipse((9, 9, 55, 55), fill=(232, 190, 70, 255))
    d.polygon([(32, 14), (14, 30), (50, 30)], fill=(150, 60, 40, 255))           # a little house on it
    d.rectangle((18, 30, 46, 48), fill=(246, 236, 210, 255))
    d.rectangle((29, 37, 35, 48), fill=(110, 70, 40, 255))
    d.rectangle((21, 33, 26, 38), fill=(120, 180, 230, 255))
    d.rectangle((38, 33, 43, 38), fill=(120, 180, 230, 255))
    return img.resize((16, 16), Image.LANCZOS)


def items():
    for name, fn in (("starter_bundle", _bundle), ("starter_base_token", _token)):
        p = A / "textures" / "item" / f"{name}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        fn().save(p, optimize=True)
        write_json(A / "models" / "item" / f"{name}.json", {"parent": "minecraft:item/generated",
                                                            "textures": {"layer0": f"{MOD}:item/{name}"}})


def lang():
    path = A / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.update(LANG)
    path.write_text(json.dumps(dict(sorted(data.items())), indent=2, ensure_ascii=False) + "\n")


def build():
    t = base()
    p = D / "structure" / "starter_base.nbt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(t.nbt())
    for name, rows in LOOT.items():
        write_json(D / "loot_table" / "chests" / "starter" / f"{name}.json",
                   {"type": "minecraft:chest", "pools": [entry(i, c) for i, c in rows]})
    items()
    lang()
    print(f"starter base: {len(t.blocks)} blocks, {W}x{H}x{DEP}; {len(LOOT)} loot tables")


if __name__ == "__main__":
    build()
