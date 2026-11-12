#!/usr/bin/env python3
"""
CobbleEffort's own Pokémon: original species designed by the user (idea and look) and finished here (names, Pokédex
entries, stats, moves, models). Each model is hand-built from boxes in Cobblemon's style
(tools/newmons/models/<species>.py on tools/megas/_boxmodel.py, shared rig tools/megas/_rig.py).

Everything is in the cobbleeffort namespace (species cobbleeffort:<name>, Showdown id cobbleeffort<name>):

  data/cobbleeffort/species/<line>/<name>.json                 the species (implemented, evolutions, moves, drops)
  data/cobbleeffort/spawn_pool_world/<name>.json               where it spawns
  data/cobbleeffort/dex_entries/pokemon/<name>.json            its Pokédex entry
  data/cobbleeffort/dexes/cobbleeffort.json                    the CobbleEffort Pokédex (a sub-dex)...
  data/cobbleeffort/dex_additions/national.json                ...added to the National Pokédex
  assets/cobbleeffort/... model, textures, animations, poser, resolver (order 0)
  assets/cobbleeffort/lang/en_us.json                          names and Pokédex text

National Pokédex numbers start at 3001 (nothing in the mod stack uses 3000-3999).

Usage: python3 tools/newmons/build.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(HERE / "models"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(TOOLS / "megas"))
sys.path.insert(0, str(TOOLS / "models"))
from _anim import write_json  # noqa: E402
from _rig import animations, poser  # noqa: E402

ROOT = TOOLS.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"


def stats(hp, atk, de, spa, spd, spe):
    return {"hp": hp, "attack": atk, "defence": de, "special_attack": spa, "special_defence": spd, "speed": spe}


def evs(**kw):
    return {k: kw.get(k, 0) for k in ("hp", "attack", "defence", "special_attack", "special_defence", "speed")}


def spawn(sid, bucket, level, weight, condition, anticondition=None, position="grounded"):
    s = {"id": sid, "pokemon": None, "presets": ["natural"], "type": "pokemon", "spawnablePositionType": position,
         "bucket": bucket, "level": level, "weight": weight, "condition": condition}
    if anticondition:
        s["anticondition"] = anticondition
    return s


UNDERGROUND = {"minSkyLight": 0, "maxSkyLight": 7}

# --- the dentistry line --------------------------------------------------------------------------------------------

DENTAL_TM = ["crunch", "thief", "protect", "rest", "substitute", "facade", "snarl", "darkpulse", "irondefense",
             "ironhead", "psychicfangs", "firefang", "icefang", "thunderfang", "poisonfang", "knockoff", "foulplay",
             "taunt", "torment", "endure", "sleeptalk", "snore", "stealthrock", "spikes", "rockslide", "rocktomb",
             "payback", "screech", "bulldoze", "terablast", "swagger", "toxic", "round"]
DENTAL_TM_STEEL = ["heavyslam", "gyroball", "metalsound", "flashcannon", "bodypress", "steelroller"]
DENTAL_TM_FINAL = ["gigaimpact", "hyperbeam", "steelbeam", "throatchop", "earthquake"]
DENTAL_EGG = ["suckerpunch", "curse", "feint", "pursuit", "counter", "hyperfang"]
DENTAL_EARLY = [(1, "tackle"), (1, "leer"), (5, "bite"), (9, "scaryface"), (12, "snarl"), (15, "poisonfang"),
                (18, "assurance"), (21, "payback")]

SPECIES = {
    "cavitot": {
        "dex": 3001, "name": "Cavitot", "line": "dentistry", "types": ["dark"],
        "abilities": ["strongjaw", "stench", "h:stakeout"], "ability_names": "Strong Jaw / Stench / Stakeout (hidden)",
        "stats": stats(50, 65, 60, 30, 45, 50), "ev": evs(attack=1), "catch": 190, "exp": 58, "friendship": 50,
        "height": 7, "weight": 185, "shoulder": True, "walk": 0.2, "egg_groups": ["mineral"],
        "moves": DENTAL_EARLY + [(25, "crunch"), (29, "jawlock"), (33, "lashout"), (37, "superfang"), (41, "hyperfang")],
        "tm": DENTAL_TM, "egg": DENTAL_EGG,
        "evolve": ("amalgum", 24, ["metalclaw"]),
        "drops": [("minecraft:bone_meal", "1-2", None), ("minecraft:sugar", "0-1", None),
                  ("cobblemon:razor_fang", None, 2.5), ("cobblemon:black_glasses", None, 2.5)],
        "entry": ("It started out as a baby tooth that was never brushed. The cavity in its crown aches all the time, "
                  "which is why it always looks so grumpy. It can't resist sweets, even though they make the ache "
                  "worse."),
        "spawns": [
            spawn("cavitot-sweet", "common", "4-20", 6.0,
                  {"canSeeSky": True, "biomes": ["#cobblemon:is_overworld"], "neededNearbyBlocks": ["minecraft:sugar_cane"]}),
            spawn("cavitot-caves", "common", "6-22", 9.0, dict(UNDERGROUND, biomes=["minecraft:dripstone_caves"])),
            spawn("cavitot-underground", "uncommon", "6-22", 3.0, dict(UNDERGROUND, biomes=["#cobblemon:is_overworld"])),
            spawn("cavitot-village", "uncommon", "5-18", 6.0,
                  {"timeRange": "night", "biomes": ["#cobblemon:is_overworld"], "structures": ["#minecraft:village"]}),
        ],
        "how": ["Wild: common near sugar cane (sugar rots teeth) and in Dripstone Caves, uncommon underground and in "
                "villages at night.", "Evolves into Amalgum at level 24."],
    },
    "amalgum": {
        "dex": 3002, "name": "Amalgum", "line": "dentistry", "types": ["dark", "steel"],
        "abilities": ["strongjaw", "sturdy", "h:stakeout"], "ability_names": "Strong Jaw / Sturdy / Stakeout (hidden)",
        "stats": stats(65, 85, 95, 40, 60, 55), "ev": evs(defence=2), "catch": 90, "exp": 144, "friendship": 50,
        "height": 11, "weight": 724, "shoulder": False, "walk": 0.25, "egg_groups": ["mineral"],
        "moves": [(1, "metalclaw"), (1, "irondefense")] + DENTAL_EARLY +
                 [(27, "crunch"), (31, "jawlock"), (35, "ironhead"), (39, "lashout"), (43, "superfang"), (47, "metalburst")],
        "tm": DENTAL_TM + DENTAL_TM_STEEL, "egg": DENTAL_EGG,
        "evolve": ("orthodread", 42, ["spikyshield"]),
        "drops": [("minecraft:bone_meal", "1-2", None), ("minecraft:iron_nugget", "1-4", None),
                  ("cobblemon:metal_coat", None, 2.5), ("cobblemon:razor_fang", None, 2.5)],
        "entry": ("Three Cavitot that had their cavities filled and fused into one. The metal in their fillings makes "
                  "it tough to crack, but all three of its faces still frown. It gnaws on iron ore to keep its caps "
                  "shiny."),
        "spawns": [
            spawn("amalgum-caves", "uncommon", "24-40", 4.0, dict(UNDERGROUND, biomes=["minecraft:dripstone_caves"])),
            spawn("amalgum-deep", "rare", "26-42", 3.0, dict(UNDERGROUND, biomes=["#cobblemon:is_deep_dark"])),
        ],
        "how": ["Evolve Cavitot at level 24.", "Wild: uncommon in Dripstone Caves, rare in the Deep Dark."],
    },
    "orthodread": {
        "dex": 3003, "name": "Orthodread", "line": "dentistry", "types": ["dark", "steel"],
        "abilities": ["strongjaw", "ironbarbs", "h:stakeout"], "ability_names": "Strong Jaw / Iron Barbs / Stakeout (hidden)",
        "stats": stats(85, 120, 120, 50, 80, 70), "ev": evs(attack=2, defence=1), "catch": 45, "exp": 250,
        "friendship": 50, "height": 18, "weight": 2050, "shoulder": False, "walk": 0.35, "egg_groups": ["mineral"],
        "moves": [(1, "metalclaw"), (1, "irondefense"), (1, "spikyshield")] + DENTAL_EARLY +
                 [(27, "crunch"), (31, "jawlock"), (35, "ironhead"), (39, "lashout"), (42, "spikyshield"),
                  (46, "superfang"), (50, "heavyslam"), (55, "metalburst"), (60, "throatchop")],
        "tm": DENTAL_TM + DENTAL_TM_STEEL + DENTAL_TM_FINAL, "egg": DENTAL_EGG,
        "evolve": None,
        "drops": [("minecraft:bone_meal", "1-3", None), ("minecraft:iron_ingot", "1-2", None),
                  ("cobblemon:metal_coat", None, 5.0), ("cobblemon:razor_fang", None, 5.0)],
        "entry": ("Eight teeth held together by braces it can never take off. It scuttles through dark caves on its "
                  "steel legs and its bite can crunch through iron. The braces put it in a foul mood, and it takes "
                  "that out on anyone it meets."),
        "spawns": [
            spawn("orthodread-deep", "ultra-rare", "42-60", 2.0, dict(UNDERGROUND, biomes=["#cobblemon:is_deep_dark"])),
            spawn("orthodread-caves", "ultra-rare", "42-60", 1.0, dict(UNDERGROUND, biomes=["minecraft:dripstone_caves"])),
        ],
        "how": ["Evolve Amalgum at level 42.", "Wild: very rare in the Deep Dark and Dripstone Caves."],
    },
}
LINES = {"dentistry": ["cavitot", "amalgum", "orthodread"]}

# --- the coal butterfly line (the CobbleEffort starter) --------------------------------------------------------------

COAL_TM = ["protect", "rest", "substitute", "facade", "sleeptalk", "snore", "endure", "flamecharge", "flamethrower",
           "fireblast", "willowisp", "sunnyday", "overheat", "heatwave", "bugbuzz", "uturn", "strugglebug", "pounce",
           "lunge", "terablast", "temperflare", "scaryface", "stringshot", "bugbite", "firefang", "solarbeam",
           "round", "swagger", "toxic", "dig"]
COAL_TM_COCOON = ["irondefense", "harden", "bodypress"]
COAL_TM_FINAL = ["xscissor", "tailwind", "airslash", "acrobatics", "gigaimpact", "hyperbeam", "rockblast", "flareblitz",
                 "skittersmack", "leechlife", "dualwingbeat", "hurricane"]
COAL_EGG = ["firstimpression", "stickyweb", "firespin", "morningsun", "infestation", "megahorn"]
COAL_EARLY = [(1, "tackle"), (1, "stringshot"), (4, "ember"), (8, "bugbite"), (12, "smokescreen"), (15, "flamecharge")]
STARTER = dict(male=0.875, egg_groups=["bug"], catch=45, friendship=50, abilities=["blaze", "h:skilllink"],
               ability_names="Blaze / Skill Link (hidden)")

SPECIES.update({
    "coalarva": {
        "dex": 3004, "name": "Coalarva", "line": "coal_butterfly", "types": ["fire", "bug"], **STARTER,
        "stats": stats(45, 55, 50, 49, 50, 60), "ev": evs(speed=1), "exp": 62,
        "height": 4, "weight": 120, "shoulder": True, "walk": 0.22,
        "moves": COAL_EARLY + [(19, "firefang"), (23, "strugglebug"), (27, "incinerate"), (31, "lunge"),
                               (36, "firespin"), (40, "flareblitz")],
        "tm": COAL_TM, "egg": COAL_EGG,
        "evolve": ("cinderoon", 16, ["harden"]),
        "drops": [("minecraft:coal", "1-2", None), ("minecraft:charcoal", "0-1", None), ("cobblemon:charcoal_stick", None, 5.0)],
        "entry": ("It lives in caves deep underground where coal seams run thick, and it eats nothing but coal. A "
                  "special organ in its abdomen turns the minerals it swallows into heat, which is why its tail end "
                  "always glows."),
        "spawns": [
            spawn("coalarva-coal", "ultra-rare", "5-15", 1.0,
                  dict(UNDERGROUND, biomes=["#cobblemon:is_overworld"], neededNearbyBlocks=["#minecraft:coal_ores"])),
        ],
        "how": ["The CobbleEffort starter: pick it at the starter screen (its own CobbleEffort page, after Cobblemon's "
                "regions).", "Wild: very rare underground next to coal ore.", "Evolves into Cinderoon at level 16."],
    },
    "cinderoon": {
        "dex": 3005, "name": "Cinderoon", "line": "coal_butterfly", "types": ["fire", "bug"], **STARTER,
        "stats": stats(60, 45, 95, 60, 85, 60), "ev": evs(defence=2), "exp": 142,
        "height": 10, "weight": 385, "shoulder": False, "walk": 0.12,
        "moves": [(1, "harden")] + COAL_EARLY + [(16, "harden"), (20, "incinerate"), (24, "irondefense"),
                                                (28, "firespin"), (32, "lunge"), (35, "burningbulwark")],
        "tm": COAL_TM + COAL_TM_COCOON, "egg": COAL_EGG,
        "evolve": ("gatterfly", 36, ["machinegunstinger"]),
        "drops": [("minecraft:coal", "1-3", None), ("minecraft:charcoal", "1-2", None), ("cobblemon:charcoal_stick", None, 10.0)],
        "entry": ("Once it has eaten enough coal, it wraps its soft body in a cocoon of cinders. The ash is thin enough "
                  "to see the Coalarva curled up inside, and it can burn some of it away to hurl a blast of fire at "
                  "anything that disturbs it."),
        "spawns": [],
        "how": ["Evolve Coalarva at level 16."],
    },
    "gatterfly": {
        "dex": 3006, "name": "Gatterfly", "line": "coal_butterfly", "types": ["fire", "bug"], **STARTER,
        "stats": stats(78, 115, 80, 104, 75, 82), "ev": evs(attack=3), "exp": 265,
        "height": 17, "weight": 1250, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": [(1, "machinegunstinger"), (1, "harden")] + COAL_EARLY +
                 [(16, "harden"), (20, "incinerate"), (24, "irondefense"), (28, "firespin"), (32, "lunge"),
                  (36, "machinegunstinger"), (40, "flamethrower"), (44, "uturn"), (48, "heatwave"),
                  (52, "quiverdance"), (56, "flareblitz"), (62, "megahorn")],
        "tm": COAL_TM + COAL_TM_COCOON + COAL_TM_FINAL, "egg": COAL_EGG,
        "evolve": None,
        "drops": [("minecraft:coal", "2-4", None), ("minecraft:blaze_powder", "0-2", None),
                  ("cobblemon:charcoal_stick", None, 15.0)],
        "entry": ("Its arms have become guns that spray stingers so fast and so hot they glow, and its wings are made "
                  "of fire. Besides fighting with them, it melts stone with its flames to build its nest."),
        "spawns": [],
        "how": ["Evolve Cinderoon at level 36. Learns its own move, Machine Gun Stinger, when it evolves."],
    },
})
LINES["coal_butterfly"] = ["coalarva", "cinderoon", "gatterfly"]

# --- the mantis line ------------------------------------------------------------------------------------------------

MANTIS_TM = ["protect", "rest", "substitute", "facade", "sleeptalk", "snore", "endure", "swordsdance", "xscissor",
             "leafblade", "seedbomb", "bulletseed", "energyball", "gigadrain", "grassknot", "trailblaze", "bugbuzz",
             "uturn", "lunge", "pounce", "falseswipe", "focusenergy", "agility", "brickbreak", "aerialace", "nightslash",
             "knockoff", "terablast", "sunnyday", "leechlife", "skittersmack", "magicalleaf", "round", "toxic"]
MANTIS_TM_MAW = ["crunch", "poisonjab", "throatchop", "firstimpression", "solarblade", "leafstorm", "closecombat"]
MANTIS_TM_GHOST = ["shadowball", "shadowclaw", "phantomforce", "poltergeist", "hex", "willowisp", "focusblast",
                   "gigaimpact", "hyperbeam", "earthquake", "spite", "nightshade"]
MANTIS_EGG = ["hypnosis", "feint", "quickguard", "leechseed", "defog", "dynamicpunch"]
MANTIS_EARLY = [(1, "leer"), (1, "furycutter"), (4, "absorb"), (7, "quickattack"), (10, "razorleaf"),
                (13, "bugbite"), (16, "grasswhistle"), (19, "falseswipe")]
MANTIS = dict(male=0.5, egg_groups=["bug", "grass"], friendship=50, abilities=["blindsight", "h:sniper"],
              ability_names="Blindsight (its own: every move it uses hits) / Sniper (hidden)")

SPECIES.update({
    "prayling": {
        "dex": 3007, "name": "Prayling", "line": "mantis", "types": ["grass", "bug"], **MANTIS,
        "stats": stats(45, 60, 40, 35, 40, 55), "ev": evs(attack=1), "catch": 190, "exp": 55,
        "height": 4, "weight": 22, "shoulder": True, "walk": 0.25,
        "moves": MANTIS_EARLY + [(22, "megadrain"), (25, "xscissor"), (28, "slash"), (31, "leafblade"),
                                 (35, "swordsdance"), (40, "powerwhip"), (45, "megahorn")],
        "tm": MANTIS_TM, "egg": MANTIS_EGG,
        "evolve": ("mawntis", 22, ["crunch"]),
        "drops": [("minecraft:wheat_seeds", "0-2", None), ("minecraft:oak_leaves", "0-1", None),
                  ("cobblemon:miracle_seed", None, 2.5)],
        "entry": ("It is born without eyes, yet it never misses. It feels the faintest stir of air through its leafy "
                  "feelers and knows exactly where its prey is, then holds its little forelegs together and waits."),
        "spawns": [
            spawn("prayling-jungle", "common", "3-18", 8.0, {"canSeeSky": True, "biomes": ["#cobblemon:is_jungle"]}),
            spawn("prayling-flowers", "uncommon", "3-18", 5.0, {"canSeeSky": True, "biomes": ["minecraft:flower_forest", "minecraft:meadow"]}),
            spawn("prayling-forest", "uncommon", "3-18", 2.0, {"canSeeSky": True, "biomes": ["#cobblemon:is_forest"]}),
        ],
        "how": ["Wild: common in jungles, uncommon in flower forests, meadows and forests.", "Evolves into Mawntis at level 22."],
    },
    "mawntis": {
        "dex": 3008, "name": "Mawntis", "line": "mantis", "types": ["grass", "bug"], **MANTIS,
        "stats": stats(65, 95, 65, 45, 60, 80), "ev": evs(attack=2), "catch": 90, "exp": 147,
        "height": 11, "weight": 380, "shoulder": False, "walk": 0.32,
        "moves": [(1, "crunch")] + MANTIS_EARLY +
                 [(22, "crunch"), (25, "xscissor"), (29, "nightslash"), (33, "leafblade"), (37, "swordsdance"),
                  (41, "powerwhip"), (46, "megahorn"), (51, "firstimpression")],
        "tm": MANTIS_TM + MANTIS_TM_MAW, "egg": MANTIS_EGG,
        "evolve": ("mantasma", 40, ["poltergeist"], [{"variant": "time_range", "range": "night"}]),
        "drops": [("minecraft:wheat_seeds", "1-3", None), ("minecraft:bone", "0-1", None), ("cobblemon:miracle_seed", None, 5.0)],
        "entry": ("Its head has split into a maw full of fangs, and a second set of legs lets it run down prey in "
                  "the undergrowth. It still has no eyes, but its scythes find their mark every time."),
        "spawns": [spawn("mawntis-jungle", "rare", "22-38", 3.0, {"canSeeSky": True, "biomes": ["#cobblemon:is_jungle"]})],
        "how": ["Evolve Prayling at level 22.", "Wild: rare in jungles."],
    },
    "mantasma": {
        "dex": 3009, "name": "Mantasma", "line": "mantis", "types": ["grass", "ghost"], **MANTIS,
        "stats": stats(90, 130, 90, 70, 85, 75), "ev": evs(attack=3), "catch": 45, "exp": 270,
        "height": 35, "weight": 2100, "shoulder": False, "walk": 0.3,
        "moves": [(1, "poltergeist"), (1, "crunch")] + MANTIS_EARLY +
                 [(22, "crunch"), (25, "xscissor"), (29, "nightslash"), (33, "leafblade"), (37, "swordsdance"),
                  (40, "poltergeist"), (44, "shadowclaw"), (48, "powerwhip"), (52, "megahorn"), (56, "phantomforce"),
                  (60, "dynamicpunch"), (64, "hypnosis"), (70, "guillotine")],
        "tm": MANTIS_TM + MANTIS_TM_MAW + MANTIS_TM_GHOST, "egg": MANTIS_EGG,
        "evolve": None,
        "drops": [("minecraft:bone", "1-3", None), ("minecraft:phantom_membrane", "0-1", None),
                  ("cobblemon:spell_tag", None, 5.0), ("cobblemon:miracle_seed", None, 5.0)],
        "entry": ("A Mawntis that hunted on a moonless night and came back as something else. It towers over the "
                  "trees, its grin glows in the dark, and its ghostly scythes cut through anything without ever "
                  "missing. Even so, it still clasps its forelegs together the way it did as a Prayling."),
        "spawns": [spawn("mantasma-night", "ultra-rare", "40-60", 1.0,
                         {"canSeeSky": True, "timeRange": "night", "biomes": ["minecraft:dark_forest", "#cobblemon:is_jungle"]})],
        "how": ["Evolve Mawntis at level 40 or higher at night.", "Wild: very rare in dark forests and jungles at night."],
    },
})
LINES["mantis"] = ["prayling", "mawntis", "mantasma"]

# --- the mummy line (the CobbleEffort water starter) ----------------------------------------------------------------

MUMMY_TM = ["protect", "rest", "substitute", "facade", "sleeptalk", "snore", "endure", "waterpulse", "surf",
            "hydropump", "raindance", "scald", "chillingwater", "liquidation", "bugbuzz", "uturn", "strugglebug",
            "pounce", "lunge", "terablast", "stringshot", "bugbite", "icebeam", "blizzard", "icywind", "shadowball",
            "hex", "curse", "round", "toxic", "sandstorm", "brine"]
MUMMY_TM_COCOON = ["irondefense", "harden", "bodypress"]
MUMMY_TM_FINAL = ["xscissor", "swordsdance", "aquacutter", "leafblade", "nightslash", "aerialace", "agility",
                  "gigaimpact", "hyperbeam", "wavecrash", "leechlife", "focusenergy", "psychocut"]
MUMMY_EGG = ["destinybond", "aquaring", "stickyweb", "mirrorcoat", "haze", "infestation"]
MUMMY_EARLY = [(1, "tackle"), (1, "stringshot"), (4, "watergun"), (8, "bugbite"), (11, "curse"), (14, "bubblebeam")]
MUMMY = dict(male=0.875, egg_groups=["bug", "water_1"], catch=45, friendship=50, abilities=["pharaohscurse", "h:torrent"],
             ability_names="Pharaoh's Curse (its own: once per battle, survives a knockout at half health with +2 Attack "
                           "and Sp. Atk) / Torrent (hidden)")

SPECIES.update({
    "mumpillar": {
        "dex": 3010, "name": "Mumpillar", "line": "mummy", "types": ["water", "bug"], **MUMMY,
        "stats": stats(50, 52, 48, 52, 57, 50), "ev": evs(special_defence=1), "exp": 62,
        "height": 4, "weight": 95, "shoulder": True, "walk": 0.2,
        "moves": MUMMY_EARLY + [(18, "waterpulse"), (22, "strugglebug"), (26, "hex"), (30, "aquatail"),
                                (34, "lunge"), (38, "hydropump")],
        "tm": MUMMY_TM, "egg": MUMMY_EGG,
        "evolve": ("sarcoon", 16, ["harden"]),
        "drops": [("minecraft:string", "1-2", None), ("minecraft:paper", "0-1", None), ("cobblemon:mystic_water", None, 5.0)],
        "entry": ("It wraps itself in strips of silk soaked in river water and never takes them off. Old tales say "
                  "anyone who unwraps one is cursed, and that it cannot be finished off: struck down, it rises again "
                  "angrier than before."),
        "spawns": [
            spawn("mumpillar-oasis", "ultra-rare", "5-15", 1.0,
                  {"canSeeSky": True, "biomes": ["#cobblemon:is_desert"], "neededNearbyBlocks": ["minecraft:water"]}),
        ],
        "how": ["A CobbleEffort starter: pick it at the starter screen (the CobbleEffort page, with Coalarva).",
                "Wild: very rare in deserts next to water (an oasis).", "Evolves into Sarcoon at level 16."],
    },
    "sarcoon": {
        "dex": 3011, "name": "Sarcoon", "line": "mummy", "types": ["water", "bug"], **MUMMY,
        "stats": stats(65, 55, 100, 55, 90, 40), "ev": evs(defence=2), "exp": 142,
        "height": 10, "weight": 410, "shoulder": False, "walk": 0.1,
        "moves": [(1, "harden")] + MUMMY_EARLY + [(16, "harden"), (20, "aquaring"), (24, "irondefense"),
                                                 (28, "waterpulse"), (32, "hex"), (35, "lunge")],
        "tm": MUMMY_TM + MUMMY_TM_COCOON, "egg": MUMMY_EGG,
        "evolve": ("pharantis", 36, ["liquidation"]),
        "drops": [("minecraft:string", "1-3", None), ("minecraft:gold_nugget", "1-3", None), ("cobblemon:mystic_water", None, 10.0)],
        "entry": ("Its silk hardens into a coffin painted like a pharaoh's. It lies still for weeks, but anything "
                  "foolish enough to pry at the lid wakes the curse, and the case's eyes light up."),
        "spawns": [],
        "how": ["Evolve Mumpillar at level 16."],
    },
    "pharantis": {
        "dex": 3012, "name": "Pharantis", "line": "mummy", "types": ["water", "bug"], **MUMMY,
        "stats": stats(75, 110, 70, 100, 74, 105), "ev": evs(speed=3), "exp": 265,
        "height": 16, "weight": 620, "shoulder": False, "walk": 0.38,
        "moves": [(1, "liquidation"), (1, "harden")] + MUMMY_EARLY +
                 [(16, "harden"), (20, "aquaring"), (24, "irondefense"), (28, "waterpulse"), (32, "hex"),
                  (36, "liquidation"), (40, "aquacutter"), (44, "xscissor"), (48, "swordsdance"), (52, "uturn"),
                  (56, "wavecrash"), (62, "megahorn")],
        "tm": MUMMY_TM + MUMMY_TM_COCOON + MUMMY_TM_FINAL, "egg": MUMMY_EGG,
        "evolve": None,
        "drops": [("minecraft:gold_ingot", "0-2", None), ("minecraft:string", "1-3", None),
                  ("cobblemon:mystic_water", None, 15.0)],
        "entry": ("It rules the river valleys with a crook of gold at the end of each scythe, and moves so fast its "
                  "foes never see it strike. Those who think they have defeated it soon learn about the pharaoh's "
                  "curse."),
        "spawns": [],
        "how": ["Evolve Sarcoon at level 36. Learns Liquidation when it evolves."],
    },
})
LINES["mummy"] = ["mumpillar", "sarcoon", "pharantis"]

# --- route one: two bugs, two birds and a rodent ---------------------------------------------------------------------

BASIC_TM = ["protect", "rest", "substitute", "facade", "sleeptalk", "snore", "endure", "terablast", "round", "toxic"]
ROUTE = dict(friendship=70)
PLAINS = ["#cobblemon:is_plains", "#cobblemon:is_grassland"]


def route_spawn(sid, bucket, level, weight, biomes, **cond):
    return spawn(sid, bucket, level, weight, dict({"canSeeSky": True, "biomes": biomes}, **cond))


SPIDER_TM = BASIC_TM + ["bugbuzz", "uturn", "pounce", "lunge", "strugglebug", "stringshot", "bugbite", "energyball",
                        "gigadrain", "bulletseed", "seedbomb", "grassknot", "trailblaze", "sunnyday", "stickyweb",
                        "leechlife", "skittersmack", "infestation"]
SPIDER_EARLY = [(1, "tackle"), (1, "stringshot"), (5, "absorb"), (9, "bugbite"), (13, "leechseed"), (17, "bulletseed")]
KNIFE_TM = BASIC_TM + ["xscissor", "uturn", "bugbuzz", "aerialace", "steelwing", "ironhead", "flashcannon",
                       "swordsdance", "agility", "falseswipe", "knockoff", "nightslash", "psychocut", "smartstrike",
                       "pounce", "lunge", "bugbite", "strugglebug", "irondefense"]
KNIFE_TM_FLY = ["airslash", "aircutter", "tailwind", "acrobatics", "dualwingbeat", "steelbeam", "gigaimpact", "hyperbeam"]
CARD_TM = BASIC_TM + ["aerialace", "airslash", "acrobatics", "uturn", "dualwingbeat", "bravebird", "tailwind", "roost",
                      "defog", "fly", "steelwing", "dazzlinggleam", "drainingkiss", "playrough", "moonblast", "charm",
                      "mistyterrain", "swift"]
CARD_TM_HAWK = ["heatwave", "hurricane", "gigaimpact", "hyperbeam", "skyattack"]
DUCK_TM = BASIC_TM + ["surf", "waterpulse", "hydropump", "raindance", "scald", "chillingwater", "icebeam", "icywind",
                      "aerialace", "airslash", "acrobatics", "uturn", "fly", "roost", "defog", "tailwind", "bravebird",
                      "hypervoice", "bodyslam"]
DUCK_TM_GOOSE = ["liquidation", "wavecrash", "gigaimpact", "hyperbeam", "hurricane"]
RAT_TM = BASIC_TM + ["bulletseed", "seedbomb", "energyball", "gigadrain", "grassknot", "trailblaze", "solarbeam",
                     "sunnyday", "bodyslam", "crunch", "superfang", "dig", "thief", "uturn", "swagger", "irontail"]
RAT_TM_KING = ["gigaimpact", "hyperbeam", "leafstorm", "woodhammer"]

SPECIES.update({
    "pipider": {
        "dex": 3013, "name": "Pipider", "line": "route_one", "types": ["bug", "grass"], **ROUTE, "male": 0.5,
        "egg_groups": ["bug", "grass"], "abilities": ["shellarmor", "swarm", "h:seedsower"],
        "ability_names": "Shell Armor / Swarm / Seed Sower (hidden)",
        "stats": stats(40, 40, 50, 25, 35, 30), "ev": evs(defence=1), "catch": 255, "exp": 39,
        "height": 1, "weight": 2, "shoulder": True, "walk": 0.18,
        "moves": SPIDER_EARLY + [(21, "stickyweb"), (25, "megadrain")],
        "tm": SPIDER_TM, "egg": ["ragepowder", "worryseed", "synthesis", "firstimpression", "spiderweb"],
        "evolve": ("blanketula", 14, ["cottonguard"]),
        "drops": [("minecraft:wheat_seeds", "1-2", None), ("minecraft:string", "0-1", None)],
        "entry": ("One of the smallest Pokémon there is: it fits on a fingertip. It hides under a seed it found and "
                  "carries it everywhere like a shell, and when it is frightened it tucks its legs in and pretends to "
                  "be an ordinary seed."),
        "spawns": [route_spawn("pipider-plains", "common", "2-10", 9.0, PLAINS + ["#cobblemon:is_forest"])],
        "how": ["Wild: common in plains, grasslands and forests.", "Evolves into Blanketula at level 14."],
    },
    "blanketula": {
        "dex": 3014, "name": "Blanketula", "line": "route_one", "types": ["bug", "grass"], **ROUTE, "male": 0.5,
        "egg_groups": ["bug", "grass"], "abilities": ["shellarmor", "swarm", "h:seedsower"],
        "ability_names": "Shell Armor / Swarm / Seed Sower (hidden)",
        "stats": stats(65, 80, 75, 45, 70, 55), "ev": evs(defence=2), "catch": 120, "exp": 140,
        "height": 5, "weight": 85, "shoulder": False, "walk": 0.25,
        "moves": [(1, "cottonguard")] + SPIDER_EARLY + [(14, "cottonguard"), (20, "stickyweb"), (24, "megadrain"),
                                                     (28, "seedbomb"), (33, "lunge"), (38, "gigadrain"), (44, "leafblade")],
        "tm": SPIDER_TM + ["xscissor", "solarbeam", "poisonjab", "leafblade"],
        "egg": ["ragepowder", "worryseed", "synthesis", "firstimpression", "spiderweb"],
        "evolve": None,
        "drops": [("minecraft:string", "1-2", None), ("minecraft:oak_leaves", "0-1", None), ("cobblemon:miracle_seed", None, 2.5)],
        "entry": ("When it outgrows its seed it picks out a big leaf and never lets go of it again. It sleeps wrapped "
                  "up in it, hides under it when anything startles it, and grows very upset if the leaf is taken away."),
        "spawns": [route_spawn("blanketula-forest", "uncommon", "14-24", 3.0, ["#cobblemon:is_forest"])],
        "how": ["Evolve Pipider at level 14.", "Wild: uncommon in forests."],
    },
    "shivnymph": {
        "dex": 3015, "name": "Shivnymph", "line": "route_one", "types": ["bug", "steel"], **ROUTE, "male": 0.5,
        "egg_groups": ["bug"], "abilities": ["sharpness", "swarm", "h:speedboost"],
        "ability_names": "Sharpness / Swarm / Speed Boost (hidden)",
        "stats": stats(40, 50, 40, 20, 30, 45), "ev": evs(attack=1), "catch": 255, "exp": 39,
        "height": 3, "weight": 30, "shoulder": True, "walk": 0.22,
        "moves": [(1, "furycutter"), (1, "leer"), (4, "bugbite")],
        "tm": KNIFE_TM, "egg": ["quickguard", "feint", "defog", "pursuit"],
        "evolve": ("sheathalis", 7, ["harden"]),
        "drops": [("minecraft:iron_nugget", "1-2", None)],
        "entry": ("It hatches near water with a tiny blade already at the end of its tail. It keeps the edge sharp by "
                  "scraping it on river stones, and flicks it at anything that comes too close."),
        "spawns": [route_spawn("shivnymph-river", "common", "2-8", 8.0, ["#cobblemon:is_river", "#cobblemon:is_freshwater"] + PLAINS)],
        "how": ["Wild: common by rivers and in plains.", "Evolves into Sheathalis at level 7."],
    },
    "sheathalis": {
        "dex": 3016, "name": "Sheathalis", "line": "route_one", "types": ["bug", "steel"], **ROUTE, "male": 0.5,
        "egg_groups": ["bug"], "abilities": ["sharpness", "swarm", "h:speedboost"],
        "ability_names": "Sharpness / Swarm / Speed Boost (hidden)",
        "stats": stats(45, 35, 85, 25, 50, 25), "ev": evs(defence=2), "catch": 120, "exp": 72,
        "height": 6, "weight": 200, "shoulder": False, "walk": 0.08,
        "moves": [(1, "harden"), (1, "irondefense"), (1, "furycutter"), (1, "leer"), (4, "bugbite"), (7, "harden")],
        "tm": KNIFE_TM, "egg": ["quickguard", "feint", "defog", "pursuit"],
        "evolve": ("cutlassfly", 10, ["xscissor"]),
        "drops": [("minecraft:iron_nugget", "1-3", None), ("minecraft:stick", "1-2", None)],
        "entry": ("Its cocoon hardens into something like a block of wood with knife handles sticking out of it. The "
                  "blades inside are its new wings growing, and it peeks out of the front to keep watch."),
        "spawns": [route_spawn("sheathalis-river", "uncommon", "7-12", 3.0, ["#cobblemon:is_river"] + PLAINS)],
        "how": ["Evolve Shivnymph at level 7.", "Wild: uncommon by rivers and in plains."],
    },
    "cutlassfly": {
        "dex": 3017, "name": "Cutlassfly", "line": "route_one", "types": ["bug", "steel"], **ROUTE, "male": 0.5,
        "egg_groups": ["bug"], "abilities": ["sharpness", "swarm", "h:speedboost"],
        "ability_names": "Sharpness / Swarm / Speed Boost (hidden)",
        "stats": stats(70, 110, 80, 40, 60, 115), "ev": evs(attack=2, speed=1), "catch": 45, "exp": 178,
        "height": 16, "weight": 480, "shoulder": False, "walk": 0.35, "fly": True,
        "moves": [(1, "xscissor"), (1, "furycutter"), (1, "leer"), (1, "bugbite"), (1, "harden"), (10, "xscissor"),
                  (12, "metalclaw"), (15, "aerialace"), (18, "slash"), (22, "aircutter"), (26, "nightslash"),
                  (30, "swordsdance"), (34, "airslash"), (38, "agility"), (42, "smartstrike"), (46, "uturn"),
                  (52, "bugbuzz")],
        "tm": KNIFE_TM + KNIFE_TM_FLY, "egg": ["quickguard", "feint", "defog", "pursuit"],
        "evolve": None,
        "drops": [("minecraft:iron_ingot", "0-1", None), ("minecraft:iron_nugget", "2-4", None)],
        "entry": ("Its wings are blades sharp enough to slice falling leaves in two. It hovers perfectly still over "
                  "rivers, then darts away faster than the eye can follow, leaving cut reeds behind it."),
        "spawns": [route_spawn("cutlassfly-river", "rare", "15-30", 1.5, ["#cobblemon:is_river", "#cobblemon:is_swamp"])],
        "how": ["Evolve Sheathalis at level 10.", "Wild: rare by rivers and in swamps."],
    },
    "cardling": {
        "dex": 3018, "name": "Cardling", "line": "route_one", "types": ["fairy", "flying"], **ROUTE, "male": 0.5,
        "egg_groups": ["flying", "fairy"], "abilities": ["keeneye", "cutecharm", "h:pixilate"],
        "ability_names": "Keen Eye / Cute Charm / Pixilate (hidden)",
        "stats": stats(40, 40, 40, 45, 50, 60), "ev": evs(speed=1), "catch": 255, "exp": 50,
        "height": 3, "weight": 18, "shoulder": True, "walk": 0.25, "fly": True,
        "moves": [(1, "peck"), (1, "growl"), (4, "disarmingvoice"), (7, "quickattack"), (10, "fairywind"),
                  (13, "gust"), (16, "sweetkiss"), (19, "wingattack"), (24, "drainingkiss"), (28, "featherdance")],
        "tm": CARD_TM, "egg": ["mirrormove", "featherdance", "babydolleyes", "wish", "pursuit"],
        "evolve": ("rubraptor", 22, ["airslash"]),
        "drops": [("minecraft:feather", "1-2", None), ("minecraft:red_dye", "0-1", None)],
        "entry": ("It sings sweetly from the branches at dawn, and its song is said to bring good luck to anyone who "
                  "hears it first thing in the morning. It is tiny, round and fearless."),
        "spawns": [route_spawn("cardling-forest", "common", "2-12", 9.0, ["#cobblemon:is_forest"] + PLAINS)],
        "how": ["Wild: common in forests, plains and grasslands.", "Evolves into Rubraptor at level 22."],
    },
    "rubraptor": {
        "dex": 3019, "name": "Rubraptor", "line": "route_one", "types": ["fairy", "flying"], **ROUTE, "male": 0.5,
        "egg_groups": ["flying", "fairy"], "abilities": ["keeneye", "cutecharm", "h:pixilate"],
        "ability_names": "Keen Eye / Cute Charm / Pixilate (hidden)",
        "stats": stats(70, 80, 65, 85, 70, 95), "ev": evs(speed=2), "catch": 90, "exp": 170,
        "height": 11, "weight": 260, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": [(1, "airslash"), (1, "peck"), (1, "growl"), (4, "disarmingvoice"), (7, "quickattack"),
                  (10, "fairywind"), (13, "gust"), (16, "sweetkiss"), (19, "wingattack"), (22, "airslash"),
                  (25, "dazzlinggleam"), (29, "agility"), (33, "roost"), (37, "playrough"), (42, "bravebird"),
                  (47, "moonblast"), (52, "hurricane")],
        "tm": CARD_TM + CARD_TM_HAWK, "egg": ["mirrormove", "featherdance", "babydolleyes", "wish", "pursuit"],
        "evolve": None,
        "drops": [("minecraft:feather", "2-3", None), ("minecraft:red_dye", "1-2", None)],
        "entry": ("A proud hawk that guards its territory from the treetops. Its red wings flash like a warning as it "
                  "dives, yet it is gentle with Pokémon smaller than itself and shares its catch with them."),
        "spawns": [route_spawn("rubraptor-forest", "rare", "22-35", 1.5, ["#cobblemon:is_forest", "#cobblemon:is_hills"])],
        "how": ["Evolve Cardling at level 22.", "Wild: rare in forests and hills."],
    },
    "squeakling": {
        "dex": 3020, "name": "Squeakling", "line": "route_one", "types": ["water", "flying"], **ROUTE, "male": 0.5,
        "egg_groups": ["water_1", "flying"], "abilities": ["waterveil", "owntempo", "h:unaware"],
        "ability_names": "Water Veil / Own Tempo / Unaware (hidden)",
        "stats": stats(45, 35, 45, 40, 45, 45), "ev": evs(hp=1), "catch": 255, "exp": 52,
        "height": 2, "weight": 15, "shoulder": True, "walk": 0.2, "swims": True,
        "moves": [(1, "tackle"), (1, "watergun"), (4, "growl"), (7, "wingattack"), (10, "aquajet"), (14, "featherdance"),
                  (18, "bubblebeam"), (22, "airslash"), (26, "aquaring")],
        "tm": DUCK_TM, "egg": ["bellydrum", "soak", "aquaring", "mirrorcoat", "brine"],
        "evolve": ("elastigoose", 25, ["uproar"]),
        "drops": [("minecraft:feather", "0-1", None), ("minecraft:slime_ball", "0-1", None)],
        "entry": ("It bobs along on rivers and ponds without a care, and squeaks whenever it is squeezed. Its body is "
                  "light and springy, so it never sinks, however rough the water."),
        "spawns": [spawn("squeakling-water", "common", "2-12", 9.0,
                         {"canSeeSky": True, "biomes": ["#cobblemon:is_river", "#cobblemon:is_freshwater", "#cobblemon:is_swamp"]},
                         position="surface")],
        "how": ["Wild: common floating on rivers, ponds and swamps.", "Evolves into Elastigoose at level 25."],
    },
    "elastigoose": {
        "dex": 3021, "name": "Elastigoose", "line": "route_one", "types": ["water", "flying"], **ROUTE, "male": 0.5,
        "egg_groups": ["water_1", "flying"], "abilities": ["waterveil", "owntempo", "h:unaware"],
        "ability_names": "Water Veil / Own Tempo / Unaware (hidden)",
        "stats": stats(80, 70, 70, 80, 70, 75), "ev": evs(hp=1, special_attack=1), "catch": 90, "exp": 165,
        "height": 15, "weight": 220, "shoulder": False, "walk": 0.3, "fly": True, "swims": True,
        "moves": [(1, "uproar"), (1, "tackle"), (1, "watergun"), (4, "growl"), (7, "wingattack"), (10, "aquajet"),
                  (14, "featherdance"), (18, "bubblebeam"), (22, "airslash"), (25, "uproar"), (29, "aquaring"),
                  (33, "hypervoice"), (38, "bravebird"), (44, "hydropump"), (50, "boomburst")],
        "tm": DUCK_TM + DUCK_TM_GOOSE, "egg": ["bellydrum", "soak", "aquaring", "mirrorcoat", "brine"],
        "evolve": None,
        "drops": [("minecraft:feather", "1-2", None), ("minecraft:slime_ball", "1-2", None)],
        "entry": ("Its neck stretches like rubber, letting it snatch food from the riverbed or honk right in a foe's "
                  "face from far away. Its honk is so loud it can be heard three valleys over."),
        "spawns": [spawn("elastigoose-water", "uncommon", "25-38", 3.0,
                         {"canSeeSky": True, "biomes": ["#cobblemon:is_river", "#cobblemon:is_freshwater", "#cobblemon:is_swamp"]},
                         position="surface")],
        "how": ["Evolve Squeakling at level 25.", "Wild: uncommon on rivers, ponds and swamps."],
    },
    "raddent": {
        "dex": 3022, "name": "Raddent", "line": "route_one", "types": ["grass", "normal"], **ROUTE, "male": 0.5,
        "egg_groups": ["field", "grass"], "abilities": ["runaway", "harvest", "h:guts"],
        "ability_names": "Run Away / Harvest / Guts (hidden)",
        "stats": stats(35, 56, 35, 25, 35, 72), "ev": evs(speed=1), "catch": 255, "exp": 51,
        "height": 3, "weight": 40, "shoulder": True, "walk": 0.32,
        "moves": [(1, "tackle"), (1, "tailwhip"), (4, "quickattack"), (7, "absorb"), (10, "bite"), (13, "bulletseed"),
                  (16, "hyperfang"), (19, "megadrain"), (23, "crunch"), (27, "seedbomb"), (31, "suckerpunch"),
                  (35, "superfang"), (40, "endeavor")],
        "tm": RAT_TM, "egg": ["finalgambit", "revenge", "switcheroo", "uproar", "leechseed"],
        "evolve": ("rattlebunch", 20, ["hornleech"]),
        "drops": [("minecraft:beetroot", "0-1", None), ("minecraft:beetroot_seeds", "1-2", None)],
        "entry": ("It plants itself in a vegetable patch and pretends to be a radish until the farmer goes home, then "
                  "nibbles everything in sight. Pull on its leaves and it squeaks and bolts."),
        "spawns": [route_spawn("raddent-plains", "common", "2-12", 10.0, PLAINS + ["#cobblemon:is_forest"]),
                   route_spawn("raddent-farms", "common", "2-12", 6.0, ["#cobblemon:is_overworld"],
                               structures=["#minecraft:village"])],
        "how": ["Wild: common in plains, grasslands, forests and villages.", "Evolves into Rattlebunch at level 20."],
    },
    "rattlebunch": {
        "dex": 3023, "name": "Rattlebunch", "line": "route_one", "types": ["grass", "normal"], **ROUTE, "male": 0.5,
        "egg_groups": ["field", "grass"], "abilities": ["runaway", "harvest", "h:guts"],
        "ability_names": "Run Away / Harvest / Guts (hidden)",
        "stats": stats(75, 88, 70, 50, 70, 97), "ev": evs(speed=2), "catch": 127, "exp": 145,
        "height": 8, "weight": 180, "shoulder": False, "walk": 0.35,
        "moves": [(1, "hornleech"), (1, "tackle"), (1, "tailwhip"), (4, "quickattack"), (7, "absorb"), (10, "bite"),
                  (13, "bulletseed"), (16, "hyperfang"), (19, "megadrain"), (20, "hornleech"), (24, "crunch"),
                  (28, "seedbomb"), (32, "suckerpunch"), (36, "superfang"), (41, "woodhammer"), (46, "endeavor")],
        "tm": RAT_TM + RAT_TM_KING, "egg": ["finalgambit", "revenge", "switcheroo", "uproar", "leechseed"],
        "evolve": None,
        "drops": [("minecraft:beetroot", "1-3", None), ("minecraft:string", "0-1", None)],
        "entry": ("Several Raddent whose leaves grew tangled together in the same patch, tied fast with a farmer's "
                  "twine. They argue constantly about which way to run, but when they agree, nothing can catch them."),
        "spawns": [route_spawn("rattlebunch-plains", "rare", "20-32", 1.5, PLAINS)],
        "how": ["Evolve Raddent at level 20.", "Wild: rare in plains and grasslands."],
    },
})
LINES["route_one"] = ["pipider", "blanketula", "shivnymph", "sheathalis", "cutlassfly", "cardling", "rubraptor",
                      "squeakling", "elastigoose", "raddent", "rattlebunch"]

# --- fossils: the tar line and the Prototaxites line (revived at Cobblemon's Restoration Tank; tools/newmons/fossils.py)

TAR_TM = BASIC_TM + ["rockslide", "rocktomb", "stoneedge", "stealthrock", "sandstorm", "ancientpower", "earthquake",
                     "bulldoze", "mudshot", "sludgebomb", "gunkshot", "bodyslam", "bodypress", "irondefense", "curse",
                     "painsplit", "spite", "rest"]
TAR_TM_FINAL = ["dragonclaw", "outrage", "crunch", "gigaimpact", "hyperbeam", "meteorbeam", "heavyslam", "dragontail",
                "headsmash"]
TAR_EGG = ["memento", "acidarmor", "stockpile", "swallow", "spitup", "curse"]
TAR_EARLY = [(1, "tackle"), (1, "harden"), (5, "mudslap"), (9, "rockthrow"), (13, "bonerush"), (17, "tarshot"),
             (21, "ancientpower"), (25, "headbutt"), (29, "rockslide"), (33, "sludgebomb"), (37, "bonemerang"),
             (41, "stoneedge")]
TAR = dict(male=0.875, egg_groups=["amorphous", "mineral"], friendship=50, abilities=["gooey", "stickyhold", "h:rockhead"],
           ability_names="Gooey / Sticky Hold / Rock Head (hidden)", labels=["fossil"])
SPIRE_TM = BASIC_TM + ["powergem", "meteorbeam", "sludgebomb", "venoshock", "earthpower", "gigadrain", "energyball",
                       "stealthrock", "toxicspikes", "irondefense", "rockslide", "stoneedge", "sandstorm", "trickroom",
                       "solarbeam", "grassknot", "bulldoze", "earthquake", "bodypress", "gyroball", "sludgewave",
                       "acidspray", "leechseed"]
SPIRE_TM_FINAL = ["gigaimpact", "hyperbeam", "solarblade"]
SPIRE_EGG = ["spore", "strengthsap", "ragepowder", "curse", "ingrain"]
SPIRE_EARLY = [(1, "tackle"), (1, "absorb"), (5, "rockthrow"), (9, "leechseed"), (13, "acid"), (17, "megadrain"),
               (21, "ancientpower"), (25, "venoshock"), (29, "gigadrain"), (33, "powergem")]
SPIRE = dict(male=0.5, egg_groups=["mineral", "grass"], friendship=50, abilities=["paleomycelium", "h:effectspore"],
             ability_names="Paleomycelium (its own: Grass moves get STAB; immune to Leech Seed, powder and spore moves) "
                           "/ Effect Spore (hidden)", labels=["fossil"])

SPECIES.update({
    "petroleodd": {
        "dex": 3024, "name": "Petroleodd", "line": "fossil", "types": ["rock"], **TAR,
        "stats": stats(70, 60, 80, 55, 65, 30), "ev": evs(defence=1), "catch": 45, "exp": 72,
        "height": 6, "weight": 410, "shoulder": False, "walk": 0.16,
        "moves": TAR_EARLY + [(48, "headsmash")], "tm": TAR_TM, "egg": TAR_EGG,
        "evolve": ("petroleossil", 45, ["dragonrush"], [{"variant": "held_item", "itemCondition": "cobblemon:kings_rock"}]),
        "consume": True,
        "drops": [("minecraft:coal", "1-2", None), ("minecraft:bone", "1-2", None), ("minecraft:black_dye", "0-1", None)],
        "entry": ("A pile of tar from the bottom of an ancient tar pit, brought back to life with the bones of old "
                  "Pokémon still inside it. It is sleepy and slow, and anything that touches it comes away stuck."),
        "spawns": [],
        "how": ["Revive Ancient Tar at a Restoration Tank. Ancient Tar is found by brushing the suspicious gravel round "
                "the tar pools of tar pits, caverns deep underground (around y -30) beside pockets of lava.",
                "Evolves into Petroleossil at level 45 while holding a King's Rock."],
    },
    "petroleossil": {
        "dex": 3025, "name": "Petroleossil", "line": "fossil", "types": ["rock", "dragon"], **TAR,
        "stats": stats(110, 115, 110, 75, 90, 40), "ev": evs(hp=1, attack=2), "catch": 45, "exp": 270,
        "height": 40, "weight": 4200, "shoulder": False, "walk": 0.22,
        "moves": [(1, "dragonrush")] + TAR_EARLY + [(45, "dragonrush"), (50, "crunch"), (55, "earthquake"),
                                                   (60, "headsmash"), (66, "gunkshot")],
        "tm": TAR_TM + TAR_TM_FINAL, "egg": TAR_EGG, "evolve": None,
        "drops": [("minecraft:coal_block", "0-1", None), ("minecraft:bone", "2-4", None), ("minecraft:bone_block", "0-1", None)],
        "entry": ("Holding a King's Rock, Petroleodd swallows tar and sludge until it becomes a mountain of it, with "
                  "the fossil skull of an ancient tyrant floating up through the middle. It roars through its jaws."),
        "spawns": [],
        "how": ["Evolve Petroleodd at level 45 while it holds a King's Rock (the King's Rock is used up)."],
    },
    "mycolith": {
        "dex": 3026, "name": "Mycolith", "line": "fossil", "types": ["rock", "poison"], **SPIRE,
        "stats": stats(80, 50, 90, 65, 60, 20), "ev": evs(defence=1), "catch": 45, "exp": 72,
        "height": 11, "weight": 839, "shoulder": False, "walk": 0.12,
        "moves": SPIRE_EARLY + [(34, "devoniandrift")], "tm": SPIRE_TM, "egg": SPIRE_EGG,
        "evolve": ("taxitower", 38, ["devoniandrift"]),
        "drops": [("minecraft:tuff", "1-2", None), ("minecraft:brown_mushroom", "0-2", None)],
        "entry": ("Revived from the Spire Fossil. Over 400 million years ago, fields of Mycolith dominated the barren "
                  "land before true trees ever took root. Researchers originally mistook its fossilized remains for "
                  "ancient timber."),
        "spawns": [],
        "how": ["Revive a Spire Fossil at a Restoration Tank. Spire Fossils are found by brushing the suspicious gravel "
                "round petrified spire stumps in forests and swamps.", "Evolves into Taxitower at level 38."],
    },
    "taxitower": {
        "dex": 3027, "name": "Taxitower", "line": "fossil", "types": ["rock", "poison"], **SPIRE,
        "stats": stats(115, 70, 125, 95, 85, 25), "ev": evs(defence=2, hp=1), "catch": 45, "exp": 265,
        "height": 80, "weight": 6441, "shoulder": False, "walk": 0.08,
        "moves": [(1, "devoniandrift")] + SPIRE_EARLY + [(38, "devoniandrift"), (42, "sludgebomb"), (46, "earthpower"),
                                                        (50, "strengthsap"), (55, "meteorbeam"), (60, "synthesis")],
        "tm": SPIRE_TM + SPIRE_TM_FINAL, "egg": SPIRE_EGG, "evolve": None,
        "drops": [("minecraft:tuff", "2-4", None), ("minecraft:brown_mushroom", "1-3", None), ("minecraft:glowstone_dust", "0-2", None)],
        "entry": ("Towering over ancient swamps, Taxitower absorbed nutrients from the surrounding soil through miles "
                  "of underground threads. When threatened, it releases blinding clouds of prehistoric spores that "
                  "haven't been breathed in eons."),
        "spawns": [],
        "how": ["Evolve Mycolith at level 38."],
    },
})
LINES["fossil"] = ["petroleodd", "petroleossil", "mycolith", "taxitower"]

# --- the jerboa mice: CobbleEffort's Pikachu-like mice (design by NyonTox, used with permission) ----------------------

JERB_TM = BASIC_TM + ["thunderbolt", "thunder", "thunderwave", "voltswitch", "wildcharge", "chargebeam", "electroball",
                      "eerieimpulse", "electricterrain", "psychic", "psyshock", "futuresight", "calmmind", "reflect",
                      "lightscreen", "trick", "trickroom", "psychicterrain", "shadowball", "irontail", "dig", "uturn",
                      "swift", "nastyplot", "encore", "charm", "thief", "zenheadbutt", "grassknot", "dazzlinggleam"]
JERB_TM_FINAL = ["gigaimpact", "hyperbeam", "expandingforce", "risingvoltage", "focusblast"]
JERB_EGG = ["wish", "fakeout", "encore", "charm", "tickle", "disarmingvoice"]
JERB_LEARN = [(1, "thundershock"), (1, "tailwhip"), (1, "confusion"), (4, "quickattack"), (7, "hypnosis"),
              (10, "nuzzle"), (13, "psybeam"), (16, "spark"), (19, "doublekick"), (22, "zenheadbutt"),
              (26, "discharge"), (30, "psychic"), (34, "thunderbolt"), (38, "agility"), (42, "calmmind"), (46, "thunder")]
JERB = dict(male=0.5, egg_groups=["field", "fairy"], friendship=70, abilities=["static", "synchronize", "h:levitate"],
            ability_names="Static / Synchronize / Levitate (hidden)", fly=True)

SPECIES.update({
    "jerbolt": {
        "dex": 3028, "name": "Jerbolt", "line": "jerboa", "types": ["electric", "psychic"], **JERB,
        "stats": stats(40, 45, 35, 60, 45, 85), "ev": evs(speed=2), "catch": 190, "exp": 112,
        "height": 3, "weight": 25, "shoulder": True, "walk": 0.35,
        "moves": JERB_LEARN, "tm": JERB_TM, "egg": JERB_EGG,
        "evolve": None, "evolve_stone": ("mesmerboa", "cobblemon:thunder_stone", ["psychicnoise"]),
        "drops": [("minecraft:glowstone_dust", "0-1", None), ("minecraft:sand", "0-1", None), ("cobblemon:thunder_stone", None, 1.0)],
        "entry": ("It floats over desert dunes at night with its tail curled round it in a ring. Anything that stares "
                  "at the turning ring for long falls into a daze, and Jerbolt hops off with its food."),
        "spawns": [
            route_spawn("jerbolt-desert", "uncommon", "5-25", 5.0, ["#cobblemon:is_desert"], timeRange="night"),
            route_spawn("jerbolt-badlands", "uncommon", "5-25", 3.0, ["#cobblemon:is_badlands", "#cobblemon:is_savanna"], timeRange="night"),
        ],
        "how": ["Wild: uncommon in deserts, badlands and savannas at night.", "Evolves into Mesmerboa when a Thunder Stone is used on it."],
    },
    "mesmerboa": {
        "dex": 3029, "name": "Mesmerboa", "line": "jerboa", "types": ["electric", "psychic"], **JERB,
        "stats": stats(60, 65, 55, 105, 85, 125), "ev": evs(speed=2, special_attack=1), "catch": 75, "exp": 218,
        "height": 7, "weight": 140, "shoulder": False, "walk": 0.4,
        "moves": [(1, "psychicnoise")] + JERB_LEARN + [(50, "psychicterrain"), (55, "risingvoltage"), (60, "expandingforce")],
        "tm": JERB_TM + JERB_TM_FINAL, "egg": JERB_EGG, "evolve": None,
        "drops": [("minecraft:glowstone_dust", "1-2", None), ("cobblemon:thunder_stone", None, 2.5)],
        "entry": ("Its tail is so long it never touches the ground: it hangs round Mesmerboa in a great ring that "
                  "crackles with electricity. Spun fast, the ring can put a whole herd of Pokémon to sleep at once."),
        "spawns": [route_spawn("mesmerboa-desert", "rare", "25-40", 1.5, ["#cobblemon:is_desert"], timeRange="night")],
        "how": ["Use a Thunder Stone on Jerbolt. It learns Psychic Noise when it evolves.",
                "Wild: rare in deserts at night."],
    },
})
LINES["jerboa"] = ["jerbolt", "mesmerboa"]

# --- the land sharks: CobbleEffort's pseudo-legendary ------------------------------------------------------------------

SHARK_TM = BASIC_TM + ["flamethrower", "fireblast", "firefang", "firepunch", "flamecharge", "willowisp", "sunnyday",
                       "overheat", "heatwave", "temperflare", "ironhead", "irondefense", "flashcannon", "heavyslam",
                       "metalclaw", "earthquake", "dig", "rockslide", "stoneedge", "crunch", "psychicfangs",
                       "thunderfang", "dragonclaw", "swordsdance", "bulkup", "bodypress", "bodyslam", "stealthrock",
                       "sandstorm", "rocktomb", "bulldoze", "scaryface", "thief"]
SHARK_TM_BIG = ["outrage", "closecombat", "brickbreak", "dragontail", "focusblast", "poweruppunch", "thunderpunch"]
SHARK_TM_FINAL = ["gigaimpact", "hyperbeam", "steelbeam", "flareblitz", "meteorbeam"]
SHARK_EGG = ["aquajet", "scaleshot", "bellydrum", "doubleedge", "outrage", "dragontail"]
SHARK_LEARN = [(1, "tackle"), (1, "leer"), (4, "ember"), (8, "bite"), (12, "metalclaw"), (16, "firefang"),
               (20, "irondefense"), (24, "flamewheel"), (28, "crunch"), (32, "ironhead"), (36, "firelash")]
SHARK = dict(male=0.5, egg_groups=["monster", "dragon"], friendship=50, catch=45, growth="slow",
             abilities=["roughskin", "flashfire", "h:toughclaws"],
             ability_names="Rough Skin / Flash Fire / Tough Claws (hidden)", labels=["pseudo_legendary"])

SPECIES.update({
    "sharkindle": {
        "dex": 3030, "name": "Sharkindle", "line": "landshark", "types": ["steel", "fire"], **SHARK,
        "stats": stats(55, 70, 55, 40, 45, 35), "ev": evs(attack=1), "exp": 60,
        "height": 7, "weight": 300, "shoulder": False, "walk": 0.3,
        "moves": SHARK_LEARN + [(40, "flareblitz")], "tm": SHARK_TM, "egg": SHARK_EGG,
        "evolve": ("forgnash", 40, ["crushclaw"]),
        "drops": [("minecraft:iron_nugget", "1-3", None), ("minecraft:blaze_powder", "0-1", None)],
        "entry": ("It swims through the ground near lava as easily as a shark through water, its orange fins glowing "
                  "where they cut through the hot rock. Its bite can dent iron."),
        "spawns": [route_spawn("sharkindle-volcanic", "ultra-rare", "15-30", 1.0, ["#cobblemon:is_volcanic", "#cobblemon:is_badlands"]),
                   spawn("sharkindle-lava", "ultra-rare", "15-30", 1.0,
                         dict(UNDERGROUND, biomes=["#cobblemon:is_overworld"], neededNearbyBlocks=["minecraft:lava"]))],
        "how": ["Wild: very rare in volcanic biomes and badlands, and underground near lava.",
                "Evolves into Forgnash at level 40."],
    },
    "forgnash": {
        "dex": 3031, "name": "Forgnash", "line": "landshark", "types": ["steel", "fire"], **SHARK,
        "stats": stats(70, 100, 80, 55, 60, 55), "ev": evs(attack=2), "exp": 144,
        "height": 14, "weight": 1200, "shoulder": False, "walk": 0.3,
        "moves": [(1, "crushclaw")] + SHARK_LEARN + [(40, "crushclaw"), (44, "firepunch"), (48, "ironhead"),
                                                    (52, "flareblitz"), (56, "swordsdance")],
        "tm": SHARK_TM + SHARK_TM_BIG, "egg": SHARK_EGG,
        "evolve": ("magmalodon", 60, ["heatcrash"]),
        "drops": [("minecraft:iron_ingot", "0-1", None), ("minecraft:blaze_powder", "1-2", None)],
        "entry": ("Once it stands on two legs, the fire inside it bursts out through its back. It hammers metal ore "
                  "with its claws to sharpen them, and the sparks fly like a forge."),
        "spawns": [route_spawn("forgnash-volcanic", "ultra-rare", "40-55", 0.5, ["#cobblemon:is_volcanic"])],
        "how": ["Evolve Sharkindle at level 40.", "Wild: extremely rare in volcanic biomes."],
    },
    "magmalodon": {
        "dex": 3032, "name": "Magmalodon", "line": "landshark", "types": ["steel", "fire"], **SHARK,
        "stats": stats(108, 135, 105, 80, 85, 87), "ev": evs(attack=3), "exp": 300,
        "height": 24, "weight": 3500, "shoulder": False, "walk": 0.3,
        "moves": [(1, "heatcrash"), (1, "crushclaw")] + SHARK_LEARN +
                 [(40, "crushclaw"), (44, "firepunch"), (48, "ironhead"), (52, "flareblitz"), (56, "swordsdance"),
                  (60, "heatcrash"), (65, "heavyslam"), (70, "shiftgear"), (76, "overheat")],
        "tm": SHARK_TM + SHARK_TM_BIG + SHARK_TM_FINAL, "egg": SHARK_EGG, "evolve": None,
        "drops": [("minecraft:iron_ingot", "1-3", None), ("minecraft:magma_cream", "1-2", None)],
        "entry": ("Its body burns hotter than a smelter, and the smoke pouring off its head hangs down its back like "
                  "dreadlocks. A single bite from its huge jaws can tear through a steel girder."),
        "spawns": [],
        "how": ["Evolve Forgnash at level 60."],
    },
})
LINES["landshark"] = ["sharkindle", "forgnash", "magmalodon"]

# --- Jormbuoy and Jorminous (from the Zorneo x Norden region fakemon series, used with the creators' permission) -----

JORM_TM = BASIC_TM + ["surf", "waterfall", "waterpulse", "hydropump", "raindance", "scald", "chillingwater", "icebeam",
                      "icywind", "blizzard", "liquidation", "dive", "whirlpool", "bodyslam", "irontail", "crunch",
                      "ironhead", "irondefense", "flipturn"]
JORM_TM_FINAL = ["shadowball", "hex", "phantomforce", "shadowclaw", "willowisp", "nightshade", "curse", "painsplit",
                 "dragonpulse", "outrage", "hurricane", "gigaimpact", "hyperbeam"]
JORM_EGG = ["dragontail", "aquaring", "mist", "haze", "octazooka"]
JORM_LEARN = [(1, "tackle"), (1, "watergun"), (4, "withdraw"), (8, "aquajet"), (12, "bite"), (16, "waterpulse"),
              (20, "wrap"), (24, "aquaring"), (28, "brine"), (32, "crunch"), (36, "aquatail"), (40, "hydropump")]
JORM = dict(male=0.5, egg_groups=["water_2", "dragon"], friendship=50, abilities=["swiftswim", "shellarmor", "h:cursedbody"],
            ability_names="Swift Swim / Shell Armor / Cursed Body (hidden)", aquatic=True)

SPECIES.update({
    "jormbuoy": {
        "dex": 3033, "name": "Jormbuoy", "line": "jorm", "types": ["water"], **JORM,
        "stats": stats(60, 50, 65, 60, 60, 45), "ev": evs(defence=1), "catch": 120, "exp": 66,
        "height": 7, "weight": 220, "shoulder": False, "walk": 0.2,
        "moves": JORM_LEARN, "tm": JORM_TM, "egg": JORM_EGG,
        "evolve": None, "evolve_stone": ("jorminous", "cobblemon:dusk_stone", ["hex"], [{"variant": "level", "minLevel": 45}]),
        "drops": [("minecraft:oak_planks", "0-2", None), ("minecraft:string", "0-1", None)],
        "entry": ("It bobs along on cold seas under a hull of old ship's timbers, shields lined up along its sides. "
                  "Sailors used to tie their boats to it, mistaking it for a buoy, until it swam away with them."),
        "spawns": [spawn("jormbuoy-ocean", "uncommon", "10-35", 4.0,
                         {"canSeeSky": True, "biomes": ["#cobblemon:is_cold_ocean", "#cobblemon:is_ocean"]}, position="surface")],
        "how": ["Wild: uncommon floating on oceans, especially cold ones.",
                "Evolves into Jorminous when a Dusk Stone is used on it at level 45 or higher."],
    },
    "jorminous": {
        "dex": 3034, "name": "Jorminous", "line": "jorm", "types": ["water", "ghost"], **JORM,
        "stats": stats(95, 90, 95, 100, 90, 70), "ev": evs(special_attack=2, hp=1), "catch": 45, "exp": 245,
        "height": 70, "weight": 3000, "shoulder": False, "walk": 0.3,
        "moves": [(1, "hex")] + JORM_LEARN + [(45, "hex"), (48, "shadowball"), (52, "dragonpulse"), (56, "phantomforce"),
                                             (62, "wavecrash")],
        "tm": JORM_TM + JORM_TM_FINAL, "egg": JORM_EGG, "evolve": None,
        "drops": [("minecraft:oak_planks", "1-3", None), ("minecraft:phantom_membrane", "0-1", None)],
        "entry": ("The ghost of a sunken raiding ship that has become a great sea serpent. When it rises out of the fog "
                  "with its shields gleaming and its oars beating, whole fleets turn back to shore."),
        "spawns": [spawn("jorminous-deep", "ultra-rare", "45-60", 1.0,
                         {"canSeeSky": True, "timeRange": "night", "biomes": ["#cobblemon:is_deep_ocean"]}, position="surface")],
        "how": ["Use a Dusk Stone on Jormbuoy at level 45 or higher. It learns Hex when it evolves.",
                "Wild: very rare on deep oceans at night."],
    },
})
LINES["jorm"] = ["jormbuoy", "jorminous"]

# abilities of our own: Cobblemon datapack abilities (data/cobbleeffort/abilities/<id>.js, a Showdown ability object)
CUSTOM_ABILITIES = {
    "blindsight": {
        "name": "Blindsight",
        "js": """{
onSourceInvulnerabilityPriority: 1,
onSourceInvulnerability(target, source, move) {
  if (move && source === this.effectState.target) return 0;
},
onSourceAccuracyPriority: -100,
onSourceAccuracy(accuracy, target, source, move) {
  if (move && source === this.effectState.target) return true;
  return accuracy;
},
flags: {},
name: "Blindsight",
rating: 3.5,
num: -3002
}
""",
        "lang": "The Pokémon is blind, yet it senses everything around it: every move it uses hits, whatever its "
                "accuracy, and even targets that are flying, underground or underwater.",
    },
    "paleomycelium": {
        "name": "Paleomycelium",
        "js": """{
onModifyMovePriority: -1,
onModifyMove(move) {
  if (move.type === 'Grass') move.forceSTAB = true;
},
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (target !== source && (move.flags['powder'] || move.id === 'leechseed')) {
    this.add('-immune', target, '[from] ability: Paleomycelium');
    return null;
  }
},
flags: {breakable: 1},
name: "Paleomycelium",
rating: 3,
num: -3004
}
""",
        "lang": "An ancient fungus long mistaken for a plant: its Grass-type moves get the same-type bonus, and it is "
                "immune to Leech Seed and to powder and spore moves.",
    },
    "pharaohscurse": {
        "name": "Pharaoh's Curse",
        "js": """{
onDamagePriority: -30,
onDamage(damage, target, source, effect) {
  if (!effect || effect.effectType !== 'Move' || damage < target.hp || target.m.pharaohsCurse) return damage;
  target.m.pharaohsCurse = true;
  this.add('-ability', target, "Pharaoh's Curse");
  const half = Math.max(1, Math.floor(target.maxhp / 2));
  this.boost({atk: 2, spa: 2}, target, target);
  if (target.hp > half) return target.hp - half;
  if (target.hp < half) this.heal(half - target.hp, target, target);
  return 0;
},
flags: {breakable: 1},
name: "Pharaoh's Curse",
rating: 4,
num: -3003
}
""",
        "lang": "Once per battle, a hit that would knock the Pokémon out doesn't: it rises again at half its HP and "
                "its Attack and Sp. Atk sharply rise.",
    },
}

# moves of our own: Cobblemon datapack moves (data/cobbleeffort/moves/<id>.js, read into Showdown at startup)
CUSTOM_MOVES = {
    "devoniandrift": {
        "name": "Devonian Drift",
        "js": """{
num: -3004,
accuracy: true,
basePower: 0,
category: "Status",
name: "Devonian Drift",
pp: 15,
priority: 0,
flags: {reflectable: 1, metronome: 1},
sideCondition: "devoniandrift",
condition: {
  duration: 5,
  onSideStart(side) {
    this.add('-sidestart', side, 'move: Devonian Drift');
  },
  onResidualOrder: 5,
  onResidualSubOrder: 1,
  onResidual(target) {
    if (target.hasType('Poison') || target.hasType('Steel') || !target.isGrounded()) return;
    this.damage(target.baseMaxhp / 8, target, null, this.dex.conditions.get('devoniandrift'));
    this.boost({spe: -1}, target, null, null, true);
  },
  onSideResidualOrder: 26,
  onSideResidualSubOrder: 12,
  onSideEnd(side) {
    this.add('-sideend', side, 'move: Devonian Drift');
  }
},
secondary: null,
target: "foeSide",
type: "Poison",
desc: "For 5 turns, heavy ancient spores cover the opposing side: at the end of each turn, every grounded opponent that is not Poison or Steel type loses 1/8 of its maximum HP and its Speed falls by 1 stage.",
shortDesc: "5 turns: grounded non-Poison/Steel foes lose 1/8 HP and -1 Spe each turn.",
contestType: "Clever"
}
""",
        "lang": "Scatters heavy, ancient spores over the opposing side for five turns. At the end of each turn they "
                "hurt every grounded opponent that isn't Poison or Steel type and weigh it down, lowering its Speed.",
        "battle": {
            "cobblemon.battle.sidestart.ally.devoniandrift": "Ancient spores drifted down around your team!",
            "cobblemon.battle.sidestart.opponent.devoniandrift": "Ancient spores drifted down around the opposing team!",
            "cobblemon.battle.sideend.ally.devoniandrift": "The ancient spores around your team settled!",
            "cobblemon.battle.sideend.opponent.devoniandrift": "The ancient spores around the opposing team settled!",
            "cobblemon.battle.damage.devoniandrift": "%1$s is weighed down by the ancient spores!",
        },
    },
    "machinegunstinger": {
        "base": "pinmissile", "num": -3001, "name": "Machine Gun Stinger", "type": "Bug", "category": "Physical",
        "basePower": 25, "accuracy": 95, "pp": 15, "multihit": [2, 5],
        "flags": {"protect": 1, "mirror": 1, "metronome": 1, "bullet": 1},
        "secondary": {"chance": 20, "status": "brn"}, "contestType": "Cool",
        "desc": "Hits two to five times. Each hit has a 20% chance to burn the target.",
        "shortDesc": "Hits 2-5 times. Each hit: 20% chance to burn.",
        "lang": "Spins up its Gatling arms and sprays the target with red-hot stingers two to five times in a row. "
                "Each stinger may leave the target with a burn.",
    },
}
# the starter screen: Cobblemon shows only data-pack categories once any exist (unless use_config_starters is on),
# so its built-in regions are shipped too, as in its default config, and ours comes after them
STARTER_CATEGORIES = [
    ("Kanto", -110, "kanto", ["Bulbasaur", "Charmander", "Squirtle"]),
    ("Johto", -109, "johto", ["Chikorita", "Cyndaquil", "Totodile"]),
    ("Hoenn", -108, "hoenn", ["Treecko", "Torchic", "Mudkip"]),
    ("Sinnoh", -107, "sinnoh", ["Turtwig", "Chimchar", "Piplup"]),
    ("Unova", -106, "unova", ["Snivy", "Tepig", "Oshawott"]),
    ("Kalos", -105, "kalos", ["Chespin", "Fennekin", "Froakie"]),
    ("Alola", -104, "alola", ["Rowlet", "Litten", "Popplio"]),
    ("Galar", -103, "galar", ["Grookey", "Scorbunny", "Sobble"]),
    ("Paldea", -101, "paldea", ["Sprigatito", "Fuecoco", "Quaxly"]),
    ("Special", -100, "special", ["Pikachu"]),
]
OUR_STARTERS = ("CobbleEffort", -99, ["cobbleeffort:coalarva", "cobbleeffort:mumpillar"])



def folder(sp):
    return f"{SPECIES[sp]['dex']:04d}_{sp}"


def group_of(sp):
    return f"cobbleeffort_{sp}"


def model_module(sp):
    spec = importlib.util.spec_from_file_location(f"newmon_{sp}", HERE / "models" / f"{sp}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_model(sp):
    cfg = SPECIES[sp]
    hand = model_module(sp)
    cfg.update(scale=hand.SCALE, hitbox=hand.HITBOX, look=hand.LOOK)
    m = hand.build()
    tw, th = m.layout()
    k = getattr(hand, "K", 1)
    tex_dir = RES / "assets" / MOD / "textures" / "pokemon" / folder(sp)
    tex_dir.mkdir(parents=True, exist_ok=True)
    tex = lambda n: f"{MOD}:textures/pokemon/{folder(sp)}/{n}.png"
    layers = {"": [], "_shiny": []}                         # resolver layers per variant (glow, translucent shell)
    for variant, sfx in ((None, ""), ("shiny", "_shiny")):
        img, glow = m.paint(tw, th, variant, k=k)
        a = np.array(img)
        shell = (a[..., 3] > 0) & (a[..., 3] < 255)        # texels painted part-transparent: the translucent layer
        g = np.array(glow)
        if g[..., 3].any():
            for f, mul in enumerate((1.0, 0.86, 0.94)):        # the glow flickers a little
                gf = g.astype(float)
                gf[..., :3] *= mul
                Image.fromarray(gf.astype(np.uint8), "RGBA").save(tex_dir / f"{sp}{sfx}_glow_{f}.png", optimize=True)
            layers[sfx].append({"name": "cobbleeffort_glow", "emissive": True, "translucent": True,
                                "texture": {"frames": [tex(f"{sp}{sfx}_glow_{f}") for f in range(3)], "fps": 6, "loop": True}})
        if shell.any():
            s = np.zeros_like(a)
            s[shell] = a[shell]
            a[shell, 3] = 0
            Image.fromarray(s, "RGBA").save(tex_dir / f"{sp}{sfx}_shell.png", optimize=True)
            layers[sfx].append({"name": "cobbleeffort_shell", "translucent": True, "texture": tex(f"{sp}{sfx}_shell")})
        Image.fromarray(a, "RGBA").save(tex_dir / f"{sp}{sfx}.png", optimize=True)
    cfg["layers"] = layers
    names = [b["name"] for b in m.bones if b["parent"] is not None]
    piv = {b["name"]: b["pivot"] for b in m.bones}
    legs = [n for n in names if n.startswith("leg")]
    top = getattr(hand, "HEIGHT", None) or max(b.lo[1] + b.size[1] for b in m.boxes)
    cfg["model_height"] = top
    extra = [{"name": "locator_root", "parent": sp, "pivot": [0, 0, 0]},
             {"name": "locator_top", "parent": sp, "pivot": [0, float(top), 0]}]
    bedrock = RES / "assets" / MOD / "bedrock" / "pokemon"
    write_json(bedrock / "models" / folder(sp) / f"{sp}.geo.json", m.geo(tw, th, f"geometry.{sp}", extra))
    write_json(bedrock / "animations" / folder(sp) / f"{group_of(sp)}.animation.json",
               animations(group_of(sp), getattr(hand, "KIND", "quadruped"), getattr(hand, "ANIM", {}), names, legs, piv))
    write_json(bedrock / "posers" / folder(sp) / f"{sp}.json", poser(group_of(sp), sp, top, hand.SCALE, names))
    write_json(bedrock / "resolvers" / folder(sp) / f"0_{sp}_base.json", {
        "species": f"{MOD}:{sp}", "order": 0,
        "variations": [
            {"aspects": [], "poser": f"{MOD}:{sp}", "model": f"{MOD}:{sp}.geo", "texture": tex(sp), "layers": layers[""]},
            {"aspects": ["shiny"], "texture": tex(f"{sp}_shiny"), **({"layers": layers["_shiny"]} if layers["_shiny"] else {})},
        ]})
    print(f"{sp}: {len(m.boxes)} cubes, texture {tw}x{th} (x{k}), {top} units tall, bones {names}")


def species_json(sp):
    c = SPECIES[sp]
    d = {
        "implemented": True, "nationalPokedexNumber": c["dex"], "name": c["name"], "primaryType": c["types"][0],
    }
    if len(c["types"]) > 1:
        d["secondaryType"] = c["types"][1]
    d.update({
        "maleRatio": c.get("male", 0.5), "height": c["height"], "weight": c["weight"], "pokedex": [f"{MOD}.species.{sp}.desc"],
        "labels": ["cobbleeffort", "custom"] + c.get("labels", []), "aspects": [], "abilities": c["abilities"], "eggGroups": c["egg_groups"],
        "baseStats": c["stats"], "evYield": c["ev"], "baseExperienceYield": c["exp"],
        "experienceGroup": c.get("growth", "medium_slow"),
        "catchRate": c["catch"], "eggCycles": 20, "baseFriendship": c["friendship"],
        "shoulderMountable": c["shoulder"], "baseScale": c["scale"],
        "hitbox": {"width": c["hitbox"][0], "height": c["hitbox"][1], "fixed": False},
        "behaviour": {
            "resting": {"canSleep": True, "willSleepOnBed": True, "times": ["day"], "drowsyChance": 0.0014,
                        "rouseChance": 0.0042},
            "moving": {"walk": {"walkSpeed": c["walk"]},
                       "swim": ({"avoidsWater": False, "canSwimInWater": True, "swimSpeed": 0.4,
                                 "canBreatheUnderwater": True} if c.get("aquatic") else
                                {"avoidsWater": False, "canSwimInWater": True, "swimSpeed": 0.3} if c.get("swims")
                                else {"avoidsWater": True, "canSwimInWater": False}),
                       **({"fly": {"canFly": True, "flySpeedHorizontal": "0.4"}} if c.get("fly") else {})},
            "combat": {"willDefendOwner": True, "willDefendSelf": sp != "cavitot"},
        },
        "drops": {"amount": 2, "entries": [
            {"item": item, **({"quantityRange": q} if q else {}), **({"percentage": p} if p else {})}
            for item, q, p in c["drops"]]},
        "moves": [f"{lv}:{mv}" for lv, mv in c["moves"]] + [f"egg:{m}" for m in c["egg"]] + [f"tm:{m}" for m in c["tm"]],
    })
    if c.get("evolve_stone"):                               # evolves when an item is used on it (e.g. a Thunder Stone)
        to, item, learn, *more = c["evolve_stone"]
        d["evolutions"] = [{"id": f"{sp}_{to}", "variant": "item_interact", "result": f"{MOD}:{to}",
                            "consumeHeldItem": False, "learnableMoves": learn, "requiredContext": item,
                            **({"requirements": more[0]} if more else {})}]
    elif c["evolve"]:
        to, lv, learn, *more = c["evolve"]
        d["evolutions"] = [{"id": f"{sp}_{to}", "variant": "level_up", "result": f"{MOD}:{to}", "consumeHeldItem": bool(c.get("consume")),
                            "learnableMoves": learn,
                            "requirements": [{"variant": "level", "minLevel": lv}] + (more[0] if more else [])}]
    pre = [s for s, o in SPECIES.items() if (o["evolve"] and o["evolve"][0] == sp)
           or (o.get("evolve_stone") and o["evolve_stone"][0] == sp)]
    if pre:
        d["preEvolution"] = f"{MOD}:{pre[0]}"
    return d


EGG_GROUPS = {"monster", "water_1", "bug", "flying", "field", "fairy", "grass", "human_like", "water_3", "mineral",
              "amorphous", "water_2", "ditto", "dragon", "undiscovered"}


def check(showdown):
    """Every move and ability must exist in Cobblemon's Showdown (data/moves.js, data/abilities.js)."""
    import re
    import zipfile
    z = zipfile.ZipFile(showdown)
    ids = lambda f: set(re.findall(r"^  ([a-z0-9]+): \{", z.read(f).decode(), re.M))
    moves, abilities = ids("data/moves.js"), ids("data/abilities.js")
    bad = []
    for sp, c in SPECIES.items():
        evo_moves = (c["evolve"][2] if c["evolve"] else []) + (c["evolve_stone"][2] if c.get("evolve_stone") else [])
        for mv in [m for _, m in c["moves"]] + c["tm"] + c["egg"] + evo_moves:
            if mv not in moves and mv not in CUSTOM_MOVES:
                bad.append(f"{sp}: move {mv}")
        for eg in c["egg_groups"]:                           # Cobblemon's EggGroup ids (a wrong one stops the server)
            if eg not in EGG_GROUPS:
                bad.append(f"{sp}: egg group {eg}")
        for ab in c["abilities"]:
            if ab.removeprefix("h:") not in abilities and ab.removeprefix("h:") not in CUSTOM_ABILITIES:
                bad.append(f"{sp}: ability {ab}")
    if bad:
        raise SystemExit("unknown in Showdown: " + ", ".join(bad))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--showdown", type=Path, help="Cobblemon's data/cobblemon/showdown.zip: check moves and abilities")
    args = ap.parse_args()
    if args.showdown:
        check(args.showdown)
    data = RES / "data" / MOD
    lang_path = RES / "assets" / MOD / "lang" / "en_us.json"
    lang = json.loads(lang_path.read_text())
    manifest, readme = [], []
    for sp, c in SPECIES.items():
        build_model(sp)
        write_json(data / "species" / c["line"] / f"{sp}.json", species_json(sp))
        spawns = [dict(s, pokemon=f"{MOD}:{sp}") for s in c["spawns"]]
        pool = data / "spawn_pool_world" / f"{sp}.json"
        if spawns:
            write_json(pool, {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": spawns})
        elif pool.exists():
            pool.unlink()
        write_json(data / "dex_entries" / "pokemon" / f"{sp}.json", {
            "id": f"{MOD}:{sp}", "speciesId": f"{MOD}:{sp}", "displayAspects": [], "conditionAspects": [],
            "forms": [{"displayForm": "Normal", "unlockForms": ["Normal"]}], "variations": []})
        lang[f"{MOD}.species.{sp}.name"] = c["name"]
        lang[f"{MOD}.species.{sp}.desc"] = c["entry"]
        for sfx in ("", "_shiny"):
            lay = [{"original": None, "emissive": bool(l.get("emissive")),
                    "retextured": (l["texture"]["frames"][0] if isinstance(l["texture"], dict) else l["texture"])}
                   for l in c["layers"][sfx]]
            manifest.append({"species": f"{sp}{sfx}", "folder": folder(sp), "model": f"{MOD}:{sp}.geo", "original": None,
                             "retextured": f"{MOD}:textures/pokemon/{folder(sp)}/{sp}{sfx}.png", "layers": lay})
        types = " / ".join(t.title() for t in c["types"])
        st = c["stats"]
        write_json(TOOLS / "readme" / f"_new_{sp}.json", {
            "dex": c["dex"], "name": c["name"], "types": types, "ability": c["ability_names"], "look": c["look"],
            "entry": c["entry"], "how": c["how"],
            "stats": [st["hp"], st["attack"], st["defence"], st["special_attack"], st["special_defence"], st["speed"]]})
        readme.append(c)
    for mid, mv in CUSTOM_MOVES.items():
        if "js" in mv:                                       # a whole move of our own (with its own condition)
            js = mv["js"]
        else:                                                # a twist on an existing move
            fields = {k: v for k, v in mv.items() if k not in ("base", "lang")}
            fields.update(isNonstandard=None, zMove={"basePower": 140}, maxMove={"basePower": 130})
            js = f'Object.assign({{}}, Dex.data.Moves["{mv['base']}"], {json.dumps(fields)})\n'
        lang.update(mv.get("battle", {}))
        (data / "moves").mkdir(parents=True, exist_ok=True)
        (data / "moves" / f"{mid}.js").write_text(js)
        lang[f"cobblemon.move.{mid}"] = mv["name"]
        lang[f"cobblemon.move.{mid}.desc"] = mv["lang"]
    for aid, ab in CUSTOM_ABILITIES.items():
        (data / "abilities").mkdir(parents=True, exist_ok=True)
        (data / "abilities" / f"{aid}.js").write_text(ab["js"])
        lang[f"cobblemon.ability.{aid}"] = ab["name"]
        lang[f"cobblemon.ability.{aid}.desc"] = ab["lang"]
    for name, order, key, mons in STARTER_CATEGORIES:
        write_json(data / "starters" / f"{key}.json", {
            "name": name, "order": order, "displayName": f"cobblemon.starterselection.category.{key}",
            "pokemon": [f"{m} level=10" for m in mons]})
    name, order, mons = OUR_STARTERS
    write_json(data / "starters" / "cobbleeffort.json", {
        "name": name, "order": order, "displayName": "cobbleeffort.starterselection.category.cobbleeffort",
        "pokemon": [f"{m} level=10" for m in mons]})
    import fossils                                           # fossil items, structures and Cobblemon fossil entries
    fossils.build(lang)
    lang["cobbleeffort.starterselection.category.cobbleeffort"] = "CobbleEffort"
    lang["cobblemon.ui.pokedex.region.cobbleeffort"] = "CobbleEffort"
    write_json(lang_path, dict(sorted(lang.items())))
    write_json(data / "dexes" / "cobbleeffort.json", {
        "type": "cobblemon:simple_pokedex_def", "id": f"{MOD}:cobbleeffort", "sortOrder": 30,
        "entries": [f"{MOD}:{sp}" for sp in sorted(SPECIES, key=lambda s: SPECIES[s]["dex"])]})
    write_json(data / "dex_additions" / "national.json", {"dexId": "cobblemon:national", "entries": [f"{MOD}:cobbleeffort"]})
    write_json(TOOLS / "preview" / "manifest_newmons.json", manifest)
    readme_table(readme)


def readme_table(cfgs):
    """The new-Pokémon table in README.md, between its <!-- newmons --> markers."""
    path = ROOT / "README.md"
    text = path.read_text()
    a, b = "<!-- newmons:start -->", "<!-- newmons:end -->"
    rows = ["| # | Pokémon | Types | Abilities | HP / Atk / Def / SpA / SpD / Spe | Height / Weight | How to get it | Pokédex |",
            "|---|---|---|---|---|---|---|---|"]
    for c in cfgs:
        st = c["stats"]
        nums = " / ".join(str(st[k]) for k in ("hp", "attack", "defence", "special_attack", "special_defence", "speed"))
        ft = c["height"] * 10 / 2.54 / 12
        size = f"{int(ft)}'{round((ft - int(ft)) * 12)}\" ({c['height'] / 10:g} m) / {c['weight'] / 10:g} kg"
        rows.append(f"| {c['dex']} | **{c['name']}** | {' / '.join(t.title() for t in c['types'])} | {c['ability_names']} | "
                    f"{nums} | {size} | {' '.join(c['how'])} | {c['entry']} |")
    path.write_text(text[:text.index(a) + len(a)] + "\n" + "\n".join(rows) + "\n" + text[text.index(b):])


if __name__ == "__main__":
    main()
