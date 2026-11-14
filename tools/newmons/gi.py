"""Gi forms (the user's design, after @magikdex's Cornera region art): Sawk, Throh and Kiq (Chawp's three evolutions)
each have a Gi form, a special evolution unlocked by a rare item, the Master's Gi (crafted, or found in dojo chests).

  Sawk's Gi   Fighting/Electric   signature move Thunder Chop
  Throh's Gi  Fighting/Fire       signature move Inferno Toss
  Kiq's Gi    Fighting/Ice        signature move Frost Roundhouse

How it works (data only, run by build.py):
  - flag species feature `gi` (an aspect) on cobblemon:sawk, cobblemon:throh, cobbleeffort:kiq;
  - species_additions/<sp>_gi.json: a form "Gi" (aspect gi; types, abilities, stats, size; its own empty evolutions so
    it can't take another Gi) appended to the species, an item_interact evolution whose result is the same species
    with the gi aspect (Cobblemon applies the result to the same Pokémon; using the item unlocks the Evolve button and
    uses up the item), and, for Sawk and Throh, preEvolution = Chawp;
  - the Master's Gi: an echo shard with custom_data {cobbleeffort_gi: "masters_gi"} + name, lore and icon (like the
    fossil items; Cobblemon's legacy {item, nbt} predicate matches it), a shaped recipe, and the `dojo` structure
    whose chest may hold one;
  - resolvers at order 5: each Gi form pins its own box model (tools/newmons/models/<sp>_gi.py) and switches off the
    layers Cobblemon gives the species (alpha eyes).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "models"))
from fossils import MOD, RES, Template, h, write_json, write_structure  # noqa: E402

TOOLS = HERE.parent

ASPECT = "gi"
BASE_ITEM = "minecraft:echo_shard"
ITEM = {"item": "masters_gi", "name": "Master's Gi", "cmd": 10, "key": "masters_gi",
        "lore": "A battered training gi handed down by a line of great masters. Use it on a Sawk, Throh or Kiq to awaken "
                "its Gi form."}
NBT = '{cobbleeffort_gi:"masters_gi"}'

FORMS = {
    "sawk": {
        "target": "cobblemon:sawk", "dex": 539, "name": "Sawk", "pre": f"{MOD}:chawp", "folder": "gi/0539_sawk",
        "types": ["fighting", "electric"], "abilities": ["sturdy", "motordrive", "h:moldbreaker"],
        "ability_names": "Sturdy / Motor Drive / Mold Breaker (hidden)",
        "stats": (75, 150, 80, 50, 80, 130), "learn": ["thunderchop"], "move_name": "Thunder Chop",
        "base_layers": ["alpha_eyes"],
        "entry": ("A Sawk that has earned the Master's Gi. Its focus is so sharp that it crackles: every chop lands with "
                  "a thunderclap, and its belt and collar spit sparks as it moves."),
    },
    "throh": {
        "target": "cobblemon:throh", "dex": 538, "name": "Throh", "pre": f"{MOD}:chawp", "folder": "gi/0538_throh",
        "types": ["fighting", "fire"], "abilities": ["guts", "flashfire", "h:moldbreaker"],
        "ability_names": "Guts / Flash Fire / Mold Breaker (hidden)",
        "stats": (135, 130, 105, 40, 100, 55), "learn": ["infernotoss"], "move_name": "Inferno Toss",
        "base_layers": ["alpha_eyes"],
        "entry": ("A Throh that has earned the Master's Gi. Its fighting spirit burns so hot that its gi never catches "
                  "fire; foes it throws land wreathed in flames."),
    },
    "kiq": {
        "target": f"{MOD}:kiq", "dex": 3147, "name": "Kiq", "pre": None, "folder": "gi/3147_kiq",
        "types": ["fighting", "ice"], "abilities": ["limber", "slushrush", "h:moldbreaker"],
        "ability_names": "Limber / Slush Rush / Mold Breaker (hidden)",
        "stats": (80, 145, 85, 40, 85, 130), "learn": ["frostroundhouse"], "move_name": "Frost Roundhouse",
        "base_layers": [],
        "moves_add": ["1:frostroundhouse", "tm:icepunch", "tm:tripleaxel", "tm:icespinner", "tm:iciclecrash",
                      "tm:avalanche", "tm:icywind", "tm:snowscape", "tm:auroraveil"],
        "entry": ("A Kiq that has earned the Master's Gi. Its kicks are so fast the air freezes in their wake; frost "
                  "grows over its shoulders, and icicles over its hips."),
    },
}

GI_MOVES = {
    "thunderchop": {
        "base": "karatechop", "num": -3040, "name": "Thunder Chop", "type": "Electric", "category": "Physical",
        "basePower": 90, "accuracy": 100, "pp": 15, "critRatio": 2, "secondary": {"chance": 20, "status": "par"},
        "flags": {"contact": 1, "protect": 1, "mirror": 1, "metronome": 1}, "contestType": "Cool",
        "desc": "Has a higher chance for a critical hit. 20% chance to paralyze the target.",
        "shortDesc": "High critical hit ratio. 20% chance to paralyze.",
        "lang": "The user chops the target with a hand crackling with lightning. Critical hits land more easily, and it "
                "may also leave the target with paralysis.",
    },
    "infernotoss": {
        "base": "circlethrow", "num": -3041, "name": "Inferno Toss", "type": "Fire", "category": "Physical",
        "basePower": 80, "accuracy": 90, "pp": 10, "priority": -6, "forceSwitch": True,
        "secondary": {"chance": 30, "status": "brn"},
        "flags": {"contact": 1, "protect": 1, "mirror": 1, "metronome": 1, "noassist": 1, "failcopycat": 1},
        "contestType": "Cool",
        "desc": "If both the user and the target have not fainted, the target is forced to switch out and be replaced "
                "with a random unfainted ally. 30% chance to burn the target.",
        "shortDesc": "Forces the target to switch. 30% chance to burn.",
        "lang": "The user grabs the target and hurls it away in a ring of fire, forcing it to switch out. It may also "
                "leave the target with a burn. In the wild, the battle ends.",
    },
    "frostroundhouse": {
        "base": "blazekick", "num": -3042, "name": "Frost Roundhouse", "type": "Ice", "category": "Physical",
        "basePower": 85, "accuracy": 90, "pp": 10, "critRatio": 2, "secondary": {"chance": 10, "status": "frz"},
        "flags": {"contact": 1, "protect": 1, "mirror": 1, "metronome": 1}, "contestType": "Cool",
        "desc": "Has a higher chance for a critical hit. 10% chance to freeze the target.",
        "shortDesc": "High critical hit ratio. 10% chance to freeze.",
        "lang": "The user spins and delivers a roundhouse kick that freezes the air. Critical hits land more easily, and "
                "it may also leave the target frozen.",
    },
}

CMD_BASE = 794800


def components():
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.{ITEM['item']}", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.{ITEM['item']}.tooltip", "color": "gray",
                                       "italic": False})],
        "minecraft:custom_model_data": CMD_BASE + ITEM["cmd"],
        "minecraft:rarity": "rare",
        "minecraft:max_stack_size": 16,
        "minecraft:custom_data": {"cobbleeffort_gi": ITEM["key"]},
    }


def stack():
    return {"id": BASE_ITEM, "count": 1, "components": components()}


def override():
    """The echo shard model override for the item's icon (fossils.build writes echo_shard.json with these)."""
    return {"predicate": {"custom_model_data": CMD_BASE + ITEM["cmd"]}, "model": f"{MOD}:item/{ITEM['item']}"}


def icon():
    """A folded white training gi: wide sleeves, crossed lapels, a black belt with hanging tails."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    white, shade, line, black = (244, 244, 238, 255), (206, 206, 200, 255), (120, 120, 126, 255), (34, 34, 40, 255)
    for y in range(16):
        for x in range(16):
            body = 4 <= x <= 11 and 2 <= y <= 14
            sleeve = (1 <= x <= 3 or 12 <= x <= 14) and 2 <= y <= 7
            shoulder = 1 <= x <= 14 and 2 <= y <= 3
            if body or sleeve or shoulder:
                c = white
                if x in (1, 14) or y == 14 or (sleeve and y == 7) or y == 2:
                    c = line
                elif sleeve and y >= 5:
                    c = shade
                if body and 2 <= y <= 9 and (abs(x - (5 + (y - 2) * 0.4)) < 0.6 or abs(x - (10 - (y - 2) * 0.4)) < 0.6):
                    c = line                                                         # the crossed lapels
                if body and 9 <= y <= 10:
                    c = black                                                        # the belt
                px[x, y] = c
    for y in range(11, 16):                                                          # its hanging tails
        px[7, y] = black
        if y < 15:
            px[8, y] = black
    return img


# --- the dojo --------------------------------------------------------------------------------------------------

def dojo():
    """A small dojo: stone-brick footing, a bamboo-mat floor, dark oak posts and beams with pale birch panels, a deep
    gabled roof of deepslate tiles, straw punching bags, lanterns, and the master's chest on a raised dais."""
    W, D = 13, 11                                      # walls; the template adds a one-block roof overhang
    ox, oz = 1, 1
    t = Template((W + 2, 13, D + 2))

    def s(x, y, z, name, props=None, nbt=None):
        t.set(x + ox, y, z + oz, name, props, nbt)
    for x in range(W):
        for z in range(D):
            s(x, 0, z, "minecraft:stone_bricks" if h(x, z, 2) > 0.18 else "minecraft:mossy_stone_bricks")
            edge = x in (0, W - 1) or z in (0, D - 1)
            s(x, 1, z, "minecraft:stone_bricks" if edge else "minecraft:bamboo_mosaic")
            for y in range(2, 7):
                if not edge:
                    s(x, y, z, "minecraft:air")
    for x in range(W):                                 # walls: posts every 3 blocks, beams, birch panels
        for z in range(D):
            if not (x in (0, W - 1) or z in (0, D - 1)):
                continue
            post = (x % 3 == 0 and z in (0, D - 1)) or (z % 3 == 0 and x in (0, W - 1)) or \
                   (x in (0, W - 1) and z in (0, D - 1))
            for y in range(2, 6):
                if post:
                    s(x, y, z, "minecraft:dark_oak_log", {"axis": "y"})
                elif y == 2:
                    s(x, y, z, "minecraft:spruce_planks")
                elif y == 5:
                    s(x, y, z, "minecraft:dark_oak_planks")
                else:
                    s(x, y, z, "minecraft:birch_planks")
    for x in (5, 6, 7):                                # the doorway (front, -z) and two side windows
        for y in (2, 3, 4):
            s(x, y, 0, "minecraft:air")
    s(5, 4, 0, "minecraft:dark_oak_planks")
    s(7, 4, 0, "minecraft:dark_oak_planks")
    for z in (4, 5):
        for x in (0, W - 1):
            s(x, 3, z, "minecraft:air")
    for i in range(7):                                 # the gabled roof (ridge along x), deepslate tiles
        y = 6 + i
        zn, zs = i - 1, D - i
        for x in range(-1, W + 1):
            if zn < zs:
                s(x, y, zn, "minecraft:deepslate_tile_stairs",
                  {"facing": "south", "half": "bottom", "shape": "straight", "waterlogged": "false"})
                s(x, y, zs, "minecraft:deepslate_tile_stairs",
                  {"facing": "north", "half": "bottom", "shape": "straight", "waterlogged": "false"})
            elif zn == zs:
                s(x, y, zn, "minecraft:deepslate_tile_slab", {"type": "bottom", "waterlogged": "false"})
        if zn < zs:
            for x in (0, W - 1):                       # gable ends
                for z in range(zn + 1, zs):
                    s(x, y, z, "minecraft:birch_planks" if y > 6 else "minecraft:dark_oak_planks")
            for x in range(1, W - 1):
                for z in range(zn + 1, zs):
                    s(x, y, z, "minecraft:air")
    for x in range(1, W - 1):                          # a ridge beam inside
        s(x, 10, 5, "minecraft:dark_oak_log", {"axis": "x"})
    for x in range(4, 9):                              # the master's dais at the back
        for z in (8, 9):
            s(x, 2, z, "minecraft:dark_oak_slab", {"type": "bottom", "waterlogged": "false"})
    s(6, 2, 9, "minecraft:chest", {"facing": "north", "type": "single", "waterlogged": "false"},
      {"id": "minecraft:chest", "LootTable": f"{MOD}:chests/dojo"})
    for x in (4, 8):
        s(x, 3, 9, "minecraft:lantern", {"hanging": "false", "waterlogged": "false"})
    for x, z in ((2, 3), (10, 3), (2, 7), (10, 7)):    # straw punching bags
        s(x, 2, z, "minecraft:oak_fence", {"north": "false", "south": "false", "east": "false", "west": "false",
                                           "waterlogged": "false"})
        s(x, 3, z, "minecraft:hay_block", {"axis": "y"})
        s(x, 4, z, "minecraft:hay_block", {"axis": "y"})
    for x in (1, W - 2):                               # lanterns by the door
        s(x, 2, 1, "minecraft:lantern", {"hanging": "false", "waterlogged": "false"})
    return t


STRUCTURE = {"build": dojo,
             "biomes": ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:cherry_grove",
                        "minecraft:taiga", "minecraft:savanna", "minecraft:windswept_hills", "minecraft:bamboo_jungle",
                        "minecraft:snowy_plains", "minecraft:grove"],
             "step": "surface_structures", "adapt": "beard_thin", "height": {"absolute": 0},
             "project": "WORLD_SURFACE_WG", "spacing": 34, "separation": 12, "salt": 51734}

LOOT = [
    {"rolls": 1, "entries": [
        {"type": "minecraft:item", "name": BASE_ITEM, "weight": 1,
         "functions": [{"function": "minecraft:set_components", "components": components()}]},
        {"type": "minecraft:empty", "weight": 2}]},
    {"rolls": {"min": 2, "max": 4}, "entries": [
        {"type": "minecraft:item", "name": "cobblemon:protein", "weight": 3},
        {"type": "minecraft:item", "name": "cobblemon:x_attack", "weight": 3},
        {"type": "minecraft:item", "name": "cobblemon:black_belt", "weight": 1},
        {"type": "minecraft:item", "name": "cobblemon:muscle_band", "weight": 1},
        {"type": "minecraft:item", "name": "cobblemon:focus_band", "weight": 1},
        {"type": "minecraft:item", "name": "cobblemon:power_bracer", "weight": 1},
        {"type": "minecraft:item", "name": "minecraft:white_wool", "weight": 4,
         "functions": [{"function": "minecraft:set_count", "count": {"min": 1, "max": 4}}]},
        {"type": "minecraft:item", "name": "minecraft:bread", "weight": 4,
         "functions": [{"function": "minecraft:set_count", "count": {"min": 1, "max": 3}}]},
        {"type": "minecraft:item", "name": "cobblemon:oran_berry", "weight": 3}]},
]


# --- the forms -------------------------------------------------------------------------------------------------

def form_json(sp, c, hand, species):
    st = dict(zip(("hp", "attack", "defence", "special_attack", "special_defence", "speed"), c["stats"]))
    f = {"name": "Gi", "aspects": [ASPECT], "primaryType": c["types"][0], "secondaryType": c["types"][1],
         "abilities": c["abilities"], "baseStats": st, "baseScale": hand.SCALE,
         "hitbox": {"width": hand.HITBOX[0], "height": hand.HITBOX[1], "fixed": False},
         "labels": ["cobbleeffort_gi"], "pokedex": [f"{MOD}.species.{sp}-{ASPECT}.desc"], "battleOnly": False,
         "evolutions": []}
    if c.get("moves_add"):                             # our own species: its learnset plus the Gi's extras
        base = species[sp]
        moves = [f"{lv}:{mv}" for lv, mv in base["moves"]] + [f"egg:{m}" for m in base["egg"]] + \
                [f"tm:{m}" for m in base["tm"]]
        f["moves"] = moves + [m for m in c["moves_add"] if m not in moves]
    return f


def build(lang, species, model_module, write_model_assets):
    """Writes everything; build.py passes its SPECIES (for Kiq's learnset) and its model helpers. Returns the preview
    manifest entries."""
    data, assets = RES / "data" / MOD, RES / "assets" / MOD
    write_json(data / "species_features" / f"{ASPECT}.json",
               {"keys": [ASPECT], "type": "flag", "isAspect": True, "default": False})
    write_json(data / "species_feature_assignments" / f"{ASPECT}.json",
               {"pokemon": [c["target"] for c in FORMS.values()], "features": [ASPECT]})
    manifest = []
    for sp, c in FORMS.items():
        name = f"{sp}_{ASPECT}"
        hand = model_module(name)
        add = {"target": c["target"],
               "evolutions": [{"id": f"{sp}_{ASPECT}", "variant": "item_interact", "result": f"{c['target']} {ASPECT}",
                               "consumeHeldItem": False, "learnableMoves": c["learn"],
                               "requiredContext": {"item": BASE_ITEM, "nbt": NBT}}],
               "forms": [form_json(sp, c, hand, species)]}
        if c["pre"]:
            add["preEvolution"] = c["pre"]
        write_json(data / "species_additions" / f"{name}.json", add)
        lang[f"{MOD}.species.{sp}-{ASPECT}.desc"] = c["entry"]
        r = write_model_assets(name, hand, c["folder"])
        tex = lambda sfx: f"{MOD}:textures/pokemon/{c['folder']}/{name}{sfx}.png"
        off = [{"name": n, "enabled": False} for n in c["base_layers"]]
        write_json(assets / "bedrock" / "pokemon" / "resolvers" / "gi" / f"{name}.json", {
            "species": c["target"], "order": 5, "variations": [
                {"aspects": [ASPECT], "poser": f"{MOD}:{name}", "model": f"{MOD}:{name}.geo", "texture": tex(""),
                 "layers": off + r["layers"][""]},
                {"aspects": [ASPECT, "shiny"], "texture": tex("_shiny"), "layers": off + r["layers"]["_shiny"]}]})
        for sfx in ("", "_shiny"):
            names = {l["name"] for l in r["layers"][sfx]}
            lay = ([{"original": None, "emissive": True, "retextured": tex(f"{sfx}_glow_0")}]
                   if "cobbleeffort_glow" in names else []) + \
                  ([{"original": None, "emissive": False, "retextured": tex(f"{sfx}_shell")}]
                   if "cobbleeffort_shell" in names else [])
            manifest.append({"species": f"{name}{sfx}", "folder": c["folder"], "model": f"{MOD}:{name}.geo",
                             "original": None, "retextured": tex(sfx), "layers": lay})
        st = c["stats"]
        write_json(TOOLS / "readme" / f"_new_{name}.json", {
            "dex": c["dex"], "name": f"{c['name']} (Gi form)", "types": " / ".join(t.title() for t in c["types"]),
            "ability": c["ability_names"], "look": hand.LOOK, "entry": c["entry"],
            "how": [f"Use a Master's Gi on a {c['name']} (it unlocks the Evolve button). It learns {c['move_name']} "
                    "when it changes.",
                    "Master's Gi: crafted from six White Wool, a Gold Ingot, a Black Belt and a Diamond, or found in "
                    "dojo chests."],
            "stats": list(st)})
    # the Master's Gi: lang, icon, model, recipe; dojo + loot
    lang[f"item.{MOD}.{ITEM['item']}"] = ITEM["name"]
    lang[f"item.{MOD}.{ITEM['item']}.tooltip"] = ITEM["lore"]
    tex = assets / "textures" / "item" / f"{ITEM['item']}.png"
    tex.parent.mkdir(parents=True, exist_ok=True)
    icon().save(tex)
    write_json(assets / "models" / "item" / f"{ITEM['item']}.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{ITEM['item']}"}})
    write_json(data / "recipe" / f"{ITEM['item']}.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["WGW", "WBW", "WDW"],
        "key": {"W": {"item": "minecraft:white_wool"}, "G": {"item": "minecraft:gold_ingot"},
                "B": {"item": "cobblemon:black_belt"}, "D": {"item": "minecraft:diamond"}},
        "result": stack()})
    write_json(data / "loot_table" / "chests" / "dojo.json", {"type": "minecraft:chest", "pools": LOOT})
    write_structure("dojo", STRUCTURE, "dojo")
    write_json(TOOLS / "preview" / "manifest_gi.json", manifest)
    return manifest
