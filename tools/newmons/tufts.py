"""Elemental Tufts for Aetherim: a tuft of hair for each type that, put in Aetherim's cosmetic slot, gives it that type
(the form "<Type>", aspect "<type>-tuft").

Data only: Cobblemon's cosmetic items match the item alone, so each type's tuft is a different vanilla item: a wool in
the type's colour (Flying: a feather; Ghost: white wool). The named Tufts are those items with a name, lore and their
own icon (custom_model_data on the item's model), crafted from the wool plus something of that type; the plain item
works just as well.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent.parent / "src" / "main" / "resources"
MOD = "cobbleeffort"
CMD_BASE = 794900

# type: (base item, crafting ingredient, colour)
TUFTS = {
    "fire": ("minecraft:red_wool", "minecraft:blaze_powder", (240, 128, 48)),
    "water": ("minecraft:blue_wool", "minecraft:kelp", (104, 144, 240)),
    "grass": ("minecraft:lime_wool", "minecraft:wheat_seeds", (120, 200, 80)),
    "electric": ("minecraft:yellow_wool", "minecraft:glowstone_dust", (248, 208, 48)),
    "ice": ("minecraft:light_blue_wool", "minecraft:snowball", (152, 216, 216)),
    "fighting": ("minecraft:orange_wool", "minecraft:leather", (192, 48, 40)),
    "poison": ("minecraft:purple_wool", "minecraft:spider_eye", (160, 64, 160)),
    "ground": ("minecraft:brown_wool", "minecraft:dirt", (224, 192, 104)),
    "flying": ("minecraft:feather", "minecraft:feather", (168, 144, 240)),
    "psychic": ("minecraft:magenta_wool", "minecraft:amethyst_shard", (248, 88, 136)),
    "bug": ("minecraft:green_wool", "minecraft:string", (168, 184, 32)),
    "rock": ("minecraft:gray_wool", "minecraft:flint", (184, 160, 56)),
    "ghost": ("minecraft:white_wool", "minecraft:phantom_membrane", (112, 88, 152)),
    "dragon": ("minecraft:cyan_wool", "minecraft:chorus_fruit", (112, 56, 248)),
    "dark": ("minecraft:black_wool", "minecraft:ink_sac", (112, 88, 72)),
    "steel": ("minecraft:light_gray_wool", "minecraft:iron_ingot", (184, 184, 208)),
    "fairy": ("minecraft:pink_wool", "minecraft:pink_petals", (238, 153, 172)),
}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1) + "\n")


def components(t, i):
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.{t}_tuft", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.tuft.tooltip", "color": "gray", "italic": False})],
        "minecraft:custom_model_data": CMD_BASE + i,
        "minecraft:max_stack_size": 16,
    }


def icon(colour):
    """A wispy tuft of hair in the type's colour: strands sweeping up from a tied base, lighter tips."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    light = tuple(min(255, int(c + (255 - c) * 0.45)) for c in colour)
    dark = tuple(int(c * 0.6) for c in colour)
    for strand in range(5):
        a = math.radians(-40 + strand * 20)
        for i in range(11):
            t = i / 10
            x = 8 + math.sin(a) * i * 0.75 + math.sin(t * 3 + strand) * 0.8
            y = 13 - i * 1.05
            c = dark if t < 0.25 else (light if t > 0.7 else colour)
            for dx in (0, 1) if t < 0.6 else (0,):
                xi, yi = int(round(x)) + dx, int(round(y))
                if 0 <= xi < 16 and 0 <= yi < 16:
                    px[xi, yi] = c + (255,)
    for x in range(6, 11):                                                          # the tie at the base
        px[x, 13] = (236, 214, 150, 255)
        px[x, 14] = (190, 160, 100, 255)
    return img


def build(lang):
    data, assets = RES / "data" / MOD, RES / "assets"
    lang[f"item.{MOD}.tuft.tooltip"] = "Give it to Aetherim (its cosmetic slot) and it takes this type."
    by_base = {}
    for i, (t, (base, extra, colour)) in enumerate(TUFTS.items(), 1):
        name = f"{t.title()} Tuft"
        lang[f"item.{MOD}.{t}_tuft"] = name
        tex = assets / MOD / "textures" / "item" / f"{t}_tuft.png"
        tex.parent.mkdir(parents=True, exist_ok=True)
        icon(colour).save(tex)
        write_json(assets / MOD / "models" / "item" / f"{t}_tuft.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{t}_tuft"}})
        by_base.setdefault(base, []).append((CMD_BASE + i, f"{MOD}:item/{t}_tuft"))
        ingredients = [{"item": base}, {"item": extra}] if base != extra else [{"item": base}, {"item": base}]
        write_json(data / "recipe" / f"{t}_tuft.json", {
            "type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": ingredients,
            "result": {"id": base, "count": 1, "components": components(t, i)}})
    for base, overrides in by_base.items():
        path = base.split(":")[1]
        parent = {"parent": "minecraft:item/generated", "textures": {"layer0": f"minecraft:item/{path}"}} \
            if path == "feather" else {"parent": f"minecraft:block/{path}"}
        write_json(assets / "minecraft" / "models" / "item" / f"{path}.json", {
            **parent, "overrides": [{"predicate": {"custom_model_data": cmd}, "model": model} for cmd, model in overrides]})
    write_json(data / "cosmetic_items" / "aetherim.json", {
        "pokemon": [f"{MOD}:aetherim"],
        "cosmeticItems": [{"consumedItem": base, "aspects": [f"{t}-tuft"]} for t, (base, _, _) in TUFTS.items()]})
    creative = HERE / "creative_items.json"
    items = json.loads(creative.read_text()) if creative.exists() else []
    items = [s for s in items if "_tuft" not in json.dumps(s)]
    items += [{"id": base, "count": 1, "components": components(t, i)} for i, (t, (base, _, _)) in enumerate(TUFTS.items(), 1)]
    write_json(creative, items)


def forms():
    """Aetherim's type forms (species "forms")."""
    return [{"name": t.title(), "primaryType": t, "aspects": [f"{t}-tuft"], "battleOnly": False} for t in TUFTS]
