"""
Gameplay data for the creatures: species, forms, features, interactions, fossil recipe, spawns, lang.

Everything here is data-only Cobblemon content:
  * Armored Mewtwo: a real "Armored" form of Mewtwo (own stats/ability), switched on by the `armored` flag.
    Using a Netherite Chestplate on your own Mewtwo consumes it and sets the flag for good (pokemon_interactions).
  * Shadow Lugia: the `shadow` flag (a look, same stats as XD). An Echo Shard used on your Lugia turns it Shadow;
    a Golden Apple purifies it. Shadow Lugia also spawns wild, ultra-rarely, in deep oceans during thunderstorms.
  * Celesteela, Iron Boulder: Cobblemon has their species data but no models, so they're switched on
    (`implemented`) via species_additions and given ultra-rare spawns (The End; mountain peaks at night).
  * Origin Dragon: a new species. Revived in Cobblemon's Fossil Restoration Machine from a Dragon Egg,
    a Nether Star and a Heavy Core. Its moves are the union of Kyurem's, Reshiram's and Zekrom's.
  * Mewtwo and Lugia get ultra-rare spawns (Cobblemon 1.8.4 has none), so the whole chain works in survival.
"""
from __future__ import annotations

import json
from pathlib import Path


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def flag(key):
    return {"keys": [key], "type": "flag", "isAspect": True, "default": False}


def merged_moves(cob_species: Path, names):
    """Union of several species' learnsets; for a move learned several ways keep the earliest level."""
    level, other = {}, []
    for n in names:
        data = json.loads(next(cob_species.glob(f"*/{n}.json")).read_text())
        for entry in data.get("moves", []):
            how, move = entry.split(":", 1)
            if how.isdigit():
                level[move] = min(level.get(move, 999), int(how))
            elif entry not in other:
                other.append(entry)
    return [f"{lv}:{mv}" for mv, lv in sorted(level.items(), key=lambda kv: (kv[1], kv[0]))] + sorted(other)


def spawn(id_, pokemon, level, weight, condition, position="grounded", bucket="ultra-rare"):
    return {"id": id_, "pokemon": pokemon, "presets": [], "type": "pokemon", "spawnablePositionType": position,
            "bucket": bucket, "level": level, "weight": weight, "condition": condition}


def build(cob_root: Path, res: Path):
    data = res / "data" / "cobbleeffort"
    cob_species = cob_root / "data" / "cobblemon" / "species"

    # ---- features ------------------------------------------------------------------------------
    write(data / "species_features" / "armored_mewtwo.json", flag("armored"))
    write(data / "species_features" / "shadow_lugia.json", flag("shadow"))
    write(data / "species_feature_assignments" / "armored_mewtwo.json", {"pokemon": ["mewtwo"], "features": ["armored_mewtwo"]})
    write(data / "species_feature_assignments" / "shadow_lugia.json", {"pokemon": ["lugia"], "features": ["shadow_lugia"]})

    # ---- species additions ---------------------------------------------------------------------
    write(data / "species_additions" / "mewtwo_armored.json", {
        "target": "cobblemon:mewtwo",
        "forms": [{
            "name": "Armored",
            "primaryType": "psychic",
            "aspects": ["armored"],
            # Pokémon GO's Armored Mewtwo trades offence for defence; same 680 total as Mewtwo
            "baseStats": {"hp": 106, "attack": 110, "defence": 140, "special_attack": 134,
                          "special_defence": 120, "speed": 70},
            "abilities": ["pressure", "h:battlearmor"],
            "labels": ["gen1", "legendary", "restricted", "cobbleeffort"],
            "battleOnly": False,
        }],
    })
    write(data / "species_additions" / "celesteela.json", {
        "target": "cobblemon:celesteela", "implemented": True, "baseScale": 0.9,
        "hitbox": {"width": 2.6, "height": 3.4, "fixed": False},
    })
    write(data / "species_additions" / "ironboulder.json", {
        "target": "cobblemon:ironboulder", "implemented": True, "baseScale": 0.85,
        "hitbox": {"width": 1.3, "height": 2.0, "fixed": False},
    })

    # ---- Origin Dragon: a new species (cobblemon namespace so plain "origindragon" works everywhere) ----
    write(res / "data" / "cobblemon" / "species" / "cobbleeffort" / "origindragon.json", {
        "implemented": True,
        "nationalPokedexNumber": 2001,
        "name": "Origin Dragon",
        "primaryType": "dragon",
        "secondaryType": "ice",
        "maleRatio": -1,
        "height": 60,
        "weight": 9990,
        "pokedex": ["cobblemon.species.origindragon.desc"],
        "labels": ["legendary", "restricted", "cobbleeffort"],
        "aspects": [],
        "abilities": ["turboblaze", "teravolt", "h:pressure"],
        "eggGroups": ["undiscovered"],
        "baseStats": {"hp": 125, "attack": 150, "defence": 110, "special_attack": 150,
                      "special_defence": 110, "speed": 105},
        "evYield": {"hp": 0, "attack": 1, "defence": 0, "special_attack": 2, "special_defence": 0, "speed": 0},
        "baseExperienceYield": 360,
        "experienceGroup": "slow",
        "catchRate": 3,
        "eggCycles": 120,
        "baseFriendship": 0,
        "baseScale": 1.0,
        "hitbox": {"width": 2.6, "height": 5.6, "fixed": False},
        "moves": merged_moves(cob_species, ["kyurem", "reshiram", "zekrom"]),
        "behaviour": {
            "moving": {"fly": {"canFly": True}, "swim": {"avoidsWater": True}},
            "resting": {"times": ["any"], "drowsyChance": 0.0014, "rouseChance": 0.0042},
            "combat": {"willDefendSelf": True, "willDefendOwner": True, "willFlee": False},
        },
    })
    write(data / "fossils" / "origindragon.json", {
        "result": "origindragon",
        "fossils": ["minecraft:dragon_egg", "minecraft:nether_star", "minecraft:heavy_core"],
    })

    # ---- interactions: use an item on your own Pokémon ------------------------------------------
    write(data / "pokemon_interactions" / "armored_mewtwo.json", {
        "requirements": [{"variant": "properties", "target": "mewtwo"}],
        "interactions": [{
            "grouping": "cobbleeffort:armor",
            "cooldown": "20",
            "requirements": [
                {"variant": "owner_held_item", "itemCondition": "minecraft:netherite_chestplate"},
                {"variant": "properties", "target": "armored=false"},
            ],
            "effects": [
                {"variant": "shrink_item", "amount": 1},
                {"variant": "script", "script": "q.pokemon.apply('armored=true');"},
                {"variant": "play_sound", "sound": "minecraft:item.armor.equip_netherite"},
                {"variant": "play_sound", "sound": "minecraft:block.smithing_table.use"},
            ],
        }],
    })
    write(data / "pokemon_interactions" / "shadow_lugia.json", {
        "requirements": [{"variant": "properties", "target": "lugia"}],
        "interactions": [
            {
                "grouping": "cobbleeffort:shadow",
                "cooldown": "20",
                "requirements": [
                    {"variant": "owner_held_item", "itemCondition": "minecraft:echo_shard"},
                    {"variant": "properties", "target": "shadow=false"},
                ],
                "effects": [
                    {"variant": "shrink_item", "amount": 1},
                    {"variant": "script", "script": "q.pokemon.apply('shadow=true');"},
                    {"variant": "play_sound", "sound": "minecraft:block.sculk_shrieker.shriek"},
                ],
            },
            {
                "grouping": "cobbleeffort:purify",
                "cooldown": "20",
                "requirements": [
                    {"variant": "owner_held_item", "itemCondition": "minecraft:golden_apple"},
                    {"variant": "properties", "target": "shadow=true"},
                ],
                "effects": [
                    {"variant": "shrink_item", "amount": 1},
                    {"variant": "script", "script": "q.pokemon.apply('shadow=false');"},
                    {"variant": "play_sound", "sound": "minecraft:block.beacon.activate"},
                ],
            },
        ],
    })

    # ---- spawns ------------------------------------------------------------------------------------
    pool = data / "spawn_pool_world"
    write(pool / "cobbleeffort_mewtwo.json", {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": [
        spawn("cobbleeffort-mewtwo-1", "mewtwo", "70", 0.4,
              {"biomes": ["#cobblemon:is_overworld"], "canSeeSky": False, "maxY": -16, "maxSkyLight": 0}),
    ]})
    write(pool / "cobbleeffort_lugia.json", {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": [
        spawn("cobbleeffort-lugia-1", "lugia", "70", 0.4,
              {"biomes": ["#cobblemon:is_deep_ocean"], "timeRange": "night"}, position="submerged"),
        spawn("cobbleeffort-lugia-shadow-1", "lugia shadow", "70", 0.3,
              {"biomes": ["#cobblemon:is_deep_ocean"], "isThundering": True}, position="submerged"),
    ]})
    write(pool / "cobbleeffort_celesteela.json", {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": [
        spawn("cobbleeffort-celesteela-1", "celesteela", "60-70", 0.6, {"biomes": ["#cobblemon:is_end"]}),
    ]})
    write(pool / "cobbleeffort_ironboulder.json", {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": [
        spawn("cobbleeffort-ironboulder-1", "ironboulder", "60-70", 0.6,
              {"biomes": ["#cobblemon:is_peak", "#cobblemon:is_mountain"], "timeRange": "night", "canSeeSky": True}),
    ]})

    # ---- names ---------------------------------------------------------------------------------------
    write(res / "assets" / "cobblemon" / "lang" / "en_us.json", {
        "cobblemon.species.origindragon.name": "Origin Dragon",
        "cobblemon.species.origindragon.desc": "Kyurem, Reshiram and Zekrom made whole again: the single dragon "
                                               "said to have existed before they split apart. Its three heads "
                                               "breathe ice, flame and lightning as one.",
    })
