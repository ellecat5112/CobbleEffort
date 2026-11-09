#!/usr/bin/env python3
"""
Celesteela (#797): a new Pokémon model for CobbleEffort, built from ellecat5112's model (made with Tripo AI).

Cobblemon 1.8.4 has Celesteela's species data (Steel/Flying, Beast Boost, Ultra Sun/Moon stats and learnset, a flier
that can't walk) but no model, so it's unimplemented. The source mesh is untextured, so this script paints it:
green bamboo segments with darker nodes, white plates and thruster housings, a white head cone with a dark visor,
glowing eyes and a red mouth marking, and thruster nozzles with an animated glow (emissive layer).

  assets/cobbleeffort/bedrock/pokemon/models/0797_celesteela/celesteela.geo.json
  assets/cobbleeffort/textures/pokemon/0797_celesteela/celesteela[_shiny].png + celesteela_glow_<n>.png
  assets/cobbleeffort/bedrock/pokemon/animations/0797_celesteela/cobbleeffort_celesteela.animation.json
  assets/cobbleeffort/bedrock/pokemon/posers/0797_celesteela/celesteela.json
  assets/cobbleeffort/bedrock/pokemon/resolvers/0797_celesteela/1_celesteela_base.json
  data/cobbleeffort/species_additions/celesteela.json, data/cobbleeffort/spawn_pool_world/0797_celesteela.json

Usage:
  python3 tools/models/celesteela.py --obj <model.glb>   # (re)voxelize the source mesh -> celesteela_voxels.npz
  python3 tools/models/celesteela.py                     # build everything from the committed voxels
"""
from __future__ import annotations

import argparse
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
NAME = "celesteela"
FOLDER = "0797_celesteela"
GROUP = f"{MOD}_{NAME}"
VOXELS = HERE / f"{NAME}_voxels.npz"
HEIGHT = 48                    # model units before baseScale (16 = one block)
BASE_SCALE = 1.15              # about 3.5 blocks tall: Cobblemon shrinks giants (Steelix, also 9.2 m, is 3.2 blocks)
HEAD_FROM = 27                 # the head cone starts at this height
GLOW_FRAMES = 3

BONES = ["body", "head", "arm_left", "arm_right"]
# colour roles
GREEN, GREEN_D, GREEN_L, WHITE, WHITE_S, DARK, RED, NOZZLE, VISOR, EYE = range(10)
PALETTES = {
    "normal": {GREEN: (78, 152, 84), GREEN_D: (46, 104, 58), GREEN_L: (128, 192, 112), WHITE: (234, 238, 230),
               WHITE_S: (188, 197, 190), DARK: (46, 50, 58), RED: (204, 56, 52), NOZZLE: (92, 44, 24),
               VISOR: (34, 38, 46), EYE: (250, 228, 150)},
    # shiny (CobbleEffort's take): brass and gold bamboo on pale silver
    "shiny": {GREEN: (196, 158, 64), GREEN_D: (148, 108, 40), GREEN_L: (232, 202, 110), WHITE: (232, 232, 240),
              WHITE_S: (186, 186, 202), DARK: (54, 50, 64), RED: (90, 140, 220), NOZZLE: (40, 70, 110),
              VISOR: (36, 34, 52), EYE: (170, 230, 255)},
}
GLOW = {"normal": {"nozzle": (255, 150, 40), "eye": (255, 236, 160)},
        "shiny": {"nozzle": (110, 200, 255), "eye": (190, 240, 255)}}


def parts(solid, lo):
    """Bone of each voxel: the source has three separate pieces (two arm-rockets and the centre); the centre's head
    cone starts at HEAD_FROM."""
    lab, n = ndimage.label(solid)
    if n != 3:
        raise SystemExit(f"expected 3 separate pieces (two arms and the body), found {n}")
    meanx = {i: np.argwhere(lab == i)[:, 0].mean() + lo[0] for i in (1, 2, 3)}
    order = sorted(meanx, key=meanx.get)                   # right arm (-x), centre, left arm (+x)
    bone = np.full(solid.shape, -1, int)
    j = np.indices(solid.shape)[1]
    bone[lab == order[1]] = 0
    bone[(lab == order[1]) & (j >= HEAD_FROM)] = 1
    bone[lab == order[2]] = 2
    bone[lab == order[0]] = 3
    return bone


def paint_roles(solid, bone, lo):
    """Colour role and glow kind (0 none, 1 nozzle, 2 eye) of every voxel."""
    X, Y, Z = solid.shape
    role = np.full(solid.shape, GREEN, int)
    glow = np.zeros(solid.shape, int)
    i, j, k = np.indices(solid.shape)
    cx = -lo[0]                                            # grid x of the model's centre line
    # front surface: the lowest k (the model faces -z) of each (i, j) column
    front = np.full((X, Y), 10 ** 6)
    for a, b, c in zip(*np.nonzero(solid)):
        front[a, b] = min(front[a, b], c)
    above_open = solid & ~np.pad(solid, ((0, 0), (0, 1), (0, 0)))[:, 1:, :]

    body = bone == 0
    role[body] = GREEN
    role[body & (j % 6 == 5)] = GREEN_D                                    # bamboo nodes
    role[body & above_open & (role == GREEN)] = GREEN_L
    on_front = np.zeros(solid.shape, bool)
    for a, b, c in zip(*np.nonzero(solid)):
        on_front[a, b, c] = c <= front[a, b] + 1
    panel = body & on_front & (np.abs(i - cx) <= 4) & (j >= 3) & (j <= 18)
    role[panel] = WHITE
    role[panel & (np.abs(i - cx) == 4)] = WHITE_S
    role[body & (j <= 1)] = WHITE_S

    head = bone == 1
    role[head] = WHITE
    role[head & (j < HEAD_FROM + 2)] = GREEN_D                             # collar
    face = head & on_front
    role[face & ((j == 34) | (j == 35))] = VISOR
    eyes = face & ((j == 34) | (j == 35)) & (np.abs(np.abs(i - cx) - 2) <= 0)
    role[eyes] = EYE
    glow[eyes] = 2
    role[face & (j == 31) & (np.abs(i - cx) <= 1)] = RED                   # mouth marking
    role[head & (j >= 40)] = GREEN                                         # the spire
    role[head & (j >= 40) & (j % 3 == 0)] = GREEN_D
    role[head & (j >= 46)] = WHITE

    for b in (2, 3):
        arm = bone == b
        pts = np.argwhere(arm).astype(float)
        mean = pts.mean(0)
        _, _, vt = np.linalg.svd(pts - mean, full_matrices=False)
        axis = vt[0] if vt[0][1] > 0 else -vt[0]                           # from the thruster (low) to the tip (high)
        proj = (pts - mean) @ axis
        t = (proj - proj.min()) / (proj.max() - proj.min())
        length = proj.max() - proj.min()
        radial = np.linalg.norm((pts - mean) - np.outer(proj, axis), axis=1)
        for (a, bb, c), tv, r in zip(pts.astype(int), t, radial):
            node = int(tv * length) % 6 == 5
            if tv < 0.28:                                                  # thruster housing
                rr = WHITE_S if 0.22 <= tv < 0.28 or node else WHITE
                if tv < 0.05:
                    rr = DARK
                    if r < 2.2:
                        rr = NOZZLE
                        glow[a, bb, c] = 1
            elif tv > 0.93:
                rr = WHITE
            else:
                rr = GREEN_D if node else GREEN
            role[a, bb, c] = rr
        role[arm & above_open & (role == GREEN)] = GREEN_L
    role[~solid] = -1
    glow[~solid] = 0
    return role, glow


def build_model():
    d = np.load(VOXELS)
    solid, lo = d["solid"], d["lo"]
    bone = parts(solid, lo)
    role, glow = paint_roles(solid, bone, lo)
    rng = np.random.default_rng(797)
    shade = 1 + rng.uniform(-0.045, 0.045, solid.shape)                   # a little per-voxel variation

    boxes = []
    for b in range(len(BONES)):
        boxes += [(b, box) for box in vx.greedy_boxes(bone == b)]
    nets = [(2 * ((i1 - i0) + (k1 - k0)), (k1 - k0) + (j1 - j0)) for _, (i0, j0, k0, i1, j1, k1) in boxes]
    tw = 64
    while True:
        pos, used = vx.pack(nets, tw)
        if used <= tw:
            break
        tw *= 2
    th = tw
    tex_dir = RES / "assets" / MOD / "textures" / "pokemon" / FOLDER
    tex_dir.mkdir(parents=True, exist_ok=True)

    def save(img, name):
        img.save(tex_dir / f"{name}.png", optimize=True)

    for variant, pal in PALETTES.items():
        sfx = "" if variant == "normal" else "_shiny"

        def body_colour(i, j, k, pal=pal):
            r = role[i, j, k]
            c = pal[r] if r >= 0 else (0, 0, 0)
            f = shade[i, j, k] if r not in (EYE, VISOR) else 1
            return tuple(int(min(255, v * f)) for v in c) + (255,)
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        for (b, box), uv in zip(boxes, pos):
            vx.paint_box(img, uv, box, body_colour)
        save(img, f"{NAME}{sfx}")
        for f in range(GLOW_FRAMES):                                        # nozzle flame flicker, eyes steady
            frng = random.Random(f"{NAME}:{variant}:{f}")
            flick = {}

            def glow_colour(i, j, k, variant=variant, f=f, frng=frng, flick=flick):
                g = glow[i, j, k]
                if not g:
                    return (0, 0, 0, 0)
                if g == 2:
                    return GLOW[variant]["eye"] + (255,)
                key = (i, j, k)
                if key not in flick:
                    flick[key] = 0.72 + 0.28 * frng.random()
                c = GLOW[variant]["nozzle"]
                return tuple(int(v * flick[key]) for v in c) + (255,)
            gimg = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            for (b, box), uv in zip(boxes, pos):
                vx.paint_box(gimg, uv, box, glow_colour)
            save(gimg, f"{NAME}{sfx}_glow_{f}")

    def ext(b):
        idx = np.argwhere(bone == b)
        return idx.min(0) + lo, idx.max(0) + 1 + lo, idx.mean(0) + lo + 0.5
    hmin, hmax, hmean = ext(1)
    piv = {"body": [0, 14, 0], "head": [0, float(HEAD_FROM), round(float(hmean[2]), 1)]}
    for b in (2, 3):
        _, _, mean = ext(b)
        piv[BONES[b]] = [round(float(v), 1) for v in mean]

    bones = [{"name": NAME, "pivot": [0, 0, 0]}]
    for b, name in enumerate(BONES):
        bone_json = {"name": name, "parent": NAME if name == "body" else "body", "pivot": piv[name], "cubes": []}
        for (bb, (i0, j0, k0, i1, j1, k1)), uv in zip(boxes, pos):
            if bb == b:
                bone_json["cubes"].append({"origin": [int(lo[0] + i0), int(lo[1] + j0), int(lo[2] + k0)],
                                           "size": [i1 - i0, j1 - j0, k1 - k0], "uv": [int(uv[0]), int(uv[1])]})
        bones.append(bone_json)
    bones.append({"name": "locator_root", "parent": NAME, "pivot": [0, 0, 0]})
    bones.append({"name": "locator_top", "parent": NAME, "pivot": [0, float(solid.shape[1]), 0]})
    geo = {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": f"geometry.{NAME}", "texture_width": tw, "texture_height": th,
                        "visible_bounds_width": 6, "visible_bounds_height": 4.5, "visible_bounds_offset": [0, 2, 0]},
        "bones": bones}]}
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "models" / FOLDER / f"{NAME}.geo.json", geo)
    print(f"model: {len(boxes)} cubes, texture {tw}x{th}; pivots {piv}")
    return piv


# ---------------------------------------------------------------------------------------------
# Animations: a heavy flier that hovers on its arm-thrusters
# ---------------------------------------------------------------------------------------------

def animations():
    A = {}
    A["hover"] = {"loop": True, "animation_length": 4.0, "bones": {
        "body": {"position": track(4, lambda t: [0, 1.0 * sin(t), 0])},
        "head": {"rotation": track(4, lambda t: [1.5 * sin(t, 1, 0.25), 4 * sin(t, 0.5), 0])},
        "arm_left": {"rotation": track(4, lambda t: [2 * sin(t, 1, 0.1), 0, 2.5 * sin(t, 1, 0.3)])},
        "arm_right": {"rotation": track(4, lambda t: [2 * sin(t, 1, 0.1), 0, -2.5 * sin(t, 1, 0.3)])},
    }}
    A["fly"] = {"loop": True, "animation_length": 2.0, "bones": {
        "body": {"rotation": track(2, lambda t: [14 + 1.5 * sin(t), 0, 2 * sin(t, 1, 0.25)]),
                 "position": track(2, lambda t: [0, 0.6 * sin(t, 2), 0])},
        "head": {"rotation": track(2, lambda t: [-8, 0, 0])},
        "arm_left": {"rotation": track(2, lambda t: [-12 + 2 * sin(t, 2), 0, 6])},
        "arm_right": {"rotation": track(2, lambda t: [-12 + 2 * sin(t, 2), 0, -6])},
    }}
    A["battle_idle"] = {"loop": True, "animation_length": 2.5, "bones": {
        "body": {"position": track(2.5, lambda t: [0, 0.7 * sin(t), 0])},
        "head": {"rotation": track(2.5, lambda t: [4, 3 * sin(t, 1), 0])},
        "arm_left": {"rotation": track(2.5, lambda t: [-14 + 2 * sin(t), 0, 4])},     # thrusters aimed forward
        "arm_right": {"rotation": track(2.5, lambda t: [-14 + 2 * sin(t), 0, -4])},
    }}
    A["sleep"] = {"loop": True, "animation_length": 5.0, "bones": {
        "body": {"position": track(5, lambda t: [0, -3 + 0.3 * sin(t), 0]), "rotation": track(5, lambda t: [5, 0, 0])},
        "head": {"rotation": track(5, lambda t: [16 + 1.5 * sin(t), 0, 0])},
        "arm_left": {"rotation": track(5, lambda t: [6, 0, -10])},                   # arms drooping
        "arm_right": {"rotation": track(5, lambda t: [6, 0, 10])},
    }}
    A["cry"] = {"animation_length": 1.6, "bones": {
        "body": {"position": keys([(0, [0, 0, 0]), (0.4, [0, 2.5, 0]), (1.2, [0, 2, 0]), (1.6, [0, 0, 0])])},
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.4, [-20, 0, 0]), (0.6, [-18, -8, 0]), (0.8, [-18, 8, 0]),
                                   (1.0, [-18, -6, 0]), (1.2, [-14, 0, 0]), (1.6, [0, 0, 0])])},
        "arm_left": {"rotation": keys([(0, [0, 0, 0]), (0.4, [0, 0, 14]), (1.2, [0, 0, 12]), (1.6, [0, 0, 0])])},
        "arm_right": {"rotation": keys([(0, [0, 0, 0]), (0.4, [0, 0, -14]), (1.2, [0, 0, -12]), (1.6, [0, 0, 0])])},
    }}
    A["physical"] = {"animation_length": 0.9, "bones": {               # Heavy Slam: rise, then drop on the target
        "body": {"position": keys([(0, [0, 0, 0]), (0.35, [0, 4, 1]), (0.55, [0, -3, -3]), (0.9, [0, 0, 0])]),
                 "rotation": keys([(0, [0, 0, 0]), (0.35, [-6, 0, 0]), (0.55, [12, 0, 0]), (0.9, [0, 0, 0])])},
        "arm_left": {"rotation": keys([(0, [0, 0, 0]), (0.35, [0, 0, 16]), (0.55, [0, 0, -6]), (0.9, [0, 0, 0])])},
        "arm_right": {"rotation": keys([(0, [0, 0, 0]), (0.35, [0, 0, -16]), (0.55, [0, 0, 6]), (0.9, [0, 0, 0])])},
    }}
    A["special"] = {"animation_length": 1.0, "bones": {                # Flash Cannon: aim the arm-cannons, fire, recoil
        "arm_left": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-28, 0, 4]), (0.45, [-22, 0, 4]), (1.0, [0, 0, 0])])},
        "arm_right": {"rotation": keys([(0, [0, 0, 0]), (0.3, [-28, 0, -4]), (0.45, [-22, 0, -4]), (1.0, [0, 0, 0])])},
        "body": {"position": keys([(0, [0, 0, 0]), (0.3, [0, 0, 0]), (0.45, [0, 0, 1.5]), (1.0, [0, 0, 0])])},
    }}
    A["status"] = {"animation_length": 1.2, "bones": {
        "head": {"rotation": keys([(0, [0, 0, 0]), (0.3, [0, -14, 0]), (0.6, [0, 14, 0]), (0.9, [0, -6, 0]), (1.2, [0, 0, 0])])},
        "body": {"position": keys([(0, [0, 0, 0]), (0.6, [0, 1.2, 0]), (1.2, [0, 0, 0])])},
    }}
    A["faint"] = {"loop": "hold_on_last_frame", "animation_length": 2.0, "bones": {
        "body": {"position": keys([(0, [0, 0, 0]), (0.6, [0, 1, 0]), (2.0, [0, -9, 0])]),
                 "rotation": keys([(0, [0, 0, 0]), (0.6, [-4, 0, 0]), (2.0, [10, 0, 18])])},
        "head": {"rotation": keys([(0, [0, 0, 0]), (2.0, [24, 0, 0])])},
        "arm_left": {"rotation": keys([(0, [0, 0, 0]), (2.0, [10, 0, -18])])},
        "arm_right": {"rotation": keys([(0, [0, 0, 0]), (2.0, [10, 0, 18])])},
    }}
    return {"format_version": "1.8.0", "animations": {f"animation.{GROUP}.{k}": v for k, v in A.items()}}


def poser():
    b = lambda a: f"q.bedrock('{GROUP}', '{a}')"
    return {
        "portraitScale": 0.95, "portraitTranslation": [0, 1.95, 0],
        "profileScale": 0.4, "profileTranslation": [0, 1.15, 0],
        "rootBone": NAME,
        "animations": {
            "cry": f"q.bedrock_stateful('{GROUP}', 'cry')",
            "physical": f"q.bedrock_primary('{GROUP}', 'physical', q.curve('symmetrical_wide'))",
            "special": f"q.bedrock_primary('{GROUP}', 'special', q.curve('symmetrical_wide'))",
            "status": f"q.bedrock_primary('{GROUP}', 'status', q.curve('symmetrical_wide'))",
            "faint": f"q.bedrock_primary('{GROUP}', 'faint', q.curve('one'))",
        },
        "poses": {
            "battle_hover": {"poseTypes": ["STAND", "HOVER", "FLOAT"], "isBattle": True, "transformTicks": 10,
                             "animations": ["q.look('head')", b("battle_idle")]},
            "hover": {"poseTypes": ["STAND", "NONE", "HOVER", "FLOAT", "PORTRAIT", "PROFILE"], "isBattle": False,
                      "transformTicks": 10, "animations": ["q.look('head')", b("hover")]},
            "fly": {"poseTypes": ["FLY", "WALK", "SWIM"], "transformTicks": 10, "animations": [b("fly")]},
            "sleep": {"poseTypes": ["SLEEP"], "transformTicks": 20, "animations": [b("sleep")]},
        },
    }


def data_files():
    tex = lambda n: f"{MOD}:textures/pokemon/{FOLDER}/{n}.png"
    glow = lambda sfx: {"name": "glow", "emissive": True, "translucent": True,
                        "texture": {"frames": [tex(f"{NAME}{sfx}_glow_{f}") for f in range(GLOW_FRAMES)], "fps": 6, "loop": True}}
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / FOLDER / f"1_{NAME}_base.json", {
        "species": f"cobblemon:{NAME}", "order": 1,
        "variations": [
            {"aspects": [], "poser": f"{MOD}:{NAME}", "model": f"{MOD}:{NAME}.geo", "texture": tex(NAME), "layers": [glow("")]},
            {"aspects": ["shiny"], "texture": tex(f"{NAME}_shiny"), "layers": [glow("_shiny")]},
        ]})
    # Cobblemon already has Celesteela's game data (types, ability, stats, moves, flying behaviour)
    write_json(RES / "data" / MOD / "species_additions" / f"{NAME}.json", {
        "target": f"cobblemon:{NAME}", "implemented": True, "baseScale": BASE_SCALE,
        "hitbox": {"width": 2.5, "height": 3.4, "fixed": False}})
    # Roaming Ultra Beast: very rarely, anywhere in the overworld, at night under the open sky; much likelier under a
    # full moon (it was Pokémon Moon's Ultra Beast). Level 55-60, as in Sun/Moon and Ultra Sun/Ultra Moon.
    base = {"pokemon": NAME, "presets": ["natural", "wild"], "type": "pokemon", "spawnablePositionType": "grounded",
            "bucket": "ultra-rare", "level": "55-60"}
    night = {"canSeeSky": True, "timeRange": "night", "biomes": ["#cobblemon:is_overworld"]}
    write_json(RES / "data" / MOD / "spawn_pool_world" / f"{FOLDER}.json", {
        "enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [],
        "spawns": [
            {"id": f"{NAME}-roaming", **base, "weight": 2.0, "condition": night},
            {"id": f"{NAME}-full-moon", **base, "weight": 15.0, "condition": {**night, "moonPhase": "0"}},
        ]})
    write_json(HERE.parent / "readme" / f"_new_{NAME}.json", {
        "name": "Celesteela", "dex": 797, "types": "Steel / Flying", "ability": "Beast Boost",
        "how": ["A roaming Ultra Beast: it can appear anywhere in the overworld at night under the open sky, very "
                "rarely, at level 55-60. A full moon makes it much likelier.",
                "Moves, stats, typing and ability are the official Ultra Sun/Ultra Moon ones (Heavy Slam at 60). It "
                "flies and can't walk.",
                "Commands: /pokespawn celesteela or /pokegive celesteela (add 'shiny' for the shiny)."],
        "look": "Green bamboo segments, white plates and a white head cone with glowing eyes; its arm-thrusters glow "
                "and flicker in the dark. It hovers, leans into flight, aims its arms to fire Flash Cannon and drops "
                "onto foes with Heavy Slam. Shiny: brass-gold bamboo on silver, with blue flames.",
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obj", type=Path, help="source mesh (.glb/.gltf/.obj or a zip of a textured OBJ)")
    args = ap.parse_args()
    if args.obj:
        P, C, F = vx.load_mesh(args.obj, samples=4_000_000)
        solid, surf, colours, lo = vx.voxelize(P, C, F, HEIGHT, face_negative_z=True)
        np.savez_compressed(VOXELS, solid=solid, lo=lo)
        print(f"voxels: {solid.shape}, {int(solid.sum())} solid -> {VOXELS.relative_to(ROOT)}")
    build_model()
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "animations" / FOLDER / f"{GROUP}.animation.json",
               animations())
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "posers" / FOLDER / f"{NAME}.json", poser())
    data_files()
    write_json(HERE.parent / "preview" / f"manifest_{NAME}.json", [
        {"species": NAME, "folder": FOLDER, "model": f"{MOD}:{NAME}.geo", "original": None,
         "retextured": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}.png",
         "layers": [{"original": None, "retextured": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}_glow_0.png", "emissive": True}]},
        {"species": f"{NAME}_shiny", "folder": FOLDER, "model": f"{MOD}:{NAME}.geo", "original": None,
         "retextured": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}_shiny.png",
         "layers": [{"original": None, "retextured": f"{MOD}:textures/pokemon/{FOLDER}/{NAME}_shiny_glow_0.png", "emissive": True}]},
    ])


if __name__ == "__main__":
    main()
