"""Text templates written by 'init' and 'add' (JSON with comments)."""

from __future__ import annotations

import json


def addon_json(name: str, namespace: str, author: str) -> str:
    return f"""{{
  // Shown in the mod list / pack screen
  "name": {json.dumps(name)},
  // Resource namespace for all your Pokemon (lowercase, a-z 0-9 _). Species ids become {namespace}:<name>
  "namespace": {json.dumps(namespace)},
  "version": "1.0.0",
  "author": {json.dumps(author)},
  "description": "Custom Pokemon made with CobbleEffort",
  // First Pokedex number handed out automatically (skips any you set by hand)
  "dex_start": 2000,
  // Minecraft 1.21.1 values (Cobblemon 1.6/1.7). max_format keeps newer versions happy too.
  "pack_format": {{ "data": 48, "resource": 34 }},
  "max_format": 999,
  // What to build: "jar" (drop-in mod for Fabric + NeoForge), "datapack", "resourcepack"
  "outputs": ["jar", "datapack", "resourcepack"]
}}
"""


def pokemon_json(*, name: str, types: list[str], archetype: str, evolutions: list[str], rig_lines: list[str],
                 dex_entry: str = "") -> str:
    evo = ", ".join(json.dumps(e) for e in evolutions)
    rig_comment = "\n".join(f"  //   {line}" for line in rig_lines)
    return f"""{{
  // ===================== REQUIRED =====================
  "name": {json.dumps(name)},
  "types": {json.dumps(types)},                 // 1 or 2 of: normal fire water grass electric ice fighting poison
                                       //   ground flying psychic bug rock ghost dragon dark steel fairy

  // ===================== OPTIONAL (delete anything you don't need) =====================
  // "dex": 2001,                      // Pokedex number (auto if omitted)
  "dex_entry": {json.dumps(dex_entry or f"A newly discovered Pokemon called {name}.")},

  // Stats: a dict, a list [hp, atk, def, spa, spd, spe], or just a total + spread preset.
  //   spreads: balanced physical special mixed tank special_tank fast bulky glass_cannon
  // "stats": {{ "hp": 60, "atk": 70, "def": 55, "spa": 80, "spd": 60, "spe": 75 }},
  // With nothing set, the total scales with evolution stage (320 / 420 / 525; 450 if it doesn't evolve).
  // "bst": 420,
  "spread": "balanced",

  // Abilities: prefix the hidden one with h:   (auto-picked from the type if omitted)
  // "abilities": ["blaze", "h:flashfire"],

  // Moves: "auto" gives a type-based learnset. Or: {{ "1": "tackle, growl", "7": "ember", "egg": [...], "tm": "auto" }}
  "moves": "auto",

  // Evolutions - one line each:  "target @ condition [+ condition]"
  //   level 36 | item fire_stone | trade | trade holding metal_coat | friendship 160 | time night
  //   holding razor_claw | move ancientpower | biome forest | rain | female | learns flamethrower
  // Put the target's folder in this same project and it gets linked automatically
  // (pre-evolution, dex order, and it inherits types/abilities/moves unless it sets its own).
  "evolutions": [{evo}],

  // walker | flier | swimmer | floater | amphibian | auto (decided from the model's bones)
  "archetype": {json.dumps(archetype)},

  // "gender": 0.5,                    // male ratio 0-1, or "genderless", "male", "female"
  // "catch_rate": 45,
  // "experience_group": "medium_slow", // erratic fast medium_fast medium_slow slow fluctuating
  // "egg_groups": ["field"],
  // "scale": 1.0,                     // in-game size multiplier (hitbox follows)
  // "height_m": 1.2, "weight_kg": 30, // Pokedex info (auto from the model size)
  // "walk_speed": 0.3,
  // "drops": ["minecraft:bone 0-2", "cobblemon:oran_berry 5%"],

  // Spawning. "auto": true = only spawns if this is a base form (evolved forms don't).
  // Delete "auto" to force spawning, or use "spawn": false to never spawn.
  "spawn": {{
    "auto": true,
    "biomes": ["overworld"],           // "forest" -> #cobblemon:is_forest, or full ids/tags
    "rarity": "uncommon",              // common uncommon rare ultra-rare
    "levels": "5-30",
    "weight": 6
    // "time": "night", "weather": "rain", "where": "grounded"   (grounded submerged surface seafloor)
  }},

  // Shiny: "auto" hue-shifts the texture (or drop a <name>_shiny.png in this folder).
  //   {{ "hue": 120, "saturation": 1.1, "brightness": 1.0 }}  or  {{ "palette": {{ "#ff8800": "#3366ff" }}, "tolerance": 10 }}
  "shiny": "auto",

  // Animation feel. Hand-made animations (in the .bbmodel or *.animation.json) always win;
  // the generator only fills in what's missing. "skip": ["status"] to leave some out.
  "animation": {{ "energy": 1.0, "speed": 1.0 }}

  // If a bone was detected wrong, fix it here, e.g.
  // "rig": {{ "head": "skull", "tails": ["tail1", "tail2"], "legs": ["lf", "rf", "lb", "rb"], "ignore": ["cape"] }},
  // Portrait framing in the party/summary screen:
  // "poser": {{ "portrait_scale": 1.8, "portrait_translation": [0, -0.4, 0], "profile_scale": 0.75 }},
  // Raw Cobblemon species fields merged in last (for anything not covered above):
  // "extra": {{ "lightingData": {{ "lightLevel": 10, "liquidGlowMode": "LAND" }} }}

  // ---- Detected rig (for reference) ----
{rig_comment}
}}
"""
