"""Digimon from the roster (tools/digimon/roster.py) + wikimon facts (tools/digimon/data/wikimon.json) -> SPECIES
entries for build.py. Rules (the user's: wikimon decides evolutions; Greymon >= 15 blocks, +10 per stage, generalised):

* stage: the roster's, else wikimon's first standard level (Baby I .. Super Ultimate; Hybrid -> Adult);
* evolutions: every wikimon Evolves To / Evolves From link between two implemented Digimon (not both in the hand-built
  Agumon line) that isn't backed only by card-game cards, a DNA (two-Digimon) evolution or a Warp Evolution; the level is the target stage's (Child 10, Adult 20,
  Perfect 35, Ultimate 50, Super Ultimate 70); a same-stage link only if it is one-way (Abbadomon -> Abbadomon Core),
  10 levels after the source's; several at once are all offered (the player picks);
* stats from the stage's total and the roster role; catch rate, spawn bucket, height and learnset by stage and type.
"""
from __future__ import annotations

import importlib.util
import json
import re
import unicodedata
from pathlib import Path

DIGI = Path(__file__).resolve().parents[1] / "digimon"

ORDER = ["Baby I", "Baby II", "Child", "Adult", "Perfect", "Ultimate", "Super Ultimate"]
STAGE = {  # evolve level, blocks tall, base stat total, catch rate, (bucket, weight, levels), exp
    "Baby I": (1, 0.35, 180, 255, ("common", 1.5, "1-5"), 40),
    "Baby II": (5, 0.5, 240, 220, ("common", 2.0, "3-10"), 55),
    "Child": (10, 1.0, 320, 150, ("common", 3.0, "8-22"), 80),
    "Adult": (20, 15.0, 420, 90, ("uncommon", 1.2, "20-35"), 150),
    "Perfect": (35, 25.0, 500, 45, ("rare", 0.5, "35-50"), 210),
    "Ultimate": (50, 35.0, 580, 15, ("ultra-rare", 0.2, "50-65"), 270),
    "Super Ultimate": (70, 45.0, 680, 3, None, 330),
}
ROLE = {  # hp, atk, def, spa, spd, spe
    "physical": (1.0, 1.35, 1.0, 0.7, 0.9, 1.05), "special": (1.0, 0.7, 0.9, 1.35, 1.1, 0.95),
    "tank": (1.25, 1.0, 1.35, 0.75, 1.05, 0.6), "speed": (0.85, 1.2, 0.8, 0.95, 0.8, 1.4),
    "mixed": (1.0, 1.15, 0.95, 1.15, 0.95, 0.8),
}
TYPE_MOVES = {
    "normal": ["tackle", "quickattack", "headbutt", "slam", "bodyslam", "doubleedge", "hypervoice", "gigaimpact"],
    "fire": ["ember", "flamecharge", "firefang", "incinerate", "flamethrower", "lavaplume", "fireblast", "overheat"],
    "water": ["watergun", "aquajet", "waterpulse", "bubblebeam", "aquatail", "surf", "liquidation", "hydropump"],
    "grass": ["vinewhip", "razorleaf", "bulletseed", "gigadrain", "seedbomb", "energyball", "powerwhip", "leafstorm"],
    "electric": ["thundershock", "spark", "shockwave", "thunderfang", "discharge", "thunderbolt", "wildcharge", "thunder"],
    "ice": ["powdersnow", "iceshard", "icywind", "icefang", "aurorabeam", "icebeam", "iciclecrash", "blizzard"],
    "fighting": ["lowkick", "karatechop", "machpunch", "brickbreak", "drainpunch", "aurasphere", "closecombat", "focusblast"],
    "poison": ["poisonsting", "acid", "poisonfang", "venoshock", "poisonjab", "sludgebomb", "gunkshot", "sludgewave"],
    "ground": ["mudslap", "mudshot", "bulldoze", "dig", "drillrun", "earthpower", "earthquake", "highhorsepower"],
    "flying": ["gust", "wingattack", "aerialace", "aircutter", "airslash", "drillpeck", "bravebird", "hurricane"],
    "psychic": ["confusion", "psybeam", "zenheadbutt", "psyshock", "psychocut", "psychic", "futuresight", "expandingforce"],
    "bug": ["bugbite", "strugglebug", "furycutter", "signalbeam", "xscissor", "bugbuzz", "lunge", "megahorn"],
    "rock": ["rockthrow", "rocktomb", "ancientpower", "rockslide", "powergem", "stoneedge", "headsmash", "rockwrecker"],
    "ghost": ["astonish", "shadowsneak", "hex", "shadowclaw", "shadowpunch", "shadowball", "phantomforce", "poltergeist"],
    "dragon": ["dragonbreath", "dragontail", "dragonclaw", "breakingswipe", "dragonpulse", "dragonrush", "outrage", "dracometeor"],
    "dark": ["bite", "pursuit", "assurance", "nightslash", "crunch", "darkpulse", "knockoff", "foulplay"],
    "steel": ["metalclaw", "mirrorshot", "ironhead", "flashcannon", "smartstrike", "meteormash", "heavyslam", "steelbeam"],
    "fairy": ["fairywind", "disarmingvoice", "drainingkiss", "dazzlinggleam", "playrough", "moonblast", "spiritbreak", "fleurcannon"],
}
TYPE_TM = {
    "normal": ["bodyslam", "hypervoice", "swordsdance"], "fire": ["flamethrower", "fireblast", "willowisp", "sunnyday"],
    "water": ["surf", "hydropump", "raindance", "liquidation"], "grass": ["energyball", "gigadrain", "leafstorm", "grassknot"],
    "electric": ["thunderbolt", "thunder", "voltswitch", "thunderwave"], "ice": ["icebeam", "blizzard", "snowscape"],
    "fighting": ["closecombat", "aurasphere", "bulkup", "brickbreak"], "poison": ["sludgebomb", "toxic", "poisonjab"],
    "ground": ["earthquake", "earthpower", "stealthrock"], "flying": ["airslash", "bravebird", "roost", "tailwind"],
    "psychic": ["psychic", "calmmind", "lightscreen", "reflect"], "bug": ["xscissor", "bugbuzz", "uturn"],
    "rock": ["stoneedge", "rockslide", "stealthrock"], "ghost": ["shadowball", "shadowclaw", "hex"],
    "dragon": ["dragonpulse", "dragonclaw", "outrage", "dragondance"], "dark": ["darkpulse", "crunch", "nastyplot", "taunt"],
    "steel": ["flashcannon", "ironhead", "irondefense", "steelbeam"], "fairy": ["moonblast", "dazzlinggleam", "playrough"],
}
TYPE_BIOMES = {
    "normal": ["#cobblemon:is_plains"], "fire": ["#cobblemon:is_badlands", "#cobblemon:is_volcanic", "#cobblemon:is_savanna"],
    "water": ["#cobblemon:is_beach", "#cobblemon:is_river", "#cobblemon:is_swamp"],
    "grass": ["#cobblemon:is_forest", "#cobblemon:is_jungle"], "electric": ["#cobblemon:is_hills", "#cobblemon:is_plains"],
    "ice": ["#cobblemon:is_snowy", "#cobblemon:is_tundra", "#cobblemon:is_glacial"],
    "fighting": ["#cobblemon:is_mountain", "#cobblemon:is_hills"], "poison": ["#cobblemon:is_swamp"],
    "ground": ["#cobblemon:is_desert", "#cobblemon:is_badlands"], "flying": ["#cobblemon:is_mountain", "#cobblemon:is_hills"],
    "psychic": ["#cobblemon:is_plains", "#cobblemon:is_forest"], "bug": ["#cobblemon:is_jungle", "#cobblemon:is_forest"],
    "rock": ["#cobblemon:is_mountain", "#cobblemon:is_badlands"], "ghost": ["#cobblemon:is_spooky"],
    "dragon": ["#cobblemon:is_mountain", "#cobblemon:is_peak"], "dark": ["#cobblemon:is_spooky", "#cobblemon:is_forest"],
    "steel": ["#cobblemon:is_mountain", "#cobblemon:is_badlands"], "fairy": ["#cobblemon:is_plains", "#cobblemon:is_forest"],
}
NIGHT = {"dark", "ghost"}
DROPS = {
    "fire": "minecraft:blaze_powder", "water": "minecraft:prismarine_shard", "grass": "minecraft:wheat_seeds",
    "electric": "minecraft:redstone", "ice": "minecraft:snowball", "fighting": "minecraft:leather",
    "poison": "minecraft:spider_eye", "ground": "minecraft:clay_ball", "flying": "minecraft:feather",
    "psychic": "minecraft:amethyst_shard", "bug": "minecraft:string", "rock": "minecraft:flint",
    "ghost": "minecraft:phantom_membrane", "dragon": "minecraft:bone", "dark": "minecraft:ink_sac",
    "steel": "minecraft:iron_nugget", "fairy": "minecraft:glowstone_dust", "normal": "minecraft:leather",
}
DEX0 = 3301                                             # roster Digimon: #3301 on (CobbleEffort's own stay below)
ABILITY_NAMES = {
    "pressure": "Pressure", "shadowtag": "Shadow Tag", "cursedbody": "Cursed Body", "noguard": "No Guard",
    "speedboost": "Speed Boost", "lightningrod": "Lightning Rod", "guts": "Guts", "ironfist": "Iron Fist",
    "intimidate": "Intimidate", "moxie": "Moxie", "grasspelt": "Grass Pelt", "serenegrace": "Serene Grace",
    "static": "Static", "filter": "Filter", "megalauncher": "Mega Launcher", "snowcloak": "Snow Cloak",
    "refrigerate": "Refrigerate", "aerilate": "Aerilate", "toughclaws": "Tough Claws", "blaze": "Blaze",
    "justified": "Justified", "flashfire": "Flash Fire", "levitate": "Levitate", "forewarn": "Forewarn",
    "analytic": "Analytic", "shellarmor": "Shell Armor", "magicguard": "Magic Guard", "sheerforce": "Sheer Force",
    "liquidooze": "Liquid Ooze", "roughskin": "Rough Skin", "synchronize": "Synchronize", "download": "Download",
    "infiltrator": "Infiltrator", "strongjaw": "Strong Jaw", "effectspore": "Effect Spore", "chlorophyll":
    "Chlorophyll", "drought": "Drought", "magicbounce": "Magic Bounce", "naturalcure": "Natural Cure", "plus": "Plus",
    "minus": "Minus", "galewings": "Gale Wings", "thickfat": "Thick Fat", "swiftswim": "Swift Swim",
    "solidrock": "Solid Rock", "innerfocus": "Inner Focus", "fluffy": "Fluffy", "cutecharm": "Cute Charm",
    "sturdy": "Sturdy", "sharpness": "Sharpness", "keeneye": "Keen Eye", "bigpecks": "Big Pecks",
    "overgrow": "Overgrow", "swarm": "Swarm", "prankster": "Prankster", "waterveil": "Water Veil",
    "poisontouch": "Poison Touch", "sandveil": "Sand Veil", "steelworker": "Steelworker", "pickpocket": "Pickpocket",
    "scrappy": "Scrappy", "skilllink": "Skill Link", "unaware": "Unaware", "motordrive": "Motor Drive",
    "flamebody": "Flame Body", "sniper": "Sniper", "rockhead": "Rock Head", "hydration": "Hydration",
    "gluttony": "Gluttony", "stamina": "Stamina", "pickup": "Pickup", "insomnia": "Insomnia",
    "technician": "Technician", "limber": "Limber", "voltabsorb": "Volt Absorb", "heavymetal": "Heavy Metal",
    "comatose": "Comatose", "angerpoint": "Anger Point", "aftermath": "Aftermath",
    "stickyhold": "Sticky Hold",
    "owntempo": "Own Tempo", "icebody": "Ice Body", "reckless": "Reckless", "flowerveil": "Flower Veil",
    "slushrush": "Slush Rush", "tintedlens": "Tinted Lens", "ripen": "Ripen", "compoundeyes": "Compound Eyes",
    "steadfast": "Steadfast", "hugepower": "Huge Power", "runaway": "Run Away",
    "grassysurge": "Grassy Surge", "snowwarning": "Snow Warning", "sapsipper": "Sap Sipper", "protean": "Protean",
    "torrent": "Torrent", "rivalry": "Rivalry", "telepathy": "Telepathy", "ironbarbs": "Iron Barbs",
    "shedskin": "Shed Skin", "adaptability": "Adaptability", "imposter": "Imposter", "healer": "Healer",
    "punkrock": "Punk Rock", "defiant": "Defiant", "soundproof": "Soundproof", "battlearmor": "Battle Armor",
    "illusion": "Illusion", "frisk": "Frisk", "sandforce": "Sand Force", "shielddust": "Shield Dust",
    "waterabsorb": "Water Absorb", "poisonpoint": "Poison Point", "sandrush": "Sand Rush", "pixilate": "Pixilate",
}


def slug(name):
    """Species id: lower-cased letters and digits, accents transliterated (Cobblemon keys the name lang on the ASCII
    species name, so AnheiNüwashou must be anheinuwashou)."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", name.lower())


def load_roster():
    spec = importlib.util.spec_from_file_location("digimon_roster", DIGI / "roster.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ROSTER


def stage_of(entry, facts):
    if entry.get("stage"):
        return entry["stage"]
    for lv in facts.get("levels", []):
        if lv in STAGE:
            return lv
        if lv == "Hybrid":
            return "Adult"
    return "Adult"


def stats_for(stage, role):
    total = STAGE[stage][2]
    w = ROLE[role]
    raw = [total * x / sum(w) for x in w]
    vals = [max(10, round(v / 5) * 5) for v in raw]
    vals[0] += total - sum(vals)
    keys = ("hp", "attack", "defence", "special_attack", "special_defence", "speed")
    return dict(zip(keys, vals))


def evs_for(role, stage):
    n = max(1, min(3, ORDER.index(stage) - 1))
    key = {"physical": "attack", "special": "special_attack", "tank": "defence", "speed": "speed", "mixed": "attack"}[role]
    e = {k: 0 for k in ("hp", "attack", "defence", "special_attack", "special_defence", "speed")}
    e[key] = n
    return e


def learnset(types, stage):
    cap = ORDER.index(stage)
    pools = [TYPE_MOVES[t] for t in types]
    out = [(1, "tackle" if "normal" not in types else "scratch"), (1, "leer")]
    for i in range(8):
        lvl = 1 + i * 8                                       # 1, 9, 17 .. 57
        if i > 2 + 2 * cap:
            break
        for k, pool in enumerate(pools):
            out.append((lvl + 4 * k, pool[i]))
    return out


def tms(types):
    out = ["protect", "rest", "substitute", "facade", "sleeptalk", "endure", "terablast", "helpinghand"]
    for t in types:
        out += TYPE_TM[t] + TYPE_MOVES[t][3:]
    return sorted(set(out))


def spawns_for(sp, types, stage, legendary):
    b = STAGE[stage][4]
    if b is None or legendary:
        return []
    bucket, weight, levels = b
    biomes = []
    for t in types:
        biomes += [x for x in TYPE_BIOMES[t] if x not in biomes]
    cond = {"canSeeSky": True, "biomes": biomes}
    if types[0] in NIGHT:
        cond["timeRange"] = "night"
    return [{"id": f"{sp}-wild", "pokemon": None, "presets": ["natural"], "type": "pokemon",
             "spawnablePositionType": "grounded", "bucket": bucket, "level": levels, "weight": weight,
             "condition": cond}]


def where(types, stage, legendary):
    b = STAGE[stage][4]
    if b is None or legendary:
        return None
    nice = {"#cobblemon:is_" + k: v for k, v in {
        "plains": "plains", "badlands": "badlands", "volcanic": "volcanic biomes", "savanna": "savannas",
        "beach": "beaches", "river": "rivers", "swamp": "swamps", "forest": "forests", "jungle": "jungles",
        "hills": "hills", "snowy": "snowy biomes", "tundra": "tundras", "glacial": "glaciers", "mountain": "mountains",
        "desert": "deserts", "peak": "peaks", "spooky": "spooky biomes"}.items()}
    biomes = []
    for t in types:
        biomes += [nice[x] for x in TYPE_BIOMES[t] if nice[x] not in biomes]
    s = ", ".join(biomes[:-1]) + (" and " if len(biomes) > 1 else "") + biomes[-1]
    return f"Wild: {b[0]} in {s}" + (" at night." if types[0] in NIGHT else ".")


def generate(SPECIES, LINES):
    ability_name = lambda a: ABILITY_NAMES.get(a, a.title())
    facts = json.loads((DIGI / "data" / "wikimon.json").read_text())
    roster = load_roster()
    hand = {sp: c for sp, c in SPECIES.items() if "digimon" in c.get("labels", [])}
    dex = DEX0                                           # roster order, so dex numbers never move
    gen = {}
    for e in roster:
        sp = slug(e["name"])
        f = facts.get(e.get("wikimon", e["name"]), {})        # "wikimon": the page when it has another title
        stage = stage_of(e, f)
        legendary = bool(e.get("legendary")) or stage == "Super Ultimate"
        lv, blocks, _, catch, _, exp = STAGE[stage]
        abil = e["abilities"]
        gen[sp] = {
            "dex": dex, "name": e["name"], "line": "digimon", "types": e["types"],
            "male": -1, "egg_groups": ["undiscovered"] if legendary else ["monster", "dragon"],
            "friendship": 0 if legendary else 70, "growth": "slow",
            "labels": ["digimon"] + (["legendary"] if legendary else []) + (["digimon_hatch"] if stage == "Baby I" else []),
            "abilities": abil,
            "ability_names": " / ".join(ability_name(a.removeprefix("h:")) + (" (hidden)" if a.startswith("h:") else "")
                                        for a in abil),
            "stats": stats_for(stage, e["role"]), "ev": evs_for(e["role"], stage),
            "catch": 3 if legendary else catch, "exp": exp,
            "height": max(1, round(blocks * 10)), "weight": min(9999, max(10, round(blocks ** 2 * 40))),
            "shoulder": blocks <= 0.5, "walk": 0.3,
            "moves": learnset(e["types"], stage), "tm": tms(e["types"]), "egg": [],
            "evolve": None, "evolve_alt": [],
            "drops": [(DROPS[e["types"][0]], "1-3" if blocks < 2 else "4-8", None)],
            "entry": e["entry"], "spawns": spawns_for(sp, e["types"], stage, legendary),
            "how": [x for x in [where(e["types"], stage, legendary)] if x],
            "_stage": stage, "_wikimon": e["name"],
        }
        dex += 1
    for sp, c in hand.items():
        c.setdefault("_stage", {"koromon": "Baby II", "agumon": "Child", "greymon": "Adult", "metalgreymon": "Perfect",
                                "blitzgreymon": "Ultimate", "omegamonalters": "Ultimate",
                                "omegamonalterb": "Super Ultimate"}.get(sp, "Adult"))
    allsp = {**hand, **gen}
    name_of = {slug(n): n for n in facts}
    # evolution links, both directions of wikimon's lists
    alias = {slug(e["wikimon"]): slug(e["name"]) for e in roster if "wikimon" in e}
    al = lambda n: alias.get(slug(n), slug(n))
    links = set()
    for n, f in facts.items():
        a = al(n)
        for e in f["to"]:
            if not e["card"] and "with" not in e and not e.get("warp"):
                links.add((a, al(e["name"])))
        for e in f["from"]:
            if not e["card"] and "with" not in e and not e.get("warp"):
                links.add((al(e["name"]), a))
    for a, b in sorted(links):
        if a not in allsp or b not in allsp or a == b or (a in hand and b in hand):
            continue                                        # the hand-built Agumon line keeps the user's design
        sa, sb = ORDER.index(allsp[a]["_stage"]), ORDER.index(allsp[b]["_stage"])
        if sb < sa:
            continue
        if sb == sa:
            if (b, a) in links:
                continue                                    # two-way same-stage links are mode changes, not evolutions
            lvl = STAGE[allsp[a]["_stage"]][0] + 10
        else:
            lvl = STAGE[allsp[b]["_stage"]][0]
        c = allsp[a]
        have = {c["evolve"][0]} if c.get("evolve") else set()
        have |= {x[0] for x in c.get("evolve_alt", [])}
        if b in have:
            continue
        if c.get("evolve") is None and a in gen:
            c["evolve"] = (b, lvl, [])
        else:
            c.setdefault("evolve_alt", []).append((b, lvl, []))
        nm = allsp[b]["name"]
        c["how"] = c.get("how", []) + [f"Evolves into {nm} at level {lvl}."]
    for sp, c in allsp.items():
        c.pop("_stage", None)
        c.pop("_wikimon", None)
    for sp, c in gen.items():
        froms = [o for o, oc in allsp.items() if (oc.get("evolve") and oc["evolve"][0] == sp)
                 or any(x[0] == sp for x in oc.get("evolve_alt", []))]
        if froms:
            c["how"].insert(0, "Evolve " + " or ".join(allsp[o]["name"] for o in froms) + ".")
        if not c["how"]:
            c["how"] = ["Not found in the wild; evolve it."]
    SPECIES.update(gen)
    LINES["digimon"] = list(gen)
    return gen
