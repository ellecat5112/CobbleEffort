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
        "how": ["Revive a Bucket of Tar at a Fossil Analyzer (needs CobbleEffort: Kanto). Tar is a sticky black fluid "
                "that pools in tar lakes on the surface of badlands, deserts, savannas and swamps, underground, and in "
                "tar pits deep underground (around y -30): scoop it up with an empty bucket.",
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

# --- Type: Error: an evil, bipedal Type: Null built for attack and speed, with the "Error" typing ----------------------

ERROR_TM = BASIC_TM + ["gigaimpact", "hyperbeam", "swordsdance", "bulkup", "agility", "uturn", "knockoff", "crunch",
                       "ironhead", "xscissor", "closecombat", "brickbreak", "shadowclaw", "nightslash", "aerialace",
                       "rockslide", "earthquake", "irontail", "thief", "taunt", "snarl", "scaryface", "bodyslam",
                       "doubleedge", "takedown", "facade", "lashout", "throatchop"]

SPECIES.update({
    "typeerror": {
        "dex": 3035, "name": "Type: Error", "line": "error", "types": ["normal"],
        "male": -1, "egg_groups": ["undiscovered"], "friendship": 0, "catch": 3, "labels": ["legendary"],
        "abilities": ["systemerror", "h:systemerror"],
        "ability_names": "System Error (its own: makes it Error type in battle)",
        "stats": stats(80, 130, 60, 90, 60, 114), "ev": evs(attack=2, speed=1), "exp": 218,
        "height": 19, "weight": 1205, "shoulder": False, "walk": 0.42, "growth": "slow",
        "moves": [(1, "tackle"), (1, "leer"), (1, "scaryface"), (5, "quickattack"), (10, "pursuit"), (15, "slash"),
                  (20, "crushclaw"), (25, "nightslash"), (30, "ironhead"), (35, "xscissor"), (40, "doubleedge"),
                  (45, "swordsdance"), (50, "extremespeed"), (55, "closecombat"), (60, "gigaimpact")],
        "tm": ERROR_TM, "egg": [], "evolve": None,
        "drops": [("minecraft:iron_ingot", "1-2", None), ("minecraft:redstone", "1-3", None)],
        "entry": ("A failed experiment built to be faster and deadlier than any other. The mask clamped over its head "
                  "keeps its corrupted power in check. Its type cannot be read: every attack hits it the same, except "
                  "the most ordinary ones."),
        "spawns": [spawn("typeerror-deepdark", "ultra-rare", "50-60", 0.5, dict(UNDERGROUND, biomes=["#cobblemon:is_deep_dark"]))],
        "how": ["Wild: extremely rare in the Deep Dark (level 50-60). Genderless; it cannot breed."],
    },
})
LINES["error"] = ["typeerror"]

# --- Tanhyll: a two-legged anteater (the user's idea and concept art; the art's own name) -----------------------------

TANHYLL_TM = BASIC_TM + ["bodyslam", "bulkup", "brickbreak", "closecombat", "drainpunch", "dig", "earthquake",
                         "rockslide", "shadowclaw", "ironhead", "knockoff", "gigaimpact", "hyperbeam", "swordsdance",
                         "firepunch", "thunderpunch", "icepunch", "poweruppunch", "lowkick", "rocktomb", "bulldoze",
                         "taunt", "thief", "uturn", "facade", "aerialace", "irontail", "focusblast", "superpower"]

SPECIES.update({
    "tanhyll": {
        "dex": 3036, "name": "Tanhyll", "line": "tanhyll", "types": ["normal", "fighting"],
        "male": 0.5, "egg_groups": ["field"], "friendship": 50, "catch": 75,
        "abilities": ["insectivore", "h:scrappy"],
        "ability_names": "Insectivore (its own: its attacks are 4x super effective on Bug types) / Scrappy (hidden)",
        "stats": stats(90, 115, 75, 55, 70, 85), "ev": evs(attack=2), "exp": 172,
        "height": 16, "weight": 700, "shoulder": False, "walk": 0.3,
        "moves": [(1, "scratch"), (1, "leer"), (5, "lick"), (9, "furyswipes"), (13, "rapidspin"), (17, "lowsweep"),
                  (21, "slash"), (25, "crushclaw"), (29, "brickbreak"), (33, "focusenergy"), (37, "hammerarm"),
                  (41, "slackoff"), (46, "closecombat"), (52, "superpower")],
        "tm": TANHYLL_TM, "egg": ["curse", "counter", "feint", "doublekick", "suckerpunch"], "evolve": None,
        "drops": [("minecraft:white_wool", "0-1", None), ("cobblemon:black_belt", None, 2.5)],
        "entry": ("It stands up on its hind legs to tear open Bug Pokémon nests with its huge claws, then slurps up "
                  "everything inside with its long hooked tongue. Bug Pokémon flee at its very scent."),
        "spawns": [route_spawn("tanhyll-savanna", "uncommon", "20-40", 3.0, ["#cobblemon:is_savanna", "#cobblemon:is_jungle"]),
                   route_spawn("tanhyll-forest", "rare", "20-40", 1.5, ["#cobblemon:is_forest", "#cobblemon:is_badlands"])],
        "how": ["Wild: uncommon in savannas and jungles, rare in forests and badlands."],
    },
})
LINES["tanhyll"] = ["tanhyll"]

# --- the kickboxing apes: skull and tiki looks -------------------------------------------------------------------------

TIKI_TM = BASIC_TM + ["bodyslam", "bulkup", "brickbreak", "closecombat", "drainpunch", "dig", "rockslide", "knockoff",
                      "firepunch", "thunderpunch", "icepunch", "poweruppunch", "lowkick", "lowsweep", "rocktomb",
                      "bulldoze", "taunt", "thief", "uturn", "facade", "aerialace", "acrobatics", "trailblaze",
                      "reversal", "coaching", "focusblast", "superpower", "scaryface"]
TIKI_TM_BIG = ["earthquake", "gigaimpact", "hyperbeam", "irontail", "stoneedge"]
TIKI_LEARN = [(1, "tackle"), (1, "leer"), (4, "rocksmash"), (8, "doublekick"), (12, "machpunch"), (16, "lowkick"),
              (20, "feint"), (24, "jumpkick"), (28, "megakick"), (32, "bulkup")]
TIKI = dict(male=0.75, egg_groups=["field", "human_like"], friendship=50, abilities=["ironfist", "reckless", "h:scrappy"],
            ability_names="Iron Fist / Reckless / Scrappy (hidden)")

SPECIES.update({
    "tikimp": {
        "dex": 3037, "name": "Tikimp", "line": "tiki", "types": ["normal", "fighting"], **TIKI,
        "stats": stats(55, 75, 45, 35, 45, 70), "ev": evs(attack=1), "catch": 150, "exp": 64,
        "height": 6, "weight": 160, "shoulder": True, "walk": 0.35,
        "moves": TIKI_LEARN, "tm": TIKI_TM, "egg": ["counter", "fakeout", "vacuumwave", "encore", "tripleaxel"],
        "evolve": ("tikilla", 32, ["highjumpkick"]),
        "drops": [("minecraft:bone", "0-1", None), ("minecraft:bamboo", "0-2", None)],
        "entry": ("It paints its face like a skull to scare off bigger Pokémon, then kickboxes anything that isn't "
                  "scared. It practises its kicks on bamboo all day long and never seems to tire."),
        "spawns": [route_spawn("tikimp-jungle", "uncommon", "10-28", 4.0, ["#cobblemon:is_jungle", "#cobblemon:is_bamboo"]),
                   route_spawn("tikimp-island", "uncommon", "10-28", 3.0, ["#cobblemon:is_tropical_island", "#cobblemon:is_beach"])],
        "how": ["Wild: uncommon in jungles, bamboo jungles, beaches and tropical islands.", "Evolves into Tikilla at level 32."],
    },
    "tikilla": {
        "dex": 3038, "name": "Tikilla", "line": "tiki", "types": ["normal", "fighting"], **TIKI,
        "stats": stats(85, 125, 80, 50, 70, 95), "ev": evs(attack=2), "catch": 60, "exp": 175,
        "height": 20, "weight": 1450, "shoulder": False, "walk": 0.32,
        "moves": [(1, "highjumpkick")] + TIKI_LEARN + [(32, "highjumpkick"), (36, "tropkick"), (40, "megapunch"),
                                                      (44, "closecombat"), (50, "hammerarm"), (56, "gigaimpact")],
        "tm": TIKI_TM + TIKI_TM_BIG, "egg": ["counter", "fakeout", "vacuumwave", "encore", "tripleaxel"], "evolve": None,
        "drops": [("minecraft:bone", "1-2", None), ("minecraft:bamboo", "1-3", None)],
        "entry": ("Its fists have grown as big as tiki masks, and it carves faces into them to look fiercer. It leads "
                  "its troop with thundering kicks and shakes its great white mane to warn rivals away."),
        "spawns": [route_spawn("tikilla-jungle", "rare", "32-50", 1.5, ["#cobblemon:is_jungle", "#cobblemon:is_tropical_island"])],
        "how": ["Evolve Tikimp at level 32. It learns High Jump Kick when it evolves.", "Wild: rare in jungles and on tropical islands."],
    },
})
LINES["tiki"] = ["tikimp", "tikilla"]

# --- the sensing rodents: eyes always closed, they feel their way with long whiskers ------------------------------------

SENSE_TM = BASIC_TM + ["swift", "dig", "thief", "uturn", "takedown", "bodyslam", "doubleedge", "crunch", "superfang",
                       "endeavor", "charm", "faketears", "thunderwave", "shadowball", "irontail", "zenheadbutt",
                       "grassknot", "trailblaze", "thunderbolt", "icebeam", "hypervoice", "suckerpunch", "playrough"]
SENSE_TM_BIG = ["gigaimpact", "hyperbeam", "psychicfangs", "thunderfang", "icefang", "firefang"]
SENSE_LEARN = [(1, "tackle"), (1, "tailwhip"), (3, "foresight"), (6, "quickattack"), (9, "bite"), (12, "detect"),
               (15, "focusenergy"), (18, "hyperfang"), (21, "mindreader")]
SENSE = dict(male=0.5, egg_groups=["field"], friendship=70, abilities=["frisk", "anticipation", "h:hustle"],
             ability_names="Frisk / Anticipation / Hustle (hidden)", egg=["counter", "reversal", "finalgambit", "screech",
                                                                         "lastresort", "uproar"])

SPECIES.update({
    "mousense": {
        "dex": 3039, "name": "Mousense", "line": "sense", "types": ["normal"], **SENSE,
        "stats": stats(40, 50, 35, 35, 40, 75), "ev": evs(speed=1), "catch": 255, "exp": 51,
        "height": 3, "weight": 25, "shoulder": True, "walk": 0.4,
        "moves": SENSE_LEARN + [(24, "crunch"), (27, "superfang"), (31, "endeavor"), (35, "doubleedge")],
        "tm": SENSE_TM, "evolve": ("sensarat", 22, ["suckerpunch"]),
        "drops": [("minecraft:string", "0-1", None), ("minecraft:wheat_seeds", "0-2", None)],
        "entry": ("Its eyes stay shut from the day it hatches. It feels its way about with its long whiskers, which can "
                  "pick up the flutter of a moth's wings across a meadow, so sneaking up on it is near impossible."),
        "spawns": [route_spawn("mousense-plains", "common", "2-22", 7.0, ["#cobblemon:is_plains", "#cobblemon:is_grassland"]),
                   route_spawn("mousense-forest", "common", "2-22", 5.0, ["#cobblemon:is_forest", "#cobblemon:is_hills"])],
        "how": ["Wild: common in plains, grasslands, forests and hills.", "Evolves into Sensarat at level 22."],
    },
    "sensarat": {
        "dex": 3040, "name": "Sensarat", "line": "sense", "types": ["normal"], **SENSE,
        "stats": stats(70, 85, 65, 50, 70, 105), "ev": evs(speed=2), "catch": 127, "exp": 145,
        "height": 6, "weight": 140, "shoulder": False, "walk": 0.38,
        "moves": [(1, "suckerpunch")] + SENSE_LEARN + [(22, "suckerpunch"), (26, "crunch"), (31, "superfang"),
                                                      (36, "endeavor"), (41, "doubleedge"), (47, "lastresort")],
        "tm": SENSE_TM + SENSE_TM_BIG, "evolve": None,
        "drops": [("minecraft:string", "1-2", None), ("minecraft:wheat_seeds", "0-3", None), ("cobblemon:silk_scarf", None, 2.5)],
        "entry": ("It sweeps its long whiskers through the dark like feelers and senses an attack before it comes, "
                  "striking first. It never opens its eyes; those who have seen them say they are as bright as stars."),
        "spawns": [route_spawn("sensarat-plains", "uncommon", "22-40", 2.5, ["#cobblemon:is_plains", "#cobblemon:is_forest"])],
        "how": ["Evolve Mousense at level 22. It learns Sucker Punch when it evolves.", "Wild: uncommon in plains and forests."],
    },
})
LINES["sense"] = ["mousense", "sensarat"]

# --- the crown moose ----------------------------------------------------------------------------------------------------

MOOSE_TM = BASIC_TM + ["bodyslam", "doubleedge", "takedown", "earthquake", "bulldoze", "stompingtantrum",
                       "highhorsepower", "rockslide", "stoneedge", "rocktomb", "ironhead", "wildcharge", "zenheadbutt",
                       "bulkup", "swordsdance", "smartstrike", "megahorn", "scaryface", "endeavor", "trailblaze",
                       "surf", "icywind", "hypervoice", "gigaimpact", "hyperbeam", "reversal", "outrage"]

SPECIES.update({
    "gigantler": {
        "dex": 3041, "name": "Gigantler", "line": "gigantler", "types": ["normal"],
        "male": 0.5, "egg_groups": ["field"], "friendship": 50, "catch": 45,
        "abilities": ["intimidate", "sapsipper", "h:sheerforce"],
        "ability_names": "Intimidate / Sap Sipper / Sheer Force (hidden)",
        "stats": stats(105, 120, 100, 50, 80, 70), "ev": evs(hp=1, attack=2), "exp": 186,
        "height": 24, "weight": 6200, "shoulder": False, "walk": 0.3,
        "moves": [(1, "tackle"), (1, "leer"), (5, "hornattack"), (10, "stomp"), (15, "headbutt"), (20, "takedown"),
                  (25, "hornleech"), (30, "bulkup"), (35, "zenheadbutt"), (40, "thrash"), (45, "headcharge"),
                  (50, "megahorn"), (56, "highhorsepower"), (62, "gigaimpact")],
        "tm": MOOSE_TM, "egg": ["doublekick", "curse", "roar", "bodypress", "workup", "rest"], "evolve": None,
        "drops": [("minecraft:leather", "1-3", None), ("minecraft:bone", "0-2", None), ("cobblemon:hard_stone", None, 5.0)],
        "entry": ("The antlers on its head grow back bigger every year, and an old bull's three crowns can span wider "
                  "than a cabin. Packs of predators turn back the moment it lowers its head, and travellers in the "
                  "northern woods take a glimpse of one as a sign of good fortune."),
        "spawns": [route_spawn("gigantler-taiga", "rare", "30-55", 2.0, ["#cobblemon:is_taiga", "#cobblemon:is_snowy_forest"]),
                   route_spawn("gigantler-swamp", "rare", "30-55", 1.0, ["#cobblemon:is_swamp", "#cobblemon:is_tundra"])],
        "how": ["Wild: rare in taigas and snowy forests, rarer in swamps and tundra."],
    },
})
LINES["gigantler"] = ["gigantler"]

# --- the hive of the fallen ---------------------------------------------------------------------------------------------

HIVE_TM = BASIC_TM + ["xscissor", "uturn", "bugbuzz", "leechlife", "lunge", "pounce", "skittersmack", "infestation",
                      "strugglebug", "shadowclaw", "shadowball", "phantomforce", "poltergeist", "hex", "willowisp",
                      "spite", "curse", "nightshade", "painsplit", "trickroom", "swordsdance", "knockoff", "nightslash",
                      "sludgebomb", "poisonjab", "gigadrain", "energyball", "seedbomb", "stoneedge", "ironhead",
                      "megahorn", "darkpulse", "scaryface", "gigaimpact", "hyperbeam", "ragepowder", "taunt",
                      "brickbreak", "agility", "smartstrike"]

SPECIES.update({
    "assoulsect": {
        "dex": 3042, "name": "Assoulsect", "line": "assoulsect", "types": ["bug", "ghost"],
        "male": -1, "egg_groups": ["undiscovered"], "friendship": 0, "catch": 25,
        "abilities": ["hivemind", "h:effectspore"],
        "ability_names": "Hive Mind (its own: a Bug-type foe's moves never harm it and strike the foe's side "
                         "instead) / Effect Spore (hidden)",
        "stats": stats(90, 125, 95, 85, 95, 70), "ev": evs(attack=2, hp=1), "exp": 270,
        "height": 22, "weight": 1666, "shoulder": False, "walk": 0.3,
        "moves": [(1, "astonish"), (1, "infestation"), (1, "strugglebug"), (6, "bugbite"), (11, "shadowsneak"),
                  (16, "stunspore"), (21, "leechlife"), (26, "hex"), (31, "xscissor"), (36, "shadowclaw"),
                  (41, "ragepowder"), (46, "phantomforce"), (51, "megahorn"), (56, "poltergeist"), (62, "memento")],
        "tm": HIVE_TM, "egg": [], "evolve": None,
        "drops": [("minecraft:spider_eye", "1-3", None), ("minecraft:brown_mushroom", "1-2", None),
                  ("minecraft:red_mushroom", "0-2", None), ("cobblemon:silver_powder", None, 10.0),
                  ("cobblemon:spell_tag", None, 5.0)],
        "entry": ("When thousands of Bug Pokémon perished, a fungus took root in what was left of them and wove "
                  "their souls into one mind. Their old heads and blades still twitch in its fog; any Bug Pokémon "
                  "that challenges it is pulled into the hive and turns on its own allies."),
        "spawns": [spawn("assoulsect-forest", "ultra-rare", "45-65", 1.0,
                         {"timeRange": "night", "biomes": ["minecraft:dark_forest", "#cobblemon:is_jungle",
                                                           "#cobblemon:is_swamp", "#cobblemon:is_mushroom"]}),
                   spawn("assoulsect-cave", "ultra-rare", "45-65", 0.6,
                         {"canSeeSky": False, "biomes": ["minecraft:lush_caves", "minecraft:deep_dark"]})],
        "how": ["Wild: very rare at night in dark forests, jungles, swamps and mushroom fields, and in lush caves "
                "and the deep dark."],
    },
})
LINES["assoulsect"] = ["assoulsect"]

# --- the brawler rodent -------------------------------------------------------------------------------------------------

CAPY_TM = BASIC_TM + ["earthquake", "bulldoze", "dig", "mudshot", "mudslap", "stompingtantrum", "highhorsepower",
                      "rockslide", "rocktomb", "stoneedge", "brickbreak", "closecombat", "bodypress", "drainpunch",
                      "bulkup", "lowkick", "lowsweep", "rocksmash", "superpower", "reversal", "crunch", "bodyslam",
                      "takedown", "doubleedge", "yawn", "amnesia", "surf", "waterpulse", "chillingwater", "endeavor",
                      "superfang", "gigaimpact", "hyperbeam", "heavyslam", "ironhead", "zenheadbutt", "bulldoze",
                      "sandstorm", "sunnyday", "raindance", "slackoff"]

SPECIES.update({
    "capybrute": {
        "dex": 3043, "name": "Capybrute", "line": "capybrute", "types": ["ground", "fighting"],
        "male": 0.5, "egg_groups": ["field"], "friendship": 70, "catch": 60,
        "abilities": ["guts", "thickfat", "h:unaware"],
        "ability_names": "Guts / Thick Fat / Unaware (hidden)",
        "stats": stats(110, 120, 105, 40, 75, 50), "ev": evs(hp=1, attack=2), "exp": 179,
        "height": 15, "weight": 1520, "shoulder": False, "walk": 0.24,
        "moves": [(1, "tackle"), (1, "mudslap"), (5, "rocksmash"), (9, "bite"), (13, "bulldoze"), (17, "yawn"),
                  (21, "brickbreak"), (25, "dig"), (29, "bodyslam"), (33, "superfang"), (37, "drainpunch"),
                  (41, "bulkup"), (45, "highhorsepower"), (50, "superpower"), (55, "closecombat"), (60, "earthquake")],
        "tm": CAPY_TM, "egg": ["slackoff", "curse", "rollout", "counter", "wideguard", "headbutt"], "evolve": None,
        "drops": [("minecraft:leather", "1-2", None), ("minecraft:wheat", "0-2", None), ("cobblemon:soft_sand", None, 4.0),
                  ("cobblemon:black_belt", None, 2.0)],
        "entry": ("It lounges by rivers as calmly as a boulder and lets other Pokémon nap on its back, but it digs "
                  "burrows through solid rock with those claws. Rile it and it charges with its head down, shrugging "
                  "off blows that would flatten a house."),
        "spawns": [route_spawn("capybrute-river", "uncommon", "25-45", 3.0, ["#cobblemon:is_river", "#cobblemon:is_swamp",
                                                                              "#cobblemon:is_savanna"]),
                   route_spawn("capybrute-hills", "uncommon", "25-45", 2.0, ["#cobblemon:is_hills", "#cobblemon:is_mountain",
                                                                              "#cobblemon:is_highlands"])],
        "how": ["Wild: uncommon by rivers, in swamps and savannas, and in hills, mountains and highlands."],
    },
})
LINES["capybrute"] = ["capybrute"]

# --- the ancient paradox of Sudowoodo -----------------------------------------------------------------------------------

ROT_TM = BASIC_TM + ["dragonclaw", "outrage", "dragonpulse", "dragontail", "scaleshot", "breakingswipe", "dracometeor",
                     "xscissor", "uturn", "lunge", "pounce", "leechlife", "bugbuzz", "megahorn", "skittersmack",
                     "woodhammer", "hornleech", "seedbomb", "bulletseed", "trailblaze", "energyball", "gigadrain",
                     "rockslide", "stoneedge", "rocktomb", "earthquake", "bulldoze", "stompingtantrum", "highhorsepower",
                     "suckerpunch", "crunch", "poisonfang", "irontail", "headsmash", "bodyslam", "takedown",
                     "doubleedge", "coil", "glare", "swordsdance", "taunt", "gigaimpact", "hyperbeam", "sunnyday"]

SPECIES.update({
    "writhingrot": {
        "dex": 3044, "name": "Writhing Rot", "line": "writhingrot", "types": ["bug", "dragon"],
        "male": -1, "egg_groups": ["undiscovered"], "friendship": 0, "catch": 10, "labels": ["paradox"],
        "abilities": ["protosynthesis"],
        "ability_names": "Protosynthesis",
        "stats": stats(95, 135, 105, 70, 75, 90), "ev": evs(attack=3), "exp": 285, "growth": "slow",
        "height": 24, "weight": 1820, "shoulder": False, "walk": 0.28,
        "moves": [(1, "wrap"), (1, "leer"), (1, "infestation"), (7, "bugbite"), (14, "dragonbreath"),
                  (21, "glare"), (28, "rockslide"), (35, "lunge"), (42, "dragonclaw"), (49, "suckerpunch"),
                  (56, "coil"), (63, "woodhammer"), (70, "firstimpression"), (77, "outrage"), (84, "headsmash")],
        "tm": ROT_TM, "egg": [], "evolve": None,
        "drops": [("minecraft:stick", "2-4", None), ("minecraft:oak_log", "0-1", None), ("minecraft:bone_meal", "1-3", None),
                  ("cobblemon:dragon_fang", None, 5.0)],
        "entry": ("An ancient Pokémon said to be the distant past of Sudowoodo, described in an old expedition "
                  "journal. Its log body is only a shell: the real Pokémon is the pale, writhing thing that lives "
                  "inside it, and it lunges out on a long neck to snatch prey."),
        "spawns": [spawn("writhingrot-forest", "ultra-rare", "50-70", 1.0,
                         {"canSeeSky": True, "biomes": ["minecraft:old_growth_birch_forest", "minecraft:old_growth_pine_taiga",
                                                        "minecraft:old_growth_spruce_taiga", "minecraft:dark_forest",
                                                        "#cobblemon:is_jungle"]})],
        "how": ["Wild: very rare in old-growth forests and taigas, dark forests and jungles."],
    },
})
LINES["writhingrot"] = ["writhingrot"]

# --- the pigs in a blanket ----------------------------------------------------------------------------------------------

BLANKET = dict(male=0.5, egg_groups=["field"], friendship=70, abilities=["thickfat", "gluttony", "h:cheekpouch"],
               ability_names="Thick Fat / Gluttony / Cheek Pouch (hidden)")
BLANKET_TM = BASIC_TM + ["bodyslam", "takedown", "doubleedge", "headbutt", "zenheadbutt", "mudslap", "mudshot",
                         "bulldoze", "dig", "yawn", "amnesia", "stockpile", "swallow", "spitup", "rollout",
                         "defensecurl", "playrough", "charm", "bite", "crunch", "heatwave", "sunnyday", "endeavor",
                         "hypervoice", "slackoff", "workup"]
BLANKET_TM_FLY = ["aerialace", "airslash", "acrobatics", "fly", "tailwind", "uturn", "roost", "bravebird",
                  "hurricane", "dualwingbeat", "gigaimpact", "hyperbeam", "defog"]
BLANKET_EARLY = [(1, "tackle"), (1, "tailwhip"), (4, "defensecurl"), (7, "mudslap"), (10, "rollout"), (13, "bite"),
                 (16, "headbutt"), (19, "stockpile"), (19, "swallow"), (22, "yawn")]

SPECIES.update({
    "wrapiglet": {
        "dex": 3045, "name": "Wrapiglet", "line": "blanket", "types": ["normal"], **BLANKET,
        "stats": stats(60, 55, 65, 35, 45, 40), "ev": evs(defence=1), "catch": 190, "exp": 64,
        "height": 6, "weight": 105, "shoulder": False, "walk": 0.2,
        "moves": BLANKET_EARLY + [(25, "bodyslam"), (29, "amnesia"), (33, "rest"), (37, "doubleedge")],
        "tm": BLANKET_TM, "egg": ["bellydrum", "curse", "slackoff", "wish", "counter"],
        "evolve": ("croissoar", 26, ["gust"]),
        "drops": [("minecraft:bread", "1-2", None), ("minecraft:porkchop", "0-1", None), ("minecraft:wheat", "0-2", None)],
        "entry": ("It wraps itself in a soft blanket of dough as soon as it hatches and naps in it the whole day long. "
                  "The dough bakes golden in the sun, and it smells so good that Pokémon follow it around."),
        "spawns": [route_spawn("wrapiglet-plains", "common", "4-24", 5.0, ["#cobblemon:is_plains", "#cobblemon:is_grassland"]),
                   spawn("wrapiglet-village", "uncommon", "4-24", 3.0,
                         {"canSeeSky": True, "biomes": ["#cobblemon:is_overworld"], "structures": ["#minecraft:village"]})],
        "how": ["Wild: common in plains and grasslands, uncommon in villages.", "Evolves into Croissoar at level 26."],
    },
    "croissoar": {
        "dex": 3046, "name": "Croissoar", "line": "blanket", "types": ["normal", "flying"], **BLANKET,
        "stats": stats(90, 90, 80, 60, 70, 95), "ev": evs(speed=2), "catch": 75, "exp": 172,
        "height": 13, "weight": 380, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": [(1, "gust")] + BLANKET_EARLY + [(26, "gust"), (30, "wingattack"), (34, "bodyslam"),
                                                  (38, "airslash"), (42, "tailwind"), (47, "doubleedge"),
                                                  (52, "bravebird"), (58, "hurricane")],
        "tm": BLANKET_TM + BLANKET_TM_FLY, "egg": ["bellydrum", "curse", "slackoff", "wish", "counter"], "evolve": None,
        "drops": [("minecraft:bread", "1-3", None), ("minecraft:porkchop", "1-2", None), ("minecraft:feather", "0-1", None)],
        "entry": ("Its blanket of dough rises and bakes into a great flaky paraglider. It leaps off hilltops and rides "
                  "the warm air for miles, steering with its ears, and leaves a trail of buttery crumbs behind it."),
        "spawns": [route_spawn("croissoar-hills", "uncommon", "26-45", 2.0, ["#cobblemon:is_hills", "#cobblemon:is_plains",
                                                                              "#cobblemon:is_highlands"])],
        "how": ["Evolve Wrapiglet at level 26. It learns Gust when it evolves.",
                "Wild: uncommon in hills, plains and highlands."],
    },
})
LINES["blanket"] = ["wrapiglet", "croissoar"]

# --- the minnow fossil --------------------------------------------------------------------------------------------------

MINNOW = dict(male=0.875, egg_groups=["water_2", "mineral"], friendship=50,
              abilities=["swiftswim", "shellarmor", "h:rattled"],
              ability_names="Swift Swim / Shell Armor / Rattled (hidden)", labels=["fossil"])
MINNOW_TM = BASIC_TM + ["surf", "waterfall", "liquidation", "aquatail", "waterpulse", "chillingwater", "raindance",
                        "rockslide", "rocktomb", "stoneedge", "rockblast", "ancientpower", "stealthrock", "sandstorm",
                        "irondefense", "ironhead", "bite", "crunch", "icefang", "takedown", "doubleedge", "uturn",
                        "flipturn", "dive", "whirlpool", "icywind", "bodypress"]
MINNOW_EARLY = [(1, "watergun"), (1, "harden"), (5, "bubble"), (9, "rockthrow"), (13, "aquajet"), (17, "bite"),
                (21, "ancientpower"), (25, "rocktomb"), (29, "aquatail"), (33, "irondefense")]

SPECIES.update({
    "minnolith": {
        "dex": 3047, "name": "Minnolith", "line": "minnow", "types": ["rock", "water"], **MINNOW,
        "stats": stats(45, 50, 70, 35, 45, 55), "ev": evs(defence=1), "catch": 45, "exp": 71,
        "height": 4, "weight": 75, "shoulder": False, "walk": 0.2, "aquatic": True,
        "moves": MINNOW_EARLY + [(37, "rockslide"), (41, "liquidation")],
        "tm": MINNOW_TM, "egg": ["aquaring", "mudshot", "screech", "flail", "brine"],
        "evolve": ("placofin", 38, ["headsmash"]),
        "drops": [("minecraft:clay_ball", "1-2", None), ("minecraft:cod", "0-1", None), ("cobblemon:hard_stone", None, 5.0)],
        "entry": ("A tiny fish that swam in rivers long before any other Pokémon. Its round body is wrapped in thin "
                  "plates of armour, and schools of them darted through the shallows like scattered pebbles."),
        "spawns": [],
        "how": ["Revive a Minnow Fossil at a Restoration Tank. Minnow Fossils are found by brushing the suspicious "
                "gravel of fossil beds on the bottoms of rivers and swamps.", "Evolves into Placofin at level 38."],
    },
    "placofin": {
        "dex": 3048, "name": "Placofin", "line": "minnow", "types": ["rock", "water"], **MINNOW,
        "stats": stats(70, 105, 115, 55, 70, 80), "ev": evs(defence=2), "catch": 45, "exp": 173,
        "height": 14, "weight": 640, "shoulder": False, "walk": 0.25, "aquatic": True,
        "moves": [(1, "headsmash")] + MINNOW_EARLY + [(38, "headsmash"), (42, "rockslide"), (46, "liquidation"),
                                                      (51, "stoneedge"), (56, "wavecrash")],
        "tm": MINNOW_TM + ["gigaimpact", "hyperbeam", "hydropump", "rockpolish"], "egg": ["aquaring", "mudshot", "screech", "flail", "brine"],
        "evolve": None,
        "drops": [("minecraft:clay_ball", "1-3", None), ("minecraft:flint", "0-2", None), ("cobblemon:hard_stone", None, 8.0)],
        "entry": ("Its bullet-shaped head is armoured like a battering ram. It crept along ancient riverbeds on its little "
                  "legs, and when it charged, the force of it could crack the stones of the riverbank."),
        "spawns": [],
        "how": ["Evolve Minnolith at level 38. It learns Head Smash when it evolves."],
    },
})
LINES["minnow"] = ["minnolith", "placofin"]

# --- the eurypterid fossil (sea scorpions) ------------------------------------------------------------------------------

EURY = dict(male=0.875, egg_groups=["water_3", "bug"], friendship=50,
            abilities=["swiftswim", "battlearmor", "h:toughclaws"],
            ability_names="Swift Swim / Battle Armor / Tough Claws (hidden)", labels=["fossil"])
EURY_TM = BASIC_TM + ["xscissor", "uturn", "leechlife", "lunge", "pounce", "bugbite", "skittersmack", "furycutter",
                      "surf", "waterfall", "liquidation", "aquatail", "waterpulse", "razorshell", "chillingwater",
                      "raindance", "flipturn", "dive", "whirlpool", "swordsdance", "knockoff", "poisonjab",
                      "rockslide", "ancientpower", "stoneedge", "irondefense", "metalclaw", "crunch", "slash",
                      "brickbreak", "agility"]
EURY_EARLY = [(1, "scratch"), (1, "watergun"), (1, "harden"), (5, "furycutter"), (9, "bubblebeam"), (13, "bugbite"),
              (17, "aquajet"), (21, "metalclaw"), (25, "razorshell"), (29, "xscissor"), (33, "swordsdance")]

SPECIES.update({
    "scorpaddle": {
        "dex": 3049, "name": "Scorpaddle", "line": "eurypterid", "types": ["bug", "water"], **EURY,
        "stats": stats(50, 80, 70, 40, 45, 70), "ev": evs(attack=1), "catch": 45, "exp": 71,
        "height": 4, "weight": 62, "shoulder": False, "walk": 0.22, "aquatic": True,
        "moves": EURY_EARLY + [(37, "liquidation"), (41, "leechlife")],
        "tm": EURY_TM, "egg": ["aquaring", "screech", "flail", "knockoff", "crabhammer"],
        "evolve": ("pterygant", 40, ["crabhammer"]),
        "drops": [("minecraft:prismarine_shard", "0-1", None), ("minecraft:flint", "0-1", None),
                  ("cobblemon:mystic_water", None, 4.0)],
        "entry": ("A sea scorpion from the oldest oceans. It rows along the sea floor with its paddles and holds "
                  "its tail spike up like a warning, though the spike was only ever for show."),
        "spawns": [],
        "how": ["Revive a Telson Fossil at a Restoration Tank. Telson Fossils are found by brushing the suspicious "
                "gravel of fossil beds on the sea floor.", "Evolves into Pterygant at level 40."],
    },
    "pterygant": {
        "dex": 3050, "name": "Pterygant", "line": "eurypterid", "types": ["bug", "water"], **EURY,
        "stats": stats(75, 120, 100, 55, 70, 75), "ev": evs(attack=2), "catch": 45, "exp": 173,
        "height": 19, "weight": 1450, "shoulder": False, "walk": 0.3, "aquatic": True,
        "moves": [(1, "crabhammer")] + EURY_EARLY + [(40, "crabhammer"), (44, "leechlife"), (48, "liquidation"),
                                                     (53, "firstimpression"), (58, "wavecrash")],
        "tm": EURY_TM + ["gigaimpact", "hyperbeam", "hydropump", "megahorn"],
        "egg": ["aquaring", "screech", "flail", "knockoff", "crabhammer"], "evolve": None,
        "drops": [("minecraft:prismarine_shard", "1-2", None), ("minecraft:flint", "0-2", None),
                  ("cobblemon:mystic_water", None, 8.0)],
        "entry": ("The largest sea scorpion that ever lived. It swept its great paddles to chase down prey in "
                  "the ancient seas, and nothing that swam could outlast it."),
        "spawns": [],
        "how": ["Evolve Scorpaddle at level 40. It learns Crabhammer when it evolves."],
    },
})
LINES["eurypterid"] = ["scorpaddle", "pterygant"]

# --- the opossum mother and her joeys -----------------------------------------------------------------------------------

POSSUM_TM = BASIC_TM + ["charm", "playrough", "dazzlinggleam", "drainingkiss", "mistyterrain", "bodyslam", "takedown",
                        "doubleedge", "headbutt", "bite", "crunch", "uturn", "helpinghand", "endeavor", "faketears",
                        "hypervoice", "swift", "irontail", "thief", "knockoff", "dig", "shadowball", "psychic",
                        "calmmind", "reflect", "lightscreen", "trailblaze"]
POSSUM_EARLY = [(1, "tackle"), (1, "tailwhip"), (4, "babydolleyes"), (8, "quickattack"), (12, "playnice"),
                (16, "covet"), (20, "charm"), (24, "takedown"), (28, "wish")]

SPECIES.update({
    "obubby": {
        "dex": 3051, "name": "Obubby", "line": "possum", "types": ["normal"], "male": 0.0,
        "egg_groups": ["field", "fairy"], "friendship": 100, "abilities": ["pickup", "cutecharm", "h:friendguard"],
        "ability_names": "Pickup / Cute Charm / Friend Guard (hidden)",
        "stats": stats(55, 40, 45, 35, 45, 35), "ev": evs(hp=1), "catch": 200, "exp": 55,
        "height": 4, "weight": 32, "shoulder": True, "walk": 0.22,
        "moves": POSSUM_EARLY + [(32, "lastresort"), (36, "playrough")],
        "tm": POSSUM_TM, "egg": ["fakeout", "lifedew", "afteryou", "yawn", "followme"],
        "evolve": ("mumossum", 30, ["joeyslingshot"]),
        "drops": [("minecraft:white_wool", "0-1", None), ("minecraft:pink_dye", "0-1", None)],
        "entry": ("It clings to its mother's back for weeks after it is born, hugging its own long tail when it gets "
                  "scared. When something startles it, it flops over and plays dead, curl of hair and all."),
        "spawns": [route_spawn("obubby-forest", "common", "3-25", 4.0, ["#cobblemon:is_forest", "#cobblemon:is_plains"],
                               timeRange="night")],
        "how": ["Wild: common in forests and plains at night.", "Evolves into Mumossum at level 30, and learns "
                "Joey Slingshot when it does."],
    },
    "mumossum": {
        "dex": 3052, "name": "Mumossum", "line": "possum", "types": ["normal", "fairy"], "male": 0.0,
        "egg_groups": ["field", "fairy"], "friendship": 100, "abilities": ["cutecharm", "healer", "h:friendguard"],
        "ability_names": "Cute Charm / Healer / Friend Guard (hidden)",
        "stats": stats(105, 70, 80, 75, 95, 50), "ev": evs(hp=2), "catch": 90, "exp": 168,
        "height": 13, "weight": 410, "shoulder": False, "walk": 0.26,
        "moves": [(1, "joeyslingshot")] + POSSUM_EARLY + [(30, "joeyslingshot"), (34, "lifedew"),
                                                          (38, "bodyslam"), (42, "dazzlinggleam"), (46, "softboiled"),
                                                          (51, "moonblast"), (56, "doubleedge")],
        "tm": POSSUM_TM + ["gigaimpact", "hyperbeam", "moonblast"], "egg": ["fakeout", "lifedew", "afteryou", "yawn",
                                                                            "followme"],
        "evolve": None,
        "drops": [("minecraft:white_wool", "1-2", None), ("minecraft:pink_dye", "0-2", None),
                  ("cobblemon:silk_scarf", None, 3.0)],
        "entry": ("It carries a half dozen of its babies wherever it goes. When something threatens them it plucks "
                  "the bravest ones off its back and slings them at the enemy with its tail; they come straight back "
                  "to it, very pleased with themselves."),
        "spawns": [route_spawn("mumossum-forest", "uncommon", "30-50", 1.5, ["#cobblemon:is_forest", "#cobblemon:is_plains"],
                               timeRange="night")],
        "how": ["Evolve Obubby at level 30. It learns Joey Slingshot when it evolves.",
                "Wild: uncommon in forests and plains at night."],
    },
})
LINES["possum"] = ["obubby", "mumossum"]

# --- the energy golem that takes the type of the tuft it holds -------------------------------------------------------------

import tufts as _tufts                                          # noqa: E402

AETHER_TM = BASIC_TM + ["swift", "hypervoice", "bodyslam", "takedown", "doubleedge", "headbutt", "zenheadbutt",
                        "brickbreak", "icepunch", "firepunch", "thunderpunch", "drainpunch", "machpunch", "bulletpunch",
                        "shadowpunch", "rockslide", "ironhead", "irondefense", "calmmind", "nastyplot", "bulkup",
                        "flamethrower", "thunderbolt", "icebeam", "energyball", "psychic", "shadowball", "darkpulse",
                        "dragonpulse", "flashcannon", "sludgebomb", "earthpower", "airslash", "bugbuzz", "dazzlinggleam",
                        "powergem", "surf", "triattack", "helpinghand", "trailblaze", "reflect", "lightscreen"]

SPECIES.update({
    "aetherim": {
        "dex": 3053, "name": "Aetherim", "line": "aetherim", "types": ["normal"], "male": -1,
        "egg_groups": ["mineral"], "friendship": 70, "catch": 120,
        "abilities": ["adaptability", "h:levitate"], "ability_names": "Adaptability / Levitate (hidden)",
        "stats": stats(70, 80, 80, 80, 80, 80), "ev": evs(hp=1, defence=1, special_defence=1), "exp": 160,
        "height": 5, "weight": 120, "shoulder": True, "walk": 0.28, "fly": True,
        "forms": _tufts.forms(),
        "moves": [(1, "tackle"), (1, "growl"), (5, "swift"), (9, "headbutt"), (13, "cometpunch"), (17, "helpinghand"),
                  (21, "triattack"), (25, "bulletpunch"), (29, "calmmind"), (33, "hypervoice"), (38, "revelationdance"),
                  (44, "bodyslam"), (50, "hyperbeam")],
        "tm": AETHER_TM, "egg": [], "evolve": None,
        "drops": [("minecraft:white_wool", "0-1", None), ("minecraft:amethyst_shard", "0-1", None),
                  ("cobblemon:silk_scarf", None, 3.0)],
        "entry": ("A little golem of pure energy that shapes a body around a pearl. Give it a tuft of hair charged "
                  "with a type's energy and it soaks it up, glowing that type's colour and becoming that type."),
        "spawns": [route_spawn("aetherim-hills", "rare", "20-40", 1.0, ["#cobblemon:is_hills", "#cobblemon:is_mountain",
                                                                         "#cobblemon:is_highlands"])],
        "how": ["Wild: rare in hills, mountains and highlands.",
                "Give it an elemental Tuft (or the matching wool, or a feather for Flying) in its cosmetic slot and it "
                "becomes that type."],
    },
})
LINES["aetherim"] = ["aetherim"]

# --- the ink line: blot, inkwell, ink titan -----------------------------------------------------------------------------

INK = dict(male=0.5, egg_groups=["amorphous", "mineral"], friendship=50,
           abilities=["liquidooze", "stickyhold", "h:clearbody"],
           ability_names="Liquid Ooze / Sticky Hold / Clear Body (hidden)", growth="slow")
INK_TM = BASIC_TM + ["waterpulse", "surf", "scald", "chillingwater", "raindance", "darkpulse", "snarl", "nightslash",
                     "knockoff", "thief", "taunt", "nastyplot", "foulplay", "suckerpunch", "flashcannon",
                     "ironhead", "irondefense", "steelbeam", "metalclaw", "smartstrike", "shadowball", "sludgebomb",
                     "gunkshot", "acidspray", "haze", "toxic", "confuseray", "painsplit", "brickbreak", "xscissor"]
INK_TM_BIG = ["earthquake", "hammerarm", "crunch", "throatchop", "gigaimpact", "hyperbeam", "hydropump", "outrage",
              "heavyslam", "stoneedge", "powerwhip"]
INK_EARLY = [(1, "watergun"), (1, "smokescreen"), (4, "metalclaw"), (8, "octazooka"), (12, "pursuit"), (16, "bite"),
             (20, "mirrorshot"), (24, "nightslash"), (28, "ironhead")]

SPECIES.update({
    "incl": {
        "dex": 3054, "name": "Incl", "line": "ink", "types": ["water", "steel"], **INK,
        "stats": stats(40, 45, 55, 50, 45, 35), "ev": evs(defence=1), "catch": 45, "exp": 60,
        "height": 4, "weight": 30, "shoulder": True, "walk": 0.22,
        "moves": INK_EARLY + [(32, "darkpulse")],
        "tm": INK_TM, "egg": ["acidarmor", "spite", "memento", "aquaring", "destinybond"],
        "evolve": ("incwell", 30, ["darkpulse"]),
        "drops": [("minecraft:ink_sac", "1-2", None), ("minecraft:iron_nugget", "0-2", None)],
        "entry": ("A drop of ink that came to life on the page of an old letter. The silver pen nib it wears as a face "
                  "is sharp, and it scribbles angry lines on anything that bothers it."),
        "spawns": [route_spawn("incl-village", "rare", "10-30", 1.5, ["#cobblemon:is_overworld"],
                               structures=["#minecraft:village"], timeRange="night"),
                   spawn("incl-cave", "rare", "10-30", 1.0, {"canSeeSky": False, "biomes": ["minecraft:deep_dark",
                                                                                          "minecraft:dripstone_caves"]})],
        "how": ["Wild: rare at night in villages, and in deep-dark and dripstone caves.",
                "Evolves into Incwell at level 30."],
    },
    "incwell": {
        "dex": 3055, "name": "Incwell", "line": "ink", "types": ["dark", "steel"], **INK,
        "stats": stats(60, 75, 80, 70, 65, 50), "ev": evs(attack=1, defence=1), "catch": 45, "exp": 144,
        "height": 13, "weight": 290, "shoulder": False, "walk": 0.25,
        "moves": [(1, "darkpulse")] + INK_EARLY + [(30, "darkpulse"), (34, "knockoff"), (38, "flashcannon"),
                                                   (43, "foulplay"), (48, "nastyplot")],
        "tm": INK_TM, "egg": ["acidarmor", "spite", "memento", "aquaring", "destinybond"],
        "evolve": ("calligrimm", 50, ["crunch"]),
        "drops": [("minecraft:ink_sac", "2-3", None), ("minecraft:glass_bottle", "0-1", None),
                  ("minecraft:iron_nugget", "1-3", None)],
        "entry": ("It lives in an inkwell it found in an abandoned study and never leaves it. At night it rises out "
                  "of the well and writes threats on the walls with the tip of its nib."),
        "spawns": [],
        "how": ["Evolve Incl at level 30. It learns Dark Pulse when it evolves.", "Evolves into Calligrimm at level 50."],
    },
    "calligrimm": {
        "dex": 3056, "name": "Calligrimm", "line": "ink", "types": ["dark", "steel"], **INK,
        "stats": stats(100, 125, 110, 90, 85, 50), "ev": evs(attack=3), "catch": 25, "exp": 270,
        "height": 70, "weight": 9990, "shoulder": False, "walk": 0.22,
        "moves": [(1, "crunch")] + INK_EARLY + [(50, "crunch"), (55, "throatchop"), (60, "steelbeam"),
                                                 (65, "hammerarm"), (70, "foulplay")],
        "tm": INK_TM + INK_TM_BIG, "egg": ["acidarmor", "spite", "memento", "aquaring", "destinybond"],
        "evolve": None,
        "drops": [("minecraft:ink_sac", "4-8", None), ("minecraft:glass", "1-3", None), ("minecraft:iron_ingot", "1-3", None),
                  ("cobblemon:black_glasses", None, 8.0)],
        "entry": ("A titan of living ink, tall as a castle tower. The shards of its shattered inkwell became its fangs, "
                  "and old tales say whatever it writes with its claws comes true, so kingdoms once begged it never "
                  "to write their names."),
        "spawns": [],
        "how": ["Evolve Incwell at level 50. It learns Crunch when it evolves."],
    },
})
LINES["ink"] = ["incl", "incwell", "calligrimm"]

# --- the hollow steed (the CobbleEffort Mudbray's evolution) --------------------------------------------------------------

STEED_TM = BASIC_TM + ["flamethrower", "fireblast", "overheat", "flareblitz", "firefang", "flamecharge", "willowisp",
                       "heatwave", "burningjealousy", "temperflare", "sunnyday", "darkpulse", "nightslash", "foulplay",
                       "crunch", "lashout", "suckerpunch", "throatchop", "snarl", "taunt", "torment", "faketears",
                       "payback", "knockoff", "scaryface", "hex", "highhorsepower", "stompingtantrum", "bodyslam",
                       "doubleedge", "takedown", "closecombat", "lowkick", "irontail", "bulkup", "roar", "gigaimpact",
                       "hyperbeam", "endeavor", "agility", "spite"]

SPECIES.update({
    "ignitemare": {
        "dex": 3057, "name": "Ignitemare", "line": "steed", "types": ["dark", "fire"],
        "male": 0.5, "egg_groups": ["field"], "friendship": 50, "catch": 60,
        "abilities": ["moody", "flamebody", "h:intimidate"],
        "ability_names": "Moody / Flame Body / Intimidate (hidden)",
        "stats": stats(85, 120, 80, 85, 75, 80), "ev": evs(attack=2), "exp": 182,
        "height": 22, "weight": 1450, "shoulder": False, "walk": 0.34,
        "pre": "mudbray cobbleeffortian",
        "moves": [(1, "tackle"), (1, "leer"), (1, "bite"), (1, "faketears"), (1, "flamecharge"), (1, "ember"),
                  (8, "assurance"), (12, "doublekick"), (16, "snarl"), (20, "firefang"), (24, "nightslash"),
                  (28, "willowisp"), (34, "lashout"), (38, "flamethrower"), (42, "burningjealousy"), (46, "foulplay"),
                  (51, "flareblitz"), (56, "suckerpunch"), (62, "overheat")],
        "tm": STEED_TM, "egg": [], "evolve": None,
        "drops": [("minecraft:bone", "1-3", None), ("minecraft:charcoal", "0-2", None),
                  ("cobblemon:charcoal_stick", None, 5.0), ("cobblemon:black_glasses", None, 2.5)],
        "entry": ("When the CobbleEffort Mudbray's sulking turns to rage, its body burns away to a shadow round its "
                  "bones. It gallops through badlands at night, snorting fire, and its hollow skull glows red with "
                  "the grudges it refuses to let go."),
        "spawns": [],
        "how": ["Evolve the CobbleEffort Mudbray at level 30. It learns Flame Charge when it evolves."],
    },
})
LINES["steed"] = ["ignitemare"]

# --- the colossus (Regigigas evolved) -------------------------------------------------------------------------------------

COLOSSUS_TM = BASIC_TM + ["ancientpower", "block", "bulldoze", "drainpunch", "earthpower", "firepunch", "focuspunch",
                          "gigaimpact", "gravity", "highhorsepower", "hyperbeam", "icepunch", "icywind", "ironhead",
                          "knockoff", "rockslide", "rocksmash", "shockwave", "stompingtantrum", "stoneedge",
                          "superpower", "thunderpunch", "earthquake", "bodyslam", "doubleedge", "bodypress",
                          "heavyslam", "closecombat", "meteormash", "brickbreak", "bulkup", "wideguard", "trickroom",
                          "megapunch", "megakick", "headlongrush", "hammerarm", "dynamicpunch", "zenheadbutt"]

SPECIES.update({
    "regideity": {
        "dex": 3058, "name": "Regideity", "line": "colossus", "types": ["normal"],
        "male": -1, "egg_groups": ["undiscovered"], "friendship": 0, "catch": 3, "labels": ["legendary"],
        "abilities": ["pressure", "h:sheerforce"],
        "ability_names": "Pressure / Sheer Force (hidden)",
        "stats": stats(120, 180, 130, 95, 130, 105), "ev": evs(attack=3), "exp": 340, "growth": "slow",
        "height": 210, "weight": 9999, "shoulder": False, "walk": 0.22,
        "pre": "cobblemon:regigigas",
        # Regigigas evolves when a Nether Star is used on it (an item worthy of a god of giants)
        "evolves_from": ("cobblemon:regigigas", "regigigas_regideity",
                         {"id": "regigigas_regideity", "variant": "item_interact", "result": "cobbleeffort:regideity",
                          "consumeHeldItem": False, "learnableMoves": ["meteormash"],
                          "requiredContext": "minecraft:nether_star"}),
        "moves": [(1, "pound"), (1, "confuseray"), (1, "foresight"), (1, "dizzypunch"), (1, "cometpunch"),
                  (1, "meteormash"), (6, "payback"), (12, "facade"), (18, "stomp"), (24, "protect"), (30, "knockoff"),
                  (36, "megapunch"), (42, "bodypress"), (48, "wideguard"), (54, "zenheadbutt"), (60, "heavyslam"),
                  (66, "hammerarm"), (72, "gigaimpact"), (78, "crushgrip"), (84, "headlongrush"), (90, "judgment")],
        "tm": COLOSSUS_TM, "egg": [], "evolve": None,
        "drops": [("minecraft:gold_ingot", "2-6", None), ("minecraft:emerald", "1-3", None),
                  ("minecraft:diamond", "0-2", None), ("cobblemon:hard_stone", None, 25.0)],
        "entry": ("Legends say it towed the continents into place with its six arms and stood astride the seas while "
                  "it worked. When it walks, mountains shake as if in an earthquake, and the halos round its ring "
                  "shine brighter the longer it has been awake."),
        "spawns": [],
        "how": ["Use a Nether Star on a Regigigas. It learns Meteor Mash when it evolves."],
    },
})
LINES["colossus"] = ["regideity"]

# --- the pinbirds (they nest on rocky crags: tools/newmons/nests.py) ------------------------------------------------------

NEST = [f"{MOD}:pinbird_nest"]
NEST_BIOMES = ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:savanna",
               "minecraft:savanna_plateau", "minecraft:windswept_savanna", "minecraft:windswept_hills",
               "minecraft:windswept_gravelly_hills"]
PIN = dict(egg_groups=["flying"], male=0.5, friendship=70, abilities=["keeneye", "bigpecks", "h:cheekpouch"],
           ability_names="Keen Eye / Big Pecks / Cheek Pouch (hidden)")
PIN_TM = BASIC_TM + ["aerialace", "airslash", "acrobatics", "uturn", "dualwingbeat", "tailwind", "roost", "defog",
                     "fly", "steelwing", "pluck", "swift", "thief", "agility", "bodyslam", "doubleedge", "hypervoice",
                     "endeavor", "workup", "sunnyday", "raindance", "takedown", "featherdance"]
PIN_TM_BIG = ["bravebird", "heatwave", "hurricane", "gigaimpact", "hyperbeam", "skyattack"]
PIN_EARLY = [(1, "tackle"), (1, "growl"), (4, "peck"), (8, "quickattack"), (12, "gust"), (15, "featherdance")]
NEST_HOW = "at pinbird nests (rocky crags topped with a great hay nest, in plains, meadows, savannas and windswept hills)"

SPECIES.update({
    "pinlet": {
        "dex": 3059, "name": "Pinlet", "line": "pinbird", "types": ["normal", "flying"], **PIN,
        "stats": stats(45, 50, 40, 30, 35, 60), "ev": evs(speed=1), "catch": 255, "exp": 50,
        "height": 4, "weight": 20, "shoulder": True, "walk": 0.24,
        "moves": PIN_EARLY + [(18, "pluck"), (21, "wingattack")],
        "tm": PIN_TM, "egg": ["mirrormove", "bravebird", "pursuit", "uproar", "roost", "doublehit"],
        "evolve": ("pinnant", 16, ["wingattack"]),
        "drops": [("minecraft:feather", "1-2", None), ("minecraft:wheat_seeds", "0-2", None)],
        "entry": ("Pinlet chicks wait in the nest with their beaks wide open, shrieking until a Pinnant drops a berry "
                  "in. The star-shaped glints in their eyes fade as they grow up."),
        "spawns": [route_spawn("pinlet-nest", "common", "3-15", 12.0, NEST_BIOMES, structures=NEST)],
        "how": [f"Wild: common {NEST_HOW}.", "Evolves into Pinnant at level 16."],
    },
    "pinnant": {
        "dex": 3060, "name": "Pinnant", "line": "pinbird", "types": ["normal", "flying"], **PIN,
        "stats": stats(65, 75, 60, 45, 50, 85), "ev": evs(speed=2), "catch": 120, "exp": 125,
        "height": 9, "weight": 230, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": PIN_EARLY + [(1, "wingattack"), (20, "pluck"), (24, "agility"), (28, "aerialace"), (32, "roost"),
                              (36, "airslash")],
        "tm": PIN_TM, "egg": [], "evolve": ("pennacrest", 36, ["bravebird"]),
        "drops": [("minecraft:feather", "1-3", None), ("minecraft:sweet_berries", "0-2", None)],
        "entry": ("It trails its two long streamers like pennants as it flies between the crag and the berry bushes, "
                  "bringing food back for the chicks. Flocks tell each other apart by the bands on their streamers."),
        "spawns": [route_spawn("pinnant-nest", "uncommon", "16-32", 6.0, NEST_BIOMES, structures=NEST)],
        "how": ["Evolve Pinlet at level 16.", f"Wild: uncommon {NEST_HOW}.", "Evolves into Pennacrest at level 36."],
    },
    "pennacrest": {
        "dex": 3061, "name": "Pennacrest", "line": "pinbird", "types": ["normal", "flying"], **PIN,
        "stats": stats(90, 110, 80, 60, 75, 100), "ev": evs(attack=3), "catch": 45, "exp": 218,
        "height": 19, "weight": 600, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": PIN_EARLY + [(1, "wingattack"), (1, "bravebird"), (20, "pluck"), (24, "agility"), (28, "aerialace"),
                              (32, "roost"), (38, "airslash"), (42, "doubleedge"), (47, "tailwind"), (52, "bravebird"),
                              (58, "hurricane")],
        "tm": PIN_TM + PIN_TM_BIG, "egg": [], "evolve": None,
        "drops": [("minecraft:feather", "2-4", None), ("minecraft:hay_block", "0-1", None),
                  ("cobblemon:sharp_beak", None, 2.5)],
        "entry": ("The matriarch of a crag-top nest. It broods over the chicks with its broad crest spread like a "
                  "parasol to shade them, and drives off any intruder with a storm of beating wings and lashing "
                  "streamers."),
        "spawns": [route_spawn("pennacrest-nest", "rare", "36-52", 3.0, NEST_BIOMES, structures=NEST)],
        "how": ["Evolve Pinnant at level 36. It learns Brave Bird when it evolves.", f"Wild: rare {NEST_HOW}."],
    },
})
LINES["pinbird"] = ["pinlet", "pinnant", "pennacrest"]

# --- Lesbeon, an Eevee evolution (two female Eevee in a party) ------------------------------------------------------------

LESBEON_REQ = [{"variant": "properties", "target": "gender=female"}]
SPECIES.update({
    "lesbeon": {
        "dex": 3062, "name": "Lesbeon", "line": "lesbeon", "types": ["fairy", "fighting"],
        "male": 0.0, "egg_groups": ["field"], "friendship": 70, "catch": 45,
        "abilities": ["friendguard", "h:competitive"],
        "ability_names": "Friend Guard / Competitive (hidden)",
        "stats": stats(75, 105, 65, 100, 95, 85), "ev": evs(attack=1, special_attack=1), "exp": 184,
        "height": 9, "weight": 260, "shoulder": False, "walk": 0.34,
        "pre": "cobblemon:eevee",
        # a female Eevee with another female Eevee in the party can evolve (Cobblemon checks level-up evolutions
        # every second and offers them with the Evolve button); the second one can still evolve with a Lesbeon there
        "evolves_from": ("cobblemon:eevee", "eevee_lesbeon", [
            {"id": "eevee_lesbeon", "variant": "level_up", "result": "cobbleeffort:lesbeon", "consumeHeldItem": False,
             "learnableMoves": ["doublekick"],
             "requirements": LESBEON_REQ + [{"variant": "party_member", "target": "eevee gender=female", "contains": True}]},
            {"id": "eevee_lesbeon_pair", "variant": "level_up", "result": "cobbleeffort:lesbeon", "consumeHeldItem": False,
             "learnableMoves": ["doublekick"],
             "requirements": LESBEON_REQ + [{"variant": "party_member", "target": "cobbleeffort:lesbeon", "contains": True}]}]),
        "moves": [(1, "tackle"), (1, "tailwhip"), (1, "helpinghand"), (1, "growl"), (1, "covet"), (1, "copycat"),
                  (1, "swift"), (1, "bite"), (1, "babydolleyes"), (1, "doublekick"), (5, "sandattack"),
                  (10, "quickattack"), (15, "drainingkiss"), (20, "lowsweep"), (25, "dazzlinggleam"),
                  (30, "brickbreak"), (35, "bulkup"), (40, "playrough"), (45, "lastresort"), (50, "closecombat"),
                  (55, "moonblast")],
        "tm": BASIC_TM + ["dazzlinggleam", "playrough", "moonblast", "drainingkiss", "mistyterrain", "charm",
                          "brickbreak", "closecombat", "drainpunch", "bulkup", "lowsweep", "lowkick", "superpower",
                          "aurasphere", "focusblast", "vacuumwave", "helpinghand", "swift", "bodyslam", "doubleedge",
                          "takedown", "irontail", "shadowball", "calmmind", "lightscreen", "reflect", "wish",
                          "batonpass", "alluringvoice", "hypervoice", "gigaimpact", "hyperbeam"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:pink_dye", "1-2", None), ("cobblemon:love_sweet", None, 5.0)],
        "entry": ("Two Eevee that love each other evolve together into Lesbeon. It stays fiercely loyal to its "
                  "partner and protects her from anything, and the Venus marks that hang from its ears glow when "
                  "the two are close."),
        "spawns": [],
        "how": ["Put two female Eevee in your party: both get the chance to evolve into Lesbeon (accept it with the "
                "Evolve button; the second can still evolve after the first, with a Lesbeon in the party). It learns "
                "Double Kick when it evolves."],
    },
})
LINES["lesbeon"] = ["lesbeon"]

# --- Ibuprofeon, an Eevee evolution for an Eevee that survives a fight on 1 HP -------------------------------------------

IBU_CALLBACK = """'An Eevee that ends a battle on exactly 1 HP (having fought) gets the chance to evolve into Ibuprofeon.';
for_each(t.actor, c.players, {
  for_each(t.battle_pokemon, t.actor.battle_pokemon, {
    t.pokemon = t.battle_pokemon.original_pokemon;
    (t.battle_pokemon.has_faced_opponents && t.pokemon.current_hp == 1 && t.pokemon.matches('eevee')) ? {
      t.pokemon.apply('ibuprofeon_ready');
    };
  });
});
"""
SPECIES.update({
    "ibuprofeon": {
        "dex": 3063, "name": "Ibuprofeon", "line": "ibuprofeon", "types": ["poison", "normal"],
        "male": 0.875, "egg_groups": ["field"], "friendship": 70, "catch": 45,
        "abilities": ["sturdy", "h:regenerator"],
        "ability_names": "Sturdy / Regenerator (hidden)",
        "stats": stats(110, 65, 110, 60, 120, 60), "ev": evs(special_defence=2), "exp": 184,
        "height": 9, "weight": 270, "shoulder": False, "walk": 0.3,
        "pre": "cobblemon:eevee",
        # the battle_ended callback flags an Eevee that survived on 1 HP; Cobblemon checks level-up evolutions every
        # second and offers them as a choice (the Evolve button), so the flagged Eevee gets the chance to evolve
        "evolves_from": ("cobblemon:eevee", "eevee_ibuprofeon",
                         {"id": "eevee_ibuprofeon", "variant": "level_up", "result": "cobbleeffort:ibuprofeon",
                          "consumeHeldItem": False, "learnableMoves": ["lifedew"],
                          "requirements": [{"variant": "properties", "target": "ibuprofeon_ready"}]}),
        "data_files": {
            "cobbleeffort/species_features/ibuprofeon_ready.json":
                {"keys": ["ibuprofeon_ready"], "type": "flag", "isAspect": False, "default": False},
            "cobbleeffort/species_feature_assignments/ibuprofeon_ready.json":
                {"pokemon": ["eevee"], "features": ["ibuprofeon_ready"]},
            "cobblemon/callbacks/battle_ended/cobbleeffort_ibuprofeon.molang": IBU_CALLBACK,
        },
        "moves": [(1, "tackle"), (1, "tailwhip"), (1, "helpinghand"), (1, "growl"), (1, "covet"), (1, "copycat"),
                  (1, "swift"), (1, "bite"), (1, "babydolleyes"), (1, "lifedew"), (5, "sandattack"),
                  (10, "quickattack"), (15, "poisonfang"), (20, "endure"), (25, "venoshock"), (30, "recover"),
                  (35, "toxic"), (40, "sludgebomb"), (45, "healbell"), (50, "painsplit"), (55, "lastresort")],
        "tm": BASIC_TM + ["sludgebomb", "venoshock", "toxicspikes", "poisonjab", "gunkshot", "acidspray", "clearsmog",
                          "recover", "painsplit", "healbell", "wish", "protect", "endure", "reflect", "lightscreen",
                          "calmmind", "irondefense", "bodyslam", "doubleedge", "takedown", "swift", "shadowball",
                          "batonpass", "yawn", "haze", "bodypress", "gigaimpact", "hyperbeam"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:paper", "1-2", None), ("cobblemon:potion", None, 10.0), ("cobblemon:full_heal", None, 2.5)],
        "entry": ("An Eevee that hung on at the very edge of fainting evolved into Ibuprofeon. It is never without its "
                  "bandages, and the pills on its tail ease the pain of any Pokémon that curls up beside it."),
        "spawns": [],
        "how": ["An Eevee that ends a battle on exactly 1 HP gets the chance to evolve into Ibuprofeon (accept it with "
                "the Evolve button). It learns Life Dew when it evolves."],
    },
})
LINES["ibuprofeon"] = ["ibuprofeon"]

# --- the imitator crabs: claws that imitate the heads of dangerous Pokémon ------------------------------------------------

CRAB = dict(egg_groups=["bug", "water_3"], male=0.5, friendship=50)
CRAB_TM = BASIC_TM + ["xscissor", "bugbite", "lunge", "pounce", "furycutter", "crunch", "firefang", "icefang",
                      "thunderfang", "psychicfangs", "rocktomb", "rockslide", "stoneedge", "irondefense", "swordsdance",
                      "knockoff", "bulldoze", "dig", "surf", "liquidation", "razorshell", "brine", "endure", "scaryface",
                      "brickbreak"]
CRAB_EARLY = [(1, "harden"), (1, "bite"), (4, "bugbite"), (8, "rockthrow"), (12, "furycutter"), (16, "rocktomb"),
              (20, "crunch")]
CRAB_ROCKY = ["#cobblemon:is_beach", "minecraft:stony_shore", "minecraft:mangrove_swamp", "#cobblemon:is_badlands"]

SPECIES.update({
    "tyrucrab": {
        "dex": 3064, "name": "Tyrucrab", "line": "mimic_crab", "types": ["bug", "rock"], **CRAB, "catch": 120,
        "abilities": ["strongjaw", "shellarmor", "h:intimidate"],
        "ability_names": "Strong Jaw / Shell Armor / Intimidate (hidden)",
        "stats": stats(50, 75, 70, 30, 40, 45), "ev": evs(attack=1), "exp": 66,
        "height": 5, "weight": 120, "shoulder": False, "walk": 0.28,
        "moves": CRAB_EARLY + [(24, "xscissor"), (28, "rockslide")],
        "tm": CRAB_TM, "egg": ["dragontail", "ancientpower", "crabhammer", "metalclaw", "rockpolish"],
        "evolve": ("crabgron", 32, ["metalclaw"]),
        "drops": [("minecraft:bone", "0-2", None), ("minecraft:orange_dye", "0-1", None)],
        "entry": ("To scare off predators it holds up its right claw, which has grown into the shape of a fearsome "
                  "tyrannosaur's head. The jaw snaps like a pincer, and a Tyrucrab that fools a foe once never stops "
                  "boasting about it."),
        "spawns": [route_spawn("tyrucrab-shore", "uncommon", "8-24", 3.0, CRAB_ROCKY)],
        "how": ["Wild: uncommon on beaches, stony shores, mangrove swamps and in badlands.",
                "Evolves into Crabgron at level 32."],
    },
    "crabgron": {
        "dex": 3065, "name": "Crabgron", "line": "mimic_crab", "types": ["bug", "steel"], **CRAB, "catch": 60,
        "abilities": ["strongjaw", "shellarmor", "h:intimidate"],
        "ability_names": "Strong Jaw / Shell Armor / Intimidate (hidden)",
        "stats": stats(65, 100, 100, 40, 55, 55), "ev": evs(attack=1, defence=1), "exp": 158,
        "height": 10, "weight": 860, "shoulder": False, "walk": 0.3,
        "moves": CRAB_EARLY + [(1, "metalclaw"), (24, "xscissor"), (28, "rockslide"), (32, "ironhead"),
                               (38, "irondefense"), (44, "heavyslam")],
        "tm": CRAB_TM + ["ironhead", "heavyslam", "flashcannon", "steelbeam", "metalclaw", "smartstrike"],
        "egg": [], "evolve": ("primaclaw", 50, ["headlongrush"]),
        "drops": [("minecraft:iron_nugget", "1-4", None), ("cobblemon:metal_coat", None, 2.5)],
        "entry": ("As it grows, its claw takes on the look of an iron-armoured beast, horns and all. Crabgron bang "
                  "their helmet-claws on rocks at night so that anything listening believes a whole herd is near."),
        "spawns": [route_spawn("crabgron-shore", "rare", "32-45", 1.0, CRAB_ROCKY)],
        "how": ["Evolve Tyrucrab at level 32. It learns Metal Claw when it evolves.",
                "Wild: rare on beaches, stony shores, mangrove swamps and in badlands.",
                "Evolves into Primaclaw at level 50."],
    },
    "primaclaw": {
        "dex": 3066, "name": "Primaclaw", "line": "mimic_crab", "types": ["bug", "ground"], **CRAB, "catch": 30,
        "abilities": ["primalmimicry", "strongjaw", "h:intimidate"],
        "ability_names": "Primal Mimicry (its own: its Water-type moves get the same-type bonus too) / Strong Jaw / "
                         "Intimidate (hidden)",
        "stats": stats(85, 130, 115, 65, 75, 65), "ev": evs(attack=3), "exp": 248, "growth": "medium_slow",
        "height": 16, "weight": 1800, "shoulder": False, "walk": 0.28,
        "moves": CRAB_EARLY + [(1, "metalclaw"), (1, "headlongrush"), (24, "xscissor"), (28, "rockslide"),
                               (32, "ironhead"), (38, "crabhammer"), (44, "earthquake"), (50, "headlongrush"),
                               (56, "wavecrash"), (62, "precipiceblades")],
        "tm": CRAB_TM + ["earthquake", "highhorsepower", "earthpower", "stompingtantrum", "wavecrash", "hydropump",
                         "aquatail", "ironhead", "heavyslam", "gigaimpact", "hyperbeam", "sandstorm", "raindance",
                         "sunnyday"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:iron_ingot", "0-2", None), ("minecraft:prismarine_shard", "1-3", None),
                  ("minecraft:red_sand", "1-3", None)],
        "entry": ("Its two claws imitate the ancient titans of land and sea so perfectly that the sight of a Primaclaw "
                  "on the shore once sent whole villages fleeing inland. The crab itself is tiny, hiding between the "
                  "two great heads."),
        "spawns": [],
        "how": ["Evolve Crabgron at level 50. It learns Headlong Rush when it evolves."],
    },
})
LINES["mimic_crab"] = ["tyrucrab", "crabgron", "primaclaw"]

# the dragon beetle line (Larvorub, Ovarupa, Dracarabo): art by @artworks218_ (Ozera region), names kept, used with the
# creator's permission
SCARAB = dict(egg_groups=["bug", "dragon"], male=0.5, friendship=50, growth="medium_slow",
              abilities=["swarm", "shedskin", "h:strongjaw"], ability_names="Swarm / Shed Skin / Strong Jaw (hidden)")
SCARAB_TM = BASIC_TM + ["xscissor", "bugbite", "lunge", "pounce", "strugglebug", "bugbuzz", "uturn", "stringshot",
                        "dragonclaw", "dragonpulse", "dragontail", "breakingswipe", "scaleshot", "crunch", "irondefense",
                        "bulldoze", "rocktomb", "rockslide", "bodyslam", "sunnyday"]
SCARAB_TM_ADULT = ["megahorn", "firstimpression", "outrage", "earthquake", "stoneedge", "dragondance", "swordsdance",
                   "firefang", "thunderfang", "psychicfangs", "dracometeor", "scaryface", "gigaimpact", "hyperbeam"]
SCARAB_EARLY = [(1, "tackle"), (1, "stringshot"), (5, "bugbite"), (9, "dragonbreath"), (13, "bite"),
                (17, "strugglebug")]
SCARAB_WILD = ["#cobblemon:is_jungle", "#cobblemon:is_savanna"]
SPECIES.update({
    "larvorub": {
        "dex": 3067, "name": "Larvorub", "line": "dragon_beetle", "types": ["bug"], **SCARAB, "catch": 190,
        "stats": stats(50, 60, 55, 30, 35, 30), "ev": evs(defence=1), "exp": 58,
        "height": 5, "weight": 62, "shoulder": False, "walk": 0.16,
        "moves": SCARAB_EARLY + [(20, "harden")],
        "tm": SCARAB_TM, "egg": ["dragondance", "firstimpression", "stickyweb", "megahorn"],
        "evolve": ("ovarupa", 20, ["harden"]),
        "drops": [("minecraft:string", "0-2", None), ("cobblemon:silver_powder", None, 2.5)],
        "entry": ("It tunnels through rotting logs on the jungle floor and eats anything softer than its horns. When "
                  "something startles it, it rears up and points those horns, though they are still too soft to hurt."),
        "spawns": [route_spawn("larvorub-wild", "common", "3-20", 8.0, SCARAB_WILD)],
        "how": ["Wild: common in jungles and savannas.", "Evolves into Ovarupa at level 20."],
    },
    "ovarupa": {
        "dex": 3068, "name": "Ovarupa", "line": "dragon_beetle", "types": ["bug", "dragon"], **SCARAB, "catch": 90,
        "stats": stats(65, 70, 115, 45, 75, 30), "ev": evs(defence=2), "exp": 145,
        "height": 10, "weight": 480, "shoulder": False, "walk": 0.06,
        "moves": SCARAB_EARLY + [(1, "harden"), (20, "harden"), (24, "irondefense"), (28, "dragontail"),
                                 (33, "xscissor"), (38, "dragonpulse")],
        "tm": SCARAB_TM, "egg": [], "evolve": ("dracarabo", 42, ["dragonrush"]),
        "drops": [("minecraft:orange_dye", "1-2", None), ("minecraft:string", "0-2", None)],
        "entry": ("Inside its hard orange casing its whole body is being rebuilt. The horn grows out through the top "
                  "first, and anything that pokes the casing gets jabbed with it."),
        "spawns": [route_spawn("ovarupa-wild", "uncommon", "20-38", 2.5, SCARAB_WILD)],
        "how": ["Evolve Larvorub at level 20. It learns Harden when it evolves.",
                "Wild: uncommon in jungles and savannas.", "Evolves into Dracarabo at level 42."],
    },
    "dracarabo": {
        "dex": 3069, "name": "Dracarabo", "line": "dragon_beetle", "types": ["bug", "dragon"], **SCARAB, "catch": 45,
        "stats": stats(90, 135, 105, 65, 80, 70), "ev": evs(attack=3), "exp": 270,
        "height": 18, "weight": 1250, "shoulder": False, "walk": 0.3,
        "moves": SCARAB_EARLY + [(1, "harden"), (1, "dragonrush"), (24, "irondefense"), (28, "dragontail"),
                                 (33, "xscissor"), (38, "crunch"), (42, "dragonrush"), (48, "megahorn"),
                                 (54, "dragondance"), (60, "outrage")],
        "tm": SCARAB_TM + SCARAB_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("cobblemon:dragon_fang", None, 5.0), ("minecraft:orange_dye", "1-3", None),
                  ("minecraft:bone", "0-1", None)],
        "entry": ("The horn on its head grows into the shape of a dragon's skull, jaws and all. It charges with the "
                  "jaws wide open, and the snap when they close can be heard right across the savanna."),
        "spawns": [route_spawn("dracarabo-wild", "rare", "42-55", 0.6, ["#cobblemon:is_jungle"])],
        "how": ["Evolve Ovarupa at level 42. It learns Dragon Rush when it evolves.", "Wild: rare in jungles."],
    },
})
LINES["dragon_beetle"] = ["larvorub", "ovarupa", "dracarabo"]

# the whip crab line (Whippersnap, Karkuttle): Zorneo region commission art by @RedmondJake, names kept (Zorneo region
# designs are used with the creators' permission)
WHIP = dict(egg_groups=["bug", "water_3"], male=0.5, friendship=50, growth="medium_fast",
            abilities=["longreach", "keeneye", "h:sniper"],
            ability_names="Long Reach / Keen Eye / Sniper (hidden)")
WHIP_TM = BASIC_TM + ["xscissor", "bugbite", "lunge", "pounce", "strugglebug", "bugbuzz", "uturn", "furycutter",
                      "leechlife", "skittersmack", "nightslash", "knockoff", "thief", "falseswipe", "swordsdance",
                      "agility", "crunch", "poisonjab", "brickbreak", "aerialace", "liquidation", "razorshell"]
WHIP_TM_ADULT = ["firstimpression", "megahorn", "throatchop", "leechlife", "gigaimpact", "hyperbeam", "crabhammer"]
WHIP_EARLY = [(1, "leer"), (1, "furycutter"), (5, "bugbite"), (9, "quickattack"), (13, "feint"),
              (17, "skittersmack"), (21, "nightslash"), (25, "xscissor")]
WHIP_WILD = ["#cobblemon:is_swamp", "#cobblemon:is_jungle", "#cobblemon:is_beach"]
SPECIES.update({
    "whippersnap": {
        "dex": 3070, "name": "Whippersnap", "line": "whip_crab", "types": ["bug"], **WHIP, "catch": 160,
        "stats": stats(45, 65, 55, 30, 40, 65), "ev": evs(speed=1), "exp": 62,
        "height": 4, "weight": 38, "shoulder": False, "walk": 0.3,
        "moves": WHIP_EARLY + [(29, "agility")],
        "tm": WHIP_TM, "egg": ["firstimpression", "pounce", "aquajet", "razorshell"],
        "evolve": ("karkuttle", 30, ["lunge"]),
        "drops": [("minecraft:string", "0-1", None), ("minecraft:cyan_dye", "0-1", None)],
        "entry": ("It looks half asleep, but its whip antennae never stop feeling around it. The moment one brushes "
                  "prey, its little claws snap shut faster than the eye can follow."),
        "spawns": [route_spawn("whippersnap-wild", "uncommon", "6-28", 4.0, WHIP_WILD)],
        "how": ["Wild: uncommon in swamps, jungles and on beaches.", "Evolves into Karkuttle at level 30."],
    },
    "karkuttle": {
        "dex": 3071, "name": "Karkuttle", "line": "whip_crab", "types": ["bug"], **WHIP, "catch": 60,
        "stats": stats(70, 115, 85, 45, 65, 105), "ev": evs(attack=1, speed=1), "exp": 168,
        "height": 15, "weight": 520, "shoulder": False, "walk": 0.38,
        "moves": WHIP_EARLY + [(1, "lunge"), (30, "lunge"), (36, "leechlife"), (42, "firstimpression"),
                               (48, "throatchop"), (54, "swordsdance"), (60, "megahorn")],
        "tm": WHIP_TM + WHIP_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:string", "1-2", None), ("minecraft:cyan_dye", "1-2", None),
                  ("minecraft:orange_dye", "0-1", None)],
        "entry": ("Its legs are so long it can step over a fallen log without slowing down. It waits with its eyes "
                  "half shut and its antennae spread wide, then lashes out with its claws from three body lengths "
                  "away."),
        "spawns": [route_spawn("karkuttle-wild", "rare", "30-45", 1.0, WHIP_WILD)],
        "how": ["Evolve Whippersnap at level 30. It learns Lunge when it evolves.",
                "Wild: rare in swamps, jungles and on beaches."],
    },
})
LINES["whip_crab"] = ["whippersnap", "karkuttle"]

# the A. Fakemon starter trio (grass wolves, fire bats, water fish): art of the A. Fakemon fanpage, names kept; their own
# page on the starter screen (FAKEMON_STARTERS)
TRIO = dict(male=0.875, catch=45, friendship=50, growth="medium_slow")
WOLF = dict(TRIO, egg_groups=["field", "grass"], abilities=["overgrow", "h:scrappy"],
            ability_names="Overgrow / Scrappy (hidden)")
BAT = dict(TRIO, egg_groups=["flying", "field"], abilities=["blaze", "h:infiltrator"],
           ability_names="Blaze / Infiltrator (hidden)")
FISH = dict(TRIO, egg_groups=["water_1", "water_2"], abilities=["torrent", "h:protean"],
            ability_names="Torrent / Protean (hidden)")
WOLF_TM = BASIC_TM + ["bulletseed", "seedbomb", "energyball", "gigadrain", "grassknot", "trailblaze", "solarbeam",
                      "sunnyday", "grassyterrain", "leafblade", "crunch", "firefang", "thunderfang", "icefang",
                      "bodyslam", "dig", "rockslide", "bulkup", "brickbreak", "roar", "howl", "uturn", "charm"]
WOLF_TM_ADULT = ["closecombat", "drainpunch", "superpower", "hammerarm", "poweruppunch", "focusblast", "leafstorm",
                 "woodhammer", "gigaimpact", "hyperbeam", "frenzyplant", "earthquake", "stoneedge"]
WOLF_EARLY = [(1, "tackle"), (1, "growl"), (4, "leafage"), (8, "bite"), (12, "razorleaf"), (15, "howl")]
BAT_TM = BASIC_TM + ["ember", "flamecharge", "flamethrower", "fireblast", "willowisp", "sunnyday", "heatwave",
                     "aerialace", "airslash", "acrobatics", "uturn", "fly", "roost", "defog", "tailwind", "leechlife",
                     "bite", "crunch", "nastyplot", "shadowball", "darkpulse", "confuseray", "screech"]
BAT_TM_ADULT = ["overheat", "hurricane", "bravebird", "gigaimpact", "hyperbeam", "blastburn", "mysticalfire",
                "hex", "nightshade"]
BAT_EARLY = [(1, "scratch"), (1, "leer"), (4, "ember"), (8, "gust"), (12, "bite"), (15, "flamecharge")]
FISH_TM = BASIC_TM + ["watergun", "waterpulse", "surf", "raindance", "chillingwater", "liquidation", "icefang",
                      "icebeam", "icywind", "crunch", "bite", "mudshot", "mudslap", "aquatail", "bulkup", "brickbreak",
                      "scaryface", "dive", "waterfall"]
FISH_TM_GROUND = ["bulldoze", "dig", "earthquake", "earthpower", "sandstorm", "stompingtantrum"]
FISH_TM_ADULT = ["hydropump", "wavecrash", "knockoff", "throatchop", "suckerpunch", "darkpulse", "nightslash",
                 "gigaimpact", "hyperbeam", "hydrocannon", "taunt", "foulplay"]
FISH_EARLY = [(1, "tackle"), (1, "leer"), (4, "watergun"), (8, "bite"), (12, "mudslap"), (15, "aquajet")]
STARTER_HOW = "One of the A. Fakemon starters: pick it at the starter screen (its own A. Fakemon page)."
SPECIES.update({
    "wigwoof": {
        "dex": 3072, "name": "Wigwoof", "line": "afakemon_wolf", "types": ["grass"], **WOLF,
        "stats": stats(50, 62, 45, 42, 45, 65), "ev": evs(speed=1), "exp": 62,
        "height": 5, "weight": 123, "shoulder": True, "walk": 0.32,
        "moves": WOLF_EARLY + [(17, "magicalleaf"), (20, "crunch"), (24, "leafblade"), (28, "bulkup")],
        "tm": WOLF_TM, "egg": ["playrough", "suckerpunch", "leechseed", "firefang"],
        "evolve": ("wolfevel", 16, ["doublekick"]),
        "drops": [("minecraft:wheat_seeds", "1-2", None), ("minecraft:yellow_dye", "0-1", None)],
        "entry": ("The blond tuft on its head is a clump of dry grass it never stops growing. It hides its eyes under "
                  "it when it is shy, and fluffs it up to look bigger when it wants to look tough."),
        "spawns": [route_spawn("wigwoof-wild", "ultra-rare", "5-15", 1.0, ["#cobblemon:is_forest", "#cobblemon:is_plains"])],
        "how": [STARTER_HOW, "Wild: very rare in forests and plains.", "Evolves into Wolfevel at level 16."],
    },
    "wolfevel": {
        "dex": 3073, "name": "Wolfevel", "line": "afakemon_wolf", "types": ["grass"], **WOLF,
        "stats": stats(65, 82, 60, 52, 58, 88), "ev": evs(speed=2), "exp": 142,
        "height": 13, "weight": 170, "shoulder": False, "walk": 0.36,
        "moves": WOLF_EARLY + [(1, "doublekick"), (16, "doublekick"), (20, "magicalleaf"), (24, "crunch"),
                               (28, "leafblade"), (32, "bulkup")],
        "tm": WOLF_TM, "egg": [], "evolve": ("lycanmoon", 36, ["drainpunch"]),
        "drops": [("minecraft:wheat_seeds", "1-3", None), ("minecraft:orange_dye", "0-1", None)],
        "entry": ("It has started walking on two legs and picks fights with anything bigger than itself, just to "
                  "prove it can. Its tail turns redder the angrier it gets."),
        "spawns": [],
        "how": ["Evolve Wigwoof at level 16. It learns Double Kick when it evolves.", "Evolves into Lycanmoon at level 36."],
    },
    "lycanmoon": {
        "dex": 3074, "name": "Lycanmoon", "line": "afakemon_wolf", "types": ["grass", "fighting"], **WOLF,
        "stats": stats(85, 125, 80, 65, 70, 105), "ev": evs(attack=3), "exp": 265,
        "height": 17, "weight": 1500, "shoulder": False, "walk": 0.38,
        "moves": WOLF_EARLY + [(1, "drainpunch"), (1, "powerwhip"), (16, "doublekick"), (20, "magicalleaf"),
                               (24, "crunch"), (28, "leafblade"), (32, "bulkup"), (36, "drainpunch"),
                               (42, "powerwhip"), (48, "closecombat"), (54, "woodhammer")],
        "tm": WOLF_TM + WOLF_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:vine", "1-3", None), ("minecraft:wheat_seeds", "1-3", None)],
        "entry": ("It ropes its opponents with a vine lasso and pulls them into the reach of its fists. Under a full "
                  "moon it howls so loudly that every Wigwoof for miles answers."),
        "spawns": [],
        "how": ["Evolve Wolfevel at level 36. It learns Drain Punch when it evolves."],
    },
    "sounflame": {
        "dex": 3075, "name": "Sounflame", "line": "afakemon_bat", "types": ["fire", "flying"], **BAT,
        "stats": stats(45, 50, 40, 60, 45, 69), "ev": evs(speed=1), "exp": 62,
        "height": 3, "weight": 75, "shoulder": True, "walk": 0.3, "fly": True,
        "moves": BAT_EARLY + [(17, "airslash"), (20, "leechlife"), (24, "flamethrower"), (28, "nastyplot")],
        "tm": BAT_TM, "egg": ["heatwave", "screech", "hypnosis", "nightshade"],
        "evolve": ("operbat", 16, ["confuseray"]),
        "drops": [("minecraft:blaze_powder", "0-1", None), ("minecraft:orange_dye", "0-1", None)],
        "entry": ("Its huge ears hear the crackle of a campfire from a mile away. It sneaks up to warm its wings by "
                  "the flames and steals the sparks to feed its own."),
        "spawns": [route_spawn("sounflame-wild", "ultra-rare", "5-15", 1.0,
                               ["#cobblemon:is_badlands", "#cobblemon:is_savanna", "#cobblemon:is_desert"])],
        "how": [STARTER_HOW, "Wild: very rare in badlands, savannas and deserts.", "Evolves into Operbat at level 16."],
    },
    "operbat": {
        "dex": 3076, "name": "Operbat", "line": "afakemon_bat", "types": ["fire", "flying"], **BAT,
        "stats": stats(60, 64, 55, 82, 60, 84), "ev": evs(special_attack=1, speed=1), "exp": 142,
        "height": 9, "weight": 100, "shoulder": False, "walk": 0.32, "fly": True,
        "moves": BAT_EARLY + [(1, "confuseray"), (16, "confuseray"), (20, "airslash"), (24, "leechlife"),
                              (28, "flamethrower"), (32, "nastyplot")],
        "tm": BAT_TM, "egg": [], "evolve": ("nosfiretu", 36, ["bitterblade"]),
        "drops": [("minecraft:blaze_powder", "0-2", None), ("minecraft:white_wool", "0-1", None)],
        "entry": ("It hides its face behind a golden mask and performs for anyone who will listen, singing in a "
                  "voice so high that windows crack. It never takes the mask off."),
        "spawns": [],
        "how": ["Evolve Sounflame at level 16. It learns Confuse Ray when it evolves.", "Evolves into Nosfiretu at level 36."],
    },
    "nosfiretu": {
        "dex": 3077, "name": "Nosfiretu", "line": "afakemon_bat", "types": ["fire", "flying"], **BAT,
        "stats": stats(78, 80, 70, 115, 82, 105), "ev": evs(special_attack=3), "exp": 265,
        "height": 18, "weight": 800, "shoulder": False, "walk": 0.34, "fly": True,
        "moves": BAT_EARLY + [(1, "bitterblade"), (16, "confuseray"), (20, "airslash"), (24, "leechlife"),
                              (28, "flamethrower"), (32, "nastyplot"), (36, "bitterblade"), (42, "hurricane"),
                              (48, "heatwave"), (54, "overheat")],
        "tm": BAT_TM + BAT_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:blaze_powder", "1-2", None), ("minecraft:gold_nugget", "1-3", None)],
        "entry": ("It wraps itself in its wings like a cape and stands perfectly still in the dark, until something "
                  "warm passes by. Then it drinks the heat from its prey, leaving it shivering."),
        "spawns": [],
        "how": ["Evolve Operbat at level 36. It learns Bitter Blade when it evolves."],
    },
    "fangfosh": {
        "dex": 3078, "name": "Fangfosh", "line": "afakemon_fish", "types": ["water"], **FISH,
        "stats": stats(50, 58, 50, 45, 46, 60), "ev": evs(attack=1), "exp": 62,
        "height": 2, "weight": 23, "shoulder": True, "walk": 0.24,
        "moves": FISH_EARLY + [(17, "chillingwater"), (20, "crunch"), (24, "aquatail"), (28, "scaryface")],
        "tm": FISH_TM, "egg": ["suckerpunch", "pursuit", "yawn", "aquaring"],
        "evolve": ("fishugly", 16, ["mudshot"]),
        "drops": [("minecraft:cod", "0-1", None), ("minecraft:bone_meal", "0-1", None)],
        "entry": ("It is always grinning like that, even when it is scared, which makes it very hard to tell what "
                  "it is feeling. It hops out of the water on its little legs to bite at ankles."),
        "spawns": [route_spawn("fangfosh-wild", "ultra-rare", "5-15", 1.0, ["#cobblemon:is_river", "#cobblemon:is_swamp"])],
        "how": [STARTER_HOW, "Wild: very rare by rivers and in swamps.", "Evolves into Fishugly at level 16."],
    },
    "fishugly": {
        "dex": 3079, "name": "Fishugly", "line": "afakemon_fish", "types": ["water", "ground"], **FISH,
        "stats": stats(68, 80, 72, 55, 60, 70), "ev": evs(attack=1, defence=1), "exp": 142,
        "height": 8, "weight": 60, "shoulder": False, "walk": 0.3,
        "moves": FISH_EARLY + [(1, "mudshot"), (16, "mudshot"), (20, "chillingwater"), (24, "crunch"),
                               (28, "bulldoze"), (32, "liquidation")],
        "tm": FISH_TM + FISH_TM_GROUND, "egg": [], "evolve": ("creepish", 36, ["throatchop"]),
        "drops": [("minecraft:cod", "0-2", None), ("minecraft:clay_ball", "0-2", None)],
        "entry": ("It wanders the riverbanks on its long fin-legs, staring at everything with its unblinking eyes. "
                  "It buries itself in the mud to sleep, with only its grin showing."),
        "spawns": [],
        "how": ["Evolve Fangfosh at level 16. It learns Mud Shot when it evolves.", "Evolves into Creepish at level 36."],
    },
    "creepish": {
        "dex": 3080, "name": "Creepish", "line": "afakemon_fish", "types": ["water", "dark"], **FISH,
        "stats": stats(88, 115, 85, 70, 75, 97), "ev": evs(attack=2, speed=1), "exp": 265,
        "height": 15, "weight": 900, "shoulder": False, "walk": 0.34,
        "moves": FISH_EARLY + [(1, "throatchop"), (16, "mudshot"), (20, "chillingwater"), (24, "crunch"),
                               (28, "liquidation"), (32, "scaryface"), (36, "throatchop"), (42, "knockoff"),
                               (48, "wavecrash"), (54, "suckerpunch")],
        "tm": FISH_TM + FISH_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:cod", "1-2", None), ("minecraft:ink_sac", "1-2", None)],
        "entry": ("It lurks in dark lagoons with only its frill above the water. When it spreads the frill and raises "
                  "its arms, even large Pokémon back away."),
        "spawns": [],
        "how": ["Evolve Fishugly at level 36. It learns Throat Chop when it evolves."],
    },
})
LINES["afakemon_wolf"] = ["wigwoof", "wolfevel", "lycanmoon"]
LINES["afakemon_bat"] = ["sounflame", "operbat", "nosfiretu"]
LINES["afakemon_fish"] = ["fangfosh", "fishugly", "creepish"]

# Phanturn: Lanturn's ghostly evolution (the user's art, artist and name not given; the name is ours)
SPECIES.update({
    "phanturn": {
        "dex": 3081, "name": "Phanturn", "line": "phantom_lure", "types": ["ghost", "electric"],
        "male": 0.5, "egg_groups": ["water_2"], "friendship": 50, "catch": 45, "growth": "slow",
        "abilities": ["voltabsorb", "cursedbody", "h:illuminate"],
        "ability_names": "Volt Absorb / Cursed Body / Illuminate (hidden)",
        "stats": stats(135, 60, 70, 115, 90, 70), "ev": evs(hp=2, special_attack=1), "exp": 250,
        "height": 16, "weight": 300, "shoulder": False, "walk": 0.3, "fly": True,
        "pre": "cobblemon:lanturn",
        # Lanturn evolves when a Reaper Cloth is used on it (Dusclops' ghostly evolution item)
        "evolves_from": ("cobblemon:lanturn", "lanturn_phanturn",
                         {"id": "lanturn_phanturn", "variant": "item_interact", "result": "cobbleeffort:phanturn",
                          "consumeHeldItem": False, "learnableMoves": ["hex"],
                          "requiredContext": "cobblemon:reaper_cloth"}),
        "moves": [(1, "astonish"), (1, "hex"), (1, "supersonic"), (1, "thunderwave"), (1, "spark"),
                  (1, "confuseray"), (6, "electroball"), (12, "bite"), (18, "nightshade"), (24, "charge"),
                  (30, "shadowball"), (36, "discharge"), (42, "crunch"), (48, "thunderbolt"), (54, "poltergeist"),
                  (60, "zapcannon")],
        "tm": BASIC_TM + ["thunderbolt", "thunder", "voltswitch", "electroball", "chargebeam", "discharge",
                          "wildcharge", "thunderfang", "electricterrain", "raindance", "shadowball", "hex",
                          "nightshade", "willowisp", "confuseray", "painsplit", "trick", "phantomforce",
                          "shadowclaw", "darkpulse", "crunch", "icebeam", "scald", "surf", "hydropump",
                          "dazzlinggleam", "gigaimpact", "hyperbeam"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:glow_ink_sac", "1-2", None), ("minecraft:gold_nugget", "1-3", None),
                  ("cobblemon:spell_tag", None, 5.0)],
        "entry": ("It drifts up out of the deep at night, trailing glowing pearls. Lost sailors follow the light of "
                  "its little golden lure, thinking it is a lantern on the shore, and are never seen again."),
        "spawns": [],
        "how": ["Use a Reaper Cloth on a Lanturn. It learns Hex when it evolves."],
    },
})
LINES["phantom_lure"] = ["phanturn"]

# Boracle and Sunflare: evolutions for Grumpig and Sunflora (the user's art, artists and names not given; names ours)
SPECIES.update({
    "boracle": {
        "dex": 3082, "name": "Boracle", "line": "fortune_pig", "types": ["psychic"],
        "male": 0.5, "egg_groups": ["field"], "friendship": 50, "catch": 45, "growth": "fast",
        "abilities": ["forewarn", "thickfat", "h:owntempo"],
        "ability_names": "Forewarn / Thick Fat / Own Tempo (hidden)",
        "stats": stats(100, 50, 80, 125, 130, 65), "ev": evs(special_attack=1, special_defence=2), "exp": 250,
        "height": 15, "weight": 1450, "shoulder": False, "walk": 0.3,
        "pre": "cobblemon:grumpig",
        # Grumpig evolves at level 45 or more while holding a Twisted Spoon (used up; permanent, like Happiny's)
        "evolves_from": ("cobblemon:grumpig", "grumpig_boracle",
                         {"id": "grumpig_boracle", "variant": "level_up", "result": "cobbleeffort:boracle",
                          "consumeHeldItem": True, "permanent": True, "learnableMoves": ["futuresight"],
                          "requirements": [{"variant": "level", "minLevel": 45},
                                           {"variant": "held_item", "itemCondition": "cobblemon:twisted_spoon"}]}),
        "moves": [(1, "splash"), (1, "futuresight"), (1, "psybeam"), (1, "teeterdance"), (5, "confusion"),
                  (10, "rest"), (15, "snore"), (20, "zenheadbutt"), (25, "powergem"), (30, "psychic"), (35, "bounce"),
                  (40, "calmmind"), (45, "futuresight"), (50, "storedpower"), (55, "psyshock"), (60, "trickroom")],
        "tm": BASIC_TM + ["psychic", "psyshock", "calmmind", "trickroom", "shadowball", "powergem", "dazzlinggleam",
                          "energyball", "focusblast", "icywind", "taunt", "trick", "lightscreen", "reflect",
                          "magicroom", "wonderroom", "nastyplot", "storedpower", "bodyslam", "bounce",
                          "gigaimpact", "hyperbeam", "expandingforce", "psychicterrain"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:amethyst_shard", "1-2", None), ("minecraft:porkchop", "0-1", None),
                  ("cobblemon:twisted_spoon", None, 2.5)],
        "entry": ("It gazes into its crystal ball and tells the fortunes of anyone who brings it food. Its "
                  "predictions are always right, though it is careful to say only the good ones out loud."),
        "spawns": [],
        "how": ["Level up a Grumpig at level 45 or higher while it holds a Twisted Spoon (the spoon is used up). "
                "It learns Future Sight when it evolves."],
    },
    "sunflare": {
        "dex": 3083, "name": "Sunflare", "line": "blaze_bloom", "types": ["grass", "fire"],
        "male": 0.5, "egg_groups": ["grass"], "friendship": 50, "catch": 60, "growth": "medium_slow",
        "abilities": ["solarpower", "chlorophyll", "h:drought"],
        "ability_names": "Solar Power / Chlorophyll / Drought (hidden)",
        "stats": stats(85, 80, 70, 130, 95, 65), "ev": evs(special_attack=3), "exp": 230,
        "height": 15, "weight": 220, "shoulder": False, "walk": 0.24,
        "pre": "cobblemon:sunflora",
        # Sunflora evolves when a Fire Stone is used on it
        "evolves_from": ("cobblemon:sunflora", "sunflora_sunflare",
                         {"id": "sunflora_sunflare", "variant": "item_interact", "result": "cobbleeffort:sunflare",
                          "consumeHeldItem": False, "learnableMoves": ["heatwave"],
                          "requiredContext": "cobblemon:fire_stone"}),
        "moves": [(1, "absorb"), (1, "growth"), (1, "heatwave"), (1, "ember"), (5, "megadrain"), (10, "flamecharge"),
                  (15, "razorleaf"), (20, "sunnyday"), (25, "gigadrain"), (30, "flamethrower"), (35, "petaldance"),
                  (40, "synthesis"), (45, "heatwave"), (50, "solarbeam"), (55, "leafstorm"), (60, "overheat")],
        "tm": BASIC_TM + ["solarbeam", "solarblade", "energyball", "gigadrain", "leafstorm", "grassknot", "sunnyday",
                          "flamethrower", "fireblast", "heatwave", "overheat", "willowisp", "earthpower",
                          "weatherball", "grassyterrain", "seedbomb", "bulletseed", "trailblaze", "flamecharge",
                          "dazzlinggleam", "gigaimpact", "hyperbeam"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:sunflower", "1-2", None), ("minecraft:wheat_seeds", "1-3", None),
                  ("minecraft:blaze_powder", "0-1", None)],
        "entry": ("On the hottest days of summer its petals burst into flame. It turns its burning face to follow the "
                  "sun across the sky and stores so much heat that it glows all through the night."),
        "spawns": [],
        "how": ["Use a Fire Stone on a Sunflora. It learns Heat Wave when it evolves."],
    },
})
LINES["fortune_pig"] = ["boracle"]
LINES["blaze_bloom"] = ["sunflare"]

# the second A. Fakemon starter trio (water monkeys, grass songbirds, fire dogs): art of the A. Fakemon fanpage
# (@a.fakemon), names and types from its art; their own page on the starter screen (FAKEMON_STARTERS_2)
MONKEY = dict(TRIO, egg_groups=["field", "water_1"], abilities=["torrent", "h:ironfist"],
              ability_names="Torrent / Iron Fist (hidden)")
SONG = dict(TRIO, egg_groups=["flying", "grass"], abilities=["overgrow", "h:punkrock"],
            ability_names="Overgrow / Punk Rock (hidden)")
DOG = dict(TRIO, egg_groups=["field"], abilities=["blaze", "h:strongjaw"],
           ability_names="Blaze / Strong Jaw (hidden)")
MONKEY_TM = BASIC_TM + ["watergun", "waterpulse", "surf", "raindance", "chillingwater", "liquidation", "aquatail",
                        "brickbreak", "bulkup", "drainpunch", "icepunch", "thunderpunch", "firepunch", "uturn",
                        "acrobatics", "knockoff", "taunt", "yawn", "bodyslam", "dig"]
MONKEY_TM_ADULT = ["closecombat", "hydropump", "wavecrash", "hammerarm", "focusblast", "superpower", "gigaimpact",
                   "hyperbeam", "hydrocannon", "bodypress", "slackoff"]
MONKEY_EARLY = [(1, "scratch"), (1, "leer"), (4, "watergun"), (8, "furyswipes"), (12, "bubblebeam"), (15, "workup")]
SONG_TM = BASIC_TM + ["bulletseed", "seedbomb", "energyball", "gigadrain", "grassknot", "trailblaze", "sunnyday",
                      "grassyterrain", "hypervoice", "round", "echoedvoice", "aerialace", "airslash", "acrobatics",
                      "uturn", "roost", "tailwind", "psychic", "psyshock", "calmmind", "dazzlinggleam", "charm"]
SONG_TM_ADULT = ["leafstorm", "solarbeam", "boomburst", "expandingforce", "futuresight", "hurricane", "gigaimpact",
                 "hyperbeam", "frenzyplant", "psychicterrain", "nastyplot"]
SONG_EARLY = [(1, "peck"), (1, "growl"), (4, "leafage"), (8, "sing"), (12, "magicalleaf"), (15, "disarmingvoice")]
DOG_TM = BASIC_TM + ["ember", "flamecharge", "flamethrower", "fireblast", "firefang", "willowisp", "sunnyday",
                     "crunch", "bite", "thunderfang", "firepunch", "thunderpunch", "bulkup", "roar", "howl",
                     "bodyslam", "playrough", "wildcharge", "dig", "uturn"]
DOG_TM_ADULT = ["flareblitz", "overheat", "shadowball", "shadowclaw", "phantomforce", "poltergeist", "hex",
                "nightshade", "gigaimpact", "hyperbeam", "blastburn", "heatwave", "psychicfangs", "closecombat"]
DOG_EARLY = [(1, "tackle"), (1, "growl"), (4, "ember"), (8, "bite"), (12, "flamewheel"), (15, "roar")]
STARTER2_HOW = "One of the second A. Fakemon trio's starters: pick it at the starter screen (its A. Fakemon II page)."
SPECIES.update({
    "brenkey": {
        "dex": 3084, "name": "Brenkey", "line": "afakemon_monkey", "types": ["water"], **MONKEY,
        "stats": stats(48, 60, 45, 45, 45, 66), "ev": evs(speed=1), "exp": 62,
        "height": 5, "weight": 98, "shoulder": True, "walk": 0.3,
        "moves": MONKEY_EARLY + [(17, "aquajet"), (20, "brickbreak"), (24, "waterpulse"), (28, "yawn")],
        "tm": MONKEY_TM, "egg": ["fakeout", "yawn", "aquaring", "machpunch"],
        "evolve": ("splakey", 16, ["machpunch"]),
        "drops": [("minecraft:bamboo", "1-2", None), ("minecraft:kelp", "0-1", None)],
        "entry": ("It sips water up through its bamboo straw and squirts it at anyone who bothers it. It acts tough, "
                  "but it would much rather be napping."),
        "spawns": [route_spawn("brenkey-wild", "ultra-rare", "5-15", 1.0, ["#cobblemon:is_jungle", "#cobblemon:is_beach"])],
        "how": [STARTER2_HOW, "Wild: very rare in jungles and on beaches.", "Evolves into Splakey at level 16."],
    },
    "splakey": {
        "dex": 3085, "name": "Splakey", "line": "afakemon_monkey", "types": ["water"], **MONKEY,
        "stats": stats(64, 82, 58, 55, 58, 88), "ev": evs(attack=1, speed=1), "exp": 142,
        "height": 11, "weight": 290, "shoulder": False, "walk": 0.36,
        "moves": MONKEY_EARLY + [(1, "machpunch"), (16, "machpunch"), (20, "aquajet"), (24, "brickbreak"),
                                 (28, "waterpulse"), (32, "bulkup")],
        "tm": MONKEY_TM, "egg": [], "evolve": ("slackey", 36, ["slackoff"]),
        "drops": [("minecraft:bamboo", "1-3", None), ("minecraft:kelp", "1-2", None)],
        "entry": ("It strikes a pose after every splash, dripping and proud. It practises its moves in rivers and "
                  "waterfalls for hours, then sleeps for the rest of the day."),
        "spawns": [],
        "how": ["Evolve Brenkey at level 16. It learns Mach Punch when it evolves.", "Evolves into Slackey at level 36."],
    },
    "slackey": {
        "dex": 3086, "name": "Slackey", "line": "afakemon_monkey", "types": ["water", "fighting"], **MONKEY,
        "stats": stats(100, 125, 90, 60, 75, 80), "ev": evs(hp=1, attack=2), "exp": 265,
        "height": 17, "weight": 1600, "shoulder": False, "walk": 0.26,
        "moves": MONKEY_EARLY + [(1, "slackoff"), (16, "machpunch"), (20, "aquajet"), (24, "brickbreak"),
                                 (28, "waterpulse"), (32, "bulkup"), (36, "slackoff"), (42, "liquidation"),
                                 (48, "drainpunch"), (54, "wavecrash"), (60, "closecombat")],
        "tm": MONKEY_TM + MONKEY_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:kelp", "1-3", None), ("minecraft:sponge", None, 2.5)],
        "entry": ("It spends its days floating in its swim ring and only moves when something gets close enough to "
                  "punch. One lazy swipe of its arm sends a wave over the whole lake."),
        "spawns": [],
        "how": ["Evolve Splakey at level 36. It learns Slack Off when it evolves."],
    },
    "whissant": {
        "dex": 3087, "name": "Whissant", "line": "afakemon_songbird", "types": ["grass"], **SONG,
        "stats": stats(45, 45, 50, 64, 55, 50), "ev": evs(special_attack=1), "exp": 62,
        "height": 4, "weight": 30, "shoulder": True, "walk": 0.26,
        "moves": SONG_EARLY + [(17, "gigadrain"), (20, "hypervoice"), (24, "synthesis"), (28, "calmmind")],
        "tm": SONG_TM, "egg": ["perishsong", "teeterdance", "featherdance", "leechseed"],
        "evolve": ("arpsant", 16, ["confusion"]),
        "drops": [("minecraft:feather", "1-2", None), ("minecraft:wheat_seeds", "0-1", None)],
        "entry": ("It whistles through its leafy wing all day long. It never plays the same tune twice, and it gets "
                  "very smug when other Pokémon stop to listen."),
        "spawns": [route_spawn("whissant-wild", "ultra-rare", "5-15", 1.0, ["#cobblemon:is_forest", "#cobblemon:is_plains"])],
        "how": [STARTER2_HOW, "Wild: very rare in forests and plains.", "Evolves into Arpsant at level 16."],
    },
    "arpsant": {
        "dex": 3088, "name": "Arpsant", "line": "afakemon_songbird", "types": ["grass", "psychic"], **SONG,
        "stats": stats(60, 55, 60, 90, 75, 65), "ev": evs(special_attack=2), "exp": 142,
        "height": 10, "weight": 140, "shoulder": False, "walk": 0.3,
        "moves": SONG_EARLY + [(1, "confusion"), (16, "confusion"), (20, "psybeam"), (24, "gigadrain"),
                               (28, "hypervoice"), (32, "calmmind")],
        "tm": SONG_TM, "egg": [], "evolve": ("violinisant", 36, ["psychicnoise"]),
        "drops": [("minecraft:feather", "1-3", None), ("minecraft:stick", "0-2", None)],
        "entry": ("It strings a curved twig with leaves to make a harp. Its music calms angry Pokémon, and the "
                  "leaves it plays on glow faintly when it is in a good mood."),
        "spawns": [],
        "how": ["Evolve Whissant at level 16. It learns Confusion when it evolves.", "Evolves into Violinisant at level 36."],
    },
    "violinisant": {
        "dex": 3089, "name": "Violinisant", "line": "afakemon_songbird", "types": ["grass", "psychic"], **SONG,
        "stats": stats(76, 60, 75, 125, 94, 100), "ev": evs(special_attack=3), "exp": 265,
        "height": 16, "weight": 380, "shoulder": False, "walk": 0.34,
        "moves": SONG_EARLY + [(1, "psychicnoise"), (16, "confusion"), (20, "psybeam"), (24, "gigadrain"),
                               (28, "hypervoice"), (32, "calmmind"), (36, "psychicnoise"), (42, "leafstorm"),
                               (48, "psychic"), (54, "boomburst"), (60, "perishsong")],
        "tm": SONG_TM + SONG_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:feather", "2-3", None), ("minecraft:stick", "1-2", None),
                  ("minecraft:note_block", None, 2.0)],
        "entry": ("It plays its long beak like a violin, drawing a twig across it as a bow. Its performances move "
                  "listeners to tears, and those who heckle it find themselves unable to stop dancing."),
        "spawns": [],
        "how": ["Evolve Arpsant at level 36. It learns Psychic Noise when it evolves."],
    },
    "flachiko": {
        "dex": 3090, "name": "Flachiko", "line": "afakemon_hound", "types": ["fire"], **DOG,
        "stats": stats(50, 64, 50, 40, 45, 60), "ev": evs(attack=1), "exp": 62,
        "height": 4, "weight": 72, "shoulder": True, "walk": 0.3,
        "moves": DOG_EARLY + [(17, "firefang"), (20, "crunch"), (24, "firepunch"), (28, "bulkup")],
        "tm": DOG_TM, "egg": ["howl", "playrough", "suckerpunch", "thunderfang"],
        "evolve": ("blaxer", 16, ["firefang"]),
        "drops": [("minecraft:bone", "0-1", None), ("minecraft:blaze_powder", "0-1", None)],
        "entry": ("It scowls at everyone it meets, but its flame tail wags uncontrollably when it is happy. Its fur "
                  "is warm enough to sleep against on cold nights."),
        "spawns": [route_spawn("flachiko-wild", "ultra-rare", "5-15", 1.0, ["#cobblemon:is_plains", "#cobblemon:is_savanna"])],
        "how": [STARTER2_HOW, "Wild: very rare in plains and savannas.", "Evolves into Blaxer at level 16."],
    },
    "blaxer": {
        "dex": 3091, "name": "Blaxer", "line": "afakemon_hound", "types": ["fire"], **DOG,
        "stats": stats(64, 92, 62, 48, 55, 84), "ev": evs(attack=2), "exp": 142,
        "height": 10, "weight": 300, "shoulder": False, "walk": 0.4,
        "moves": DOG_EARLY + [(1, "firefang"), (16, "firefang"), (20, "crunch"), (24, "firepunch"),
                              (28, "thunderpunch"), (32, "bulkup")],
        "tm": DOG_TM, "egg": [], "evolve": ("cerbego", 36, ["infernalparade"]),
        "drops": [("minecraft:bone", "0-2", None), ("minecraft:blaze_powder", "0-2", None)],
        "entry": ("It bounds into battle and boxes with its front paws, faster than the eye can follow. The spiked "
                  "collar round its neck grows from its own fur."),
        "spawns": [],
        "how": ["Evolve Flachiko at level 16. It learns Fire Fang when it evolves.", "Evolves into Cerbego at level 36."],
    },
    "cerbego": {
        "dex": 3092, "name": "Cerbego", "line": "afakemon_hound", "types": ["fire", "ghost"], **DOG,
        "stats": stats(90, 120, 85, 85, 70, 80), "ev": evs(attack=3), "exp": 265,
        "height": 18, "weight": 1800, "shoulder": False, "walk": 0.38,
        "moves": DOG_EARLY + [(1, "infernalparade"), (16, "firefang"), (20, "crunch"), (24, "firepunch"),
                              (28, "thunderpunch"), (32, "bulkup"), (36, "infernalparade"), (42, "shadowclaw"),
                              (48, "flareblitz"), (54, "phantomforce"), (60, "overheat")],
        "tm": DOG_TM + DOG_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:bone", "1-3", None), ("minecraft:blaze_powder", "1-2", None),
                  ("cobblemon:spell_tag", None, 5.0)],
        "entry": ("It guards the way to the land of the dead. The souls it has turned back burn beside it as purple "
                  "ghost-fire, and in battle they flare up as two more heads."),
        "spawns": [],
        "how": ["Evolve Blaxer at level 36. It learns Infernal Parade when it evolves."],
    },
})
LINES["afakemon_monkey"] = ["brenkey", "splakey", "slackey"]
LINES["afakemon_songbird"] = ["whissant", "arpsant", "violinisant"]
LINES["afakemon_hound"] = ["flachiko", "blaxer", "cerbego"]

# Magnalien: the CobbleEffortian (UFO) Magneton's evolution, after the A. Fakemon fanpage's art (its name)
SPECIES.update({
    "magnalien": {
        "dex": 3093, "name": "Magnalien", "line": "mothership", "types": ["electric", "psychic"],
        "male": -1, "egg_groups": ["mineral"], "friendship": 50, "catch": 30, "growth": "medium_fast",
        "abilities": ["levitate", "analytic", "h:telepathy"],
        "ability_names": "Levitate / Analytic / Telepathy (hidden)",
        "stats": stats(75, 60, 105, 135, 100, 60), "ev": evs(special_attack=3), "exp": 268,
        "height": 22, "weight": 1900, "shoulder": False, "walk": 0.26, "fly": True,
        "pre": "magneton cobbleeffortian",
        "moves": [(1, "tackle"), (1, "thundershock"), (1, "confusion"), (1, "supersonic"), (1, "thunderwave"),
                  (1, "psychic"), (1, "electricterrain"), (12, "electroball"), (16, "psybeam"), (20, "spark"),
                  (24, "confuseray"), (28, "magnetrise"), (34, "psychic"), (40, "discharge"), (46, "futuresight"),
                  (52, "lightscreen"), (58, "lockon"), (64, "zapcannon"), (70, "expandingforce")],
        "tm": BASIC_TM + ["thunderbolt", "thunder", "voltswitch", "electroball", "chargebeam", "discharge",
                          "electricterrain", "raindance", "psychic", "psyshock", "calmmind", "futuresight",
                          "shadowball", "dazzlinggleam", "trickroom", "storedpower", "psychicterrain",
                          "expandingforce", "lightscreen", "reflect", "triattack", "gigaimpact", "hyperbeam",
                          "magnetrise", "eerieimpulse"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:iron_ingot", "1-3", None), ("minecraft:redstone", "2-4", None),
                  ("minecraft:glowstone_dust", "1-3", None)],
        "entry": ("A mothership that carries the little saucers it was formed from docked round its rim. It hovers "
                  "silently over fields at night, and whatever its rainbow beam touches is never quite where it was "
                  "left in the morning."),
        "spawns": [],
        "how": ["Evolve a CobbleEffortian Magneton at level 45. It learns Psychic when it evolves."],
    },
})
LINES["mothership"] = ["magnalien"]

# the onion line (Tearion, Shallorn, Pungallium): after the A. Fakemon fanpage's art, names ours
ONION = dict(egg_groups=["grass"], male=0.5, friendship=50, growth="medium_slow",
             abilities=["stench", "harvest", "h:aftermath"], ability_names="Stench / Harvest / Aftermath (hidden)")
ONION_TM = BASIC_TM + ["bulletseed", "seedbomb", "energyball", "gigadrain", "grassknot", "trailblaze", "sunnyday",
                       "grassyterrain", "sludgebomb", "venoshock", "acidspray", "toxicspikes", "faketears",
                       "sleeppowder", "stunspore", "poisonpowder", "synthesis", "charm"]
ONION_TM_ADULT = ["sludgewave", "solarbeam", "leafstorm", "petalblizzard", "gunkshot", "toxic", "gigaimpact",
                  "hyperbeam", "dazzlinggleam"]
ONION_EARLY = [(1, "absorb"), (1, "growl"), (4, "faketears"), (8, "poisonpowder"), (12, "megadrain"),
               (16, "acid")]
ONION_WILD = ["#cobblemon:is_plains", "#cobblemon:is_grassland", "#cobblemon:is_forest"]
SPECIES.update({
    "tearion": {
        "dex": 3094, "name": "Tearion", "line": "onion", "types": ["grass"], **ONION, "catch": 190,
        "stats": stats(40, 35, 45, 45, 40, 30), "ev": evs(special_attack=1), "exp": 52,
        "height": 4, "weight": 25, "shoulder": True, "walk": 0.24,
        "moves": ONION_EARLY,
        "tm": ONION_TM, "egg": ["leechseed", "ingrain", "tearfullook", "strengthsap"],
        "evolve": ("shallorn", 18, ["sludge"]),
        "drops": [("minecraft:wheat_seeds", "1-2", None), ("minecraft:white_dye", "0-1", None)],
        "entry": ("It cries all the time, and so does everyone standing near it. It buries itself up to its leaves in "
                  "garden soil and sobs quietly when it is pulled up."),
        "spawns": [route_spawn("tearion-wild", "common", "3-18", 7.0, ONION_WILD)],
        "how": ["Wild: common in plains, grasslands and forests.", "Evolves into Shallorn at level 18."],
    },
    "shallorn": {
        "dex": 3095, "name": "Shallorn", "line": "onion", "types": ["grass", "poison"], **ONION, "catch": 120,
        "stats": stats(60, 50, 70, 70, 65, 40), "ev": evs(special_attack=1, special_defence=1), "exp": 138,
        "height": 9, "weight": 210, "shoulder": False, "walk": 0.2,
        "moves": ONION_EARLY + [(1, "sludge"), (18, "sludge"), (22, "stunspore"), (26, "gigadrain"),
                                (30, "venoshock"), (34, "synthesis")],
        "tm": ONION_TM, "egg": [], "evolve": ("pungallium", 34, ["petaldance"]),
        "drops": [("minecraft:wheat_seeds", "1-3", None), ("minecraft:brown_dye", "0-1", None)],
        "entry": ("It has stopped crying and grown gloomy instead, drooping its leaves over its face and sighing "
                  "into its moustache. The faint stink around it keeps everyone at a polite distance."),
        "spawns": [route_spawn("shallorn-wild", "uncommon", "18-34", 2.0, ONION_WILD + ["#cobblemon:is_swamp"])],
        "how": ["Evolve Tearion at level 18. It learns Sludge when it evolves.", "Wild: uncommon in plains, grasslands, "
                "forests and swamps.", "Evolves into Pungallium at level 34."],
    },
    "pungallium": {
        "dex": 3096, "name": "Pungallium", "line": "onion", "types": ["grass", "poison"], **ONION, "catch": 45,
        "stats": stats(85, 65, 90, 110, 95, 45), "ev": evs(special_attack=2, special_defence=1), "exp": 240,
        "height": 12, "weight": 480, "shoulder": False, "walk": 0.22,
        "moves": ONION_EARLY + [(1, "petaldance"), (18, "sludge"), (22, "stunspore"), (26, "gigadrain"),
                                (30, "venoshock"), (34, "petaldance"), (40, "sludgebomb"), (46, "petalblizzard"),
                                (52, "toxic"), (58, "sludgewave")],
        "tm": ONION_TM + ONION_TM_ADULT, "egg": [], "evolve": None,
        "drops": [("minecraft:purple_dye", "1-2", None), ("minecraft:wheat_seeds", "1-3", None),
                  ("minecraft:allium", "1-2", None)],
        "entry": ("Its great flower-head smells so strongly that its own eyes stream with tears and its tongue hangs "
                  "out in disgust. Bug Pokémon that come to feed on its nectar fall from the air in a faint."),
        "spawns": [route_spawn("pungallium-wild", "rare", "34-50", 0.6, ["#cobblemon:is_swamp", "#cobblemon:is_forest"])],
        "how": ["Evolve Shallorn at level 34. It learns Petal Dance when it evolves.", "Wild: rare in swamps and forests."],
    },
})
LINES["onion"] = ["tearion", "shallorn", "pungallium"]

# --- the Nicodex: 19 Pokémon of the Ashtray Wastes (CobbleEffort: Kanto), one per type; the user's designs, names,
# concepts and Pokédex entries; signature abilities/moves in nico_battle.py ---------------------------------------
ASHTRAY = ["#cobbleeffort_kanto:is_ashtray"]
NICO = dict(friendship=50, growth="medium_fast")
NICO_HOW = "Wild: {} in the Ashtray Wastes (an overworld biome added by CobbleEffort: Kanto)."


def nico_spawn(sid, bucket, level, weight):
    return route_spawn(sid, bucket, level, weight, ASHTRAY)


SPECIES.update({
    "nicotiny": {
        "dex": 3097, "name": "Nicotiny", "line": "nico_seedling", "types": ["grass"], **NICO, "catch": 190,
        "male": 0.5, "egg_groups": ["grass"],
        "abilities": ["pestdeterrent", "chlorophyll", "h:effectspore"],
        "ability_names": "Pest Deterrent / Chlorophyll / Effect Spore (hidden)",
        "stats": stats(50, 40, 55, 70, 75, 60), "ev": evs(special_defence=1), "exp": 64,
        "height": 3, "weight": 8, "shoulder": True, "walk": 0.24,
        "moves": [(1, "absorb"), (1, "growth"), (5, "poisonpowder"), (9, "megadrain"), (13, "stunspore"),
                  (17, "leechseed"), (21, "gigadrain"), (25, "toxic"), (29, "synthesis"), (33, "energyball"),
                  (37, "sleeppowder"), (41, "leafstorm")],
        "tm": BASIC_TM + ["energyball", "gigadrain", "grassknot", "solarbeam", "sunnyday", "grassyterrain",
                          "sludgebomb", "venoshock", "toxicspikes", "magicalleaf", "charm", "trailblaze"],
        "egg": ["ingrain", "strengthsap", "spikyshield"], "evolve": None,
        "drops": [("minecraft:wheat_seeds", "1-2", None), ("minecraft:fern", "0-1", None)],
        "entry": ("Farmers once planted Nicotiny around their gardens to keep Caterpie away, though touching its "
                  "leaves gives trainers a sudden dizzy spell."),
        "spawns": [nico_spawn("nicotiny-ashtray", "common", "4-24", 8.0)],
        "how": [NICO_HOW.format("common"), "Its ability Pest Deterrent lowers the Attack of Bug-type foes when it "
                "switches in."],
    },
    "emberbutt": {
        "dex": 3098, "name": "Emberbutt", "line": "nico_ember", "types": ["fire"], **NICO, "catch": 170,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["flamebody", "flashfire", "h:whitesmoke"],
        "ability_names": "Flame Body / Flash Fire / White Smoke (hidden)",
        "stats": stats(45, 70, 50, 55, 45, 95), "ev": evs(speed=1), "exp": 66,
        "height": 3, "weight": 4, "shoulder": True, "walk": 0.3,
        "moves": [(1, "ember"), (1, "tackle"), (5, "smokescreen"), (9, "cherryflick"), (13, "flamecharge"),
                  (17, "firefang"), (21, "incinerate"), (25, "willowisp"), (29, "flamewheel"), (33, "lavaplume"),
                  (39, "flareblitz")],
        "tm": BASIC_TM + ["flamethrower", "fireblast", "overheat", "willowisp", "flamecharge", "sunnyday", "uturn",
                          "quickattack", "temperflare", "heatwave", "endeavor"],
        "egg": ["burnup", "extremespeed", "fireblast"], "evolve": None,
        "drops": [("minecraft:paper", "1-2", None), ("minecraft:blaze_powder", "0-1", None)],
        "entry": ("It feeds on dry paper and dry leaves to keep the tip of its snout glowing. If extinguished, it "
                  "falls into a deep, sluggish sleep."),
        "spawns": [nico_spawn("emberbutt-ashtray", "common", "4-24", 8.0)],
        "how": [NICO_HOW.format("common"), "It learns Cherry Flick at level 9."],
    },
    "bongwater": {
        "dex": 3099, "name": "Bongwater", "line": "nico_hookah", "types": ["water", "poison"], **NICO, "catch": 150,
        "male": 0.5, "egg_groups": ["water_1", "amorphous"],
        "abilities": ["waterveil", "liquidooze", "h:stench"],
        "ability_names": "Water Veil / Liquid Ooze / Stench (hidden)",
        "stats": stats(50, 35, 55, 60, 60, 40), "ev": evs(special_attack=1), "exp": 62,
        "height": 6, "weight": 40, "shoulder": False, "walk": 0.2,
        "moves": [(1, "watergun"), (1, "smog"), (5, "bubble"), (9, "acid"), (13, "bubblebeam"), (17, "clearsmog"),
                  (21, "haze"), (25, "bubblefilter"), (30, "sludge")],
        "tm": BASIC_TM + ["surf", "scald", "waterpulse", "raindance", "sludgebomb", "venoshock", "acidspray",
                          "haze", "clearsmog", "toxicspikes", "chillingwater"],
        "egg": ["aquaring", "mist", "acidarmor"], "evolve": ("hookahdra", 36, ["dragonpulse"]),
        "drops": [("minecraft:glass_bottle", "1-2", None)],
        "entry": ("Its belly gurgles with every breath it draws through its glass neck. The water inside slowly turns "
                  "brown, and it has to swim in clean rivers to rinse itself out."),
        "spawns": [nico_spawn("bongwater-ashtray", "common", "5-30", 6.0)],
        "how": [NICO_HOW.format("common"), "It learns Bubble Filter at level 25.", "Evolves into Hookahdra at "
                "level 36."],
    },
    "hookahdra": {
        "dex": 3100, "name": "Hookahdra", "line": "nico_hookah", "types": ["water", "poison"], **NICO, "catch": 45,
        "male": 0.5, "egg_groups": ["water_1", "amorphous"],
        "abilities": ["waterveil", "liquidooze", "h:stench"],
        "ability_names": "Water Veil / Liquid Ooze / Stench (hidden)",
        "stats": stats(95, 70, 95, 110, 95, 60), "ev": evs(special_attack=2, hp=1), "exp": 241,
        "height": 23, "weight": 1650, "shoulder": False, "walk": 0.22,
        "moves": [(1, "watergun"), (1, "smog"), (1, "dragonpulse"), (5, "bubble"), (9, "acid"), (13, "bubblebeam"),
                  (17, "clearsmog"), (21, "haze"), (25, "bubblefilter"), (30, "sludge"), (36, "dragonpulse"),
                  (42, "scald"), (48, "sludgebomb"), (54, "hydropump"), (60, "sludgewave")],
        "tm": BASIC_TM + ["surf", "scald", "waterpulse", "raindance", "sludgebomb", "venoshock", "acidspray",
                          "haze", "clearsmog", "toxicspikes", "chillingwater", "hydropump", "sludgewave",
                          "dragonpulse", "dracometeor", "icebeam", "gigaimpact", "hyperbeam", "calmmind"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:glass_bottle", "1-3", None), ("minecraft:gold_nugget", "2-5", None)],
        "entry": ("By drawing air through its water-filled belly, Hookahdra cools down its internal furnace, releasing "
                  "sweet-smelling clouds from its many snouts."),
        "spawns": [nico_spawn("hookahdra-ashtray", "rare", "36-50", 0.5)],
        "how": ["Evolve Bongwater at level 36. It learns Dragon Pulse when it evolves.", NICO_HOW.format("rare")],
    },
    "vapulon": {
        "dex": 3101, "name": "Vapulon", "line": "nico_vapor", "types": ["electric", "flying"], **NICO, "catch": 120,
        "male": 0.5, "egg_groups": ["flying", "mineral"],
        "abilities": ["cloudchaser", "motordrive", "h:galewings"],
        "ability_names": "Cloud Chaser / Motor Drive / Gale Wings (hidden)",
        "stats": stats(60, 55, 60, 100, 70, 120), "ev": evs(speed=2), "exp": 166,
        "height": 4, "weight": 15, "shoulder": True, "walk": 0.35, "fly": True,
        "moves": [(1, "thundershock"), (1, "peck"), (5, "charge"), (9, "gust"), (13, "shockwave"), (17, "airslash"),
                  (21, "electroball"), (25, "mist"), (29, "discharge"), (33, "uturn"), (37, "hurricane"),
                  (41, "thunder")],
        "tm": BASIC_TM + ["thunderbolt", "thunder", "voltswitch", "electroball", "chargebeam", "electricterrain",
                          "raindance", "airslash", "hurricane", "uturn", "roost", "tailwind", "defog", "acrobatics",
                          "agility", "thunderwave"],
        "egg": ["mist", "featherdance"], "evolve": None,
        "drops": [("minecraft:redstone", "1-3", None), ("minecraft:feather", "0-1", None)],
        "entry": ("Popular among younger trainers in bustling cities, Vapulon charges itself at wall outlets and "
                  "exhales massive plumes that smell faintly of artificial berries."),
        "spawns": [nico_spawn("vapulon-ashtray", "uncommon", "18-40", 2.0)],
        "how": [NICO_HOW.format("uncommon"), "Its ability Cloud Chaser fills the field with fog for 5 turns: Electric "
                "moves get stronger and non-Electric Pokémon miss more."],
    },
    "mentholynx": {
        "dex": 3102, "name": "Mentholynx", "line": "nico_menthol", "types": ["ice", "dark"], **NICO, "catch": 75,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["icebody", "infiltrator", "h:snowcloak"],
        "ability_names": "Ice Body / Infiltrator / Snow Cloak (hidden)",
        "stats": stats(70, 105, 65, 60, 70, 110), "ev": evs(attack=1, speed=1), "exp": 172,
        "height": 9, "weight": 310, "shoulder": False, "walk": 0.38,
        "moves": [(1, "scratch"), (1, "powdersnow"), (5, "leer"), (9, "icefang"), (13, "bite"), (17, "iceshard"),
                  (21, "frostbitedrag"), (25, "nightslash"), (29, "icywind"), (33, "crunch"), (37, "iciclecrash"),
                  (43, "tripleaxel")],
        "tm": BASIC_TM + ["icebeam", "blizzard", "iciclespear", "icefang", "crunch", "knockoff", "suckerpunch",
                          "throatchop", "uturn", "snowscape", "aurorabeam", "honeclaws", "swordsdance", "foulplay"],
        "egg": ["glare", "suckerpunch"], "evolve": None,
        "drops": [("minecraft:snowball", "1-3", None), ("minecraft:packed_ice", "0-1", None)],
        "entry": ("Its icy breath masks the harshness of winter air, lulling lost travelers into staying out in the "
                  "cold far longer than they should."),
        "spawns": [nico_spawn("mentholynx-ashtray", "uncommon", "18-40", 2.0)],
        "how": [NICO_HOW.format("uncommon"), "It learns Frostbite Drag at level 21."],
    },
    "chawchamp": {
        "dex": 3103, "name": "Chawchamp", "line": "nico_chaw", "types": ["fighting"], **NICO, "catch": 90,
        "male": 0.5, "egg_groups": ["water_1", "human_like"],
        "abilities": ["guts", "thickfat", "h:ironfist"],
        "ability_names": "Guts / Thick Fat / Iron Fist (hidden)",
        "stats": stats(95, 115, 85, 45, 70, 55), "ev": evs(attack=2), "exp": 170,
        "height": 8, "weight": 640, "shoulder": False, "walk": 0.28,
        "moves": [(1, "pound"), (1, "leer"), (5, "machpunch"), (9, "mudslap"), (13, "brickbreak"),
                  (17, "spittoonslug"), (21, "bulkup"), (25, "drainpunch"), (29, "bodyslam"), (33, "superpower"),
                  (37, "closecombat")],
        "tm": BASIC_TM + ["brickbreak", "drainpunch", "closecombat", "bulkup", "rocktomb", "earthquake", "knockoff",
                          "icepunch", "thunderpunch", "firepunch", "bodypress", "waterpulse", "gunkshot", "poisonjab"],
        "egg": ["fakeout", "stockpile", "spitup", "swallow"], "evolve": None,
        "drops": [("minecraft:slime_ball", "1-2", None), ("minecraft:dried_kelp", "1-2", None)],
        "entry": ("Chawchamp constantly chews on bitter herbs to stay focused during sparring matches. Its jaw strength "
                  "can crush a Geodude."),
        "spawns": [nico_spawn("chawchamp-ashtray", "uncommon", "18-40", 2.0)],
        "how": [NICO_HOW.format("uncommon"), "It learns Spittoon Slug at level 17."],
    },
    "tarragon": {
        "dex": 3104, "name": "Tarragon", "line": "nico_tar", "types": ["poison", "dragon"], **NICO, "catch": 45,
        "male": 0.5, "egg_groups": ["dragon", "amorphous"],
        "abilities": ["resincoat", "stickyhold", "h:liquidooze"],
        "ability_names": "Resin Coat / Sticky Hold / Liquid Ooze (hidden)",
        "stats": stats(100, 95, 110, 85, 85, 40), "ev": evs(defence=2), "exp": 186,
        "height": 15, "weight": 1800, "shoulder": False, "walk": 0.2,
        "moves": [(1, "acid"), (1, "dragonbreath"), (5, "smog"), (9, "mudslap"), (13, "dragontail"),
                  (17, "sludge"), (21, "toxicspikes"), (25, "dragonclaw"), (29, "poisonjab"), (33, "gunkshot"),
                  (39, "dragonrush"), (45, "outrage")],
        "tm": BASIC_TM + ["sludgebomb", "gunkshot", "poisonjab", "toxicspikes", "dragonclaw", "dragonpulse",
                          "outrage", "earthquake", "stealthrock", "stoneedge", "irontail", "bodypress", "dragontail"],
        "egg": ["acidarmor", "stickyweb"], "evolve": None,
        "drops": [("minecraft:coal", "1-3", None), ("minecraft:black_dye", "1-2", None)],
        "entry": ("Born from the accumulated grime of industrial chimneys, Tarragon's heavy, tar-soaked wings make flight "
                  "difficult, forcing it to crawl along cavern walls."),
        "spawns": [nico_spawn("tarragon-ashtray", "rare", "30-50", 0.6)],
        "how": [NICO_HOW.format("rare"), "Its ability Resin Coat halves damage from contact moves and slows the "
                "attacker."],
    },
    "ashtraylor": {
        "dex": 3105, "name": "Ashtraylor", "line": "nico_ashtray", "types": ["ground", "rock"], **NICO, "catch": 75,
        "male": 0.5, "egg_groups": ["monster", "mineral"],
        "abilities": ["sturdy", "flashfire", "h:shellarmor"],
        "ability_names": "Sturdy / Flash Fire / Shell Armor (hidden)",
        "stats": stats(100, 80, 130, 50, 90, 25), "ev": evs(defence=2), "exp": 168,
        "height": 10, "weight": 2600, "shoulder": False, "walk": 0.14,
        "moves": [(1, "tackle"), (1, "sandattack"), (5, "withdraw"), (9, "mudslap"), (13, "rocktomb"),
                  (17, "smother"), (21, "bulldoze"), (25, "rockslide"), (29, "irondefense"), (33, "earthquake"),
                  (39, "headsmash")],
        "tm": BASIC_TM + ["earthquake", "bulldoze", "dig", "stealthrock", "rockslide", "stoneedge", "rocktomb",
                          "sandstorm", "bodypress", "irondefense", "heavyslam", "willowisp", "sandtomb"],
        "egg": ["shellsmash", "yawn"], "evolve": None,
        "drops": [("minecraft:gray_dye", "1-3", None), ("minecraft:flint", "1-2", None)],
        "entry": ("Travelers use Ashtraylor's basin-like back to safely extinguish campfires. It absorbs the leftover "
                  "cinders to harden its stony shell."),
        "spawns": [nico_spawn("ashtraylor-ashtray", "common", "10-36", 5.0)],
        "how": [NICO_HOW.format("common"), "It learns Smother at level 17."],
    },
    "wispuff": {
        "dex": 3106, "name": "Wispuff", "line": "nico_smoke", "types": ["flying", "ghost"], **NICO, "catch": 120,
        "male": -1, "egg_groups": ["amorphous"],
        "abilities": ["lingeringscent", "levitate", "h:whitesmoke"],
        "ability_names": "Lingering Scent / Levitate / White Smoke (hidden)",
        "stats": stats(60, 45, 55, 95, 80, 95), "ev": evs(special_attack=1, speed=1), "exp": 150,
        "height": 6, "weight": 1, "shoulder": True, "walk": 0.28, "fly": True,
        "moves": [(1, "gust"), (1, "astonish"), (5, "smokescreen"), (9, "ominouswind"), (13, "hex"),
                  (17, "airslash"), (21, "haze"), (25, "shadowball"), (29, "defog"), (33, "hurricane"),
                  (37, "destinybond")],
        "tm": BASIC_TM + ["shadowball", "hex", "willowisp", "airslash", "hurricane", "tailwind", "defog", "uturn",
                          "painsplit", "trick", "nightshade", "confuseray"],
        "egg": ["memento", "curse"], "evolve": None,
        "drops": [("minecraft:gunpowder", "0-1", None), ("minecraft:light_gray_dye", "1-2", None)],
        "entry": ("It clings to curtains and clothing long after leaving a room. You can always tell when a Wispuff has "
                  "passed through by the stale chill in the air."),
        "spawns": [nico_spawn("wispuff-ashtray", "common", "8-32", 5.0)],
        "how": [NICO_HOW.format("common"), "Its ability Lingering Scent leaves a haze for 3 turns after it faints "
                "that hurts non-Ghost Pokémon."],
    },
    "hypnodose": {
        "dex": 3107, "name": "Hypnodose", "line": "nico_patch", "types": ["psychic"], **NICO, "catch": 120,
        "male": -1, "egg_groups": ["amorphous"],
        "abilities": ["steadyrelease", "healer", "h:innerfocus"],
        "ability_names": "Steady Release / Healer / Inner Focus (hidden)",
        "stats": stats(80, 40, 75, 85, 105, 65), "ev": evs(special_defence=2), "exp": 158,
        "height": 4, "weight": 2, "shoulder": True, "walk": 0.24, "fly": True,
        "moves": [(1, "confusion"), (1, "hypnosis"), (5, "disable"), (9, "psybeam"), (13, "calmmind"),
                  (17, "healpulse"), (21, "psyshock"), (25, "wish"), (29, "psychic"), (33, "healbell"),
                  (37, "storedpower")],
        "tm": BASIC_TM + ["psychic", "psyshock", "calmmind", "lightscreen", "reflect", "trickroom", "storedpower",
                          "healpulse", "dazzlinggleam", "shadowball", "thunderwave", "psychicterrain"],
        "egg": ["lifedew", "afteryou"], "evolve": None,
        "drops": [("minecraft:paper", "1-2", None), ("minecraft:purple_dye", "0-1", None)],
        "entry": ("Hypnodose latches onto stressed Pokémon, releasing a calm, rhythmic psychic pulse that eases "
                  "agitation—though removing it causes sudden irritability."),
        "spawns": [nico_spawn("hypnodose-ashtray", "uncommon", "16-38", 2.0)],
        "how": [NICO_HOW.format("uncommon"), "Its ability Steady Release cures confusion and restores PP on its side "
                "every turn."],
    },
    "hornworm": {
        "dex": 3108, "name": "Hornworm", "line": "nico_hornworm", "types": ["bug"], **NICO, "catch": 150,
        "male": 0.5, "egg_groups": ["bug"],
        "abilities": ["toxingourmet", "shielddust", "h:gluttony"],
        "ability_names": "Toxin Gourmet / Shield Dust / Gluttony (hidden)",
        "stats": stats(85, 80, 75, 40, 70, 50), "ev": evs(hp=1, attack=1), "exp": 140,
        "height": 5, "weight": 60, "shoulder": False, "walk": 0.18,
        "moves": [(1, "tackle"), (1, "stringshot"), (5, "bugbite"), (9, "poisonsting"), (13, "headbutt"),
                  (17, "strugglebug"), (21, "hornattack"), (25, "leechlife"), (29, "pinmissile"), (33, "megahorn"),
                  (38, "firstimpression")],
        "tm": BASIC_TM + ["xscissor", "uturn", "lunge", "bugbuzz", "pounce", "leechlife", "poisonjab", "bodyslam",
                          "stickyweb", "irondefense", "skittersmack"],
        "egg": ["stockpile", "slackoff"], "evolve": None,
        "drops": [("minecraft:slime_ball", "0-1", None), ("minecraft:lime_dye", "1-2", None)],
        "entry": ("While most Bug-types avoid Nicotiny, Hornworm devours entire fields of them, storing the bitter "
                  "alkaloids in its body to deter predators."),
        "spawns": [nico_spawn("hornworm-ashtray", "common", "6-28", 7.0)],
        "how": [NICO_HOW.format("common"), "Its ability Toxin Gourmet heals it instead of hurting it when it is hit "
                "by a Poison- or Grass-type move."],
    },
    "meerschaum": {
        "dex": 3109, "name": "Meerschaum", "line": "nico_pipe", "types": ["rock", "fairy"], **NICO, "catch": 60,
        "male": 0.5, "egg_groups": ["mineral", "fairy"],
        "abilities": ["patinapolish", "sturdy", "h:magicguard"],
        "ability_names": "Patina Polish / Sturdy / Magic Guard (hidden)",
        "stats": stats(80, 70, 110, 85, 110, 45), "ev": evs(defence=1, special_defence=1), "exp": 178,
        "height": 9, "weight": 950, "shoulder": False, "walk": 0.24,
        "moves": [(1, "tackle"), (1, "fairywind"), (5, "defensecurl"), (9, "rockthrow"), (13, "drainingkiss"),
                  (17, "ancientpower"), (21, "irondefense"), (25, "dazzlinggleam"), (29, "powergem"),
                  (33, "cosmicpower"), (37, "moonblast")],
        "tm": BASIC_TM + ["powergem", "rockslide", "stoneedge", "stealthrock", "moonblast", "dazzlinggleam",
                          "drainingkiss", "calmmind", "irondefense", "bodypress", "meteorbeam", "mistyterrain"],
        "egg": ["wish", "stealthrock"], "evolve": None,
        "drops": [("minecraft:quartz", "1-2", None), ("minecraft:calcite", "1-2", None)],
        "entry": ("Artisans carve Meerschaum into intricate shapes. The darker and richer its golden-brown coloration, "
                  "the older and more powerful the Pokémon is."),
        "spawns": [nico_spawn("meerschaum-ashtray", "rare", "26-46", 0.8)],
        "how": [NICO_HOW.format("rare"), "Its ability Patina Polish raises its Defense and Sp. Def whenever a Fire- or "
                "Poison-type move hits it."],
    },
    "cigarghast": {
        "dex": 3110, "name": "Cigarghast", "line": "nico_cigar", "types": ["ghost", "fire"], **NICO, "catch": 60,
        "male": 0.5, "egg_groups": ["amorphous"],
        "abilities": ["flashfire", "cursedbody", "h:infiltrator"],
        "ability_names": "Flash Fire / Cursed Body / Infiltrator (hidden)",
        "stats": stats(70, 60, 75, 110, 90, 85), "ev": evs(special_attack=2), "exp": 180,
        "height": 8, "weight": 30, "shoulder": False, "walk": 0.24, "fly": True,
        "moves": [(1, "ember"), (1, "astonish"), (5, "smokescreen"), (9, "hex"), (13, "willowisp"),
                  (17, "incinerate"), (21, "smokering"), (25, "shadowball"), (29, "flamethrower"), (33, "nastyplot"),
                  (37, "infernalparade"), (41, "overheat")],
        "tm": BASIC_TM + ["shadowball", "hex", "flamethrower", "fireblast", "overheat", "willowisp", "nastyplot",
                          "heatwave", "trick", "painsplit", "darkpulse", "sunnyday"],
        "egg": ["destinybond", "memento"], "evolve": None,
        "drops": [("minecraft:brown_dye", "1-2", None), ("minecraft:gold_nugget", "1-3", None)],
        "entry": ("Said to haunt old study rooms and velvet lounges, Cigarghast's glowing ember eye is often the only "
                  "thing visible in the dark."),
        "spawns": [route_spawn("cigarghast-ashtray", "rare", "26-46", 0.8, ASHTRAY, timeRange="night")],
        "how": [NICO_HOW.format("rare, at night"), "It learns Smoke Ring at level 21."],
    },
    "zynx": {
        "dex": 3111, "name": "Zynx", "line": "nico_pouch", "types": ["fairy", "ice"], **NICO, "catch": 150,
        "male": 0.5, "egg_groups": ["fairy"],
        "abilities": ["refrigerate", "pixilate", "h:cutecharm"],
        "ability_names": "Refrigerate / Pixilate / Cute Charm (hidden)",
        "stats": stats(55, 45, 60, 90, 70, 110), "ev": evs(speed=2), "exp": 152,
        "height": 2, "weight": 2, "shoulder": True, "walk": 0.3,
        "moves": [(1, "pound"), (1, "powdersnow"), (5, "fairywind"), (9, "icywind"), (13, "drainingkiss"),
                  (17, "liptingle"), (21, "aurorabeam"), (25, "dazzlinggleam"), (29, "icebeam"), (33, "moonblast"),
                  (37, "blizzard")],
        "tm": BASIC_TM + ["icebeam", "blizzard", "icywind", "dazzlinggleam", "moonblast", "drainingkiss",
                          "mistyterrain", "snowscape", "charm", "calmmind", "uturn", "playrough"],
        "egg": ["fakeout", "sweetkiss"], "evolve": None,
        "drops": [("minecraft:snowball", "1-2", None), ("minecraft:light_blue_dye", "0-1", None)],
        "entry": ("Compact and discreet, Zynx hides inside trainers' pockets. A single touch gives an instant jolt of "
                  "icy clarity and focus."),
        "spawns": [nico_spawn("zynx-ashtray", "uncommon", "16-38", 2.0)],
        "how": [NICO_HOW.format("uncommon"), "It learns Lip Tingle at level 17."],
    },
    "zippolt": {
        "dex": 3112, "name": "Zippolt", "line": "nico_lighter", "types": ["steel", "electric"], **NICO, "catch": 90,
        "male": -1, "egg_groups": ["mineral"],
        "abilities": ["flashfire", "static", "h:lightningrod"],
        "ability_names": "Flash Fire / Static / Lightning Rod (hidden)",
        "stats": stats(60, 95, 95, 70, 70, 90), "ev": evs(attack=1, speed=1), "exp": 170,
        "height": 4, "weight": 70, "shoulder": True, "walk": 0.3,
        "moves": [(1, "metalclaw"), (1, "thundershock"), (5, "spark"), (9, "mirrorshot"), (13, "shockwave"),
                  (17, "flintsnap"), (21, "irondefense"), (25, "thunderfang"), (29, "ironhead"), (33, "wildcharge"),
                  (39, "steelbeam")],
        "tm": BASIC_TM + ["flashcannon", "ironhead", "thunderbolt", "voltswitch", "wildcharge", "thunderwave",
                          "irondefense", "steelbeam", "electricterrain", "gyroball", "metalsound", "firefang"],
        "egg": ["shiftgear", "magnetrise"], "evolve": None,
        "drops": [("minecraft:iron_nugget", "2-5", None), ("minecraft:flint", "1-2", None)],
        "entry": ("Celebrated for its signature metallic clink, Zippolt can keep its tiny flame alive even in the "
                  "middle of a fierce gale."),
        "spawns": [nico_spawn("zippolt-ashtray", "uncommon", "16-38", 2.0)],
        "how": [NICO_HOW.format("uncommon"), "It learns Flint Snap at level 17."],
    },
    "snuffel": {
        "dex": 3113, "name": "Snuffel", "line": "nico_snuff", "types": ["normal"], **NICO, "catch": 190,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["pickup", "runaway", "h:aromaveil"],
        "ability_names": "Pickup / Run Away / Aroma Veil (hidden)",
        "stats": stats(70, 60, 55, 60, 55, 80), "ev": evs(speed=1), "exp": 72,
        "height": 3, "weight": 25, "shoulder": True, "walk": 0.3,
        "moves": [(1, "scratch"), (1, "sandattack"), (5, "quickattack"), (9, "dig"), (13, "headbutt"),
                  (17, "sneezefit"), (21, "furyswipes"), (25, "yawn"), (29, "bodyslam"), (33, "hypervoice"),
                  (37, "doubleedge")],
        "tm": BASIC_TM + ["dig", "bodyslam", "hypervoice", "uturn", "thief", "swift", "yawn", "bulldoze",
                          "playrough", "facade", "workup"],
        "egg": ["followme", "covet"], "evolve": None,
        "drops": [("minecraft:brown_dye", "1-2", None), ("minecraft:sugar", "0-1", None)],
        "entry": ("Snuffel stores pulverized herbs in tiny pouches near its snout. A single pinch wakes it up instantly "
                  "from hibernation."),
        "spawns": [nico_spawn("snuffel-ashtray", "common", "4-26", 8.0)],
        "how": [NICO_HOW.format("common"), "It learns Sneeze Fit at level 17."],
    },
    "cartelord": {
        "dex": 3114, "name": "Cartelord", "line": "nico_baron", "types": ["dark", "grass"], **NICO, "catch": 45,
        "male": 0.5, "egg_groups": ["grass", "human_like"],
        "abilities": ["hooked", "intimidate", "h:prankster"],
        "ability_names": "Hooked / Intimidate / Prankster (hidden)",
        "stats": stats(85, 110, 80, 75, 80, 80), "ev": evs(attack=2), "exp": 190,
        "height": 18, "weight": 520, "shoulder": False, "walk": 0.28,
        "moves": [(1, "absorb"), (1, "pursuit"), (5, "leechseed"), (9, "bite"), (13, "razorleaf"),
                  (17, "feintattack"), (21, "seedbomb"), (25, "nastyplot"), (29, "nightslash"), (33, "leafblade"),
                  (37, "knockoff"), (43, "powerwhip")],
        "tm": BASIC_TM + ["knockoff", "suckerpunch", "darkpulse", "leafblade", "seedbomb", "energyball", "swordsdance",
                          "taunt", "torment", "foulplay", "trailblaze", "gigadrain", "throatchop"],
        "egg": ["spikyshield", "partingshot"], "evolve": None,
        "drops": [("minecraft:emerald", "0-1", None), ("minecraft:wheat", "1-3", None)],
        "entry": ("Cartelord controls vast swaths of farmland. Once a Pokémon gets a taste of the sweet nectar it "
                  "produces, it refuses to eat anything else."),
        "spawns": [nico_spawn("cartelord-ashtray", "rare", "30-50", 0.6)],
        "how": [NICO_HOW.format("rare"), "Its ability Hooked keeps any Pokémon that touches it from switching out on "
                "the next turn."],
    },
    "nicodrake": {
        "dex": 3115, "name": "Nicodrake", "line": "nico_dragon", "types": ["dragon", "poison"],
        "friendship": 0, "growth": "slow", "catch": 3, "male": -1, "egg_groups": ["undiscovered"],
        "labels": ["legendary"],
        "abilities": ["pressure", "h:aromaveil"], "ability_names": "Pressure / Aroma Veil (hidden)",
        "stats": stats(100, 100, 90, 130, 90, 90), "ev": evs(special_attack=3), "exp": 300,
        "height": 26, "weight": 900, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": [(1, "dragonbreath"), (1, "smog"), (1, "safeguard"), (10, "twister"), (20, "venoshock"),
                  (30, "dragonpulse"), (40, "alkaloidroar"), (50, "sludgewave"), (60, "dragondance"),
                  (70, "dracometeor"), (80, "toxic")],
        "tm": BASIC_TM + ["dragonpulse", "dracometeor", "sludgebomb", "sludgewave", "flamethrower", "fireblast",
                          "calmmind", "roost", "hurricane", "outrage", "dragondance", "hyperbeam", "gigaimpact",
                          "toxicspikes", "venoshock"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:gold_ingot", "2-4", None), ("minecraft:dragon_breath", "1-2", None)],
        "entry": ("Ancient murals depict shamans summoning Nicodrake through ceremonial braziers to commune with "
                  "spirits and sharpen their minds."),
        "spawns": [nico_spawn("nicodrake-ashtray", "ultra-rare", "60-70", 0.1)],
        "how": ["Wild: ultra-rare in the Ashtray Wastes (an overworld biome added by CobbleEffort: Kanto), level 60-70.",
                "It learns Alkaloid Roar at level 40."],
    },
})
for _sp in ("nicotiny", "emberbutt", "vapulon", "mentholynx", "chawchamp", "tarragon", "ashtraylor", "wispuff",
            "hypnodose", "hornworm", "meerschaum", "cigarghast", "zynx", "zippolt", "snuffel", "cartelord", "nicodrake"):
    LINES[SPECIES[_sp]["line"]] = [_sp]
LINES["nico_hookah"] = ["bongwater", "hookahdra"]

# --- the Liquor Meadows' 20 Pokémon (CobbleEffort: Kanto 0.8.0's biome), one per type: the user's designs, names,
# concepts and Pokédex entries; signature abilities/moves in liquor_battle.py -------------------------------------
LIQUOR = ["#cobbleeffort_kanto:is_liquor"]
LIQ = dict(friendship=70, growth="medium_fast")
LIQ_HOW = "Wild: {} in the Liquor Meadows (an overworld biome added by CobbleEffort: Kanto 0.8.0)."


def liq_spawn(sid, bucket, level, weight, **cond):
    return route_spawn(sid, bucket, level, weight, LIQUOR, **cond)


def liq_water(sid, bucket, level, weight):
    s = spawn(sid, bucket, level, weight, {"biomes": LIQUOR}, position="submerged")
    s["presets"] = ["water"]
    return s


SPECIES.update({
    "hopsprout": {
        "dex": 3116, "name": "Hopsprout", "line": "liq_hops", "types": ["grass"], **LIQ, "catch": 190,
        "male": 0.5, "egg_groups": ["grass", "fairy"],
        "abilities": ["aromaticharvest", "chlorophyll", "h:sweetveil"],
        "ability_names": "Aromatic Harvest / Chlorophyll / Sweet Veil (hidden)",
        "stats": stats(65, 55, 70, 85, 85, 70), "ev": evs(special_defence=1), "exp": 140,
        "height": 4, "weight": 9, "shoulder": True, "walk": 0.26,
        "moves": [(1, "absorb"), (1, "sweetscent"), (5, "growth"), (9, "megadrain"), (13, "sleeppowder"),
                  (17, "magicalleaf"), (21, "aromatherapy"), (25, "gigadrain"), (29, "sunnyday"), (33, "energyball"),
                  (37, "synthesis"), (41, "petalblizzard")],
        "tm": BASIC_TM + ["energyball", "gigadrain", "grassknot", "solarbeam", "sunnyday", "raindance",
                          "grassyterrain", "magicalleaf", "charm", "dazzlinggleam", "trailblaze", "seedbomb"],
        "egg": ["leechseed", "ingrain", "floralhealing"], "evolve": None,
        "drops": [("minecraft:wheat_seeds", "1-2", None), ("minecraft:lime_dye", "0-1", None)],
        "entry": ("Brewers prize Hopsprout for the bitter, floral oils on its petals. When frightened, it releases a "
                  "musky scent that puts predators to sleep."),
        "spawns": [liq_spawn("hopsprout-liquor", "common", "4-26", 8.0)],
        "how": [LIQ_HOW.format("common"), "Its ability Aromatic Harvest heals it and its allies a little every turn "
                "in sun or rain."],
    },
    "flambeer": {
        "dex": 3117, "name": "Flambéer", "line": "liq_spirit", "types": ["fire", "water"], **LIQ, "catch": 90,
        "male": -1, "egg_groups": ["amorphous"],
        "abilities": ["flashfire", "waterabsorb", "h:levitate"],
        "ability_names": "Flash Fire / Water Absorb / Levitate (hidden)",
        "stats": stats(70, 50, 70, 115, 90, 85), "ev": evs(special_attack=2), "exp": 172,
        "height": 6, "weight": 40, "shoulder": False, "walk": 0.24, "fly": True,
        "moves": [(1, "ember"), (1, "watergun"), (5, "willowisp"), (9, "bubblebeam"), (13, "flamecharge"),
                  (17, "scald"), (20, "blueignition"), (25, "lavaplume"), (29, "steameruption"), (33, "flamethrower"),
                  (39, "hydropump"), (45, "overheat")],
        "tm": BASIC_TM + ["flamethrower", "fireblast", "overheat", "willowisp", "heatwave", "scald", "surf",
                          "hydropump", "waterpulse", "raindance", "sunnyday", "calmmind", "chillingwater"],
        "egg": ["mist", "acidarmor"], "evolve": None,
        "drops": [("minecraft:blaze_powder", "1-2", None), ("minecraft:glass_bottle", "0-1", None)],
        "entry": ("Its liquid body is so pure and volatile that a single spark sets its surface ablaze with a cool, "
                  "ghost-blue flame."),
        "spawns": [liq_spawn("flambeer-liquor", "uncommon", "18-40", 2.0)],
        "how": [LIQ_HOW.format("uncommon"), "It learns Blue Ignition at level 20."],
    },
    "sakekoi": {
        "dex": 3118, "name": "Sakekoi", "line": "liq_koi", "types": ["water"], **LIQ, "catch": 90,
        "male": 0.5, "egg_groups": ["water_2"],
        "abilities": ["warminfusion", "swiftswim", "h:serenegrace"],
        "ability_names": "Warm Infusion / Swift Swim / Serene Grace (hidden)",
        "stats": stats(80, 60, 75, 95, 105, 75), "ev": evs(special_defence=2), "exp": 172,
        "height": 6, "weight": 110, "shoulder": False, "walk": 0.3, "aquatic": True,
        "moves": [(1, "watergun"), (1, "splash"), (5, "aquajet"), (9, "bubblebeam"), (13, "calmmind"),
                  (17, "waterpulse"), (21, "aquaring"), (25, "scald"), (29, "lifedew"), (33, "surf"), (39, "moonblast"),
                  (45, "hydropump")],
        "tm": BASIC_TM + ["surf", "scald", "waterpulse", "hydropump", "icebeam", "raindance", "calmmind",
                          "chillingwater", "dazzlinggleam", "psychic", "whirlpool"],
        "egg": ["flail", "soak", "lifedew"], "evolve": None,
        "drops": [("minecraft:cod", "1-2", None), ("minecraft:red_dye", "0-1", None)],
        "entry": ("Sakekoi thrives in steaming mountain springs. Locals believe a visit from one brings prosperity, "
                  "harmony, and a bountiful rice harvest."),
        "spawns": [liq_water("sakekoi-liquor", "uncommon", "16-40", 3.0)],
        "how": [LIQ_HOW.format("uncommon, swimming in its whisky-coloured ponds and lakes,"),
                "Its ability Warm Infusion raises its Sp. Atk when a Fire-type move hits it and thaws its frozen party."],
    },
    "joltini": {
        "dex": 3119, "name": "Joltini", "line": "liq_cocktail", "types": ["electric", "fairy"], **LIQ, "catch": 90,
        "male": 0.5, "egg_groups": ["fairy", "amorphous"],
        "abilities": ["motordrive", "static", "h:prankster"],
        "ability_names": "Motor Drive / Static / Prankster (hidden)",
        "stats": stats(60, 50, 60, 105, 80, 120), "ev": evs(speed=2), "exp": 168,
        "height": 6, "weight": 8, "shoulder": True, "walk": 0.3, "fly": True,
        "moves": [(1, "thundershock"), (1, "fairywind"), (5, "charge"), (9, "drainingkiss"), (13, "shockwave"),
                  (17, "zestshock"), (21, "dazzlinggleam"), (25, "discharge"), (29, "moonblast"), (33, "thunderbolt"),
                  (39, "thunder")],
        "tm": BASIC_TM + ["thunderbolt", "thunder", "voltswitch", "electroball", "thunderwave", "electricterrain",
                          "dazzlinggleam", "moonblast", "drainingkiss", "mistyterrain", "calmmind", "charm"],
        "egg": ["encore", "sweetkiss"], "evolve": None,
        "drops": [("minecraft:glowstone_dust", "1-2", None), ("minecraft:yellow_dye", "0-1", None)],
        "entry": ("Joltini vibrates at high frequencies, creating static sparks along its rim. One sip of its "
                  "electrified nectar can keep a trainer awake for three days."),
        "spawns": [liq_spawn("joltini-liquor", "uncommon", "18-40", 2.0)],
        "how": [LIQ_HOW.format("uncommon"), "It learns Zest Shock at level 17."],
    },
    "ontherox": {
        "dex": 3120, "name": "Ontherox", "line": "liq_ice", "types": ["ice", "rock"], **LIQ, "catch": 60,
        "male": -1, "egg_groups": ["mineral"],
        "abilities": ["slowmelt", "sturdy", "h:icebody"],
        "ability_names": "Slow Melt / Sturdy / Ice Body (hidden)",
        "stats": stats(95, 110, 130, 45, 80, 30), "ev": evs(defence=2), "exp": 178,
        "height": 13, "weight": 3200, "shoulder": False, "walk": 0.16,
        "moves": [(1, "tackle"), (1, "powdersnow"), (5, "harden"), (9, "iceshard"), (13, "rocktomb"),
                  (17, "iceball"), (21, "rockslide"), (25, "irondefense"), (29, "iciclecrash"), (33, "stoneedge"),
                  (39, "headsmash")],
        "tm": BASIC_TM + ["avalanche", "iciclespear", "icebeam", "blizzard", "rockslide", "stoneedge", "stealthrock",
                          "earthquake", "bodypress", "irondefense", "snowscape", "heavyslam", "icepunch"],
        "egg": ["mirrorcoat", "rapidspin"], "evolve": None,
        "drops": [("minecraft:ice", "1-3", None), ("minecraft:blue_ice", "0-1", None)],
        "entry": ("Unlike normal ice, Ontherox is forged under immense pressure, making it so dense that it clinks like "
                  "solid stone and takes weeks to thaw."),
        "spawns": [liq_spawn("ontherox-liquor", "rare", "26-46", 0.8)],
        "how": [LIQ_HOW.format("rare"), "Its ability Slow Melt halves super-effective Fire damage, and a Fire hit "
                "slicks the ground, lowering its foes' Speed."],
    },
    "brawlerry": {
        "dex": 3121, "name": "Brawlerry", "line": "liq_brawl", "types": ["fighting"], **LIQ, "catch": 90,
        "male": 0.5, "egg_groups": ["field", "human_like"],
        "abilities": ["guts", "tangledfeet", "h:ironfist"],
        "ability_names": "Guts / Tangled Feet / Iron Fist (hidden)",
        "stats": stats(100, 120, 85, 40, 70, 65), "ev": evs(attack=2), "exp": 172,
        "height": 14, "weight": 1350, "shoulder": False, "walk": 0.28,
        "moves": [(1, "tackle"), (1, "leer"), (5, "machpunch"), (9, "swagger"), (13, "brickbreak"),
                  (17, "barroomblitz"), (21, "bulkup"), (25, "drainpunch"), (29, "hammerarm"), (33, "dynamicpunch"),
                  (39, "closecombat")],
        "tm": BASIC_TM + ["brickbreak", "drainpunch", "closecombat", "bulkup", "icepunch", "firepunch",
                          "thunderpunch", "earthquake", "rockslide", "bodypress", "knockoff", "swagger", "bodyslam"],
        "egg": ["fakeout", "bellydrum"], "evolve": None,
        "drops": [("minecraft:wheat", "1-3", None), ("minecraft:leather", "0-1", None)],
        "entry": ("Brawlerry loves noisy taverns and friendly sparring. Though it stumbles unpredictably when dizzy, "
                  "its wild haymakers hit with devastating force."),
        "spawns": [liq_spawn("brawlerry-liquor", "uncommon", "18-40", 2.0)],
        "how": [LIQ_HOW.format("uncommon"), "It learns Barroom Blitz at level 17."],
    },
    "absinthia": {
        "dex": 3122, "name": "Absinthia", "line": "liq_fairy", "types": ["poison", "psychic"], **LIQ, "catch": 60,
        "male": 0.0, "egg_groups": ["fairy", "amorphous"],
        "abilities": ["corrosion", "synchronize", "h:magicbounce"],
        "ability_names": "Corrosion / Synchronize / Magic Bounce (hidden)",
        "stats": stats(70, 50, 65, 115, 95, 100), "ev": evs(special_attack=2), "exp": 178,
        "height": 8, "weight": 30, "shoulder": False, "walk": 0.26, "fly": True,
        "moves": [(1, "confusion"), (1, "poisonpowder"), (5, "sweetscent"), (9, "psybeam"), (13, "venoshock"),
                  (17, "greenmuse"), (21, "hypnosis"), (25, "sludgebomb"), (29, "psychic"), (33, "nastyplot"),
                  (39, "sludgewave")],
        "tm": BASIC_TM + ["psychic", "psyshock", "calmmind", "sludgebomb", "sludgewave", "venoshock", "toxicspikes",
                          "dazzlinggleam", "shadowball", "trick", "nastyplot", "psychicterrain", "energyball"],
        "egg": ["confuseray", "mistyterrain"], "evolve": None,
        "drops": [("minecraft:green_dye", "1-2", None), ("minecraft:sugar", "1-2", None)],
        "entry": ("Artists in ancient cities sought out Absinthia for inspiration, though staring too long into its "
                  "swirling emerald eyes causes vivid hallucinations."),
        "spawns": [liq_spawn("absinthia-liquor", "uncommon", "20-42", 1.6, timeRange="night")],
        "how": [LIQ_HOW.format("uncommon, at night,"), "It learns Green Muse at level 17."],
    },
    "agavolem": {
        "dex": 3123, "name": "Agavolem", "line": "liq_agave", "types": ["ground", "grass"], **LIQ, "catch": 60,
        "male": -1, "egg_groups": ["mineral", "grass"],
        "abilities": ["roughskin", "sandveil", "h:sapsipper"],
        "ability_names": "Rough Skin / Sand Veil / Sap Sipper (hidden)",
        "stats": stats(100, 115, 110, 55, 75, 40), "ev": evs(attack=1, defence=1), "exp": 182,
        "height": 18, "weight": 2900, "shoulder": False, "walk": 0.18,
        "moves": [(1, "tackle"), (1, "absorb"), (5, "sandattack"), (9, "razorleaf"), (13, "bulldoze"),
                  (17, "roastpress"), (21, "spikes"), (25, "seedbomb"), (29, "earthquake"), (33, "woodhammer"),
                  (39, "headlongrush")],
        "tm": BASIC_TM + ["earthquake", "bulldoze", "dig", "stealthrock", "spikes", "rockslide", "stoneedge",
                          "seedbomb", "woodhammer", "leafblade", "sandstorm", "sunnyday", "bodypress", "trailblaze"],
        "egg": ["spikyshield", "needlearm"], "evolve": None,
        "drops": [("minecraft:terracotta", "1-3", None), ("minecraft:cactus", "0-1", None)],
        "entry": ("Agavolem spends decades absorbing desert sunlight into its spiky core. When baked by volcanic heat, "
                  "its sap turns into a sweet, fiery nectar."),
        "spawns": [liq_spawn("agavolem-liquor", "uncommon", "22-44", 1.6)],
        "how": [LIQ_HOW.format("uncommon"), "It learns Roast & Press at level 17."],
    },
    "corkscrew": {
        "dex": 3124, "name": "Corkscrew", "line": "liq_cork", "types": ["flying", "steel"], **LIQ, "catch": 120,
        "male": -1, "egg_groups": ["mineral", "flying"],
        "abilities": ["superluck", "skilllink", "h:technician"],
        "ability_names": "Super Luck / Skill Link / Technician (hidden)",
        "stats": stats(60, 100, 80, 45, 60, 120), "ev": evs(speed=2), "exp": 166,
        "height": 5, "weight": 22, "shoulder": True, "walk": 0.34, "fly": True,
        "moves": [(1, "peck"), (1, "metalclaw"), (5, "focusenergy"), (9, "aerialace"), (13, "drillpeck"),
                  (17, "popoff"), (21, "steelwing"), (25, "drillrun"), (29, "bravebird"), (33, "ironhead"),
                  (39, "swordsdance")],
        "tm": BASIC_TM + ["aerialace", "acrobatics", "bravebird", "drillrun", "ironhead", "steelwing", "uturn",
                          "swordsdance", "agility", "tailwind", "roost", "flashcannon", "dualwingbeat"],
        "egg": ["rapidspin", "featherdance"], "evolve": None,
        "drops": [("minecraft:iron_nugget", "2-5", None), ("minecraft:feather", "0-1", None)],
        "entry": ("Corkscrew spins rapidly to bore through wooden casks and dense tree bark. The sound of it taking "
                  "flight echoes like a popping bottle."),
        "spawns": [liq_spawn("corkscrew-liquor", "uncommon", "18-40", 2.0)],
        "how": [LIQ_HOW.format("uncommon"), "It learns Pop Off at level 17."],
    },
    "sommelgeist": {
        "dex": 3125, "name": "Sommelgeist", "line": "liq_cellar", "types": ["psychic", "ghost"], **LIQ, "catch": 45,
        "male": 0.5, "egg_groups": ["amorphous"],
        "abilities": ["agedvintage", "cursedbody", "h:magicbounce"],
        "ability_names": "Aged Vintage / Cursed Body / Magic Bounce (hidden)",
        "stats": stats(65, 45, 65, 95, 95, 75), "ev": evs(special_defence=2), "exp": 174,
        "height": 14, "weight": 1, "shoulder": False, "walk": 0.24, "fly": True,
        "moves": [(1, "confusion"), (1, "astonish"), (5, "disable"), (9, "hex"), (13, "psybeam"), (17, "calmmind"),
                  (21, "shadowball"), (25, "psychic"), (29, "trickroom"), (33, "storedpower"), (39, "futuresight")],
        "tm": BASIC_TM + ["psychic", "psyshock", "shadowball", "hex", "calmmind", "trickroom", "storedpower",
                          "willowisp", "nastyplot", "trick", "painsplit", "dazzlinggleam", "darkpulse"],
        "egg": ["imprison", "destinybond"], "evolve": None,
        "drops": [("minecraft:sweet_berries", "1-3", None), ("minecraft:red_dye", "0-1", None)],
        "entry": ("Sommelgeist haunts centuries-old underground cellars, judging the quality of buried casks and "
                  "guarding rare vintages from thieves."),
        "spawns": [liq_spawn("sommelgeist-liquor", "rare", "28-48", 0.8, timeRange="night")],
        "how": [LIQ_HOW.format("rare, at night,"), "Its ability Aged Vintage raises a random stat at the end of every "
                "turn it stays in battle."],
    },
    "meadbee": {
        "dex": 3126, "name": "Meadbee", "line": "liq_mead", "types": ["bug", "fairy"], **LIQ, "catch": 150,
        "male": 0.5, "egg_groups": ["bug", "fairy"],
        "abilities": ["honeygather", "sweetveil", "h:friendguard"],
        "ability_names": "Honey Gather / Sweet Veil / Friend Guard (hidden)",
        "stats": stats(75, 80, 65, 60, 80, 90), "ev": evs(speed=1, hp=1), "exp": 156,
        "height": 4, "weight": 12, "shoulder": True, "walk": 0.3, "fly": True,
        "moves": [(1, "bugbite"), (1, "sweetscent"), (5, "fairywind"), (9, "strugglebug"), (13, "drainingkiss"),
                  (17, "pollenpuff"), (21, "nectartoast"), (25, "bugbuzz"), (29, "playrough"), (33, "uturn"),
                  (39, "quiverdance")],
        "tm": BASIC_TM + ["bugbuzz", "uturn", "pollenpuff", "playrough", "dazzlinggleam", "drainingkiss", "charm",
                          "acrobatics", "lunge", "pounce", "mistyterrain", "tailwind"],
        "egg": ["helpinghand", "attract"], "evolve": None,
        "drops": [("minecraft:honeycomb", "1-2", None), ("minecraft:honey_bottle", "0-1", None)],
        "entry": ("Ancient warriors celebrated victories alongside swarms of Meadbee, whose fermented honey was said to "
                  "grant courage and song."),
        "spawns": [liq_spawn("meadbee-liquor", "common", "6-30", 6.0, timeRange="day")],
        "how": [LIQ_HOW.format("common, by day,"), "It learns Nectar Toast at level 21."],
    },
    "peatling": {
        "dex": 3127, "name": "Peatling", "line": "liq_peat", "types": ["rock", "fire"], **LIQ, "catch": 150,
        "male": 0.5, "egg_groups": ["mineral", "field"],
        "abilities": ["smokycask", "flamebody", "h:whitesmoke"],
        "ability_names": "Smoky Cask / Flame Body / White Smoke (hidden)",
        "stats": stats(75, 85, 105, 80, 70, 40), "ev": evs(defence=2), "exp": 160,
        "height": 4, "weight": 260, "shoulder": False, "walk": 0.2,
        "moves": [(1, "ember"), (1, "rockthrow"), (5, "smokescreen"), (9, "smog"), (13, "rocktomb"),
                  (17, "lavaplume"), (21, "ancientpower"), (25, "willowisp"), (29, "rockslide"), (33, "flamethrower"),
                  (39, "eruption")],
        "tm": BASIC_TM + ["rockslide", "stoneedge", "stealthrock", "flamethrower", "fireblast", "willowisp",
                          "heatwave", "sludgebomb", "sunnyday", "sandstorm", "earthpower", "irondefense"],
        "egg": ["yawn", "curse"], "evolve": None,
        "drops": [("minecraft:charcoal", "1-3", None), ("minecraft:moss_block", "0-1", None)],
        "entry": ("Dug up from ancient coastal bogs, Peatling burns slowly for centuries, infusing nearby water springs "
                  "with its distinct smoky flavor."),
        "spawns": [liq_spawn("peatling-liquor", "common", "8-30", 5.0)],
        "how": [LIQ_HOW.format("common"), "Its ability Smoky Cask powers up its Fire and Poison moves and fills the "
                "field with smoke that stops stats being lowered."],
    },
    "spiritskull": {
        "dex": 3128, "name": "Spiritskull", "line": "liq_skull", "types": ["ghost", "poison"], **LIQ, "catch": 60,
        "male": -1, "egg_groups": ["amorphous"],
        "abilities": ["cursedbody", "levitate", "h:infiltrator"],
        "ability_names": "Cursed Body / Levitate / Infiltrator (hidden)",
        "stats": stats(65, 55, 75, 110, 95, 90), "ev": evs(special_attack=2), "exp": 176,
        "height": 4, "weight": 30, "shoulder": False, "walk": 0.26, "fly": True,
        "moves": [(1, "astonish"), (1, "acid"), (5, "smog"), (9, "hex"), (13, "venoshock"), (17, "confuseray"),
                  (21, "hangover"), (25, "sludgebomb"), (29, "shadowball"), (33, "nastyplot"), (39, "sludgewave")],
        "tm": BASIC_TM + ["shadowball", "hex", "sludgebomb", "sludgewave", "venoshock", "toxicspikes", "willowisp",
                          "nastyplot", "trick", "painsplit", "darkpulse", "psychic"],
        "egg": ["memento", "destinybond"], "evolve": None,
        "drops": [("minecraft:bone", "1-2", None), ("minecraft:amethyst_shard", "0-2", None)],
        "entry": ("Legend says Spiritskull forms inside abandoned bottles left on sunken ships. Those who drink from it "
                  "experience vivid memories that aren't their own."),
        "spawns": [liq_spawn("spiritskull-liquor", "rare", "26-46", 0.8, timeRange="night")],
        "how": [LIQ_HOW.format("rare, at night,"), "It learns Hangover at level 21."],
    },
    "caskade": {
        "dex": 3129, "name": "Caskade", "line": "liq_cask", "types": ["water", "grass"], **LIQ, "catch": 75,
        "male": 0.5, "egg_groups": ["monster", "grass"],
        "abilities": ["oakmaturation", "shellarmor", "h:harvest"],
        "ability_names": "Oak Maturation / Shell Armor / Harvest (hidden)",
        "stats": stats(105, 75, 120, 65, 95, 30), "ev": evs(defence=2), "exp": 180,
        "height": 10, "weight": 2400, "shoulder": False, "walk": 0.14,
        "moves": [(1, "tackle"), (1, "withdraw"), (5, "watergun"), (9, "absorb"), (13, "bubblebeam"),
                  (17, "leechseed"), (21, "aquaring"), (25, "gigadrain"), (29, "shellsmash"), (33, "woodhammer"),
                  (39, "hydropump")],
        "tm": BASIC_TM + ["surf", "scald", "waterpulse", "gigadrain", "energyball", "seedbomb", "woodhammer",
                          "bodypress", "irondefense", "raindance", "grassyterrain", "earthquake", "stealthrock"],
        "egg": ["recycle", "stockpile", "slackoff"], "evolve": None,
        "drops": [("minecraft:oak_planks", "1-3", None), ("minecraft:sweet_berries", "1-3", None)],
        "entry": ("Caskade wanders mountain trails for decades, allowing rainwater and wild berries to ferment inside "
                  "its oaken shell into a prized elixir."),
        "spawns": [liq_spawn("caskade-liquor", "common", "10-34", 4.0)],
        "how": [LIQ_HOW.format("common"), "Its ability Oak Maturation doubles the effect of the Berry it holds and "
                "grows a new one two turns after it eats it."],
    },
    "stillforge": {
        "dex": 3130, "name": "Stillforge", "line": "liq_still", "types": ["steel", "fire"], **LIQ, "catch": 45,
        "male": -1, "egg_groups": ["mineral"],
        "abilities": ["heatproof", "steamengine", "h:filter"],
        "ability_names": "Heatproof / Steam Engine / Filter (hidden)",
        "stats": stats(90, 75, 110, 110, 85, 40), "ev": evs(special_attack=2), "exp": 190,
        "height": 26, "weight": 5800, "shoulder": False, "walk": 0.18,
        "moves": [(1, "ember"), (1, "metalclaw"), (5, "irondefense"), (9, "flamecharge"), (13, "flashcannon"),
                  (17, "distill"), (21, "lavaplume"), (25, "steelbeam"), (29, "flamethrower"), (33, "shiftgear"),
                  (39, "overheat")],
        "tm": BASIC_TM + ["flashcannon", "steelbeam", "ironhead", "heavyslam", "flamethrower", "fireblast",
                          "overheat", "heatwave", "irondefense", "willowisp", "sunnyday", "bodypress", "scald"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:copper_ingot", "2-4", None), ("minecraft:raw_copper", "1-2", None)],
        "entry": ("Engineered by master craftsmen, Stillforge boils impure water inside its copper belly and condenses "
                  "it into pure, elemental energy."),
        "spawns": [liq_spawn("stillforge-liquor", "rare", "30-50", 0.6)],
        "how": [LIQ_HOW.format("rare"), "It learns Distill at level 17."],
    },
    "stumblepup": {
        "dex": 3131, "name": "Stumblepup", "line": "liq_hound", "types": ["normal"], **LIQ, "catch": 190,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["liquidcourage", "friendguard", "h:tangledfeet"],
        "ability_names": "Liquid Courage / Friend Guard / Tangled Feet (hidden)",
        "stats": stats(60, 65, 55, 35, 50, 45), "ev": evs(hp=1), "exp": 62,
        "height": 4, "weight": 70, "shoulder": True, "walk": 0.28,
        "moves": [(1, "tackle"), (1, "tailwhip"), (5, "lick"), (9, "bite"), (13, "headbutt"), (17, "helpinghand"),
                  (21, "takedown"), (25, "playrough"), (30, "doubleedge")],
        "tm": BASIC_TM + ["bodyslam", "playrough", "crunch", "icefang", "firefang", "dig", "helpinghand", "swagger",
                          "facade", "rest", "snowscape"],
        "egg": ["yawn", "covet", "wish"], "evolve": ("tavernhound", 30, ["superfang"]),
        "drops": [("minecraft:bone", "0-1", None), ("minecraft:white_wool", "0-1", None)],
        "entry": ("Trained to rescue lost hikers in snowy passes, Stumblepup carries a warming tonic in its neck "
                  "barrel—though it often spills half of it tripping over its own paws."),
        "spawns": [liq_spawn("stumblepup-liquor", "common", "4-26", 7.0)],
        "how": [LIQ_HOW.format("common"), "Evolves into Tavern Hound at level 30."],
    },
    "tavernhound": {
        "dex": 3132, "name": "Tavern Hound", "line": "liq_hound", "types": ["normal"], **LIQ, "catch": 75,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["liquidcourage", "friendguard", "h:tangledfeet"],
        "ability_names": "Liquid Courage / Friend Guard / Tangled Feet (hidden)",
        "stats": stats(110, 115, 90, 50, 85, 50), "ev": evs(hp=2, attack=1), "exp": 186,
        "height": 14, "weight": 910, "shoulder": False, "walk": 0.24,
        "moves": [(1, "superfang"), (1, "tackle"), (1, "tailwhip"), (5, "lick"), (9, "bite"), (13, "headbutt"),
                  (17, "helpinghand"), (21, "takedown"), (25, "playrough"), (30, "superfang"), (34, "bodyslam"),
                  (40, "doubleedge"), (46, "gigaimpact")],
        "tm": BASIC_TM + ["bodyslam", "playrough", "crunch", "icefang", "firefang", "dig", "helpinghand", "swagger",
                          "facade", "earthquake", "gigaimpact", "hyperbeam", "snowscape", "bulkup"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:bone", "1-2", None), ("minecraft:white_wool", "1-2", None)],
        "entry": ("It strides the snowy passes with a full keg of warm tonic under its chin, and lost hikers who hear "
                  "it baying know help is coming, slowly but surely."),
        "spawns": [liq_spawn("tavernhound-liquor", "rare", "30-46", 0.8)],
        "how": ["Evolve Stumblepup at level 30. It learns Super Fang when it evolves.", LIQ_HOW.format("rare")],
    },
    "bootlegger": {
        "dex": 3133, "name": "Bootlegger", "line": "liq_bandit", "types": ["dark"], **LIQ, "catch": 190,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["pickpocket", "quickfeet", "h:prankster"],
        "ability_names": "Pickpocket / Quick Feet / Prankster (hidden)",
        "stats": stats(50, 60, 45, 45, 45, 75), "ev": evs(speed=1), "exp": 62,
        "height": 4, "weight": 60, "shoulder": True, "walk": 0.32,
        "moves": [(1, "scratch"), (1, "leer"), (5, "thief"), (9, "bite"), (13, "faketears"), (17, "feintattack"),
                  (22, "contrabandswap"), (26, "nightslash"), (30, "suckerpunch")],
        "tm": BASIC_TM + ["thief", "knockoff", "suckerpunch", "crunch", "uturn", "taunt", "torment", "foulplay",
                          "darkpulse", "dig", "snarl"],
        "egg": ["covet", "switcheroo", "partingshot"],
        "evolve": ("moonshiner", 34, ["knockoff"], [{"variant": "time_range", "range": "night"}]),
        "drops": [("minecraft:glass_bottle", "0-1", None), ("minecraft:gray_dye", "0-1", None)],
        "entry": ("A little smuggler that hauls a stolen jug through the woods at dusk. If it is caught, it plays dead "
                  "until whoever caught it looks away, then bolts with whatever it can carry."),
        "spawns": [liq_spawn("bootlegger-liquor", "common", "4-26", 6.0, timeRange="night")],
        "how": [LIQ_HOW.format("common, at night,"), "It learns Contraband Swap at level 22.",
                "Evolves into Moonshiner at level 34 at night."],
    },
    "moonshiner": {
        "dex": 3134, "name": "Moonshiner", "line": "liq_bandit", "types": ["dark"], **LIQ, "catch": 60,
        "male": 0.5, "egg_groups": ["field"],
        "abilities": ["pickpocket", "quickfeet", "h:prankster"],
        "ability_names": "Pickpocket / Quick Feet / Prankster (hidden)",
        "stats": stats(75, 105, 70, 80, 70, 105), "ev": evs(attack=1, speed=2), "exp": 188,
        "height": 13, "weight": 380, "shoulder": False, "walk": 0.3,
        "moves": [(1, "knockoff"), (1, "scratch"), (1, "leer"), (5, "thief"), (9, "bite"), (13, "faketears"),
                  (17, "feintattack"), (22, "contrabandswap"), (26, "nightslash"), (30, "suckerpunch"), (34, "knockoff"),
                  (40, "nastyplot"), (46, "darkpulse"), (52, "partingshot")],
        "tm": BASIC_TM + ["thief", "knockoff", "suckerpunch", "crunch", "uturn", "taunt", "torment", "foulplay",
                          "darkpulse", "dig", "snarl", "nastyplot", "willowisp", "gunkshot", "throatchop"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:glass_bottle", "1-2", None), ("minecraft:leather", "0-1", None)],
        "entry": ("Moonshiner builds hidden stills deep in mountain forests, using reflective mirrors to hide its "
                  "campfire smoke from patrolling Ranger Pokémon."),
        "spawns": [liq_spawn("moonshiner-liquor", "rare", "34-50", 0.6, timeRange="night")],
        "how": ["Evolve Bootlegger at level 34 at night. It learns Knock Off when it evolves.",
                LIQ_HOW.format("rare, at night,")],
    },
    "bacchudrake": {
        "dex": 3135, "name": "Bacchudrake", "line": "liq_dragon", "types": ["dragon", "fairy"],
        "friendship": 100, "growth": "slow", "catch": 3, "male": -1, "egg_groups": ["undiscovered"],
        "labels": ["legendary"],
        "abilities": ["serenegrace", "h:sweetveil"], "ability_names": "Serene Grace / Sweet Veil (hidden)",
        "stats": stats(100, 90, 90, 130, 100, 90), "ev": evs(special_attack=3), "exp": 300,
        "height": 28, "weight": 1100, "shoulder": False, "walk": 0.3, "fly": True,
        "moves": [(1, "dragonbreath"), (1, "fairywind"), (1, "safeguard"), (10, "twister"), (20, "drainingkiss"),
                  (30, "dragonpulse"), (40, "effervescentroar"), (50, "moonblast"), (60, "dragondance"),
                  (70, "dracometeor"), (80, "lifedew")],
        "tm": BASIC_TM + ["dragonpulse", "dracometeor", "moonblast", "dazzlinggleam", "calmmind", "roost", "hurricane",
                          "outrage", "dragondance", "hyperbeam", "gigaimpact", "mistyterrain", "surf"],
        "egg": [], "evolve": None,
        "drops": [("minecraft:glow_berries", "2-4", None), ("minecraft:gold_ingot", "2-4", None)],
        "entry": ("Said to appear only once a century during the grandest autumn harvest, Bacchudrake's joyous roar "
                  "turns ordinary river water into sparkling nectar."),
        "spawns": [liq_spawn("bacchudrake-liquor", "ultra-rare", "60-70", 0.1)],
        "how": ["Wild: ultra-rare in the Liquor Meadows (an overworld biome added by CobbleEffort: Kanto 0.8.0), level "
                "60-70.", "It learns Effervescent Roar at level 40."],
    },
})
for _sp in ("hopsprout", "flambeer", "sakekoi", "joltini", "ontherox", "brawlerry", "absinthia", "agavolem", "corkscrew",
            "sommelgeist", "meadbee", "peatling", "spiritskull", "caskade", "stillforge", "bacchudrake"):
    LINES[SPECIES[_sp]["line"]] = [_sp]
LINES["liq_hound"] = ["stumblepup", "tavernhound"]
LINES["liq_bandit"] = ["bootlegger", "moonshiner"]

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
    "hivemind": {
        "name": "Hive Mind",
        "js": """{
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (!source || source === target || source.side === target.side || !source.hasType('Bug')) return;
  this.add('-activate', target, 'ability: Hive Mind');
  if (move.category !== 'Status') {
    const own = source.side.active.filter(p => p && !p.fainted && p.hp > 0);
    const victim = own.length ? this.sample(own) : source;
    const damage = this.actions.getDamage(source, victim, move);
    if (typeof damage === 'number' && damage > 0) this.damage(damage, victim, target, this.effect);
  }
  return null;
},
flags: {breakable: 1},
name: "Hive Mind",
rating: 3.5,
num: -3007
}
""",
        "lang": "Thousands of fallen Bug Pokémon live on in it, bound by a fungus: a Bug-type foe's moves can never "
                "harm it. The hive seizes them, and the attack strikes the foe's own side instead.",
        "battle": {
            "cobblemon.battle.activate.hivemind": "%1$s's hive mind seized the attack!",
            "cobblemon.battle.damage.hivemind": "%1$s was struck by its own side's attack!",
        },
    },
    "insectivore": {
        "name": "Insectivore",
        "js": """{
onModifyMovePriority: -3,
onModifyMove(move) {
  if (move.category === 'Status') return;
  const before = move.onEffectiveness;
  move.onEffectiveness = function (typeMod, target, type, m) {
    if (target && target.hasType('Bug')) return type === 'Bug' ? 2 : 0;
    return before ? before.call(this, typeMod, target, type, m) : typeMod;
  };
},
onAnyNegateImmunity(pokemon, type) {
  if (pokemon && pokemon.hasType('Bug') && this.activePokemon === this.effectState.target && this.activeMove &&
      this.activeMove.category !== 'Status') return false;
},
flags: {},
name: "Insectivore",
rating: 3,
num: -3006
}
""",
        "lang": "The Pokémon was made to hunt Bug Pokémon: all of its attacks are extremely super effective (4x) on "
                "Bug types, whatever their type, and nothing about them makes a Bug type immune.",
    },
    "systemerror": {
        "name": "System Error",
        "js": """{
onEffectiveness(typeMod, target, type, move) {
  if (!move || target !== this.effectState.target) return typeMod;
  return move.type === 'Normal' ? 1 : 0;
},
onNegateImmunity(pokemon, type) {
  if (type === 'Ghost') return false;
},
onModifyMovePriority: -2,
onModifyMove(move) {
  if (move.type !== 'Normal' || move.category === 'Status') return;
  move.ignoreImmunity = Object.assign({}, typeof move.ignoreImmunity === 'object' ? move.ignoreImmunity : {}, {Normal: true});
  move.onEffectiveness = function (typeMod, target, type) {
    return type === 'Normal' ? 1 : 0;
  };
},
flags: {failroleplay: 1, noreceiver: 1, noentrain: 1, notrace: 1, failskillswap: 1, cantsuppress: 1},
name: "System Error",
rating: 4,
num: -3005
}
""",
        "lang": "The Pokémon's type is Error: every move hits it for neutral damage except Normal-type moves, which "
                "are super effective. Its own Normal-type moves hit everything for neutral damage, ghosts included, "
                "and are super effective on Normal types.",
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
    "primalmimicry": {
        "name": "Primal Mimicry",
        "js": """{
onModifyMovePriority: -1,
onModifyMove(move) {
  if (move.type === 'Water') move.forceSTAB = true;
},
flags: {},
name: "Primal Mimicry",
rating: 3,
num: -3011
}
""",
        "lang": "One claw imitates the titan of the land, the other the titan of the sea: its Water-type moves get the "
                "same-type bonus as well.",
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
    "joeyslingshot": {
        "base": "populationbomb", "num": -3010, "name": "Joey Slingshot", "type": "Normal", "category": "Physical",
        "basePower": 15, "accuracy": 100, "pp": 10, "multihit": 6, "multiaccuracy": False,
        "flags": {"protect": 1, "mirror": 1, "metronome": 1}, "contestType": "Cute",
        "desc": "The user slings its six babies at the target one after another with its tail. Hits six times.",
        "shortDesc": "Hits 6 times.",
        "lang": "The user plucks its babies off its back and slingshots them at the target with its tail, one after "
                "another: six hits in a row.",
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
# the A. Fakemon trio's own page after ours (the fanpage's grass, fire and water starters)
FAKEMON_STARTERS = ("A. Fakemon", -98, ["cobbleeffort:wigwoof", "cobbleeffort:sounflame", "cobbleeffort:fangfosh"])
FAKEMON_STARTERS_2 = ("A. Fakemon II", -97, ["cobbleeffort:whissant", "cobbleeffort:flachiko", "cobbleeffort:brenkey"])



from nico_battle import NICO_ABILITIES, NICO_MOVES                  # the Nicodex's own abilities and moves  # noqa: E402
CUSTOM_ABILITIES.update(NICO_ABILITIES)
CUSTOM_MOVES.update(NICO_MOVES)
from liquor_battle import LIQ_ABILITIES, LIQ_MOVES                # the Liquor Meadows' own abilities and moves  # noqa: E402
CUSTOM_ABILITIES.update(LIQ_ABILITIES)
CUSTOM_MOVES.update(LIQ_MOVES)

def ascii_name(name):
    """The species json's name, in plain ASCII like Cobblemon's own ("Flabebe"): Cobblemon builds the lang key and the
    Showdown id from it and drops other letters, so "Flambéer" would look for cobbleeffort.species.flamber.name. The
    accented spelling goes in the lang file."""
    import unicodedata
    return unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()


def folder(sp):
    return f"{SPECIES[sp]['dex']:04d}_{sp}"


def group_of(sp):
    return f"cobbleeffort_{sp}"


def model_module(sp):
    spec = importlib.util.spec_from_file_location(f"newmon_{sp}", HERE / "models" / f"{sp}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_model_assets(sp, hand, fold):
    """Build a box-model module: its textures (+ glow/shell layers, FORM_VARIANTS), geo, animations and poser, all
    named `sp` under folder `fold`. Returns what a resolver needs. Also used by regional.py for forms with a model of
    their own."""
    m = hand.build()
    tw, th = m.layout()
    k = getattr(hand, "K", 1)
    # borrowed heads (BORROW: tools/newmons/borrowed/<src>.json from borrow_heads.py): their footprints go below our
    # own texture area, their bones are mounted on one of ours (moved to `at`, turned by `rotation`)
    borrowed, extra_bones, y_off = [], [], th
    for bi, bw in enumerate(getattr(hand, "BORROW", [])):
        src = json.loads((HERE / "borrowed" / f"{bw['src']}.json").read_text())
        W, H = src["texture"]
        borrowed.append((bw, src, y_off))
        pre = bw.get("prefix", f"b{bi}_")
        delta = [t - a for t, a in zip(bw["at"], src["anchor"])]
        mv = lambda p: [round(v + d, 4) for v, d in zip(p, delta)]
        extra_bones.append({"name": f"{pre}mount", "parent": bw["parent"], "pivot": [float(v) for v in bw["at"]],
                            "rotation": [float(v) for v in bw.get("rotation", (0, 0, 0))]})
        for b in src["bones"]:
            nb = {"name": pre + b["name"], "parent": pre + (b["parent"] or "mount"), "pivot": mv(b["pivot"])}
            if b.get("rotation"):
                nb["rotation"] = b["rotation"]
            cubes = []
            for c in b["cubes"]:
                nc = dict(c, origin=mv(c["origin"]), uv=[c["uv"][0], c["uv"][1] + y_off])
                if "pivot" in c:
                    nc["pivot"] = mv(c["pivot"])
                cubes.append(nc)
            if cubes:
                nb["cubes"] = cubes
            extra_bones.append(nb)
        y_off += H
    tw_full, th_full = (max(tw, 256), y_off) if borrowed else (tw, th)

    def with_borrowed(img, key):
        """Our painted texture on the full-size canvas, with the borrowed footprints (variant `key`) pasted below."""
        if not borrowed:
            return img
        out = Image.new("RGBA", (tw_full * k, th_full * k))
        out.paste(img, (0, 0))
        for bw, src, yo in borrowed:
            f = HERE / "borrowed" / f"{bw['src']}{key}.png"
            if f.exists():
                part = Image.open(f).convert("RGBA")
                out.paste(part.resize((part.size[0] * k, part.size[1] * k), Image.NEAREST), (0, yo * k))
        return out
    tex_dir = RES / "assets" / MOD / "textures" / "pokemon" / fold
    tex_dir.mkdir(parents=True, exist_ok=True)
    tex = lambda n: f"{MOD}:textures/pokemon/{fold}/{n}.png"
    layers = {"": [], "_shiny": []}                         # resolver layers per variant (glow, translucent shell)
    for variant, sfx in ((None, ""), ("shiny", "_shiny")):
        img, glow = m.paint(tw, th, variant, k=k)
        img = with_borrowed(img, sfx)
        glow = with_borrowed(glow, "_emissive" + sfx) if borrowed else glow
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
    # forms that only change the texture (e.g. a type form): FORM_VARIANTS = [(aspect, variant key), ...]; each is
    # painted with variant=<key> and <key>_shiny, with its own glow layer when it glows
    form_vars = []
    for aspect, key in getattr(hand, "FORM_VARIANTS", []):
        for vkey, shiny in ((key, False), (f"{key}_shiny", True)):
            img, glow = m.paint(tw, th, vkey, k=k)
            Image.fromarray(np.array(img), "RGBA").save(tex_dir / f"{sp}_{vkey}.png", optimize=True)
            lay = []
            g = np.array(glow)
            if g[..., 3].any():
                Image.fromarray(g, "RGBA").save(tex_dir / f"{sp}_{vkey}_glow.png", optimize=True)
                lay.append({"name": "cobbleeffort_glow", "emissive": True, "translucent": True, "texture": tex(f"{sp}_{vkey}_glow")})
            form_vars.append({"aspects": [aspect] + (["shiny"] if shiny else []), "texture": tex(f"{sp}_{vkey}"),
                              "layers": lay})
    names = [b["name"] for b in m.bones if b["parent"] is not None]
    piv = {b["name"]: b["pivot"] for b in m.bones}
    legs = [n for n in names if n.startswith("leg")]
    top = getattr(hand, "HEIGHT", None) or max(b.lo[1] + b.size[1] for b in m.boxes)
    # Cobblemon multiplies the hitbox by baseScale: HITBOX is in model units, like the model itself
    model_h, box_h = top * hand.SCALE / 16, hand.HITBOX[1] * hand.SCALE
    if not 0.5 * model_h <= box_h <= max(1.5 * model_h, 0.3):             # (tiny ones may be a bit bigger)
        raise SystemExit(f"{sp}: hitbox {box_h:.2f} blocks tall in game but the model is {model_h:.2f} "
                         f"(HITBOX is scaled by SCALE)")
    root = m.bones[0]["name"]
    extra = [{"name": "locator_root", "parent": root, "pivot": [0, 0, 0]},
             {"name": "locator_top", "parent": root, "pivot": [0, float(top), 0]}]
    bedrock = RES / "assets" / MOD / "bedrock" / "pokemon"
    write_json(bedrock / "models" / fold / f"{sp}.geo.json", m.geo(tw_full, th_full, f"geometry.{sp}", extra + extra_bones))
    write_json(bedrock / "animations" / fold / f"{group_of(sp)}.animation.json",
               animations(group_of(sp), getattr(hand, "KIND", "quadruped"), getattr(hand, "ANIM", {}), names, legs, piv))
    write_json(bedrock / "posers" / fold / f"{sp}.json", poser(group_of(sp), sp, top, hand.SCALE, names))
    print(f"{sp}: {len(m.boxes)} cubes, texture {tw}x{th} (x{k}), {top} units tall, bones {names}")
    return {"tex": tex, "layers": layers, "form_vars": form_vars, "top": top, "names": names}


def build_model(sp):
    cfg = SPECIES[sp]
    hand = model_module(sp)
    cfg.update(scale=hand.SCALE, hitbox=hand.HITBOX, look=hand.LOOK)
    r = write_model_assets(sp, hand, folder(sp))
    tex, layers = r["tex"], r["layers"]
    cfg["layers"] = layers
    cfg["model_height"] = r["top"]
    write_json(RES / "assets" / MOD / "bedrock" / "pokemon" / "resolvers" / folder(sp) / f"0_{sp}_base.json", {
        "species": f"{MOD}:{sp}", "order": 0,
        "variations": [
            {"aspects": [], "poser": f"{MOD}:{sp}", "model": f"{MOD}:{sp}.geo", "texture": tex(sp), "layers": layers[""]},
            {"aspects": ["shiny"], "texture": tex(f"{sp}_shiny"), **({"layers": layers["_shiny"]} if layers["_shiny"] else {})},
        ] + r["form_vars"]})


def species_json(sp):
    c = SPECIES[sp]
    d = {
        "implemented": True, "nationalPokedexNumber": c["dex"], "name": ascii_name(c["name"]), "primaryType": c["types"][0],
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
    if c.get("forms"):                                      # forms picked by aspects (e.g. a type form from a cosmetic)
        d["forms"] = c["forms"]
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
        if c.get("consume"):
            # Cobblemon takes the held item as soon as it OFFERS the evolution (the Evolve button), then drops offers
            # whose requirements stop passing unless they're permanent: like its own Happiny/Oval Stone evolution
            d["evolutions"][0]["permanent"] = True
    pre = [s for s, o in SPECIES.items() if (o["evolve"] and o["evolve"][0] == sp)
           or (o.get("evolve_stone") and o["evolve_stone"][0] == sp)]
    if c.get("pre"):                                        # evolves from another mod's form (e.g. a regional one)
        d["preEvolution"] = c["pre"]
    elif pre:
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
        for rel, content in c.get("data_files", {}).items():   # extra data files (features, MoLang callbacks)
            out = RES / "data" / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, str):
                out.write_text(content)
            else:
                write_json(out, content)
        if c.get("evolves_from"):                          # another mod's species evolves into ours (Cobblemon appends)
            target, name, evo = c["evolves_from"]
            write_json(data / "species_additions" / f"{name}.json",
                       {"target": target, "evolutions": evo if isinstance(evo, list) else [evo]})
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
        lang.update(ab.get("battle", {}))
    for name, order, key, mons in STARTER_CATEGORIES:
        write_json(data / "starters" / f"{key}.json", {
            "name": name, "order": order, "displayName": f"cobblemon.starterselection.category.{key}",
            "pokemon": [f"{m} level=10" for m in mons]})
    for key, (name, order, mons) in (("cobbleeffort", OUR_STARTERS), ("afakemon", FAKEMON_STARTERS),
                                      ("afakemon2", FAKEMON_STARTERS_2)):
        write_json(data / "starters" / f"{key}.json", {
            "name": name, "order": order, "displayName": f"cobbleeffort.starterselection.category.{key}",
            "pokemon": [f"{m} level=10" for m in mons]})
    import fossils                                           # fossil items, structures and Cobblemon fossil entries
    fossils.build(lang)
    import nests                                             # nest structures (the pinbirds spawn at theirs)
    nests.build(lang)
    _tufts.build(lang)                                       # Aetherim's elemental tufts (cosmetic items + named tufts)
    import subprocess                                       # the creative tab's item list (fossils, tufts, collections)
    subprocess.run([sys.executable, str(HERE.parent / "make_creative_tab.py")], check=True)
    lang["cobbleeffort.starterselection.category.cobbleeffort"] = "CobbleEffort"
    lang["cobbleeffort.starterselection.category.afakemon"] = "A. Fakemon"
    lang["cobbleeffort.starterselection.category.afakemon2"] = "A. Fakemon II"
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
        inches = round(c["height"] * 10 / 2.54)
        size = f"{inches // 12}'{inches % 12}\" ({c['height'] / 10:g} m) / {c['weight'] / 10:g} kg"
        rows.append(f"| {c['dex']} | **{c['name']}** | {' / '.join(t.title() for t in c['types'])} | {c['ability_names']} | "
                    f"{nums} | {size} | {' '.join(c['how'])} | {c['entry']} |")
    path.write_text(text[:text.index(a) + len(a)] + "\n" + "\n".join(rows) + "\n" + text[text.index(b):])


if __name__ == "__main__":
    main()
