"""
Armored Mewtwo: Cobblemon's own Mewtwo model with armour bolted onto its existing bones.

Because every armour piece hangs off Mewtwo's own bones (head_angle, torso3, arms, legs), Cobblemon's Mewtwo
poser and animations drive the armoured model unchanged. The armour is packed into extra rows appended below
Mewtwo's 128x128 texture, so the original UVs stay valid.

Design (after the reference / Pokémon GO): slate-grey armour with a visor helmet whose eye slits glow purple,
two big curling red horns, a chest plate with a red centre stripe and collar, waist armour with hanging hip
plates, shoulder pads, sleeves and bracers with glowing teal crystals, and thigh armour with crystal knee caps.
The purple tail and pale lower legs stay exposed.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from modelkit import Bone, Model, Paint, hexc

ARMOR = hexc("3e4b50")
ARMOR_HI = hexc("5b6d72")
ARMOR_DK = hexc("273034")
RED = hexc("c43b3d")
RED_DK = hexc("85262a")
TEAL = (124, 232, 212, 255)
EYE = (196, 96, 255, 255)


def plate(stripe=False, rivets=True):
    """Armour plate: bevelled light edge on top rows, rivets, optional red centre stripe on the front."""
    def pat(face, u, v, fw, fh):
        if stripe and face == "front" and abs(u - (fw - 1) / 2) < 1:
            return RED
        if face in ("front", "back", "left", "right") and v == 0:
            return ARMOR_HI
        if face in ("front", "back", "left", "right") and v == fh - 1:
            return ARMOR_DK
        if rivets and face == "front" and v == 1 and u in (1, fw - 2):
            return ARMOR_HI
        return None
    return Paint(ARMOR, noise=0.05, pattern=pat)


def crystal_plate():
    """Plate with a glowing teal crystal on the front."""
    def pat(face, u, v, fw, fh):
        if face == "front" and abs(u - (fw - 1) / 2) <= 0.5 and abs(v - (fh - 1) / 2) <= 1:
            return TEAL
        return plate().pattern(face, u, v, fw, fh)
    return Paint(ARMOR, noise=0.05, pattern=pat)


def visor():
    def pat(face, u, v, fw, fh):
        if face == "front":
            if v == 1 and (1 <= u <= 2 or fw - 3 <= u <= fw - 2):
                return EYE
            if v == fh - 1 and 2 <= u <= fw - 3:
                return RED
            return ARMOR_DK if v == 0 else None
        return None
    return Paint(ARMOR, noise=0.04, pattern=pat)


def horn():
    def pat(face, u, v, fw, fh):
        return RED_DK if face in ("bottom", "back") or u == 0 else None
    return Paint(RED, noise=0.05, pattern=pat)


def armor_pieces(m: Model):
    # helmet: cap, side guards, visor with glowing eye slits, crest
    m.cube("head_angle", (-4.5, 42.4, -4.45), (9, 3, 10), plate(rivets=False))
    for side in (-1, 1):
        m.cube("head_angle", (side * 4.75 - 0.5, 38.4, -4.2), (1, 5, 9), plate(rivets=False))
    m.cube("head_angle", (-4.5, 39.4, -4.95), (9, 3, 1), visor())
    m.cube("head_angle", (-1, 44.9, -4.6), (2, 2, 8), Paint(RED, noise=0.04))
    # armour caps over Mewtwo's ears (they're their own bones, so the caps follow the ears)
    m.cube("ear_right", (-3.85, 43.8, -0.65), (1, 4, 4), plate(rivets=False), inflate=0.35)
    m.cube("ear_left", (2.85, 43.8, -0.65), (1, 4, 4), plate(rivets=False), inflate=0.35)
    # curling red horns sweeping up, out and back
    for side in (-1, 1):
        name = "horn_armor_right" if side < 0 else "horn_armor_left"
        m.chain(name, "head_angle", (side * 4.5, 43.5, 0.5),
                [(4, 3, 3, (-15, 0, side * 55)), (5, 3, 3, (-30, 0, -side * 15)), (4, 2, 2, (-35, 0, -side * 20)),
                 (3, 2, 2, (-40, 0, -side * 20))], horn())

    # chest plate over torso3, collar, waist ring, abdomen plate and hip plates (tassets)
    m.cube("torso3", (-5, 29.6, -1.7), (10, 6, 8), plate(stripe=True), rotation=(-25, 0, 0), pivot=(0, 34.05, -1.1), inflate=0.3)
    m.cube("torso3", (-3.5, 34.2, -0.8), (7, 2, 6), plate(rivets=False), rotation=(-15, 0, 0), pivot=(0, 34.05, -1.1))
    m.cube("torso2", (-3, 24.35, -2.9), (6, 3, 6), crystal_plate(), inflate=0.2)
    m.cube("torso", (-4.5, 19.3, -4.5), (9, 5, 9), plate(stripe=True), rotation=(-7.5, 0, 0), pivot=(0, 19.8, 0.5))
    for x in (-3.75, 0.75):
        m.cube("torso", (x, 13.5, -4.9), (3, 6, 1), plate(rivets=False), rotation=(-7.5, 0, 0), pivot=(0, 19.8, 0.5))

    # right arm: shoulder pad (+ fin), sleeve, bracer with a crystal; then mirrored to the left
    m.cube("arm_right", (-7.5, 29.75, -1.4), (5, 4, 5), plate())
    m.cube("arm_right", (-7, 33.4, -0.9), (4, 2, 4), Paint(RED, noise=0.04), rotation=(0, 0, 20), pivot=(-5, 33.5, 1))
    m.cube("arm_right", (-12.5, 30.25, -0.4), (6, 3, 3), plate(rivets=False), inflate=0.15)
    m.cube("arm_right2", (-18.7, 30.25, -0.4), (6, 3, 3), crystal_plate(), inflate=0.2)
    # right leg: thigh armour with a crystal knee
    m.cube("leg_right", (-8.7, 15.25, -2.9), (6, 8, 7), plate(), inflate=0.45)
    m.cube("leg_right", (-7.2, 12.0, -3.6), (3, 3, 1), Paint(TEAL[:3], pattern=lambda *a: TEAL, emissive=True))
    m.mirror_x({"arm_right": "arm_left", "arm_right2": "arm_left2", "leg_right": "leg_left"})


def build_form(cob_root: Path, A: Path, NS: str):
    folder = "0150_mewtwo"
    src = cob_root / "assets" / "cobblemon"
    geo = json.loads((src / "bedrock" / "pokemon" / "models" / folder / "mewtwo.geo.json").read_text())
    g = geo["minecraft:geometry"][0]
    tw, th = g["description"]["texture_width"], g["description"]["texture_height"]

    m = Model("mewtwo_armor", tex_width=tw, seed=150)
    for b in g["bones"]:   # register Mewtwo's bones so armour can hang off them
        m.bones[b["name"]] = Bone(b["name"], b.get("parent"), tuple(b.get("pivot", (0, 0, 0))))
    existing = set(m.bones)
    armor_pieces(m)
    armor_h = m._pack()
    armor_img, armor_glow = m._paint(armor_h)

    new_h = th
    while new_h < th + armor_h:
        new_h *= 2
    bones_by_name = {b["name"]: b for b in g["bones"]}
    for c in m.cubes:
        cd = {"origin": [round(v, 3) for v in c.origin], "size": list(c.size), "uv": [c.uv[0], c.uv[1] + th]}
        if c.inflate:
            cd["inflate"] = c.inflate
        if c.rotation:
            cd["pivot"] = [round(v, 3) for v in (c.pivot or c.origin)]
            cd["rotation"] = [round(v, 3) for v in c.rotation]
        if c.bone not in bones_by_name:
            b = m.bones[c.bone]
            entry = {"name": b.name, "parent": b.parent, "pivot": [round(v, 3) for v in b.pivot]}
            if b.rotation:
                entry["rotation"] = [round(v, 3) for v in b.rotation]
            g["bones"].append(entry)
            bones_by_name[b.name] = entry
        bones_by_name[c.bone].setdefault("cubes", []).append(cd)
    g["description"]["identifier"] = "geometry.mewtwo_armored"
    g["description"]["texture_height"] = new_h
    out_geo = A / "bedrock" / "pokemon" / "models" / folder / "mewtwo_armored.geo.json"
    out_geo.parent.mkdir(parents=True, exist_ok=True)
    out_geo.write_text(json.dumps(geo, indent=1) + "\n")

    tex_dir = A / "textures" / "pokemon" / folder
    tex_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "_shiny"):
        base = Image.open(src / "textures" / "pokemon" / folder / f"mewtwo{suffix}.png").convert("RGBA")
        out = Image.new("RGBA", (tw, new_h), (0, 0, 0, 0))
        out.paste(base, (0, 0))
        out.paste(armor_img, (0, th))
        out.save(tex_dir / f"mewtwo_armored{suffix}.png", optimize=True)
    glow = Image.new("RGBA", (tw, new_h), (0, 0, 0, 0))
    if armor_glow is not None:
        glow.paste(armor_glow, (0, th))
    glow.save(tex_dir / "mewtwo_armored_emissive.png", optimize=True)

    tex = lambda n: f"{NS}:textures/pokemon/{folder}/{n}.png"
    layer = [{"name": "cobbleeffort_armor_glow", "texture": tex("mewtwo_armored_emissive"), "emissive": True, "translucent": True}]
    resolver = {
        "species": "cobblemon:mewtwo",
        "order": 9000,
        "variations": [
            {"aspects": ["armored"], "poser": "cobblemon:mewtwo", "model": f"{NS}:mewtwo_armored.geo",
             "texture": tex("mewtwo_armored"), "layers": layer},
            {"aspects": ["armored", "shiny"], "texture": tex("mewtwo_armored_shiny"), "layers": layer},
        ],
    }
    out_res = A / "bedrock" / "pokemon" / "resolvers" / "creatures" / folder / "9000_mewtwo_armored.json"
    out_res.parent.mkdir(parents=True, exist_ok=True)
    out_res.write_text(json.dumps(resolver, indent=2) + "\n")
    return [{"species": "mewtwo_armored", "folder": folder, "model": f"{NS}:mewtwo_armored.geo",
             "original": "cobblemon:textures/pokemon/0150_mewtwo/mewtwo.png", "original_model": "cobblemon:mewtwo.geo",
             "retextured": tex("mewtwo_armored"), "layers": [{"original": None, "retextured": tex("mewtwo_armored_emissive"), "emissive": True}]}]
