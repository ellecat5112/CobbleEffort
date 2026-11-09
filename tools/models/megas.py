#!/usr/bin/env python3
"""
Custom Mega Evolutions for the Ancient Paradox Pokémon, through Mega Showdown, from ellecat5112's models (made with
Tripo AI, untextured, so they're painted here).

  Mega Great Tusk · Mega Scream Tail · Mega Brute Bonnet · Mega Flutter Mane · Mega Slither Wing

The base forms come from Cobblemon: AllTheMons x Mega Showdown (Cobblemon 1.8.4 has their data but no models).
Everything here is data, read by Mega Showdown and Cobblemon:

  data/cobbleeffort/species_additions/<species>_mega.json       the "Mega" form: types, ability, stats, battleOnly
  data/cobbleeffort/species_feature_assignments/paradox_megas.json   Mega Showdown's mega_evolution feature
  data/cobbleeffort/mega_showdown/mega/<stone>.json              the mega (stone id, Pokémon, aspect to apply)
  data/cobbleeffort/mega_showdown/showdown/held_items/<stone>.js the stone for Showdown (megaStone mapping)
  data/cobbleeffort/recipe/<stone>.json                          crafting the stone in survival
  data/cobbleeffort/dex_entry_additions/<species>_mega.json     the form in the Pokédex
  assets/cobbleeffort/... model, textures (+ glow), animations, poser, resolver (aspect "mega", order 10)
  assets/minecraft/models/item/amethyst_shard.json             custom_model_data overrides for the stone icons

A stone is an amethyst shard carrying Mega Showdown's components (registry_type_component "mega",
registry_location_component cobbleeffort:<stone>): Mega Showdown maps any such stack to its Showdown item, so no
code is needed. The shard's custom_model_data picks the stone's own icon.

Usage:
  python3 tools/models/megas.py --src greattusk=<model.glb> ...   # (re)voxelize sources -> mega_<name>_voxels.npz
  python3 tools/models/megas.py                                   # build everything from the committed voxels
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _voxel as vx  # noqa: E402
from _anim import keys, sin, track, write_json  # noqa: E402

ROOT = HERE.parent.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"
BASE_ITEM = "minecraft:amethyst_shard"
CMD_BASE = 794700

# ---------------------------------------------------------------------------------------------
# The five megas
# ---------------------------------------------------------------------------------------------

MEGAS = {
    "greattusk": {
        "display": "Great Tusk", "dex": 984, "folder": "0984_greattusk", "stone": "greattuskite", "stone_name": "Great Tuskite",
        "height": 40, "front": "-x", "scale": 1.8, "hitbox": [3.5, 4.5], "kind": "quadruped",
        "types": ["ground", "fighting"], "ability": "toughclaws",
        "stats": [115, 171, 161, 53, 73, 97],
        "dex_text": "Its tusks have grown into great curling blades and its hide bristles with glowing amber crystals. "
                    "Ancient records describe it charging through mountains.",
        "recipe": {"pattern": ["bpb", "kek", " d "], "key": {"b": "minecraft:bone_block", "p": "minecraft:packed_mud",
                    "k": "minecraft:brown_terracotta", "e": "mega_showdown:mega_stone", "d": "minecraft:diamond"}},
        "stone_colours": [(150, 104, 66), (255, 150, 60)],
        "bones": {"leg_h": 6, "head": {"z_max": 13, "y_min": 23}, "tail": {"z_min": 52}},
    },
    "screamtail": {
        "display": "Scream Tail", "dex": 985, "folder": "0985_screamtail", "stone": "screamtailite", "stone_name": "Scream Tailite",
        "height": 32, "front": "+z", "scale": 0.88, "hitbox": [1.8, 1.8], "kind": "biped",
        "types": ["fairy", "psychic"], "ability": "magicbounce",
        "stats": [115, 65, 129, 95, 145, 121],
        "dex_text": "Its fur has grown into a great curling mane and its tail into a soft, swirling sphere. Its scream "
                    "is said to have shaken whole valleys.",
        "recipe": {"pattern": ["wpw", "kek", " d "], "key": {"w": "minecraft:pink_wool", "p": "minecraft:pink_petals",
                    "k": "minecraft:amethyst_shard", "e": "mega_showdown:mega_stone", "d": "minecraft:diamond"}},
        "stone_colours": [(245, 150, 196), (200, 60, 140)],
        "bones": {"leg_h": 4, "foot_y": 1, "head": {"z_max": 18, "y_min": 17}, "tail": {"z_min": 16, "y_max": 14}},
    },
    "brutebonnet": {
        "display": "Brute Bonnet", "dex": 986, "folder": "0986_brutebonnet", "stone": "brutebonnetite", "stone_name": "Brute Bonnetite",
        "height": 40, "front": "+z", "scale": 0.8, "hitbox": [1.3, 2.0], "kind": "quadruped",
        "types": ["grass", "dark"], "ability": "strongjaw",
        "stats": [111, 167, 129, 79, 129, 55],
        "dex_text": "A towering cap grows from the back of a great reptile. Spores drift from it like smoke, and its jaws "
                    "can crush stone.",
        "recipe": {"pattern": ["rmr", "kek", " d "], "key": {"r": "minecraft:red_mushroom_block", "m": "minecraft:moss_block",
                    "k": "minecraft:brown_mushroom", "e": "mega_showdown:mega_stone", "d": "minecraft:diamond"}},
        "stone_colours": [(70, 110, 60), (190, 40, 58)],
        "bones": {"leg_h": 6, "head": {"z_max": 5, "y_min": 6, "y_max": 16}, "tail": {"z_min": 27}, "cap": {"y_min": 28}},
    },
    "fluttermane": {
        "display": "Flutter Mane", "dex": 987, "folder": "0987_fluttermane", "stone": "fluttermanite", "stone_name": "Flutter Manite",
        "height": 36, "front": "+z", "scale": 0.78, "hitbox": [0.9, 1.8], "kind": "floater",
        "types": ["ghost", "fairy"], "ability": "levitate",
        "stats": [55, 55, 65, 175, 165, 155],
        "dex_text": "Its mane streams like a banner and red jewels hang from its brim. It drifts silently, singing a "
                    "song no one can recall afterwards.",
        "recipe": {"pattern": ["mjm", "kek", " d "], "key": {"m": "minecraft:phantom_membrane", "j": "minecraft:echo_shard",
                    "k": "minecraft:purple_dye", "e": "mega_showdown:mega_stone", "d": "minecraft:diamond"}},
        "stone_colours": [(90, 50, 130), (240, 90, 170)],
        "bones": {"head": {"y_min": 24, "z_max": 20}, "mane": {"y_min": 16}, "skirt": {"y_max": 9}},
    },
    "slitherwing": {
        "display": "Slither Wing", "dex": 988, "folder": "0988_slitherwing", "stone": "slitherwingite", "stone_name": "Slither Wingite",
        "height": 44, "front": "+z", "scale": 1.27, "hitbox": [2.2, 3.5], "kind": "moth",
        "types": ["bug", "fighting"], "ability": "moxie",
        "stats": [85, 175, 99, 85, 125, 101],
        "dex_text": "Its wings have grown into great blazing sails that scatter embers when it strikes. It was said to "
                    "bring the dawn.",
        "recipe": {"pattern": ["sbs", "kek", " d "], "key": {"s": "minecraft:string", "b": "minecraft:blaze_powder",
                    "k": "minecraft:orange_dye", "e": "mega_showdown:mega_stone", "d": "minecraft:diamond"}},
        "stone_colours": [(242, 230, 205), (240, 120, 40)],
        "bones": {"leg_h": 3, "foot_y": 0, "wing": {"x_from_centre": 6, "y_min": 12}, "head": {"z_max": 8, "y_min": 8, "y_max": 26},
                  "tail": {"z_min": 25}},
    },
}


def name_of(sp):
    return f"{sp}_mega"


def group_of(sp):
    return f"{MOD}_{sp}_mega"


# ---------------------------------------------------------------------------------------------
# Bones
# ---------------------------------------------------------------------------------------------

def segment(sp, solid, lo):
    cfg = MEGAS[sp]["bones"]
    X, Y, Z = solid.shape
    i, j, k = np.indices(solid.shape)
    cx = -lo[0]
    names = ["body"]
    bone = np.where(solid, 0, -1)

    def add(name, mask):
        names.append(name)
        bone[mask & solid & (bone == 0)] = len(names) - 1

    if "wing" in cfg:
        w = cfg["wing"]
        add("wing_left", (i - cx >= w["x_from_centre"]) & (j >= w["y_min"]))
        add("wing_right", (cx - i >= w["x_from_centre"]) & (j >= w["y_min"]))
    if "cap" in cfg:
        add("cap", j >= cfg["cap"]["y_min"])
    if "head" in cfg:
        h = cfg["head"]
        add("head", (k <= h.get("z_max", Z)) & (j >= h.get("y_min", 0)) & (j <= h.get("y_max", Y)))
    if "mane" in cfg:
        add("mane", (j >= cfg["mane"]["y_min"]) & ((k >= 20) | (i <= cx - 5)))
    if "skirt" in cfg:
        add("skirt", j <= cfg["skirt"]["y_max"])
    if "tail" in cfg:
        t = cfg["tail"]
        add("tail", (k >= t["z_min"]) & (j <= t.get("y_max", Y)))
    legs = []
    if "leg_h" in cfg:
        # feet: separate clusters touching the ground; each leg grows up from its foot to leg_h
        # a foot: a cluster of (x, z) columns whose lowest voxel is near the ground (models don't stand perfectly level)
        body_solid = solid & (bone == 0)
        anyc = body_solid.any(1)
        lowest = np.where(anyc, np.argmax(body_solid, axis=1), 10 ** 6)
        low = anyc & (lowest <= cfg.get("foot_y", 3))
        lab2, n = ndimage.label(low)
        feet = [np.argwhere(lab2 == c) for c in range(1, n + 1)]            # (x, z) pairs
        feet = [f for f in feet if len(f) >= 3]
        if feet:
            cents = np.array([[f[:, 0].mean(), f[:, 1].mean()] for f in feet])
            radius = np.array([max(2.5, 0.5 * max(np.ptp(f[:, 0]), np.ptp(f[:, 1])) + 2.0) for f in feet])
            zc = cents[:, 1].mean()
            leg_of = np.full(solid.shape, -1)
            cand = solid & (bone == 0) & (j < cfg["leg_h"])
            for a, b2, c in zip(*np.nonzero(cand)):
                d = np.hypot(cents[:, 0] - a, cents[:, 1] - c)
                f = int(np.argmin(d))
                if d[f] <= radius[f]:
                    leg_of[a, b2, c] = f
            order = sorted(range(len(feet)), key=lambda f: (cents[f, 1], -cents[f, 0]))
            for f in order:
                side = "left" if cents[f, 0] >= cx else "right"
                end = "front" if cents[f, 1] <= zc else "back"
                base = f"leg_{end}_{side}"
                nm = base
                n2 = 2
                while nm in names:
                    nm = f"{base}{n2}"
                    n2 += 1
                names.append(nm)
                bone[leg_of == f] = len(names) - 1
                legs.append(nm)
    return bone, names, legs


def pivots(bone, names, lo, solid):
    piv = {}
    for b, nm in enumerate(names):
        idx = np.argwhere(bone == b)
        if not len(idx):
            piv[nm] = [0, 0, 0]
            continue
        mn, mx, mean = idx.min(0) + lo, idx.max(0) + 1 + lo, idx.mean(0) + lo + 0.5
        if nm == "body":
            piv[nm] = [0, round(float(mean[1]), 1), round(float(mean[2]), 1)]
        elif nm.startswith("leg"):
            piv[nm] = [round(float(mean[0]), 1), float(mx[1]), round(float(mean[2]), 1)]
        elif nm == "head":
            piv[nm] = [round(float(mean[0]), 1), round(float(mn[1] + (mx[1] - mn[1]) * 0.3), 1), float(mx[2])]
        elif nm == "tail":
            piv[nm] = [round(float(mean[0]), 1), round(float(mean[1]), 1), float(mn[2])]
        elif nm.startswith("wing"):
            inner = mn[0] if nm == "wing_left" else mx[0]
            piv[nm] = [float(inner), round(float(mean[1]), 1), round(float(mean[2]), 1)]
        elif nm in ("cap", "mane"):
            piv[nm] = [round(float(mean[0]), 1), float(mn[1]), round(float(mean[2]), 1)]
        elif nm == "skirt":
            piv[nm] = [round(float(mean[0]), 1), float(mx[1]), round(float(mean[2]), 1)]
        else:
            piv[nm] = [round(float(v), 1) for v in mean]
    return piv


# ---------------------------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------------------------

def h3(i, j, k, salt=0):
    """A stable per-voxel pseudo-random number in [0, 1)."""
    return ((i * 73856093) ^ (j * 19349663) ^ (k * 83492791) ^ (salt * 2654435761)) % 1000 / 1000


def paint(sp, solid, bone, names, lo, shiny):
    """-> (colour [X,Y,Z,3] uint8, glow [X,Y,Z,3] uint8 with zeros where nothing glows)."""
    X, Y, Z = solid.shape
    i, j, k = np.indices(solid.shape)
    cx = -lo[0]
    col = np.zeros(solid.shape + (3,), float)
    glow = np.zeros(solid.shape + (3,), float)
    # thin parts (spikes, fins, strands, crystals): nowhere near them is the model more than ~2 voxels thick
    edt = ndimage.distance_transform_edt(np.pad(solid, 1))[1:-1, 1:-1, 1:-1]
    thin = solid & (ndimage.maximum_filter(edt, size=5) <= 2.0)
    top_open = solid & ~np.pad(solid, ((0, 0), (0, 1), (0, 0)))[:, 1:, :]
    bot_open = solid & ~np.pad(solid, ((0, 0), (1, 0), (0, 0)))[:, :-1, :]
    front = np.full((X, Y), 10 ** 6)
    for a, b, c in zip(*np.nonzero(solid)):
        front[a, b] = min(front[a, b], c)
    on_front = np.zeros(solid.shape, bool)
    for a, b, c in zip(*np.nonzero(solid)):
        on_front[a, b, c] = c <= front[a, b]
    B = {nm: bone == n for n, nm in enumerate(names)}
    none = np.zeros(solid.shape, bool)
    head = B.get("head", none)
    legs = np.zeros(solid.shape, bool)
    for nm, m in B.items():
        if nm.startswith("leg"):
            legs |= m

    def put(mask, c):
        col[mask & solid] = c

    def shine(mask, c):
        glow[mask & solid] = c

    def eyes(colour, glow_colour, dx=2, rows=None):
        """Two eye voxels on the front of the head."""
        if not head.any():
            return
        hy = np.argwhere(head)[:, 1]
        r0 = rows if rows is not None else int(hy.min() + (hy.max() - hy.min()) * 0.55)
        m = head & on_front & ((j == r0) | (j == r0 + 1)) & (np.abs(np.abs(i - cx) - dx) <= 0)
        put(m, colour)
        shine(m, glow_colour)

    if sp == "greattusk":
        fur, fur_l, hoof = ((74, 59, 51), (107, 84, 70), (40, 32, 28)) if not shiny else ((62, 72, 86), (96, 110, 126), (34, 38, 46))
        ivory, ring = ((234, 220, 192), (190, 172, 140)) if not shiny else ((244, 238, 226), (200, 196, 186))
        amber = (255, 140, 52) if not shiny else (120, 220, 255)
        put(solid, fur)
        put(top_open, fur_l)
        put(legs & (j <= 1), hoof)
        tusk = (head & (np.abs(i - cx) >= 6)) | (thin & (k <= Z * 0.4) & (j >= Y * 0.45))       # the great curled tusks
        put(tusk, ivory)
        put(tusk & ((j + k) % 4 == 0), ring)
        crystals = thin & ~tusk & ~head & (j >= 4)
        put(crystals, amber)
        shine(crystals & (np.vectorize(h3)(i, j, k) < 0.5), amber)
        put(B.get("tail", none) & thin, amber)
        eyes((230, 40, 30) if not shiny else (60, 200, 255), (255, 60, 40) if not shiny else (90, 220, 255), dx=3)
    elif sp == "screamtail":
        pink, pink_l, belly = ((245, 160, 198), (255, 196, 222), (255, 214, 230)) if not shiny else ((250, 214, 120), (255, 234, 168), (255, 246, 214))
        magenta = (210, 64, 138) if not shiny else (232, 140, 40)
        put(solid, pink)
        put(thin, pink_l)
        put(on_front & ~head & (np.abs(i - cx) <= 4) & (j >= 4) & (j <= 14), belly)
        tail = B.get("tail", none)
        ang = np.arctan2(j - 6, k - 24)
        put(tail & (((ang * 3 + np.hypot(j - 6, k - 24) * 0.6).astype(int)) % 2 == 0), pink_l)   # the tail's swirl
        put(head & on_front & (j >= 25) & (np.abs(i - cx) <= 2), magenta)                       # forehead spiral
        put(head & (j >= 28), magenta)                                                          # ear tips
        put(legs, pink_l)
        eyes((40, 110, 120) if not shiny else (120, 60, 160), (110, 230, 240) if not shiny else (200, 140, 255), dx=3)
    elif sp == "brutebonnet":
        cap_c, spot, gill = ((180, 38, 58), (240, 226, 196), (218, 194, 160)) if not shiny else ((70, 150, 210), (236, 244, 250), (196, 214, 226))
        stem, stem_d = ((112, 98, 88), (84, 72, 64)) if not shiny else ((150, 140, 120), (118, 108, 92))
        scale_c, scale_l, spine = ((63, 74, 53), (93, 107, 75), (120, 30, 40)) if not shiny else ((90, 70, 110), (124, 100, 146), (220, 160, 60))
        orange = (224, 122, 46) if not shiny else (120, 220, 200)
        cap = B.get("cap", none)
        put(solid, stem)
        put(solid & (j < 14), scale_c)                                                          # the reptile
        put(solid & (j < 14) & (((i + k) // 2) % 2 == 0), scale_l)
        put(thin & (j < 14) & top_open, spine)
        put(B.get("tail", none) & thin, spine)
        put(solid & (j >= 14) & ~cap & ((j % 4) == 0), stem_d)
        put(solid & (j >= 14) & ~cap & thin, orange)                                            # little mushrooms
        shine(solid & (j >= 14) & ~cap & thin & (np.vectorize(h3)(i, j, k, 3) < 0.25), orange)
        put(cap, cap_c)
        put(cap & (np.vectorize(h3)(i // 2, j // 2, k // 2, 7) < 0.18) & top_open, spot)
        put(cap & bot_open, gill)
        eyes((240, 210, 60) if not shiny else (255, 120, 200), (255, 230, 90) if not shiny else (255, 140, 210), dx=2)
    elif sp == "fluttermane":
        body_c, body_d = ((76, 42, 107), (52, 28, 78)) if not shiny else ((70, 120, 90), (46, 86, 62))
        mane_c, mane_l = ((194, 64, 143), (232, 120, 186)) if not shiny else ((236, 196, 86), (252, 226, 140))
        hat, jewel = ((46, 26, 69), (232, 71, 95)) if not shiny else ((30, 60, 46), (120, 220, 255))
        mane = B.get("mane", none)
        skirt = B.get("skirt", none)
        put(solid, body_c)
        put(skirt, body_d)
        put(skirt & thin & (j <= 3), mane_l)                                                    # tattered hem
        put(mane, mane_c)
        put(mane & (((j + k) // 3) % 2 == 0), mane_l)
        put(head & (j >= 29), hat)
        brim = head & (j >= 28) & (j <= 29)
        put(brim, mane_c)
        shine(brim & (np.vectorize(h3)(i, j, k, 5) < 0.4), mane_l)
        beads = thin & (j >= 16) & (j <= 27) & ~mane & (np.abs(i - cx) >= 6) & (np.abs(i - cx) <= 8) & on_front
        put(beads, jewel)
        shine(beads, jewel)
        eyes((255, 210, 90) if not shiny else (255, 120, 120), (255, 226, 120) if not shiny else (255, 150, 150), dx=2)
    elif sp == "slitherwing":
        fluff, brown = ((242, 230, 207), (107, 74, 53)) if not shiny else ((236, 242, 246), (70, 84, 110))
        wing_a, wing_b, vein = ((240, 138, 43), (255, 210, 90), (90, 51, 32)) if not shiny else ((120, 200, 240), (220, 246, 255), (40, 70, 110))
        ember = (255, 110, 40) if not shiny else (130, 230, 255)
        put(solid, fluff)
        put(legs | B.get("tail", none), brown)
        put(B.get("tail", none) & ((k % 4) == 0), fluff)
        put(solid & bot_open & ~legs, brown)
        for w in ("wing_left", "wing_right"):
            m = B.get(w, none)
            dist = np.abs(i - cx)
            t = np.clip((dist - 6) / 18 + (j - 12) / 60, 0, 1)
            wc = np.array(wing_a)[None] * (1 - t[m & solid])[:, None] + np.array(wing_b)[None] * t[m & solid][:, None]
            col[m & solid] = wc
            put(m & (((dist + j) % 7) == 0), vein)
            edge = m & thin & (np.vectorize(h3)(i, j, k, 9) < 0.35)
            put(edge, ember)
            shine(edge, ember)
        put(head & thin & (j >= 20), wing_a)                                                    # antennae
        shine(head & thin & (j >= 22), ember)
        eyes((70, 150, 255) if not shiny else (255, 140, 60), (110, 180, 255) if not shiny else (255, 170, 90), dx=2)
    # light from above, a little per-voxel variation (glowing voxels stay clean)
    shade = 1 + (np.vectorize(h3)(i, j, k, 11) - 0.5) * 0.09
    shade = shade + np.where(top_open, 0.06, 0) - np.where(bot_open, 0.08, 0)
    lit = (glow.sum(-1) == 0)
    col = np.where(lit[..., None], col * shade[..., None], col)
    return np.clip(col, 0, 255).astype(np.uint8), np.clip(glow, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------------------------
# Animations
# ---------------------------------------------------------------------------------------------

def animations(sp, names, legs, piv):
    kind = MEGAS[sp]["kind"]
    has = set(names)
    A = {}
    bob = 1.0 if kind == "floater" else 0.3

    def legs_walk(period, amp):
        out = {}
        for n, leg in enumerate(sorted(legs)):
            phase = 0.5 * ((n % 2) ^ (("back" in leg) and kind == "quadruped"))
            out[leg] = {"rotation": track(period, lambda t, ph=phase: [amp * sin(t, 1, ph), 0, 0])}
        return out

    idle = {"body": {"position": track(3, lambda t: [0, -bob * (1 - math.cos(2 * math.pi * t)) / 2 if kind != "floater" else bob * sin(t), 0])}}
    if "head" in has:
        idle["head"] = {"rotation": track(3, lambda t: [2 * sin(t, 1, 0.2), 4 * sin(t, 0.5), 0])}
    if "tail" in has:
        idle["tail"] = {"rotation": track(3, lambda t: [0, 8 * sin(t), 0])}
    if "cap" in has:
        idle["cap"] = {"rotation": track(3, lambda t: [1.5 * sin(t, 1, 0.3), 0, 2 * sin(t)])}
    if "mane" in has:
        idle["mane"] = {"rotation": track(3, lambda t: [3 * sin(t, 1, 0.25), 6 * sin(t), 0])}
    if "skirt" in has:
        idle["skirt"] = {"rotation": track(3, lambda t: [4 * sin(t, 1, 0.4), 0, 3 * sin(t)])}
    if "wing_left" in has:
        idle["wing_left"] = {"rotation": track(3, lambda t: [0, 6 * sin(t), 4 * sin(t)])}
        idle["wing_right"] = {"rotation": track(3, lambda t: [0, -6 * sin(t), -4 * sin(t)])}
    A["ground_idle"] = {"loop": True, "animation_length": 3.0, "bones": idle}

    walk = {"body": {"position": track(1, lambda t: [0, -0.4 * abs(sin(t)), 0]), "rotation": track(1, lambda t: [0, 0, 1.5 * sin(t)])}}
    if kind == "floater":
        walk = {"body": {"rotation": track(1.5, lambda t: [12, 0, 2 * sin(t)]), "position": track(1.5, lambda t: [0, 0.8 * sin(t, 2), 0])}}
    if "head" in has:
        walk["head"] = {"rotation": track(1, lambda t: [3 * sin(t, 2, 0.25), 0, 0])}
    if "tail" in has:
        walk["tail"] = {"rotation": track(1, lambda t: [0, 12 * sin(t), 0])}
    if "mane" in has:
        walk["mane"] = {"rotation": track(1.5, lambda t: [-10 + 3 * sin(t, 2), 8 * sin(t), 0])}
    if "skirt" in has:
        walk["skirt"] = {"rotation": track(1.5, lambda t: [-12 + 4 * sin(t, 2), 0, 0])}
    if "cap" in has:
        walk["cap"] = {"rotation": track(1, lambda t: [2 * sin(t, 2), 0, 3 * sin(t)])}
    if "wing_left" in has:
        walk["wing_left"] = {"rotation": track(1, lambda t: [0, 10 * sin(t, 2), 14 * sin(t, 2)])}
        walk["wing_right"] = {"rotation": track(1, lambda t: [0, -10 * sin(t, 2), -14 * sin(t, 2)])}
    walk.update(legs_walk(1, 22))
    A["ground_walk"] = {"loop": True, "animation_length": 1.5 if kind == "floater" else 1.0, "bones": walk}

    battle = {"body": {"position": track(2, lambda t: [0, -0.5 - 0.3 * sin(t) if kind != "floater" else 0.8 * sin(t), 0])}}
    if "head" in has:
        battle["head"] = {"rotation": track(2, lambda t: [10 + 2 * sin(t), 3 * sin(t, 0.5), 0])}
    if "tail" in has:
        battle["tail"] = {"rotation": track(2, lambda t: [-10, 14 * sin(t), 0])}
    if "mane" in has:
        battle["mane"] = {"rotation": track(2, lambda t: [6 * sin(t), 10 * sin(t, 1, 0.3), 0])}
    if "skirt" in has:
        battle["skirt"] = {"rotation": track(2, lambda t: [6 * sin(t, 1, 0.4), 0, 0])}
    if "cap" in has:
        battle["cap"] = {"rotation": track(2, lambda t: [4, 0, 3 * sin(t)])}
    if "wing_left" in has:
        battle["wing_left"] = {"rotation": track(2, lambda t: [0, 18 + 8 * sin(t, 2), 10])}
        battle["wing_right"] = {"rotation": track(2, lambda t: [0, -18 - 8 * sin(t, 2), -10])}
    A["battle_idle"] = {"loop": True, "animation_length": 2.0, "bones": battle}

    leg_top = max((piv[l][1] for l in legs), default=0)
    drop = -(leg_top - 1) if legs else (-4 if kind == "floater" else -2)
    sleep = {"body": {"position": track(4, lambda t: [0, drop - 0.3 * (1 - math.cos(2 * math.pi * t)) / 2, 0])}}
    for leg in legs:
        sleep[leg] = {"position": track(4, lambda t: [0, drop, 0]), "rotation": track(4, lambda t, l=leg: [-75 if "front" in l else 60, 0, 0])}
    if "head" in has:
        sleep["head"] = {"rotation": track(4, lambda t: [16 + 1.5 * sin(t), 0, 0])}
    if "tail" in has:
        sleep["tail"] = {"rotation": track(4, lambda t: [0, 35, 0])}
    if "wing_left" in has:
        sleep["wing_left"] = {"rotation": track(4, lambda t: [0, -30, -8])}
        sleep["wing_right"] = {"rotation": track(4, lambda t: [0, 30, 8])}
    if "mane" in has:
        sleep["mane"] = {"rotation": track(4, lambda t: [10, 0, 0])}
    A["sleep"] = {"loop": True, "animation_length": 4.0, "bones": sleep}

    cry = {"body": {"position": keys([(0, [0, 0, 0]), (0.35, [0, 1, 0]), (1.1, [0, 0.8, 0]), (1.5, [0, 0, 0])])}}
    if "head" in has:
        cry["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [-25, 0, 0]), (0.55, [-22, -8, 0]), (0.75, [-22, 8, 0]), (1.1, [-15, 0, 0]), (1.5, [0, 0, 0])])}
    if "wing_left" in has:
        cry["wing_left"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [0, 25, 15]), (1.1, [0, 20, 12]), (1.5, [0, 0, 0])])}
        cry["wing_right"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [0, -25, -15]), (1.1, [0, -20, -12]), (1.5, [0, 0, 0])])}
    if "mane" in has:
        cry["mane"] = {"rotation": keys([(0, [0, 0, 0]), (0.35, [-15, 10, 0]), (1.1, [-10, -10, 0]), (1.5, [0, 0, 0])])}
    A["cry"] = {"animation_length": 1.5, "bones": cry}

    phys = {"body": {"position": keys([(0, [0, 0, 0]), (0.25, [0, 0.4, 2]), (0.45, [0, -0.6, -5]), (0.8, [0, 0, 0])]),
                     "rotation": keys([(0, [0, 0, 0]), (0.25, [-6, 0, 0]), (0.45, [10, 0, 0]), (0.8, [0, 0, 0])])}}
    if "head" in has:
        phys["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [-20, 0, 0]), (0.45, [30, 0, 0]), (0.8, [0, 0, 0])])}
    if "tail" in has:
        phys["tail"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -30, 0]), (0.45, [0, 40, 0]), (0.8, [0, 0, 0])])}
    if "wing_left" in has:
        phys["wing_left"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, 30, 20]), (0.45, [0, -10, -10]), (0.8, [0, 0, 0])])}
        phys["wing_right"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -30, -20]), (0.45, [0, 10, 10]), (0.8, [0, 0, 0])])}
    A["physical"] = {"animation_length": 0.8, "bones": phys}

    spec = {"body": {"position": keys([(0, [0, 0, 0]), (0.3, [0, 0.8, 0]), (0.6, [0, 0.8, 0]), (1.0, [0, 0, 0])])}}
    if "head" in has:
        spec["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [-18, 0, 0]), (0.6, [-18, 0, 0]), (1.0, [0, 0, 0])])}
    for w, sgn in (("wing_left", 1), ("wing_right", -1)):
        if w in has:
            spec[w] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [0, 20 * sgn, 20 * sgn]), (0.6, [0, 20 * sgn, 20 * sgn]), (1.0, [0, 0, 0])])}
    if "cap" in has:
        spec["cap"] = {"rotation": keys([(0, [0, 0, 0]), (0.3, [0, 0, 6]), (0.45, [0, 0, -6]), (0.6, [0, 0, 4]), (1.0, [0, 0, 0])])}
    A["special"] = {"animation_length": 1.0, "bones": spec}

    status = {"body": {"position": keys([(0, [0, 0, 0]), (0.5, [0, 0.6, 0]), (1.0, [0, 0, 0])])}}
    if "head" in has:
        status["head"] = {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -14, 0]), (0.5, [0, 14, 0]), (0.75, [0, -6, 0]), (1.0, [0, 0, 0])])}
    A["status"] = {"animation_length": 1.0, "bones": status}

    faint = {"body": {"position": keys([(0, [0, 0, 0]), (2.0, [0, drop, 0])]), "rotation": keys([(0, [0, 0, 0]), (2.0, [8, 0, 10])])}}
    for leg in legs:
        faint[leg] = {"position": keys([(0, [0, 0, 0]), (2.0, [0, drop, 0])]),
                      "rotation": keys([(0, [0, 0, 0]), (2.0, [-75 if "front" in leg else 60, 0, 0])])}
    if "head" in has:
        faint["head"] = {"rotation": keys([(0, [0, 0, 0]), (2.0, [28, 0, 0])])}
    A["faint"] = {"loop": "hold_on_last_frame", "animation_length": 2.0, "bones": faint}
    return {"format_version": "1.8.0", "animations": {f"animation.{group_of(sp)}.{k}": v for k, v in A.items()}}


def poser(sp, names):
    g = group_of(sp)
    b = lambda a: f"q.bedrock('{g}', '{a}')"
    look = ["q.look('head')"] if "head" in names else []
    floater = MEGAS[sp]["kind"] == "floater"
    stand_types = ["STAND", "NONE", "FLOAT", "HOVER", "PORTRAIT", "PROFILE"]
    h = MEGAS[sp]["height"] * MEGAS[sp]["scale"] / 16
    return {
        "portraitScale": round(1.6 / max(1.0, h), 2), "portraitTranslation": [0, round(h * 0.55, 2), 0],
        "profileScale": round(0.95 / max(1.0, h), 2), "profileTranslation": [0, round(h * 0.25, 2), 0],
        "rootBone": name_of(sp),
        "animations": {
            "cry": f"q.bedrock_stateful('{g}', 'cry')",
            "physical": f"q.bedrock_primary('{g}', 'physical', q.curve('symmetrical_wide'))",
            "special": f"q.bedrock_primary('{g}', 'special', q.curve('symmetrical_wide'))",
            "status": f"q.bedrock_primary('{g}', 'status', q.curve('symmetrical_wide'))",
            "faint": f"q.bedrock_primary('{g}', 'faint', q.curve('one'))",
        },
        "poses": {
            "battle_standing": {"poseTypes": ["STAND", "FLOAT", "HOVER"], "isBattle": True, "transformTicks": 10,
                                "animations": look + [b("battle_idle")]},
            "standing": {"poseTypes": stand_types, "isBattle": False, "transformTicks": 10, "animations": look + [b("ground_idle")]},
            "walking": {"poseTypes": ["WALK", "SWIM", "FLY"], "transformTicks": 10, "animations": look + [b("ground_walk")]},
            "sleeping": {"poseTypes": ["SLEEP"], "transformTicks": 20, "animations": [b("sleep")]},
        },
    }


# ---------------------------------------------------------------------------------------------
# Building
# ---------------------------------------------------------------------------------------------

def build_model(sp):
    cfg = MEGAS[sp]
    d = np.load(HERE / f"mega_{sp}_voxels.npz")
    solid, lo = d["solid"], d["lo"]
    bone, names, legs = segment(sp, solid, lo)
    piv = pivots(bone, names, lo, solid)
    boxes = []
    for b in range(len(names)):
        boxes += [(b, box) for box in vx.greedy_boxes(bone == b)]
    nets = [(2 * ((i1 - i0) + (k1 - k0)), (k1 - k0) + (j1 - j0)) for _, (i0, j0, k0, i1, j1, k1) in boxes]
    tw = 64
    while True:
        pos, used = vx.pack(nets, tw)
        if used <= tw:
            break
        tw *= 2
    th = tw
    nm = name_of(sp)
    tex_dir = RES / "assets" / MOD / "textures" / "pokemon" / cfg["folder"]
    tex_dir.mkdir(parents=True, exist_ok=True)
    for shiny in (False, True):
        col, glow = paint(sp, solid, bone, names, lo, shiny)
        sfx = "_shiny" if shiny else ""
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        for (b, box), uv in zip(boxes, pos):
            vx.paint_box(img, uv, box, lambda i, j, k: tuple(int(v) for v in col[i, j, k]) + (255,))
        img.save(tex_dir / f"{nm}{sfx}.png", optimize=True)
        for f in range(3):                                   # the glow flickers a little
            rng = random.Random(f"{sp}:{shiny}:{f}")
            flick = {}

            def gcol(i, j, k):
                g = glow[i, j, k]
                if not g.any():
                    return (0, 0, 0, 0)
                if (i, j, k) not in flick:
                    flick[(i, j, k)] = 0.72 + 0.28 * rng.random()
                return tuple(int(v * flick[(i, j, k)]) for v in g) + (255,)
            gimg = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            for (b, box), uv in zip(boxes, pos):
                vx.paint_box(gimg, uv, box, gcol)
            gimg.save(tex_dir / f"{nm}{sfx}_glow_{f}.png", optimize=True)

    bones = [{"name": nm, "pivot": [0, 0, 0]}]
    parent_of = lambda n: nm if n == "body" or n.startswith("leg") else "body"
    for b, n in enumerate(names):
        bj = {"name": n, "parent": parent_of(n), "pivot": piv[n], "cubes": []}
        for (bb, (i0, j0, k0, i1, j1, k1)), uv in zip(boxes, pos):
            if bb == b:
                bj["cubes"].append({"origin": [int(lo[0] + i0), int(lo[1] + j0), int(lo[2] + k0)],
                                    "size": [i1 - i0, j1 - j0, k1 - k0], "uv": [int(uv[0]), int(uv[1])]})
        bones.append(bj)
    bones.append({"name": "locator_root", "parent": nm, "pivot": [0, 0, 0]})
    bones.append({"name": "locator_top", "parent": nm, "pivot": [0, float(solid.shape[1]), 0]})
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "models" / cfg["folder"] / f"{nm}.geo.json", {
        "format_version": "1.12.0", "minecraft:geometry": [{
            "description": {"identifier": f"geometry.{nm}", "texture_width": tw, "texture_height": th,
                            "visible_bounds_width": 6, "visible_bounds_height": 5, "visible_bounds_offset": [0, 2, 0]},
            "bones": bones}]})
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "animations" / cfg["folder"] / f"{group_of(sp)}.animation.json",
               animations(sp, names, legs, piv))
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "posers" / cfg["folder"] / f"{nm}.json", poser(sp, names))
    print(f"{sp}: {len(boxes)} cubes, texture {tw}x{th}, bones {names}")
    return names


def data_files(sp):
    cfg = MEGAS[sp]
    nm = name_of(sp)
    tex = lambda n: f"{MOD}:textures/pokemon/{cfg['folder']}/{n}.png"
    glow = lambda sfx: {"name": "cobbleeffort_mega_glow", "emissive": True, "translucent": True,
                        "texture": {"frames": [tex(f"{nm}{sfx}_glow_{f}") for f in range(3)], "fps": 6, "loop": True}}
    # the mega's look: only when the Pokémon has the "mega" aspect, so the base form (from AllTheMons x MSD) is untouched
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / "megas" / cfg["folder"] / f"10_{nm}.json", {
        "species": f"cobblemon:{sp}", "order": 10,
        "variations": [
            {"aspects": ["mega"], "poser": f"{MOD}:{nm}", "model": f"{MOD}:{nm}.geo", "texture": tex(nm), "layers": [glow("")]},
            {"aspects": ["mega", "shiny"], "texture": tex(f"{nm}_shiny"), "layers": [glow("_shiny")]},
        ]})
    hp, atk, de, spa, spd, spe = cfg["stats"]
    write_json(RES / "data" / MOD / "species_additions" / f"{sp}_mega.json", {
        "target": f"cobblemon:{sp}",
        "forms": [{
            "name": "Mega", "primaryType": cfg["types"][0], "secondaryType": cfg["types"][1],
            "abilities": [cfg["ability"], cfg["ability"], f"h:{cfg['ability']}"],
            "pokedex": [f"cobblemon.species.{sp}-mega.desc"], "labels": ["gen9", "paradox", "mega"], "aspects": ["mega"],
            "baseStats": {"hp": hp, "attack": atk, "defence": de, "special_attack": spa, "special_defence": spd, "speed": spe},
            "baseScale": cfg["scale"], "hitbox": {"width": cfg["hitbox"][0], "height": cfg["hitbox"][1], "fixed": False},
            "battleOnly": True, "dynamaxBlocked": True,
        }]})
    write_json(RES / "data" / MOD / "mega_showdown" / "mega" / f"{cfg['stone']}.json", {
        "showdown_id": cfg["stone"], "pokemons": [cfg["display"]],
        "aspect_conditions": {"apply": {"aspects": ["mega_evolution=mega"]}, "revert": {"aspects": ["mega_evolution=none"]}}})
    js = RES / "data" / MOD / "mega_showdown" / "showdown" / "held_items" / f"{cfg['stone']}.js"
    js.parent.mkdir(parents=True, exist_ok=True)
    js.write_text(f"""({{
  name: "{cfg['stone_name']}",
  spritenum: 0,
  megaStone: {{ "{cfg['display']}": "{cfg['display']}-Mega" }},
  itemUser: ["{cfg['display']}"],
  onTakeItem(item, source) {{
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  }},
  num: {9100 + list(MEGAS).index(sp)},
  gen: 9,
  isNonstandard: "Past",
}})
""")
    write_json(RES / "data" / MOD / "dex_entry_additions" / f"{sp}_mega.json", {
        "entryId": f"cobblemon:{sp}", "forms": [{"displayForm": "Mega", "unlockForms": ["Mega"]}]})
    r = cfg["recipe"]
    write_json(RES / "data" / MOD / "recipe" / f"{cfg['stone']}.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": r["pattern"],
        "key": {c: {"item": it} for c, it in r["key"].items()},
        "result": {"id": BASE_ITEM, "count": 1, "components": stone_components(sp)}})


def stone_components(sp):
    cfg = MEGAS[sp]
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.{cfg['stone']}", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.{cfg['stone']}.tooltip", "color": "gray", "italic": False})],
        "minecraft:custom_model_data": CMD_BASE + 1 + list(MEGAS).index(sp),
        "minecraft:rarity": "epic",
        "minecraft:max_stack_size": 1,
        "mega_showdown:registry_type_component": "mega",
        "mega_showdown:registry_location_component": f"{MOD}:{cfg['stone']}",
    }


def stone_icons():
    """16x16 icons: a round gem in the Pokémon's colours with Mega Showdown's double-helix mark."""
    out = RES / "assets" / MOD / "textures" / "item"
    out.mkdir(parents=True, exist_ok=True)
    for sp, cfg in MEGAS.items():
        a, b = cfg["stone_colours"]
        img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        px = img.load()
        for y in range(16):
            for x in range(16):
                dx, dy = x - 7.5, y - 7.5
                r = math.hypot(dx, dy)
                if r > 6.6:
                    continue
                t = (dy + 7) / 14                                     # lighter at the top
                c = tuple(int(a[n] * (1.25 - 0.5 * t)) for n in range(3))
                if r > 5.6:
                    c = tuple(int(v * 0.6) for v in c)               # rim
                hx = 7.5 + 2.6 * math.sin(y * 0.9)
                if abs(x - hx) < 0.9 and 2 <= y <= 13:
                    c = b
                hx2 = 7.5 - 2.6 * math.sin(y * 0.9)
                if abs(x - hx2) < 0.9 and 2 <= y <= 13:
                    c = tuple(min(255, int(v * 1.2 + 40)) for v in b)
                if (x, y) in ((5, 4), (6, 4), (5, 5)):
                    c = (255, 255, 255)                              # shine
                px[x, y] = tuple(max(0, min(255, v)) for v in c) + (255,)
        img.save(out / f"{cfg['stone']}.png")
        write_json(RES / "assets" / MOD / "models" / "item" / f"{cfg['stone']}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{cfg['stone']}"}})
    write_json(RES / "assets" / "minecraft" / "models" / "item" / "amethyst_shard.json", {
        "parent": "minecraft:item/generated", "textures": {"layer0": "minecraft:item/amethyst_shard"},
        "overrides": [{"predicate": {"custom_model_data": CMD_BASE + 1 + n}, "model": f"{MOD}:item/{cfg['stone']}"}
                      for n, (sp, cfg) in enumerate(MEGAS.items())]})


def lang():
    path = RES / "assets" / MOD / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    for sp, cfg in MEGAS.items():
        data[f"item.{MOD}.{cfg['stone']}"] = cfg["stone_name"]
        data[f"item.{MOD}.{cfg['stone']}.tooltip"] = f"Lets {cfg['display']} Mega Evolve in battle."
        data[f"cobblemon.species.{sp}-mega.desc"] = cfg["dex_text"]
    write_json(path, dict(sorted(data.items())))


def feature_assignment():
    write_json(RES / "data" / MOD / "species_feature_assignments" / "paradox_megas.json",
               {"pokemon": list(MEGAS), "features": ["mega_evolution"]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", action="append", default=[], help="species=path of a source mesh to (re)voxelize")
    args = ap.parse_args()
    for s in args.src:
        sp, path = s.split("=", 1)
        cfg = MEGAS[sp]
        P, C, F = vx.load_mesh(path, samples=3_000_000)
        solid, surf, col, lo = vx.voxelize(P, C, F, cfg["height"], front=cfg["front"])
        np.savez_compressed(HERE / f"mega_{sp}_voxels.npz", solid=solid, lo=lo)
        print(f"{sp}: voxels {solid.shape}")
    manifest = []
    for sp, cfg in MEGAS.items():
        build_model(sp)
        data_files(sp)
        for sfx in ("", "_shiny"):
            manifest.append({"species": f"{sp}_mega{sfx}", "folder": cfg["folder"], "model": f"{MOD}:{name_of(sp)}.geo",
                             "original": None, "retextured": f"{MOD}:textures/pokemon/{cfg['folder']}/{name_of(sp)}{sfx}.png",
                             "layers": [{"original": None, "retextured": f"{MOD}:textures/pokemon/{cfg['folder']}/{name_of(sp)}{sfx}_glow_0.png", "emissive": True}]})
    stone_icons()
    lang()
    feature_assignment()
    write_json(HERE.parent / "preview" / "manifest_megas.json", manifest)
    write_json(HERE.parent / "readme" / "_megas.json", {sp: {k: cfg[k] for k in ("display", "stone_name", "types", "ability", "stats")} | {"recipe": cfg["recipe"]} for sp, cfg in MEGAS.items()})


if __name__ == "__main__":
    main()
