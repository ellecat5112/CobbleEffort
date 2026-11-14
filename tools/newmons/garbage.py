"""The Garbage Bag (the user's design): a rare drop from Garbodor; using it on a CobbleEffortian Slugma evolves it into
Petroil. Like the fossils and the Master's Gi it is an echo shard told apart by custom_data
{cobbleeffort_item: "garbage_bag"} (+ name, lore, custom_model_data icon), so Cobblemon's drop entries (which take
item components) and item_interact evolutions (the legacy {item, nbt} predicate) can both use it. fossils.build adds
its icon override and creative tab entry; regional.py adds it to Garbodor's drops and makes it Slugma's evolution item.
"""
from __future__ import annotations

import json

from PIL import Image

MOD = "cobbleeffort"
BASE_ITEM = "minecraft:echo_shard"
CMD_BASE = 794800
ITEM = {"item": "garbage_bag", "name": "Garbage Bag", "cmd": 11, "key": "garbage_bag",
        "lore": "A bulging bag of rubbish that a Garbodor never let go of. It smells awful. A CobbleEffortian Slugma "
                "would love it."}
NBT = '{cobbleeffort_item:"garbage_bag"}'
DROP_PERCENT = 1.0                                       # per draw: Garbodor draws 4 times a defeat (~4% a defeat)


def components():
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.{ITEM['item']}", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.{ITEM['item']}.tooltip", "color": "gray",
                                       "italic": False})],
        "minecraft:custom_model_data": CMD_BASE + ITEM["cmd"],
        "minecraft:rarity": "rare",
        "minecraft:max_stack_size": 16,
        "minecraft:custom_data": {"cobbleeffort_item": ITEM["key"]},
    }


def stack():
    return {"id": BASE_ITEM, "count": 1, "components": components()}


def override():
    return {"predicate": {"custom_model_data": CMD_BASE + ITEM["cmd"]}, "model": f"{MOD}:item/{ITEM['item']}"}


def drop_entry():
    """The entry for a Pokémon's drop table (Cobblemon's ItemDropEntry takes `components`)."""
    return {"item": BASE_ITEM, "percentage": DROP_PERCENT, "components": components()}


def evolution_context():
    return {"item": BASE_ITEM, "nbt": NBT}


def icon():
    """A bulging dark green rubbish bag, tied at the top, with a fish bone and a can poking out."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    bag, shade, light, line = (62, 104, 66, 255), (42, 74, 48, 255), (96, 142, 90, 255), (24, 40, 28, 255)
    for y in range(16):
        for x in range(16):
            cx = 7.5
            if 5 <= y <= 15:
                w = 6.2 - abs(y - 11.0) * 0.45
                if abs(x - cx) <= w:
                    c = bag
                    if abs(x - cx) > w - 1.1 or y == 15:
                        c = line
                    elif x < cx - 2 and y < 11:
                        c = light
                    elif x > cx + 2:
                        c = shade
                    px[x, y] = c
    for x, y in ((6, 3), (7, 4), (8, 4), (9, 3), (5, 2), (10, 2), (7, 3), (8, 3)):
        px[x, y] = line if (x, y) in ((5, 2), (10, 2)) else bag          # the tied knot and its ears
    for x, y in ((11, 6), (12, 5), (13, 4)):
        px[x, y] = (230, 226, 210, 255)                                  # a fish bone
    for x, y in ((3, 7), (3, 8), (2, 7), (2, 8)):
        px[x, y] = (190, 196, 206, 255)                                  # a tin can
    return img


def build_assets(lang, res):
    """Icon, item model and lang (called from fossils.build)."""
    assets = res / "assets" / MOD
    lang[f"item.{MOD}.{ITEM['item']}"] = ITEM["name"]
    lang[f"item.{MOD}.{ITEM['item']}.tooltip"] = ITEM["lore"]
    tex = assets / "textures" / "item" / f"{ITEM['item']}.png"
    tex.parent.mkdir(parents=True, exist_ok=True)
    icon().save(tex)
    (assets / "models" / "item").mkdir(parents=True, exist_ok=True)
    (assets / "models" / "item" / f"{ITEM['item']}.json").write_text(json.dumps(
        {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{ITEM['item']}"}}, indent=1) + "\n")
