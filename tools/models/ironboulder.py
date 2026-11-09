#!/usr/bin/env python3
"""
Iron Boulder (#1022): a new Pokémon model for CobbleEffort, built from ellecat5112's model (made with Tripo AI).

Cobblemon 1.8.4 has Iron Boulder's species data (Rock/Psychic, Quark Drive, Scarlet/Violet stats and learnset,
Mighty Cleave at 56) but no model, so it's unimplemented. This script makes it playable:

  assets/cobbleeffort/bedrock/pokemon/models/1022_ironboulder/ironboulder.geo.json    model (voxelized, box UV)
  assets/cobbleeffort/textures/pokemon/1022_ironboulder/ironboulder[_shiny].png       textures
  assets/cobbleeffort/bedrock/pokemon/animations/1022_ironboulder/...animation.json   animations
  assets/cobbleeffort/bedrock/pokemon/posers/1022_ironboulder/ironboulder.json        poser
  assets/cobbleeffort/bedrock/pokemon/resolvers/1022_ironboulder/1_ironboulder_base.json
  data/cobbleeffort/species_additions/ironboulder.json    implemented, size, hitbox
  data/cobbleeffort/spawn_pool_world/1022_ironboulder.json  "roaming legendary" spawns

Usage:
  python3 tools/models/ironboulder.py --obj <model.obj>   # (re)voxelize the source mesh -> ironboulder_voxels.npz
  python3 tools/models/ironboulder.py                     # build everything from the committed voxels

Every id is in the cobbleeffort namespace (and the animation group is "cobbleeffort_ironboulder"), so nothing clashes
with a resource pack that also adds an Iron Boulder; the resolver's order 1 puts this model above an order-0 one.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _voxel as vx  # noqa: E402
from _anim import keys, sin, track, write_json  # noqa: E402

ROOT = HERE.parent.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"
NAME = "ironboulder"
FOLDER = "1022_ironboulder"
GROUP = f"{MOD}_{NAME}"                  # animation groups are global by file name
VOXELS = HERE / f"{NAME}_voxels.npz"
HEIGHT = 28                              # model units (16 = one block) before baseScale
BASE_SCALE = 0.86                        # 28 units * 0.86 / 16 = 1.5 blocks, Iron Boulder's 1.5 m
PALETTE_SIZE = 10

BONES = ["body", "head", "leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"]


# ---------------------------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------------------------

def segment(solid, lo):
    """Bone of every voxel (index into BONES), from the model's layout (grid i = x, j = y, k = z; front is low k,
    the left side high i). Head and blades: the front 7 rows. Back legs: everything behind the hips (k >= 27).
    Front legs: below the chest (j <= 9) under the front half. The rest is the body."""
    X, Y, Z = solid.shape
    i, j, k = np.indices(solid.shape)
    left = (lo[0] + i) >= 0
    lab = np.zeros(solid.shape, int)
    lab[k <= 6] = 1
    front_leg = (j <= 9) & (k >= 9) & (k <= 22)
    lab[front_leg & left] = 2
    lab[front_leg & ~left] = 3
    back_leg = k >= 27
    lab[back_leg & left] = 4
    lab[back_leg & ~left] = 5
    lab[~solid] = -1
    return lab


def pivots(lab, lo):
    """Bone pivots in model units: legs at the top of the leg (shoulder / hip), the head where it meets the body."""
    def ext(b):
        idx = np.argwhere(lab == b)
        return idx.min(0) + lo, idx.max(0) + 1 + lo, idx.mean(0) + lo + 0.5
    out = {"body": [0, 12, 0]}
    hmin, hmax, _ = ext(1)
    out["head"] = [0, float(hmin[1] + hmax[1]) / 2, float(hmax[2])]
    for b in (2, 3):
        mn, mx, mean = ext(b)
        out[BONES[b]] = [round(float(mean[0]), 1), float(mx[1]), round(float(mean[2]), 1)]
    for b in (4, 5):
        mn, mx, mean = ext(b)
        out[BONES[b]] = [round(float(mean[0]), 1), float(mx[1]) - 1, float(mn[2]) + 1]
    return out


def grade(palette):
    """The source's stone is light grey with dark speckle, which averages out too dark: lift the greys (not the
    dark plates or the orange) and take the brown cast out of them."""
    out = []
    for r, g, b in palette:
        mx, mn = max(r, g, b), min(r, g, b)
        if mx - mn < 30 and mx > 60:
            v = (r + g + b) / 3
            v2 = 255 * (v / 255) ** 0.72
            out.append(tuple(int(min(255, v2 + (c - v) * 0.4)) for c in (r, g, b)))
        elif mx - mn > 60:
            out.append(tuple(int(min(255, c * 1.08)) for c in (r, g, b)))     # a touch more vivid orange
        else:
            out.append((r, g, b))
    return out


def shiny_palette(palette):
    """Shiny: the orange-red accents turn electric cyan (a Future paradox glow), the stone gets a cool tint, the dark
    plates go navy."""
    out = []
    for r, g, b in palette:
        mx, mn = max(r, g, b), min(r, g, b)
        if mx - mn > 60 and r >= g >= b:                      # orange / red accent
            out.append((int(b * 0.6), int(min(255, g * 0.9 + 60)), min(255, int(r * 1.05))))
        elif mx < 70:                                         # dark plates
            out.append((int(r * 0.7), int(g * 0.8), min(255, int(b * 1.4 + 18))))
        else:                                                 # stone
            out.append((int(r * 0.93), int(g * 0.97), min(255, int(b * 1.06 + 6))))
    return out


def build_model():
    d = np.load(VOXELS)
    solid, surf, colours, lo = d["solid"], d["surf"], d["colours"], d["lo"]
    palette, labels = vx.quantize(colours, surf, PALETTE_SIZE, seed=1022)
    labels = vx.denoise(labels, surf, passes=2)
    labels = vx.fill_interior_labels(labels, surf, solid)
    bone_of = segment(solid, lo)
    piv = pivots(bone_of, lo)

    boxes = []          # (bone, box)
    for b in range(len(BONES)):
        boxes += [(b, box) for box in vx.greedy_boxes(bone_of == b)]
    nets = [(2 * ((i1 - i0) + (k1 - k0)), (k1 - k0) + (j1 - j0)) for _, (i0, j0, k0, i1, j1, k1) in boxes]
    tw = 64
    while True:
        pos, used = vx.pack(nets, tw)
        if used <= tw:
            break
        tw *= 2
    th = tw

    graded = grade(palette)
    colour_lists = {"normal": graded, "shiny": shiny_palette(graded)}
    for variant, cols in colour_lists.items():
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        def colour_of(i, j, k, cols=cols):
            return tuple(cols[labels[i, j, k]]) + (255,)
        for (b, box), uv in zip(boxes, pos):
            vx.paint_box(img, uv, box, colour_of)
        sfx = "" if variant == "normal" else "_shiny"
        dest = RES / "assets" / MOD / "textures" / "pokemon" / FOLDER / f"{NAME}{sfx}.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, optimize=True)

    bones = [{"name": NAME, "pivot": [0, 0, 0]}]
    for b, name in enumerate(BONES):
        bone = {"name": name, "parent": "body" if name == "head" else NAME, "pivot": piv[name], "cubes": []}
        for (bb, (i0, j0, k0, i1, j1, k1)), uv in zip(boxes, pos):
            if bb == b:
                bone["cubes"].append({"origin": [int(lo[0] + i0), int(lo[1] + j0), int(lo[2] + k0)],
                                      "size": [i1 - i0, j1 - j0, k1 - k0], "uv": [int(uv[0]), int(uv[1])]})
        bones.append(bone)
    bones.append({"name": "locator_root", "parent": NAME, "pivot": [0, 0, 0]})
    hmin = np.argwhere(bone_of == 1).min(0) + lo
    bones.append({"name": "locator_top", "parent": NAME, "pivot": [0, float(solid.shape[1]), 0]})
    geo = {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": f"geometry.{NAME}", "texture_width": tw, "texture_height": th,
                        "visible_bounds_width": 4, "visible_bounds_height": 3.5, "visible_bounds_offset": [0, 1.5, 0]},
        "bones": bones}]}
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "models" / FOLDER / f"{NAME}.geo.json", geo)
    print(f"model: {len(boxes)} cubes, texture {tw}x{th}, palette {len(palette)}; pivots {piv}")
    return piv


# ---------------------------------------------------------------------------------------------
# Animations (keyframes sampled from simple periodic motions)
# ---------------------------------------------------------------------------------------------

def animations(piv):
    A = {}
    legs = ["leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"]

    A["ground_idle"] = {"loop": True, "animation_length": 4.0, "bones": {
        "body": {"position": track(4, lambda t: [0, -0.25 * (1 - math.cos(2 * math.pi * t)) / 2, 0])},
        "head": {"rotation": track(4, lambda t: [1.5 * sin(t, 1, 0.1), 2 * sin(t, 0.5), 0])},
    }}
    A["ground_walk"] = {"loop": True, "animation_length": 1.0, "bones": {
        "body": {"position": track(1, lambda t: [0, -0.35 * abs(sin(t)), 0]),
                 "rotation": track(1, lambda t: [0, 0, 1.2 * sin(t)])},
        "head": {"rotation": track(1, lambda t: [2.5 * sin(t, 2, 0.25), 0, 0])},
    }}
    A["battle_idle"] = {"loop": True, "animation_length": 2.0, "bones": {
        "body": {"position": track(2, lambda t: [0, -0.6 - 0.25 * sin(t), 0]),
                 "rotation": track(2, lambda t: [2, 0, 1.0 * sin(t, 1, 0.25)])},
        "head": {"rotation": track(2, lambda t: [12 + 2 * sin(t), 3 * sin(t, 0.5), 0])},   # blades lowered, ready to charge
        "leg_front_left": {"rotation": track(2, lambda t: [0, 0, -3])},
        "leg_front_right": {"rotation": track(2, lambda t: [0, 0, 3])},
    }}
    drop = -(piv["leg_front_left"][1] - 2)               # lie down: lower everything by the legs' height
    A["sleep"] = {"loop": True, "animation_length": 4.0, "bones": {
        "body": {"position": track(4, lambda t: [0, drop - 0.3 * (1 - math.cos(2 * math.pi * t)) / 2, 0])},
        "head": {"rotation": track(4, lambda t: [14 + 1.5 * sin(t), 0, 0])},
        "leg_front_left": {"position": track(4, lambda t: [0, drop, 0]), "rotation": track(4, lambda t: [-82, 0, 0])},
        "leg_front_right": {"position": track(4, lambda t: [0, drop, 0]), "rotation": track(4, lambda t: [-82, 0, 0])},
        # the back legs already slant backwards, so they tuck forward under the belly
        "leg_back_left": {"position": track(4, lambda t: [0, drop + 3, 0]), "rotation": track(4, lambda t: [-55, 0, 0])},
        "leg_back_right": {"position": track(4, lambda t: [0, drop + 3, 0]), "rotation": track(4, lambda t: [-55, 0, 0])},
    }}
    A["cry"] = {"animation_length": 1.5, "bones": {
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-28, 0, 0]), (0.5, [-26, -8, 0]), (0.7, [-26, 8, 0]),
                                   (0.9, [-26, -6, 0]), (1.1, [-20, 0, 0]), (1.5, [0, 0, 0])])},
        "body": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-6, 0, 0]), (1.1, [-5, 0, 0]), (1.5, [0, 0, 0])]),
                 "position": keys([(0, [0, 0, 0]), (0.3, [0, 1, 0]), (1.1, [0, 0.8, 0]), (1.5, [0, 0, 0])])},
        "leg_front_left": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-18, 0, 0]), (1.1, [-15, 0, 0]), (1.5, [0, 0, 0])])},
        "leg_front_right": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-18, 0, 0]), (1.1, [-15, 0, 0]), (1.5, [0, 0, 0])])},
    }}
    A["physical"] = {"animation_length": 0.75, "bones": {          # Mighty Cleave: rear back, then slash the blades down
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.25, [-25, 0, 0]), (0.4, [40, 0, 0]), (0.75, [0, 0, 0])])},
        "body": {"position": keys([(0, [0, 0, 0]), (0.25, [0, 0.5, 2]), (0.4, [0, -0.8, -4]), (0.75, [0, 0, 0])]),
                 "rotation": keys([(0, [0, 0, 0]), (0.25, [-5, 0, 0]), (0.4, [8, 0, 0]), (0.75, [0, 0, 0])])},
    }}
    A["special"] = {"animation_length": 1.0, "bones": {            # psychic power: head raised, body braced
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-20, 0, 0]), (0.7, [-20, 0, 0]), (1.0, [0, 0, 0])])},
        "body": {"position": keys([(0, [0, 0, 0]), (0.3, [0, -0.8, 0]), (0.7, [0, -0.8, 0]), (1.0, [0, 0, 0])])},
    }}
    A["status"] = {"animation_length": 1.0, "bones": {
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.25, [0, -15, 0]), (0.5, [0, 15, 0]), (0.75, [0, -8, 0]), (1.0, [0, 0, 0])])},
    }}
    A["faint"] = {"loop": "hold_on_last_frame", "animation_length": 2.0, "bones": {
        "body": {"position": keys([(0, [0, 0, 0]), (0.8, [0, drop * 0.6, 0]), (2.0, [0, drop, 0])]),
                 "rotation": keys([(0, [0, 0, 0]), (0.8, [6, 0, 0]), (2.0, [8, 0, 6])])},
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.8, [20, 0, 0]), (2.0, [30, 0, 0])])},
        **{leg: {"position": keys([(0, [0, 0, 0]), (2.0, [0, drop + (3 if "back" in leg else 0), 0])]),
                 "rotation": keys([(0, [0, 0, 0]), (2.0, [-82 if "front" in leg else -55, 0, 0])])} for leg in legs},
    }}
    return {"format_version": "1.8.0", "animations": {f"animation.{GROUP}.{k}": v for k, v in A.items()}}


def poser():
    b = lambda a: f"q.bedrock('{GROUP}', '{a}')"
    walk = "q.quadruped_walk(0.6, 0.9, 'leg_front_left', 'leg_front_right', 'leg_back_left', 'leg_back_right')"
    return {
        "portraitScale": 1.55, "portraitTranslation": [-0.55, 1.05, 0],
        "profileScale": 0.62, "profileTranslation": [0, 0.78, 0],
        "rootBone": NAME,
        "animations": {
            "cry": f"q.bedrock_stateful('{GROUP}', 'cry')",
            "physical": f"q.bedrock_primary('{GROUP}', 'physical', q.curve('symmetrical_wide'))",
            "special": f"q.bedrock_primary('{GROUP}', 'special', q.curve('symmetrical_wide'))",
            "status": f"q.bedrock_primary('{GROUP}', 'status', q.curve('symmetrical_wide'))",
            "faint": f"q.bedrock_primary('{GROUP}', 'faint', q.curve('one'))",
        },
        "poses": {
            "battle_standing": {"poseTypes": ["STAND"], "isBattle": True, "transformTicks": 10,
                                "animations": ["q.look('head')", b("battle_idle")]},
            "standing": {"poseTypes": ["STAND", "NONE", "FLOAT", "PORTRAIT", "PROFILE"], "isBattle": False,
                         "transformTicks": 10, "animations": ["q.look('head')", b("ground_idle")]},
            "walking": {"poseTypes": ["WALK", "SWIM"], "transformTicks": 10,
                        "animations": ["q.look('head')", b("ground_walk"), walk]},
            "sleeping": {"poseTypes": ["SLEEP"], "transformTicks": 20, "animations": [b("sleep")]},
        },
    }


# ---------------------------------------------------------------------------------------------
# Data: implemented, size, and the "roaming legendary" spawns
# ---------------------------------------------------------------------------------------------

def data_files():
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / FOLDER / f"1_{NAME}_base.json", {
        "species": f"cobblemon:{NAME}", "order": 1,
        "variations": [
            {"aspects": [], "poser": f"{MOD}:{NAME}", "model": f"{MOD}:{NAME}.geo",
             "texture": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}.png", "layers": []},
            {"aspects": ["shiny"], "texture": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}_shiny.png"},
        ]})
    # Cobblemon already has Iron Boulder's game data (types, ability, stats, moves); it only lacked a model
    write_json(RES / "data" / MOD / "species_additions" / f"{NAME}.json", {
        "target": f"cobblemon:{NAME}", "implemented": True, "baseScale": BASE_SCALE,
        "hitbox": {"width": 1.5, "height": 1.6, "fixed": False}})
    # Roaming legendary: it can turn up anywhere on the overworld surface, but only very rarely,
    # at Iron Boulder's postgame level (75); a thunderstorm (Quark Drive / Electric Terrain) makes it likelier.
    base = {"pokemon": NAME, "presets": ["natural", "wild"], "type": "pokemon", "spawnablePositionType": "grounded",
            "bucket": "ultra-rare", "level": "70-75"}
    surface = {"canSeeSky": True, "minSkyLight": 8, "maxSkyLight": 15, "biomes": ["#cobblemon:is_overworld"]}
    write_json(RES / "data" / MOD / "spawn_pool_world" / f"{FOLDER}.json", {
        "enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [],
        "spawns": [
            {"id": f"{NAME}-roaming", **base, "weight": 2.0, "condition": surface},
            {"id": f"{NAME}-storm", **base, "weight": 15.0, "condition": {**surface, "isThundering": True}},
        ]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obj", type=Path, help="source mesh to voxelize: .obj, .glb/.gltf, or a .zip of a textured OBJ "
                                             "(writes ironboulder_voxels.npz)")
    args = ap.parse_args()
    if args.obj:
        # a dense vertex-coloured OBJ (the original Tripo export) loads fast; anything else (GLB, a textured OBJ in
        # a zip, a low-poly export) is sampled evenly over its surface
        dense = args.obj.suffix.lower() == ".obj" and args.obj.stat().st_size > 50_000_000
        P, C, F = vx.load_obj(args.obj) if dense else vx.load_mesh(args.obj)
        solid, surf, colours, lo = vx.voxelize(P, C, F, HEIGHT, face_negative_z=True)
        np.savez_compressed(VOXELS, solid=solid, surf=surf, colours=colours.astype(np.float32), lo=lo)
        print(f"voxels: {solid.shape}, {int(solid.sum())} solid -> {VOXELS.relative_to(ROOT)}")
    piv = build_model()
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "animations" / FOLDER / f"{GROUP}.animation.json",
               animations(piv))
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "posers" / FOLDER / f"{NAME}.json", poser())
    data_files()
    write_json(HERE.parent / "readme" / f"_new_{NAME}.json", {     # for the player README (make_readme.py)
        "name": "Iron Boulder", "dex": 1022, "types": "Rock / Psychic", "ability": "Quark Drive",
        "how": ["A roaming legendary: it can appear anywhere on the overworld surface, very rarely, "
                "at level 70-75. Thunderstorms make it much likelier (Quark Drive / Electric Terrain).",
                "Moves, stats, typing and ability are the official Scarlet/Violet ones (Mighty Cleave at level 56).",
                "Commands: /pokespawn ironboulder or /pokegive ironboulder (add 'shiny' for the shiny)."],
        "look": "A stone-and-steel paradox with its great blade-horns; it lowers them to charge in battle, rears up "
                "to cry and slashes down with Mighty Cleave. Shiny: electric-cyan accents and navy plates.",
    })
    write_json(HERE.parent / "preview" / f"manifest_{NAME}.json", [{
        "species": NAME, "folder": FOLDER, "model": f"{MOD}:{NAME}.geo", "original": None,
        "retextured": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}.png", "layers": []}])


if __name__ == "__main__":
    main()
