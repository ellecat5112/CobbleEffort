#!/usr/bin/env python3
"""
Mega Evolutions for every Paradox Pokémon (the 22 the Pokémon Fandom wiki lists: 11 Ancient incl. Koraidon,
11 Future incl. Miraidon), through Mega Showdown, with craftable mega stones.

Each mega's model is hand-built from boxes in Cobblemon's style (tools/megas/models/<species>.py on
tools/megas/_boxmodel.py) and painted by its shaders. Only megas with a model module are built, so they can be
added a few at a time. Everything else is data, read by Mega Showdown and Cobblemon:

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

Stats: base + 100, keeping the Paradox rule that Ancient stats are odd and Future stats even. Types stay.

Usage: python3 tools/megas/build.py --cobblemon <cobblemon>/common/src/main/resources
"""
from __future__ import annotations

import importlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(TOOLS / "models"))
from _anim import write_json  # noqa: E402
from _rig import animations, poser  # noqa: E402

ROOT = TOOLS.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"
BASE_ITEM = "minecraft:amethyst_shard"
CMD_BASE = 794700

A, F = "ancient", "future"


def mega(display, dex, era, types, ability, ability_name, stats, stone_name, recipe, colours, dex_text):
    return {"display": display, "dex": dex, "era": era, "types": types, "ability": ability, "ability_name": ability_name,
            "stats": stats, "stone_name": stone_name, "recipe": recipe, "stone_colours": colours, "dex_text": dex_text}


def rec(top, side, extra=None):
    """A stone recipe: `top` across the top, `side` either side of the Mega Stone, a Diamond below (`extra` under
    the corners if given)."""
    pattern = ["ttt", "sms", f"{'x' if extra else ' '}d{'x' if extra else ' '}"]
    key = {"t": top, "s": side, "m": "mega_showdown:mega_stone", "d": "minecraft:diamond"}
    if extra:
        key["x"] = extra
    return {"pattern": pattern, "key": key}


# The order is fixed: it numbers the stones' icons (custom_model_data) and Showdown item nums.
MEGAS = {
    "greattusk": mega("Great Tusk", 984, A, ["ground", "fighting"], "toughclaws", "Tough Claws", [115, 171, 171, 53, 53, 107],
                      "Great Tuskite", rec("minecraft:bone_block", "minecraft:mud_bricks"), [(70, 88, 150), (232, 222, 196)],
                      "Its tusks have grown into great curling arcs and its hide into stone-hard plates. It rolls through "
                      "mountains as if they were sand."),
    "screamtail": mega("Scream Tail", 985, A, ["fairy", "psychic"], "punkrock", "Punk Rock", [115, 65, 129, 95, 135, 131],
                       "Scream Tailite", rec("minecraft:pink_wool", "minecraft:note_block"), [(246, 176, 196), (226, 92, 130)],
                       "Its fluffy mane bristles and its tail has grown long enough to coil round its foes. Its scream can "
                       "shatter boulders."),
    "brutebonnet": mega("Brute Bonnet", 986, A, ["grass", "dark"], "grassysurge", "Grassy Surge", [121, 167, 129, 79, 129, 45],
                        "Brute Bonnetite", rec("minecraft:moss_block", "minecraft:red_mushroom_block", "minecraft:brown_mushroom"),
                        [(120, 84, 60), (150, 210, 90)],
                        "Its stalk has grown into a colossal trunk like the giant fungi of ancient times, taller than the "
                        "trees around it. Moss hangs from its cap, and its fists can fell a forest."),
    "fluttermane": mega("Flutter Mane", 987, A, ["ghost", "fairy"], "levitate", "Levitate", [75, 55, 75, 175, 155, 135],
                        "Flutter Manite", rec("minecraft:phantom_membrane", "minecraft:amethyst_shard"), [(40, 84, 96), (210, 50, 90)],
                        "Its feathery mane spreads like great wings and its beads glow with eerie light. Its cries are said "
                        "to drive whole villages from their homes."),
    "slitherwing": mega("Slither Wing", 988, A, ["bug", "fighting"], "moxie", "Moxie", [85, 175, 109, 85, 115, 101],
                        "Slither Wingite", rec("minecraft:blaze_powder", "minecraft:white_wool"), [(232, 82, 40), (250, 196, 70)],
                        "Its six wings blaze like a wildfire. It crawls through the forest on its many legs, scorching all "
                        "it touches."),
    "sandyshocks": mega("Sandy Shocks", 989, A, ["electric", "ground"], "magnetpull", "Magnet Pull", [85, 81, 127, 161, 105, 111],
                        "Sandy Shockite", rec("minecraft:iron_ingot", "minecraft:lodestone", "minecraft:sand"), [(150, 160, 176), (212, 58, 58)],
                        "Its magnets have grown into great arches crackling with sand. It drags whole sandstorms behind it."),
    "roaringmoon": mega("Roaring Moon", 1005, A, ["dragon", "dark"], "intimidate", "Intimidate", [105, 179, 91, 55, 121, 139],
                        "Roaring Moonite", rec("minecraft:crying_obsidian", "minecraft:phantom_membrane"), [(60, 140, 190), (210, 30, 70)],
                        "Its wings have joined into a great crescent like a blood-red moon. Old tales say it rose on nights "
                        "when the moon turned red."),
    "koraidon": mega("Koraidon", 1007, A, ["fighting", "dragon"], "toughclaws", "Tough Claws", [100, 175, 135, 85, 120, 155],
                     "Koraidonite", rec("minecraft:sunflower", "minecraft:blaze_rod"), [(216, 52, 42), (240, 196, 80)],
                     "Its wing-feathers have unfurled into a blazing crown. The sun is said to burn hotter wherever it "
                     "spreads them."),
    "walkingwake": mega("Walking Wake", 1009, A, ["water", "dragon"], "drizzle", "Drizzle", [99, 83, 111, 165, 103, 129],
                        "Walking Wakite", rec("minecraft:prismarine_shard", "minecraft:nautilus_shell"), [(110, 70, 170), (40, 170, 170)],
                        "Its mane streams like burning water. Old stories say rain followed wherever it walked."),
    "gougingfire": mega("Gouging Fire", 1020, A, ["fire", "dragon"], "drought", "Drought", [105, 155, 141, 65, 113, 111],
                        "Gouging Firite", rec("minecraft:magma_block", "minecraft:gold_ingot"), [(190, 50, 30), (240, 200, 80)],
                        "Its golden mane flares into a crown of flame. The ground smoulders under its hooves."),
    "ragingbolt": mega("Raging Bolt", 1021, A, ["electric", "dragon"], "electricsurge", "Electric Surge", [125, 73, 111, 177, 109, 95],
                       "Raging Boltite", rec("minecraft:lightning_rod", "minecraft:yellow_dye"), [(140, 110, 190), (240, 200, 60)],
                       "Its storm-cloud mane crackles constantly. Lightning is said to answer its roar."),
    "irontreads": mega("Iron Treads", 990, F, ["ground", "steel"], "steelworker", "Steelworker", [90, 142, 150, 72, 90, 126],
                       "Iron Treadite", rec("minecraft:iron_block", "minecraft:redstone", "minecraft:rail"), [(70, 72, 80), (220, 40, 60)],
                       "Its treads have widened into great glowing wheels. It speeds across the land like a runaway train."),
    "ironbundle": mega("Iron Bundle", 991, F, ["ice", "water"], "snowwarning", "Snow Warning", [56, 80, 114, 164, 90, 166],
                       "Iron Bundlite", rec("minecraft:blue_ice", "minecraft:iron_ingot", "minecraft:redstone"), [(220, 50, 50), (80, 190, 230)],
                       "Its sack has become a huge cannon of ice. It glides through blizzards it makes itself."),
    "ironhands": mega("Iron Hands", 992, F, ["fighting", "electric"], "ironfist", "Iron Fist", [154, 180, 138, 50, 98, 50],
                      "Iron Handite", rec("minecraft:iron_block", "minecraft:redstone_block", "minecraft:copper_ingot"), [(60, 64, 84), (250, 200, 40)],
                      "Its hands have grown into colossal pistons. One punch can flatten a building."),
    "ironjugulis": mega("Iron Jugulis", 993, F, ["dark", "flying"], "levitate", "Levitate", [94, 80, 106, 162, 100, 128],
                        "Iron Jugulite", rec("minecraft:phantom_membrane", "minecraft:iron_ingot", "minecraft:redstone"), [(40, 44, 70), (230, 70, 160)],
                        "Its three heads glow with targeting lights and its wings have turned to blades."),
    "ironmoth": mega("Iron Moth", 994, F, ["fire", "poison"], "corrosion", "Corrosion", [80, 70, 80, 180, 130, 130],
                     "Iron Mothite", rec("minecraft:blaze_rod", "minecraft:iron_ingot", "minecraft:redstone"), [(240, 140, 40), (60, 60, 70)],
                     "Its wing panels have spread into a blazing halo that scorches the air around it."),
    "ironthorns": mega("Iron Thorns", 995, F, ["rock", "electric"], "sandstream", "Sand Stream", [100, 174, 140, 70, 104, 82],
                       "Iron Thornite", rec("minecraft:iron_block", "minecraft:redstone", "minecraft:green_dye"), [(120, 190, 70), (50, 54, 60)],
                       "Its armour has thickened into a fortress of spikes humming with electricity."),
    "ironvaliant": mega("Iron Valiant", 1006, F, ["fairy", "fighting"], "justified", "Justified", [74, 160, 100, 150, 70, 136],
                        "Iron Valiantite", rec("minecraft:iron_sword", "minecraft:pink_dye", "minecraft:redstone"), [(110, 180, 90), (240, 100, 160)],
                        "Its blades have lengthened into a flowing cape of light. It fights as gracefully as it dances."),
    "miraidon": mega("Miraidon", 1008, F, ["electric", "dragon"], "transistor", "Transistor", [100, 85, 120, 175, 135, 155],
                     "Miraidonite", rec("minecraft:lightning_rod", "minecraft:amethyst_shard"), [(60, 60, 150), (240, 230, 90)],
                     "Its body-fins have flared into wings of pure light. It races through the sky faster than lightning."),
    "ironleaves": mega("Iron Leaves", 1010, F, ["grass", "psychic"], "sharpness", "Sharpness", [90, 170, 108, 70, 128, 124],
                       "Iron Leafite", rec("minecraft:oak_leaves", "minecraft:iron_ingot", "minecraft:redstone"), [(80, 170, 70), (230, 60, 120)],
                       "Its blade-horns have grown into a crest of glowing swords that can cut through steel."),
    "ironboulder": mega("Iron Boulder", 1022, F, ["rock", "psychic"], "solidrock", "Solid Rock", [90, 160, 100, 68, 128, 144],
                        "Iron Boulderite", rec("minecraft:polished_blackstone", "minecraft:iron_ingot", "minecraft:redstone"), [(80, 80, 88), (240, 150, 40)],
                        "Its horn-blade glows white-hot and its armour has grown into a moving fortress."),
    "ironcrown": mega("Iron Crown", 1023, F, ["steel", "psychic"], "psychicsurge", "Psychic Surge", [90, 72, 120, 162, 128, 118],
                      "Iron Crownite", rec("minecraft:iron_block", "minecraft:redstone", "minecraft:prismarine_crystals"), [(40, 170, 180), (230, 230, 240)],
                      "Its crest-blades have spread into a crown of floating swords that guard it on every side."),
}
FOLDER = lambda sp: f"{MEGAS[sp]['dex']:04d}_{sp}"
STONE = lambda sp: MEGAS[sp]["stone_name"].lower().replace(" ", "")


def name_of(sp):
    return f"{sp}_mega"


def group_of(sp):
    return f"cobbleeffort_{sp}_mega"


_MODELS = {}


def model_module(sp):
    """tools/megas/models/<sp>.py, loaded by path (some names, e.g. ironboulder, are also new-Pokémon builders)."""
    if sp not in _MODELS:
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"mega_model_{sp}", HERE / "models" / f"{sp}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODELS[sp] = mod
    return _MODELS[sp]


def built():
    """The megas with a model module, in config order."""
    return [sp for sp in MEGAS if (HERE / "models" / f"{sp}.py").exists()]


# --- model, textures, animations ---------------------------------------------------------------------------------

def build_model(sp):
    hand = model_module(sp)
    cfg = MEGAS[sp]
    cfg["scale"], cfg["hitbox"], cfg["kind"] = hand.SCALE, hand.HITBOX, getattr(hand, "KIND", "quadruped")
    cfg["anim"] = getattr(hand, "ANIM", {})
    m = hand.build()
    tw, th = m.layout()
    nm = name_of(sp)
    tex_dir = RES / "assets" / MOD / "textures" / "pokemon" / FOLDER(sp)
    tex_dir.mkdir(parents=True, exist_ok=True)
    for variant, sfx in ((None, ""), ("shiny", "_shiny")):
        img, glow = m.paint(tw, th, variant)
        img.save(tex_dir / f"{nm}{sfx}.png", optimize=True)
        for f, k in enumerate((1.0, 0.82, 0.92)):            # the glow pulses a little
            g = np.array(glow).astype(float)
            g[..., :3] *= k
            Image.fromarray(g.astype(np.uint8), "RGBA").save(tex_dir / f"{nm}{sfx}_glow_{f}.png", optimize=True)
    names = [b["name"] for b in m.bones if b["parent"] is not None]
    piv = {b["name"]: b["pivot"] for b in m.bones}
    legs = [n for n in names if n.startswith("leg")]
    top = max(b.lo[1] + b.size[1] for b in m.boxes)
    cfg["height"] = top
    extra = [{"name": "locator_root", "parent": nm, "pivot": [0, 0, 0]},
             {"name": "locator_top", "parent": nm, "pivot": [0, float(top), 0]}]
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "models" / FOLDER(sp) / f"{nm}.geo.json",
               m.geo(tw, th, f"geometry.{nm}", extra))
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "animations" / FOLDER(sp) / f"{group_of(sp)}.animation.json",
               animations(group_of(sp), MEGAS[sp]["kind"], MEGAS[sp]["anim"], names, legs, piv))
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "posers" / FOLDER(sp) / f"{nm}.json",
               poser(group_of(sp), nm, MEGAS[sp]["height"], MEGAS[sp]["scale"], names))
    print(f"{sp}: {len(m.boxes)} cubes, texture {tw}x{th}, bones {names}")


# --- data ----------------------------------------------------------------------------------------------------------

def data_files(sp):
    cfg = MEGAS[sp]
    nm = name_of(sp)
    tex = lambda n: f"{MOD}:textures/pokemon/{FOLDER(sp)}/{n}.png"
    glow = lambda sfx: {"name": "cobbleeffort_mega_glow", "emissive": True, "translucent": True,
                        "texture": {"frames": [tex(f"{nm}{sfx}_glow_{f}") for f in range(3)], "fps": 6, "loop": True}}
    # the mega's look: only with the "mega" aspect, so the base form (from another mod) is untouched. Cobblemon merges
    # layers by name across every matching variation, so the base form's layers (glow, alpha eyes: painted for the
    # base mesh) are switched off on the mega
    inherited = [{"name": n, "enabled": False} for n in sorted(BASE_LAYERS.get(sp, set()))]
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / "megas" / FOLDER(sp) / f"10_{nm}.json", {
        "species": f"cobblemon:{sp}", "order": 10,
        "variations": [
            {"aspects": ["mega"], "poser": f"{MOD}:{nm}", "model": f"{MOD}:{nm}.geo", "texture": tex(nm),
             "layers": inherited + [glow("")]},
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
    write_json(RES / "data" / MOD / "mega_showdown" / "mega" / f"{STONE(sp)}.json", {
        "showdown_id": STONE(sp), "pokemons": [cfg["display"]],
        "aspect_conditions": {"apply": {"aspects": ["mega_evolution=mega"]}, "revert": {"aspects": ["mega_evolution=none"]}}})
    js = RES / "data" / MOD / "mega_showdown" / "showdown" / "held_items" / f"{STONE(sp)}.js"
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
    write_json(RES / "data" / MOD / "recipe" / f"{STONE(sp)}.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": r["pattern"],
        "key": {c: {"item": it} for c, it in r["key"].items()},
        "result": {"id": BASE_ITEM, "count": 1, "components": stone_components(sp)}})


def stone_components(sp):
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.{STONE(sp)}", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.{STONE(sp)}.tooltip", "color": "gray", "italic": False})],
        "minecraft:custom_model_data": CMD_BASE + 1 + list(MEGAS).index(sp),
        "minecraft:rarity": "epic",
        "minecraft:max_stack_size": 1,
        "mega_showdown:registry_type_component": "mega",
        "mega_showdown:registry_location_component": f"{MOD}:{STONE(sp)}",
    }


def stone_icons(sps):
    """16x16 icons: a round gem in the Pokémon's colours with Mega Showdown's double-helix mark."""
    out = RES / "assets" / MOD / "textures" / "item"
    out.mkdir(parents=True, exist_ok=True)
    for sp in sps:
        a, b = MEGAS[sp]["stone_colours"]
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
        img.save(out / f"{STONE(sp)}.png")
        write_json(RES / "assets" / MOD / "models" / "item" / f"{STONE(sp)}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{STONE(sp)}"}})
    write_json(RES / "assets" / "minecraft" / "models" / "item" / "amethyst_shard.json", {
        "parent": "minecraft:item/generated", "textures": {"layer0": "minecraft:item/amethyst_shard"},
        "overrides": [{"predicate": {"custom_model_data": CMD_BASE + 1 + list(MEGAS).index(sp)}, "model": f"{MOD}:item/{STONE(sp)}"}
                      for sp in sps]})


def lang(sps):
    path = RES / "assets" / MOD / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    for sp in sps:
        cfg = MEGAS[sp]
        data[f"item.{MOD}.{STONE(sp)}"] = cfg["stone_name"]
        data[f"item.{MOD}.{STONE(sp)}.tooltip"] = f"Lets {cfg['display']} Mega Evolve in battle."
        data[f"cobblemon.species.{sp}-mega.desc"] = cfg["dex_text"]
    write_json(path, dict(sorted(data.items())))


BASE_LAYERS: dict[str, set[str]] = {}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cobblemon", required=True, type=Path, help="Cobblemon's common/src/main/resources")
    args = ap.parse_args()
    sys.path.insert(0, str(TOOLS))
    from stack import Stack, resolver_layer_names
    stack = Stack(args.cobblemon)
    # every layer the stack's own resolvers give each species (the bridge's packs ship none of their own)
    BASE_LAYERS.update(resolver_layer_names([l for l in stack.layers if not l.bridge]))
    sps = built()
    manifest = []
    for sp in sps:
        build_model(sp)
        data_files(sp)
        for sfx in ("", "_shiny"):
            manifest.append({"species": f"{sp}_mega{sfx}", "folder": FOLDER(sp), "model": f"{MOD}:{name_of(sp)}.geo",
                             "original": None, "retextured": f"{MOD}:textures/pokemon/{FOLDER(sp)}/{name_of(sp)}{sfx}.png",
                             "layers": [{"original": None, "retextured": f"{MOD}:textures/pokemon/{FOLDER(sp)}/{name_of(sp)}{sfx}_glow_0.png", "emissive": True}]})
    stone_icons(sps)
    lang(sps)
    write_json(RES / "data" / MOD / "species_feature_assignments" / "paradox_megas.json",
               {"pokemon": sps, "features": ["mega_evolution"]})
    write_json(TOOLS / "preview" / "manifest_megas.json", manifest)
    write_json(TOOLS / "readme" / "_megas.json",
               {sp: {k: MEGAS[sp][k] for k in ("display", "stone_name", "types", "ability", "ability_name", "stats", "recipe", "era")}
                for sp in sps})
    readme_table(sps)
    sys.path.insert(0, str(TOOLS))
    import make_creative_tab                                 # the creative tab lists the stones
    make_creative_tab.main()


def readme_table(sps):
    """The mega table in README.md, between its <!-- megas --> markers."""
    path = ROOT / "README.md"
    text = path.read_text()
    a, b = "<!-- megas:start -->", "<!-- megas:end -->"
    rows = ["| Mega | Era | Types | Ability | HP / Atk / Def / SpA / SpD / Spe | Stone | Look |", "|---|---|---|---|---|---|---|"]
    for sp in sps:
        c = MEGAS[sp]
        look = model_module(sp).LOOK
        rows.append(f"| Mega {c['display']} | {c['era'].title()} | {' / '.join(t.title() for t in c['types'])} | "
                    f"{c['ability_name']} | {' / '.join(map(str, c['stats']))} | {c['stone_name']} | {look} |")
    left = len(MEGAS) - len(sps)
    note = f"\n\n*{left} more on the way.*" if left else ""
    path.write_text(text[:text.index(a) + len(a)] + "\n" + "\n".join(rows) + note + "\n" + text[text.index(b):])


if __name__ == "__main__":
    main()
