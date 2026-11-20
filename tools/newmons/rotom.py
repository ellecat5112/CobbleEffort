"""CobbleEffort's extra Rotom forms (the user's request, 1.8.0): 33 new appliances for Rotom (Invasion added in 1.10.0), each with its own form-
change item and in Mega Showdown's Rotom Catalogue cycle (the Catalogue part is a mixin in CobbleEffort: Distortion).

* Forms ride on Cobblemon's own `appliance` feature: Mega Showdown sets features as raw strings ("appliance=drill"
  gives the aspect "drill-appliance"), Cobblemon keeps a saved feature's value as it is, and Mega Showdown's Rotom
  Units and Catalogue setting "appliance=heat" etc. replace ours naturally. species_additions append the forms to
  cobblemon:rotom (Levitate, the appliance forms' stats, Heat Rotom's learnset with its own form-change move).
* Models: one box model per form (`tools/newmons/models/rotom_<key>.py`, on `_rotomform.py`), written to
  `bedrock/pokemon/*/rotom/`; one resolver at order 9001 (above Mega Showdown's Rotom resolvers, and above our
  cosmetics, which mirror only the vanilla forms) pins model, poser and texture and switches every other layer off.
* Items: echo shards (like the fossils) carrying Mega Showdown's `registry_type_component` = form_change_interact
  and `registry_location_component` = cobbleeffort:rotom_<key>, so Mega Showdown's own ItemStack hook runs our
  `data/cobbleeffort/mega_showdown/form_change_interact/rotom_<key>.json` (use on your Rotom: into the form; again:
  back to plain Rotom). Shaped recipes round a Cell Battery, loaded only with Mega Showdown (fabric/neoforge
  conditions). Icons are drawn in rotom_icons.py; fossils.build adds the echo-shard model overrides.

    python3 tools/newmons/rotom.py --cobblemon <cobblemon>/common/src/main/resources
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
RES = TOOLS.parent / "src" / "main" / "resources"
MOD = "cobbleeffort"
BASE_ITEM = "minecraft:echo_shard"
CMD_BASE = 794800
CMD0 = 20                                               # after the fossils (1-9), the Master's Gi (10), the Garbage Bag (11)
ORDER = 9001
MSD_EFFECT = "mega_showdown:rotom_effect"
JOSEON, ABYSS, CALIGO = "Joseon Region fakemon art", "The_Aussie_Artist's Pokémon Abyss art", "CaligoMilites' art"
SHEET = "the user's Rotom doodle sheets (artist not named)"

# key: (form name, types, form-change move, item name, recipe (T, F) round a Cell Battery, Pokédex entry, credit)
FORMS = {
    "drill": ("Drill", ["electric", "steel"], "steelbeam", "Drill Engine", ("minecraft:iron_pickaxe", "minecraft:iron_ingot"),
              "This Rotom has taken over a drilling rig. It chews through bedrock with its grinding teeth and leaves "
              "tunnels so neat that miners follow them home.", JOSEON),
    "jetski": ("Jetski", ["electric", "dragon"], "dracometeor", "Jet Ski Engine", ("#minecraft:boats", "minecraft:prismarine_shard"),
               "It skims across lakes pretending to be a shark, and laughs its crackling laugh when swimmers scramble "
               "for the shore.", JOSEON),
    "atv": ("ATV", ["electric", "rock"], "powergem", "ATV Engine", ("minecraft:minecart", "minecraft:copper_ingot"),
            "Its huge tyres grip any rock. It loves sneaking up behind hikers on mountain trails and revving its "
            "engine until they jump.", JOSEON),
    "harvester": ("Harvester", ["electric", "bug"], "bugbuzz", "Harvester Engine", ("minecraft:iron_axe", "#minecraft:saplings"),
                  "It can fell and mulch a tree in seconds. Keep one out of your garden, or it will happily chew through "
                  "every tree it can reach.", JOSEON),
    "string": ("String", ["ghost", "grass"], "energyball", "Phantom Bow", ("minecraft:string", "minecraft:spruce_planks"),
               "It plays haunting melodies on moonlit nights. Plants nearby are said to grow towards the sound.", ABYSS),
    "beat": ("Beat", ["ghost", "fighting"], "aurasphere", "Phantom Drumsticks", ("minecraft:note_block", "minecraft:leather"),
             "Its plasma arms drum faster than the eye can follow. Every beat lands like a punch.", ABYSS),
    "brass": ("Brass", ["ghost", "steel"], "flashcannon", "Phantom Mouthpiece", ("minecraft:gold_ingot", "minecraft:copper_ingot"),
              "Its fanfare is loud enough to rattle windows. It marches through towns at dawn, waking everyone up.", ABYSS),
    "grand": ("Grand", ["ghost", "psychic"], "psychic", "Phantom Piano Key", ("minecraft:note_block", "minecraft:quartz"),
              "It plays an empty concert hall by itself. Listeners say its music shows them memories they had "
              "forgotten.", ABYSS),
    "rotomboy": ("Rotom Boy", ["electric", "ghost"], "thunder", "Retro Cartridge", ("minecraft:glass_pane", "minecraft:light_gray_concrete"),
                 "This Rotom haunts an old handheld game console. The ghost of a Pikachu it once played as glows "
                 "round it.", CALIGO),
    "watch": ("Watch", ["electric", "psychic"], "futuresight", "Watch Strap", ("minecraft:clock", "minecraft:red_dye"),
              "It counts its Trainer's steps and buzzes when they sit still too long. It always knows what time it "
              "will be.", SHEET),
    "charger": ("Charger", ["electric"], "zapcannon", "Charging Cable", ("minecraft:redstone", "minecraft:copper_ingot"),
                "It plugs itself into walls and drinks electricity until it glows. Devices left near it charge in "
                "seconds, or burst.", SHEET),
    "tv": ("TV", ["electric", "dark"], "nightdaze", "Remote Control", ("minecraft:glass_pane", "minecraft:black_concrete"),
           "It shows only a shadowy figure and the words \"this program is unavailable\". Viewers cannot look away.", SHEET),
    "vacuum": ("Vacuum", ["electric", "poison"], "sludgebomb", "Vacuum Hose", ("minecraft:hopper", "minecraft:iron_ingot"),
               "It sucks up dust, dirt and the odd small Pokémon. What it cannot digest it blows back out as a choking "
               "cloud.", SHEET),
    "toaster": ("Toaster", ["electric", "fire"], "fireblast", "Toaster Coil", ("minecraft:bread", "minecraft:iron_ingot"),
                "It pops out toast so hot it bursts into flame. It gets grumpy if nobody eats it.", SHEET),
    "breaker": ("Breaker", ["electric", "ground"], "earthpower", "Circuit Fuse", ("minecraft:lever", "minecraft:gray_concrete"),
                "It lives in fuse boxes and flips its switches for fun. When it trips, every light in the house goes out "
                "and it sulks.", SHEET),
    "antenna": ("Antenna", ["electric", "fairy"], "moonblast", "Rabbit-Ear Antenna", ("minecraft:lightning_rod", "minecraft:pink_dye"),
                "It wiggles its rabbit-ear antennas to tune in to far-off signals, and grins its braced grin when it "
                "catches one.", SHEET),
    "earbuds": ("Earbuds", ["electric", "normal"], "hypervoice", "Earbud Case", ("minecraft:amethyst_shard", "minecraft:white_concrete"),
                "It snaps its case shut on anything that gets too close and plays music into the ears of anyone who "
                "picks it up.", SHEET),
    "rccar": ("RC Car", ["electric", "ground"], "earthpower", "RC Remote", ("minecraft:slime_ball", "minecraft:powered_rail"),
              "It races round courtyards at full speed and flips off ramps. It brings the ball back, but only "
              "sometimes.", SHEET),
    "clippers": ("Clippers", ["electric", "steel"], "mirrorshot", "Clipper Blade", ("minecraft:shears", "minecraft:iron_ingot"),
                 "It buzzes through fur and hair alike. Fluffy Pokémon flee when they hear it coming.", SHEET),
    "phantom": ("Phantom", ["ghost", "dark"], "shadowball", "Frayed Cord", ("minecraft:phantom_membrane", "minecraft:purple_dye"),
                "A Rotom that slipped out of its appliance and swelled into a shadow. Only its plug is left to show "
                "what it was.", SHEET),
    "mixer": ("Mixer", ["electric", "fighting"], "focusblast", "Mixer Whisk", ("minecraft:sugar", "minecraft:egg"),
              "It whips cream and beats eggs with startling force. Its whisks have punched holes in kitchen walls.", SHEET),
    "keytar": ("Keytar", ["electric", "normal"], "boomburst", "Keytar Strap", ("minecraft:note_block", "minecraft:purple_dye"),
               "It plays power chords at deafening volume. It never stops showing off.", SHEET),
    "disc": ("Disc", ["electric", "ice"], "icebeam", "Compact Disc", ("minecraft:jukebox", "minecraft:light_blue_dye"),
             "It spins its disc so fast the air around it chills. It only plays the songs it likes.", SHEET),
    "jet": ("Jet", ["electric", "flying"], "hurricane", "Jet Turbine", ("minecraft:firework_rocket", "minecraft:feather"),
            "It roars across the sky trailing flames. It dives at flocks of bird Pokémon just to scatter them.", SHEET),
    "spider": ("Spider", ["electric", "bug"], "pollenpuff", "Spider-Bot Core", ("minecraft:cobweb", "minecraft:spider_eye"),
               "A Rotom inside a robot spider. It spins wire webs in the corners of rooms and watches through its big "
               "lens eyes.", SHEET),
    "lighter": ("Lighter", ["electric", "fire"], "flamethrower", "Lighter Flint", ("minecraft:flint_and_steel", "minecraft:blaze_powder"),
                "It flicks its pink flame on and off to startle people. It lights campfires when it is in a good mood.", SHEET),
    "shredder": ("Shredder", ["electric", "dark"], "darkpulse", "Shredder Blade", ("minecraft:paper", "minecraft:iron_bars"),
                 "It shreds homework, letters and maps. Anything it eats is gone for good.", SHEET),
    "lamp": ("Lamp", ["electric", "fairy"], "dazzlinggleam", "Light Bulb", ("minecraft:lantern", "minecraft:glowstone_dust"),
             "It lights the way for lost travellers at night, then switches off just before they get home.", SHEET),
    "clock": ("Clock", ["electric", "dragon"], "roaroftime", "Clock Hand", ("minecraft:clock", "minecraft:white_concrete"),
              "It spins its hands back and forth and makes the people who watch it lose track of time.", SHEET),
    "ereader": ("E-Reader", ["electric", "psychic"], "psyshock", "E-Ink Screen", ("minecraft:book", "minecraft:glass_pane"),
                "It reads every book it can find, up to chapter six, and then forgets them all and starts again.", SHEET),
    "curler": ("Curler", ["electric", "fairy"], "drainingkiss", "Curling Wand", ("minecraft:blaze_rod", "minecraft:pink_dye"),
               "It curls the fur of any Pokémon that sits still. Its spiral eyes make onlookers dizzy.", SHEET),
    "tonic": ("Tonic", ["electric", "poison"], "venoshock", "Tonic Cap", ("minecraft:glass_bottle", "minecraft:glistering_melon_slice"),
              "A Rotom inside a bottle of tonic. It flexes its plasma arm and offers a dose to anyone who looks tired.", SHEET),
    "invasion": ("Invasion", ["electric", "psychic"], "psychoboost", "Tripod Beacon", ("minecraft:ender_eye", "minecraft:chain"),
                 "A Rotom that slipped into a walker from beyond the sky. It strides over towns on its four long legs, "
                 "grinning, and nobody knows what it is looking for.", "Unknown-Dan's art (@unknown__dan)"),
}


def title(key):
    """The form's display name: "Drill Rotom", but "Rotom Boy" (already has Rotom in it)."""
    name = FORMS[key][0]
    return name if "Rotom" in name else f"{name} Rotom"


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def module(key):
    import build  # noqa: F401  (puts the box-model toolkit on sys.path)
    f = HERE / "models" / f"rotom_{key}.py"
    if not f.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"rotomform_{key}", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def built():
    """The forms with a model so far, in FORMS order."""
    return [k for k in FORMS if (HERE / "models" / f"rotom_{k}.py").exists()]


def cmd(key):
    return CMD_BASE + CMD0 + list(FORMS).index(key)


def components(key):
    name = FORMS[key][3]
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.rotom_{key}", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.rotom_{key}.tooltip", "color": "gray", "italic": False})],
        "minecraft:custom_model_data": cmd(key),
        "minecraft:rarity": "rare",
        "minecraft:max_stack_size": 1,
        "minecraft:custom_data": {"cobbleeffort_item": f"rotom_{key}"},
        "mega_showdown:registry_type_component": "form_change_interact",
        "mega_showdown:registry_location_component": f"{MOD}:rotom_{key}",
    } if name else {}


def stacks():
    return [{"id": BASE_ITEM, "count": 1, "components": components(k)} for k in built()]


def overrides():
    """Echo-shard model overrides (custom_model_data ascending; fossils.build puts them after its own)."""
    return [{"predicate": {"custom_model_data": cmd(k)}, "model": f"{MOD}:item/rotom_{k}"} for k in built()]


def showdown_moves(cob):
    z = zipfile.ZipFile(cob / "data" / "cobblemon" / "showdown.zip")
    src = z.read("data/moves.js").decode()
    return set(re.findall(r"^\s{1,4}([a-z0-9]+): \{", src, re.M))


def base_layer_names(cob):
    import regional
    names = set(regional.base_layer_names(cob, "rotom", "0479_rotom"))
    for f in (RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers").rglob("*rotom*.json"):   # our cosmetics'
        if f.parent.name == "rotom":
            continue
        for v in json.loads(f.read_text()).get("variations", []):
            names |= {l["name"] for l in v.get("layers", [])}
    return sorted(names - {"cobbleeffort_glow", "cobbleeffort_shell"})


def recipe(key):
    t, f = FORMS[key][4]
    ing = lambda i: {"tag": i[1:]} if i.startswith("#") else {"item": i}
    return {"fabric:load_conditions": [{"condition": "fabric:all_mods_loaded", "values": ["mega_showdown"]}],
            "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "mega_showdown"}],
            "type": "minecraft:crafting_shaped", "category": "misc", "pattern": [" T ", "FCF", " T "],
            "key": {"T": ing(t), "F": ing(f), "C": {"item": "cobblemon:cell_battery"}},
            "result": {"id": BASE_ITEM, "count": 1, "components": components(key)}}


def form_change(key):
    a = f"{key}-appliance"
    return {"pokemons": ["Rotom"], "effect": MSD_EFFECT, "consume": 0,
            "aspect_conditions": {"apply": {"aspects": [f"appliance={key}"], "aspect": {"blacklist_aspects": [[a]]}},
                                  "revert": {"aspects": ["appliance=none"], "aspect": {"required_aspects": [[a]]}}}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cobblemon", type=Path, required=True)
    cob = ap.parse_args().cobblemon
    import build as nb
    nb.RES = RES
    species = json.loads((cob / "data" / "cobblemon" / "species" / "generation4" / "rotom.json").read_text())
    heat = species["forms"][0]
    moves_ok = showdown_moves(cob)
    base_moves = [m for m in heat["moves"] if not m.startswith("form_change:")]
    off = [{"name": n, "enabled": False} for n in base_layer_names(cob)]
    lang_path = RES / "assets" / MOD / "lang" / "en_us.json"
    lang = json.loads(lang_path.read_text())
    forms, variations, manifest = [], [], []
    data = RES / "data" / MOD
    keys = built()
    for key in keys:
        name, types, move, item, rec, entry, credit = FORMS[key]
        if move not in moves_ok:
            raise SystemExit(f"rotom {key}: unknown move {move}")
        hand = module(key)
        r = nb.write_model_assets(f"rotom_{key}", hand, "rotom")
        f = {"name": name.replace(" ", "").replace("-", ""), "primaryType": types[0], "aspects": [f"{key}-appliance"],
             "labels": ["gen4", "cobbleeffort_rotom"], "abilities": ["levitate", "h:levitate"],
             "baseStats": heat["baseStats"], "maleRatio": -1, "height": max(1, round(hand.SCALE * hand.HITBOX[1] * 10)),
             "weight": heat["weight"], "baseExperienceYield": heat["baseExperienceYield"],
             "moves": base_moves + [f"form_change:{move}"], "pokedex": [f"{MOD}.species.rotom-{key}.desc"],
             "baseScale": hand.SCALE, "hitbox": {"width": hand.HITBOX[0], "height": hand.HITBOX[1], "fixed": False},
             "evolutions": [], "battleOnly": False, "behaviour": heat["behaviour"] | {"fireImmune": "fire" in types}}
        if len(types) > 1:
            f["secondaryType"] = types[1]
        forms.append(f)
        tex = r["tex"]
        variations += [{"aspects": [f"{key}-appliance"], "poser": f"{MOD}:rotom_{key}", "model": f"{MOD}:rotom_{key}.geo",
                        "texture": tex(f"rotom_{key}"), "layers": off + r["layers"][""]},
                       {"aspects": [f"{key}-appliance", "shiny"], "texture": tex(f"rotom_{key}_shiny"),
                        "layers": off + r["layers"]["_shiny"]}]
        write_json(data / "mega_showdown" / "form_change_interact" / f"rotom_{key}.json", form_change(key))
        write_json(data / "recipe" / f"rotom_{key}.json", recipe(key))
        write_json(RES / "assets" / MOD / "models" / "item" / f"rotom_{key}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/rotom_{key}"}})
        lang[f"item.{MOD}.rotom_{key}"] = item
        lang[f"item.{MOD}.rotom_{key}.tooltip"] = (f"Use it on your Rotom to turn it into {title(key)} "
                                                   f"({' / '.join(t.title() for t in types)}); use it again to change back.")
        lang[f"{MOD}.species.rotom-{key}.desc"] = entry
        write_json(TOOLS / "readme" / f"_new_rotom_{key}.json", {
            "dex": 479, "name": f"{title(key)} (CobbleEffort form)", "types": " / ".join(t.title() for t in types),
            "ability": "Levitate", "look": hand.LOOK, "entry": entry,
            "how": [f"Use a {item} on your Rotom (craft it round a Cell Battery; needs Mega Showdown); its Rotom "
                    f"Catalogue cycles through this form too. Learns {move_name(move)} in this form."],
            "stats": [heat["baseStats"][s] for s in ("hp", "attack", "defence", "special_attack", "special_defence", "speed")]})
        names = {l["name"] for l in r["layers"][""]}       # the preview's layers: glow and the translucent shell
        man_layers = ([{"original": None, "emissive": True, "retextured": tex(f"rotom_{key}_glow_0")}]
                      if "cobbleeffort_glow" in names else []) + \
                     ([{"original": None, "emissive": False, "retextured": tex(f"rotom_{key}_shell")}]
                      if "cobbleeffort_shell" in names else [])
        manifest.append({"species": f"rotom_{key}", "folder": "rotom", "model": f"{MOD}:rotom_{key}.geo", "original": None,
                         "retextured": tex(f"rotom_{key}"), "layers": man_layers, "translucent": "cobbleeffort_shell" in names})
    write_json(data / "species_additions" / "rotom_forms.json", {"target": "cobblemon:rotom", "forms": forms})
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / "rotom" / "rotom_forms.json",
               {"species": "cobblemon:rotom", "order": ORDER, "variations": variations})
    import rotom_icons
    rotom_icons.write_all(RES / "assets" / MOD / "textures" / "item", keys)
    lang_path.write_text(json.dumps(lang, indent=2, ensure_ascii=False) + "\n")
    write_json(TOOLS / "preview" / "manifest_rotom.json", manifest)
    print(f"rotom forms: {len(keys)} ({', '.join(keys)})")


def move_name(m):
    special = {"steelbeam": "Steel Beam", "dracometeor": "Draco Meteor", "powergem": "Power Gem", "bugbuzz": "Bug Buzz",
               "energyball": "Energy Ball", "aurasphere": "Aura Sphere", "flashcannon": "Flash Cannon", "zapcannon": "Zap Cannon",
               "futuresight": "Future Sight", "nightdaze": "Night Daze", "sludgebomb": "Sludge Bomb", "fireblast": "Fire Blast",
               "earthpower": "Earth Power", "hypervoice": "Hyper Voice", "mirrorshot": "Mirror Shot", "shadowball": "Shadow Ball",
               "focusblast": "Focus Blast", "icebeam": "Ice Beam", "pollenpuff": "Pollen Puff", "darkpulse": "Dark Pulse",
               "dazzlinggleam": "Dazzling Gleam", "roaroftime": "Roar of Time", "drainingkiss": "Draining Kiss",
               "psychoboost": "Psycho Boost"}
    return special.get(m, m.title())


if __name__ == "__main__":
    main()
