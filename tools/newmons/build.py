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

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(HERE / "models"))
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
    for variant, sfx in ((None, ""), ("shiny", "_shiny")):
        img, _ = m.paint(tw, th, variant, k=k)
        img.save(tex_dir / f"{sp}{sfx}.png", optimize=True)
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
    tex = lambda n: f"{MOD}:textures/pokemon/{folder(sp)}/{n}.png"
    write_json(bedrock / "resolvers" / folder(sp) / f"0_{sp}_base.json", {
        "species": f"{MOD}:{sp}", "order": 0,
        "variations": [
            {"aspects": [], "poser": f"{MOD}:{sp}", "model": f"{MOD}:{sp}.geo", "texture": tex(sp), "layers": []},
            {"aspects": ["shiny"], "texture": tex(f"{sp}_shiny")},
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
        "maleRatio": 0.5, "height": c["height"], "weight": c["weight"], "pokedex": [f"{MOD}.species.{sp}.desc"],
        "labels": ["cobbleeffort", "custom"], "aspects": [], "abilities": c["abilities"], "eggGroups": c["egg_groups"],
        "baseStats": c["stats"], "evYield": c["ev"], "baseExperienceYield": c["exp"], "experienceGroup": "medium_slow",
        "catchRate": c["catch"], "eggCycles": 20, "baseFriendship": c["friendship"],
        "shoulderMountable": c["shoulder"], "baseScale": c["scale"],
        "hitbox": {"width": c["hitbox"][0], "height": c["hitbox"][1], "fixed": False},
        "behaviour": {
            "resting": {"canSleep": True, "willSleepOnBed": True, "times": ["day"], "drowsyChance": 0.0014,
                        "rouseChance": 0.0042},
            "moving": {"walk": {"walkSpeed": c["walk"]}, "swim": {"avoidsWater": True, "canSwimInWater": False}},
            "combat": {"willDefendOwner": True, "willDefendSelf": sp != "cavitot"},
        },
        "drops": {"amount": 2, "entries": [
            {"item": item, **({"quantityRange": q} if q else {}), **({"percentage": p} if p else {})}
            for item, q, p in c["drops"]]},
        "moves": [f"{lv}:{mv}" for lv, mv in c["moves"]] + [f"egg:{m}" for m in c["egg"]] + [f"tm:{m}" for m in c["tm"]],
    })
    if c["evolve"]:
        to, lv, learn = c["evolve"]
        d["evolutions"] = [{"id": f"{sp}_{to}", "variant": "level_up", "result": f"{MOD}:{to}", "consumeHeldItem": False,
                            "learnableMoves": learn, "requirements": [{"variant": "level", "minLevel": lv}]}]
    pre = [s for s, o in SPECIES.items() if o["evolve"] and o["evolve"][0] == sp]
    if pre:
        d["preEvolution"] = f"{MOD}:{pre[0]}"
    return d


def check(showdown):
    """Every move and ability must exist in Cobblemon's Showdown (data/moves.js, data/abilities.js)."""
    import re
    import zipfile
    z = zipfile.ZipFile(showdown)
    ids = lambda f: set(re.findall(r"^  ([a-z0-9]+): \{", z.read(f).decode(), re.M))
    moves, abilities = ids("data/moves.js"), ids("data/abilities.js")
    bad = []
    for sp, c in SPECIES.items():
        for mv in [m for _, m in c["moves"]] + c["tm"] + c["egg"] + (c["evolve"][2] if c["evolve"] else []):
            if mv not in moves:
                bad.append(f"{sp}: move {mv}")
        for ab in c["abilities"]:
            if ab.removeprefix("h:") not in abilities:
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
        write_json(data / "spawn_pool_world" / f"{sp}.json",
                   {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": spawns})
        write_json(data / "dex_entries" / "pokemon" / f"{sp}.json", {
            "id": f"{MOD}:{sp}", "speciesId": f"{MOD}:{sp}", "displayAspects": [], "conditionAspects": [],
            "forms": [{"displayForm": "Normal", "unlockForms": ["Normal"]}], "variations": []})
        lang[f"{MOD}.species.{sp}.name"] = c["name"]
        lang[f"{MOD}.species.{sp}.desc"] = c["entry"]
        for sfx in ("", "_shiny"):
            manifest.append({"species": f"{sp}{sfx}", "folder": folder(sp), "model": f"{MOD}:{sp}.geo", "original": None,
                             "retextured": f"{MOD}:textures/pokemon/{folder(sp)}/{sp}{sfx}.png", "layers": []})
        types = " / ".join(t.title() for t in c["types"])
        st = c["stats"]
        write_json(TOOLS / "readme" / f"_new_{sp}.json", {
            "dex": c["dex"], "name": c["name"], "types": types, "ability": c["ability_names"], "look": c["look"],
            "entry": c["entry"], "how": c["how"],
            "stats": [st["hp"], st["attack"], st["defence"], st["special_attack"], st["special_defence"], st["speed"]]})
        readme.append(c)
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
