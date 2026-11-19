"""Tamer life for CobbleEffort: Digital (0.16.0): Digizoid armor and swords (textures drawn here, original pixel art),
coloured Digizoid ingots and the upgrade template, smithing recipes from Netherite, the Digi-Farm Terminal, the Chest
Harness, the Tamer NPC classes and dialogues, and lang. The Colosseum structure lives in make_world.py. Run by
make_assets.py, or alone.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "common" / "src" / "main" / "resources"
NS = "cobbleeffort_digital"
A = ROOT / "assets" / NS
D = ROOT / "data" / NS

METALS = {  # metal: (base, dark, light, accent)
    "red_digizoid": ((180, 34, 34), (110, 16, 20), (240, 110, 100), (255, 210, 120)),
    "blue_digizoid": ((40, 92, 220), (20, 44, 130), (130, 180, 255), (200, 240, 255)),
    "gold_digizoid": ((226, 176, 40), (150, 106, 20), (255, 230, 130), (255, 255, 220)),
    "black_digizoid": ((40, 40, 52), (18, 18, 24), (90, 90, 110), (170, 90, 255)),
}
PIECES = ["helmet", "chestplate", "leggings", "boots"]
NETHERITE = {"helmet": "netherite_helmet", "chestplate": "netherite_chestplate", "leggings": "netherite_leggings",
             "boots": "netherite_boots", "sword": "netherite_sword"}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def C(c, k=1.0, a=255):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c[:3]) + (a,)


def save(im, rel):
    p = A / "textures" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, optimize=True)


def outline(im, col=(20, 18, 24)):
    w, hh = im.size
    src = im.copy()
    px, sp = im.load(), src.load()
    for y in range(hh):
        for x in range(w):
            if sp[x, y][3]:
                continue
            if any(0 <= x + dx < w and 0 <= y + dy < hh and sp[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = C(col)
    return im


def armor_layer(metal, layer):
    """A 64x32 armor layer: plated metal with panel seams and edge highlights (the helmet's overlay area stays clear)."""
    base, dark, light, acc = METALS[metal]
    im = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    px = im.load()
    for y in range(32):
        for x in range(64):
            if layer == 1 and x >= 32 and y < 16:
                continue                                   # the hat overlay: nothing over the helmet
            c = base
            if x % 8 == 0 or y % 8 == 0:
                c = dark
            elif x % 8 == 1 or y % 8 == 1:
                c = light
            if (x + y * 2) % 13 == 0 and metal == "black_digizoid":
                c = acc
            if metal == "gold_digizoid" and (x * 3 + y) % 17 == 0:
                c = acc
            px[x, y] = C(c)
    return im


def icon(metal, piece):
    base, dark, light, acc = METALS[metal]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()

    def put(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            px[x, y] = C(c)
    if piece == "helmet":
        for y in range(3, 11):
            for x in range(3, 13):
                if (x - 7.5) ** 2 / 25 + (y - 9) ** 2 / 36 <= 1:
                    put(x, y, light if x < 7 and y < 6 else base)
        for x in range(4, 12):
            put(x, 8, dark)
    elif piece == "chestplate":
        for y in range(2, 14):
            for x in range(2, 14):
                arm = y < 7 and (x < 5 or x > 10)
                torso = 4 <= x <= 11
                if (arm or torso) and not (y < 4 and 6 <= x <= 9):
                    put(x, y, light if x in (4, 5) else dark if x == 11 else base)
    elif piece == "leggings":
        for y in range(2, 15):
            for x in range(3, 13):
                if y < 5 or (x <= 7 and x >= 3) or (x >= 9 and x <= 12):
                    if y >= 5 and x in (7, 8, 9) and not (x == 7 or x == 9):
                        continue
                    put(x, y, dark if y == 4 else light if x in (3, 9) else base)
    elif piece == "boots":
        for (x0, x1) in ((2, 7), (9, 14)):
            for y in range(7, 14):
                for x in range(x0, x1):
                    if y < 11 and x > x0 + 3:
                        continue
                    put(x, y, light if x == x0 else base if y < 12 else dark)
    elif piece == "sword":
        for i in range(11):
            put(4 + i, 11 - i, light)
            put(5 + i, 11 - i, base)
            put(4 + i, 10 - i, acc if i % 4 == 0 else base)
        for (x, y) in ((2, 11), (3, 12), (4, 13), (5, 12), (6, 11), (3, 10), (6, 13)):
            put(x, y, (110, 80, 50))
        put(2, 14, dark)
        put(1, 15, dark)
    elif piece == "ingot":
        for y in range(4, 12):
            if y < 7:
                x0, x1 = 4 + (7 - y), 11 + (7 - y)
                col = light if y == 4 else base
            else:
                x0, x1, col = 2, 12, base if y < 9 else dark
            for x in range(x0, x1 + 1):
                put(x, y, col)
        for x in (4, 5, 6):
            put(x, 8, (255, 255, 255))
    return outline(im)


def template_icon():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()
    for y in range(2, 14):
        for x in range(3, 13):
            edge = x in (3, 12) or y in (2, 13)
            px[x, y] = C((60, 64, 78) if edge else (120, 130, 150))
    for (x, y) in ((7, 5), (8, 5), (6, 6), (9, 6), (6, 7), (9, 7), (7, 8), (8, 8), (7, 10), (8, 10)):
        px[x, y] = C((90, 230, 255))
    return outline(im)


def terminal_textures():
    def side(x, y):
        if x in (0, 15) or y in (0, 15):
            return (70, 74, 84)
        return (130, 120, 70) if (x + y) % 6 else (110, 100, 60)       # hay-coloured farm panels

    def front(x, y):
        if 2 <= x <= 13 and 2 <= y <= 9:
            if x in (2, 13) or y in (2, 9):
                return (40, 44, 50)
            return (120, 240, 120) if (x * 2 + y) % 5 == 0 else (30, 90, 40)
        return side(x, y)

    def top(x, y):
        return (90, 240, 160) if x in (7, 8) and y in (7, 8) else (100, 104, 112)
    for name, fn in (("digi_farm_terminal_side", side), ("digi_farm_terminal_front", front), ("digi_farm_terminal_top", top)):
        im = Image.new("RGBA", (16, 16))
        for y in range(16):
            for x in range(16):
                im.putpixel((x, y), C(fn(x, y)))
        save(im, f"block/{name}.png")


def harness_icon():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()
    for y in range(5, 13):
        for x in range(3, 13):
            px[x, y] = C((150, 100, 50) if (x + y) % 4 else (120, 80, 40))
    for x in range(3, 13):
        px[x, 8] = C((90, 60, 30))
    px[7, 9] = C((220, 200, 120))
    px[8, 9] = C((220, 200, 120))
    for x in range(1, 15):
        if x < 3 or x > 12:
            px[x, 6] = C((80, 50, 30))
    return outline(im)


def shaped(name, pattern, key, result, count=1, cat="misc"):
    write_json(D / "recipe" / f"{name}.json", {"type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern,
                                               "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": result, "count": count}})


def shapeless(name, items, result, count=1):
    write_json(D / "recipe" / f"{name}.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
                                               "ingredients": [{"item": i} for i in items], "result": {"id": result, "count": count}})


def build():
    n = lambda s: f"{NS}:{s}"
    for metal in METALS:
        save(armor_layer(metal, 1), f"models/armor/{metal}_layer_1.png")
        save(armor_layer(metal, 2), f"models/armor/{metal}_layer_2.png")
        for piece in PIECES + ["sword"]:
            save(icon(metal, piece), f"item/{metal}_{piece}.png")
            parent = "minecraft:item/handheld" if piece == "sword" else "minecraft:item/generated"
            write_json(A / "models" / "item" / f"{metal}_{piece}.json", {"parent": parent, "textures": {"layer0": f"{NS}:item/{metal}_{piece}"}})
            write_json(D / "recipe" / f"{metal}_{piece}_smithing.json", {
                "type": "minecraft:smithing_transform", "template": {"item": n("digizoid_upgrade_smithing_template")},
                "base": {"item": f"minecraft:{NETHERITE[piece]}"}, "addition": {"item": n(f"{metal}_ingot")},
                "result": {"id": n(f"{metal}_{piece}"), "count": 1}})
        save(icon(metal, "ingot"), f"item/{metal}_ingot.png")
        write_json(A / "models" / "item" / f"{metal}_ingot.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{metal}_ingot"}})
    shapeless("red_digizoid_ingot", [n("chrome_digizoid_ingot"), "minecraft:redstone_block"], n("red_digizoid_ingot"))
    shapeless("blue_digizoid_ingot", [n("chrome_digizoid_ingot"), "minecraft:lapis_block"], n("blue_digizoid_ingot"))
    shapeless("gold_digizoid_ingot", [n("chrome_digizoid_ingot"), "minecraft:gold_block"], n("gold_digizoid_ingot"))
    shapeless("black_digizoid_ingot", [n("chrome_digizoid_ingot"), "minecraft:obsidian", "minecraft:ender_pearl"], n("black_digizoid_ingot"))
    save(template_icon(), "item/digizoid_upgrade_smithing_template.png")
    write_json(A / "models" / "item" / "digizoid_upgrade_smithing_template.json", {"parent": "minecraft:item/generated",
                                                                                   "textures": {"layer0": f"{NS}:item/digizoid_upgrade_smithing_template"}})
    shaped("digizoid_upgrade_smithing_template", ["DCD", "DND", "DDD"], {"D": "minecraft:diamond", "C": n("chrome_digizoid_ingot"),
                                                                          "N": "minecraft:netherite_upgrade_smithing_template"},
           n("digizoid_upgrade_smithing_template"))
    shaped("digizoid_upgrade_smithing_template_copy", ["DTD", "DBD", "DDD"], {"D": "minecraft:diamond", "T": n("digizoid_upgrade_smithing_template"),
                                                                               "B": n("chrome_digizoid_block")},
           n("digizoid_upgrade_smithing_template"), 2)
    terminal_textures()
    write_json(A / "blockstates" / "digi_farm_terminal.json", {"variants": {"": {"model": f"{NS}:block/digi_farm_terminal"}}})
    write_json(A / "models" / "block" / "digi_farm_terminal.json", {"parent": "minecraft:block/orientable", "textures": {
        "front": f"{NS}:block/digi_farm_terminal_front", "side": f"{NS}:block/digi_farm_terminal_side",
        "top": f"{NS}:block/digi_farm_terminal_top"}})
    write_json(A / "models" / "item" / "digi_farm_terminal.json", {"parent": f"{NS}:block/digi_farm_terminal"})
    write_json(D / "loot_table" / "blocks" / "digi_farm_terminal.json", {"type": "minecraft:block", "pools": [{
        "rolls": 1, "entries": [{"type": "minecraft:item", "name": n("digi_farm_terminal")}],
        "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    shaped("digi_farm_terminal", ["IGI", "HCH", "III"], {"I": "minecraft:iron_ingot", "G": "minecraft:glass_pane",
                                                          "H": "minecraft:hay_block", "C": n("digi_core")}, n("digi_farm_terminal"))
    save(harness_icon(), "item/chest_harness.png")
    write_json(A / "models" / "item" / "chest_harness.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/chest_harness"}})
    shaped("chest_harness", ["L L", "LCL", "LLL"], {"L": "minecraft:leather", "C": "minecraft:chest"}, n("chest_harness"))
    tags = ROOT / "data" / "minecraft" / "tags"
    for tag, vals in (("block/mineable/pickaxe", ["digi_farm_terminal"]),):
        p = tags / f"{tag}.json"
        obj = json.loads(p.read_text()) if p.exists() else {"replace": False, "values": []}
        obj["values"] = sorted(set(obj["values"]) | {n(v) for v in vals})
        write_json(p, obj)
    for kind, tagname in (("helmet", "head_armor"), ("chestplate", "chest_armor"), ("leggings", "leg_armor"), ("boots", "foot_armor"), ("sword", "swords")):
        p = tags / "item" / f"{tagname}.json"
        obj = json.loads(p.read_text()) if p.exists() else {"replace": False, "values": []}
        obj["values"] = sorted(set(obj["values"]) | {n(f"{m}_{kind}") for m in METALS})
        write_json(p, obj)
    # the Tamer NPCs: a singles class and a doubles class, each with its challenge dialogue
    for cls, fmt in (("tamer", "singles"), ("tamer_doubles", "doubles")):
        write_json(D / "npcs" / f"{cls}.json", {"names": ["Tamer"], "hitbox": "player", "canDespawn": False, "autoHealParty": True,
                                                "battleConfiguration": {"canChallenge": True},
                                                "interaction": {"type": "dialogue", "dialogue": n(cls)}, "skill": 3, "presets": []})
        write_json(D / "dialogues" / f"{cls}.json", {"pages": [{
            "id": "intro", "speaker": "npc",
            "lines": ["Our Digimon against yours!" if fmt == "singles" else "Two on two: you and your best pair against mine!"],
            "input": {"type": "option", "vertical": False, "options": [
                {"value": "battle", "text": "Battle!", "action": ["q.dialogue.close();", f"q.npc.start_battle(q.player, '{fmt}');"]},
                {"value": "later", "text": "Not now", "action": ["q.dialogue.close();"]}]}}],
            "speakers": {"npc": {"face": "q.npc.face(false);", "name": {"type": "expression", "expression": "q.npc.name"}}}})
    lang = {
        f"item.{NS}.digizoid_upgrade_smithing_template": "Digizoid Upgrade",
        f"item.{NS}.digizoid_upgrade_smithing_template.tooltip": "Smithing: a Netherite piece + a coloured Digizoid Ingot.",
        f"block.{NS}.digi_farm_terminal": "Digi-Farm Terminal",
        f"item.{NS}.chest_harness": "Chest Harness",
        f"item.{NS}.chest_harness.tooltip": "Use it on your own Adult or bigger Digimon: it carries a double chest (sneak and use an empty hand on it).",
        f"{NS}.harness.too_small": "%s is too small to carry a harness (Adult and up).",
        f"{NS}.harness.already": "%s already wears a harness.",
        f"{NS}.harness.on": "%s wears the harness: sneak and use an empty hand on it to open it.",
        f"{NS}.harness.title": "%s's packs",
        f"{NS}.forge.title": "%s's forge",
        f"{NS}.tamer.crack_team": "Crack Team Officer",
        f"{NS}.tamer.nature_spirits": "Nature Spirits Tamer",
        f"{NS}.tamer.deep_savers": "Deep Savers Tamer",
        f"{NS}.tamer.nightmare_soldiers": "Nightmare Soldiers Tamer",
        f"{NS}.tamer.dragons_roar": "Dragon's Roar Tamer",
        f"{NS}.tamer.virus_busters": "Virus Busters Tamer",
        f"{NS}.tamer.appears": "A wandering Tamer is looking for a battle!",
        f"{NS}.tamer.colosseum": "The Colosseum's three Tamers await: 1v1, 2v2 and 3v3.",
        f"{NS}.tamer.won": "+%s Tamer Rank points (%s).",
        f"{NS}.tamer.already_today": "You've beaten this Colosseum Tamer today already: no points until tomorrow.",
        f"{NS}.tamer.rank_up": "Tamer Rank up: %s!",
        f"{NS}.tamer.rank": "Tamer Rank: %s points (%s).",
        f"{NS}.rank.rookie": "Rookie", f"{NS}.rank.champion": "Champion", f"{NS}.rank.ultimate": "Ultimate", f"{NS}.rank.mega": "Mega",
        f"{NS}.gear.red_digizoid": "Red Digizoid: the heaviest armor, strong knockback resistance.",
        f"{NS}.gear.blue_digizoid": "Blue Digizoid: light; each piece +4% speed.",
        f"{NS}.gear.gold_digizoid": "Gold Digizoid: 2+ pieces reflect a third of projectiles and soften magic and blasts.",
        f"{NS}.gear.black_digizoid": "Black Digizoid: full set: sneak while sprinting to phase 6 blocks ahead.",
        f"{NS}.gear.red_digizoid_sword": "Red Digizoid: hits hardest.",
        f"{NS}.gear.blue_digizoid_sword": "Blue Digizoid: strikes fast.",
        f"{NS}.gear.gold_digizoid_sword": "Gold Digizoid: a gleaming all-rounder.",
        f"{NS}.gear.black_digizoid_sword": "Black Digizoid: right-click to blink where you look.",
    }
    names = {"red_digizoid": "Red Digizoid", "blue_digizoid": "Blue Digizoid", "gold_digizoid": "Gold Digizoid", "black_digizoid": "Black Digizoid"}
    for m, nm in names.items():
        lang[f"item.{NS}.{m}_ingot"] = f"{nm} Ingot"
        for piece in PIECES + ["sword"]:
            lang[f"item.{NS}.{m}_{piece}"] = f"{nm} {piece.title()}"
    return lang


if __name__ == "__main__":
    lang = build()
    f = A / "lang" / "en_us.json"
    d = json.loads(f.read_text()) if f.exists() else {}
    d.update(lang)
    write_json(f, dict(sorted(d.items())))
