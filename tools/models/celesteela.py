#!/usr/bin/env python3
"""
Celesteela (#797): a new Pokémon model for CobbleEffort, built from ellecat5112's model (made with Tripo AI).

Cobblemon 1.8.4 has Celesteela's species data (Steel/Flying, Beast Boost, Ultra Sun/Moon stats and learnset, a flier
that can't walk) but no model, so it's unimplemented. The source mesh is untextured, so this script paints it:
in the scheme of the user's reference picture: pale sea-green arm shafts with white straps and a glowing gold tip
panel, bright cyan frills over dark teal nozzle clusters with glowing cyan rims, a striped sage-and-mint cloak with a
white segmented spine, dark teal plates, and a white segmented head spire (emissive layer for the glows).

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
# colour roles (scheme from the user's reference picture: pale sea-green, white straps, cyan frills, dark teal nozzles)
(SHAFT, SHAFT_L, BAND, FRILL, FRILL_L, NOZZLE, RIM, TIP, CLOAK_A, CLOAK_B, CLOAK_C, SPINE, SPINE_D, PANEL, HEAD,
 HEAD_RING, EYE) = range(17)
PALETTES = {
    "normal": {SHAFT: (108, 180, 170), SHAFT_L: (138, 202, 192), BAND: (238, 244, 242), FRILL: (84, 212, 214),
               FRILL_L: (150, 236, 234), NOZZLE: (30, 58, 60), RIM: (96, 226, 232), TIP: (236, 196, 52),
               CLOAK_A: (190, 222, 210), CLOAK_B: (128, 182, 174), CLOAK_C: (218, 238, 228), SPINE: (240, 244, 242),
               SPINE_D: (176, 190, 188), PANEL: (46, 110, 112), HEAD: (238, 242, 240), HEAD_RING: (120, 170, 170),
               EYE: (120, 236, 240)},
    # shiny (CobbleEffort's take): pearl-white shafts with rose-gold frills and warm orange glow
    "shiny": {SHAFT: (214, 210, 222), SHAFT_L: (232, 228, 238), BAND: (250, 246, 236), FRILL: (226, 150, 132),
              FRILL_L: (244, 196, 178), NOZZLE: (60, 44, 58), RIM: (255, 168, 90), TIP: (255, 228, 140),
              CLOAK_A: (230, 220, 228), CLOAK_B: (204, 190, 206), CLOAK_C: (244, 236, 238), SPINE: (252, 250, 246),
              SPINE_D: (206, 196, 200), PANEL: (128, 76, 96), HEAD: (250, 248, 246), HEAD_RING: (200, 160, 170),
              EYE: (255, 190, 120)},
}
GLOW_ROLES = {RIM: "rim", TIP: "tip", EYE: "eye"}
GLOW = {"normal": {"rim": (96, 230, 236), "tip": (255, 214, 70), "eye": (140, 240, 244)},
        "shiny": {"rim": (255, 170, 90), "tip": (255, 232, 150), "eye": (255, 196, 130)}}


def parts(solid, lo):
    """Bone of each voxel: the source has three separate pieces (two arm-rockets and the centre); the centre's head
    cone starts at HEAD_FROM."""
    lab, n = ndimage.label(solid)
    if n < 3:
        raise SystemExit(f"expected 3 separate pieces (two arms and the body), found {n}")
    sizes = ndimage.sum(solid, lab, range(1, n + 1))
    big = [int(c) + 1 for c in np.argsort(sizes)[::-1][:3]]
    if n > 3:                                              # stray bits join the nearest of the three pieces
        _, (ii, jj, kk) = ndimage.distance_transform_edt(~np.isin(lab, big), return_indices=True)
        lab = np.where(solid, lab[ii, jj, kk], 0)
    meanx = {i: np.argwhere(lab == i)[:, 0].mean() + lo[0] for i in big}
    order = sorted(meanx, key=meanx.get)                   # right arm (-x), centre, left arm (+x)
    bone = np.full(solid.shape, -1, int)
    j = np.indices(solid.shape)[1]
    bone[lab == order[1]] = 0
    bone[(lab == order[1]) & (j >= HEAD_FROM)] = 1
    bone[lab == order[2]] = 2
    bone[lab == order[0]] = 3
    return bone


def paint_roles(solid, bone, lo):
    """Colour role of every voxel (glowing roles are listed in GLOW_ROLES)."""
    X, Y, Z = solid.shape
    role = np.full(solid.shape, CLOAK_A, int)
    i, j, k = np.indices(solid.shape)
    cx = -lo[0]                                            # grid x of the centre line
    front = np.full((X, Y), 10 ** 6)
    for a, b, c in zip(*np.nonzero(solid)):
        front[a, b] = min(front[a, b], c)
    on_front = np.zeros(solid.shape, bool)
    for a, b, c in zip(*np.nonzero(solid)):
        on_front[a, b, c] = c <= front[a, b] + 1
    top_open = solid & ~np.pad(solid, ((0, 0), (0, 1), (0, 0)))[:, 1:, :]
    body, head = bone == 0, bone == 1
    centre = np.argwhere(body).mean(0)

    # the cloak: vertical stripes around the body, lighter towards the hem
    ang = np.arctan2(k - centre[2], i - centre[0])
    stripe = (np.floor((ang + math.pi) / (2 * math.pi) * 21).astype(int)) % 3
    role[body] = np.choose(stripe, [CLOAK_A, CLOAK_B, CLOAK_C])[body]
    hem = body & (j <= 8) & (stripe == 1)
    role[hem] = CLOAK_A                                     # the lower cloak fades to the pale stripes
    spine = body & on_front & (np.abs(i - cx) <= 1) & (j >= 3)
    role[spine] = SPINE
    role[spine & (j % 3 == 0)] = SPINE_D
    upper_side = body & (j >= 18) & (np.abs(i - cx) >= 5)
    role[upper_side] = PANEL                                # dark teal plates by the head
    role[upper_side & top_open] = FRILL
    feet = body & (j <= 2)
    role[feet] = NOZZLE
    role[feet & ((j == 0) | (np.abs(i - cx) >= 7))] = RIM

    # the head spire: white with teal rings, a teal collar with cyan trim, small glowing eyes
    role[head] = HEAD
    role[head & (j % 3 == 0) & (j >= HEAD_FROM + 4)] = HEAD_RING
    collar = head & (j < HEAD_FROM + 3)
    role[collar] = PANEL
    role[collar & top_open] = FRILL
    eyes = head & on_front & ((j == 33) | (j == 34)) & (np.abs(np.abs(i - cx) - 2) == 0)
    role[eyes] = EYE

    # the arm-rockets, from the nozzles (t = 0) to the tip (t = 1)
    for b in (2, 3):
        arm = bone == b
        pts = np.argwhere(arm).astype(float)
        mean = pts.mean(0)
        _, _, vt = np.linalg.svd(pts - mean, full_matrices=False)
        axis = vt[0] if vt[0][1] > 0 else -vt[0]
        proj = (pts - mean) @ axis
        t = (proj - proj.min()) / (proj.max() - proj.min())
        radial = np.linalg.norm((pts - mean) - np.outer(proj, axis), axis=1)
        rmax_low = radial[t < 0.05].max() if (t < 0.05).any() else radial.max()
        tip_top = proj.max()
        for (a, bb, c), tv, r, pv in zip(pts.astype(int), t, radial, proj):
            if tv < 0.18:                                   # nozzle cluster
                rr = NOZZLE
                if tv < 0.04 and r > rmax_low - 1.6:
                    rr = RIM
                elif (a + bb + c) % 7 == 0 and tv < 0.12:
                    rr = RIM                                # the cyan seams between the nozzles
            elif tv < 0.30:                                 # the frill collar above the nozzles
                rr = FRILL_L if (a + 2 * bb + c) % 3 == 0 else FRILL
            elif any(lo_ <= tv < hi for lo_, hi in ((0.52, 0.555), (0.66, 0.695), (0.80, 0.835))):
                rr = BAND                                   # white straps
            else:
                rr = SHAFT_L if top_open[a, bb, c] else SHAFT
            if pv > tip_top - 1.2 and top_open[a, bb, c]:
                rr = TIP                                    # the glowing panel on the tip
            role[a, bb, c] = rr
    role[~solid] = -1
    return role


def build_model():
    d = np.load(VOXELS)
    solid, lo = d["solid"], d["lo"]
    solid = vx.smooth(solid)                       # Cobblemon-style: rounder shapes, no voxel specks
    bone = parts(solid, lo)
    role = paint_roles(solid, bone, lo)
    rng = np.random.default_rng(797)
    shade = 1 + rng.uniform(-0.015, 0.015, solid.shape)                   # only a hint of per-voxel variation

    boxes = vx.fit_bone_boxes(bone, len(BONES))
    nearest = vx.nearest_solid(solid)
    exposed = vx.exposure(solid)
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
            f = shade[i, j, k] if r not in GLOW_ROLES else 1
            return tuple(int(min(255, v * f)) for v in c) + (255,)
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        for (b, box), uv in zip(boxes, pos):
            vx.paint_box_shaded(img, uv, box, vx.at_nearest(nearest, body_colour), exposed)
        save(img, f"{NAME}{sfx}")
        for f in range(GLOW_FRAMES):                                        # nozzle flame flicker, eyes steady
            frng = random.Random(f"{NAME}:{variant}:{f}")
            flick = {}

            def glow_colour(i, j, k, variant=variant, f=f, frng=frng, flick=flick):
                g = GLOW_ROLES.get(role[i, j, k])
                if not g:
                    return (0, 0, 0, 0)
                if g != "rim":
                    return GLOW[variant][g] + (255,)
                key = (i, j, k)
                if key not in flick:                         # the nozzle rims flicker, the tip and eyes stay steady
                    flick[key] = 0.7 + 0.3 * frng.random()
                return tuple(int(v * flick[key]) for v in GLOW[variant]["rim"]) + (255,)
            gimg = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            for (b, box), uv in zip(boxes, pos):
                vx.paint_box(gimg, uv, box, vx.at_nearest(nearest, glow_colour))
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
        "look": "Pale sea-green arm-rockets with white straps, cyan frills and glowing nozzle rims and tips, a "
                "striped sage cloak and a white segmented spire. It hovers, leans into flight, aims its arms to fire "
                "Flash Cannon and drops onto foes with Heavy Slam. Shiny: pearl white with rose-gold frills and an "
                "orange glow.",
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
