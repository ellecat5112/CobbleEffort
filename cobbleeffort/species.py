"""Species data: turns a friendly pokemon.json into Cobblemon's species JSON.

Shortcuts handled here:
  * stats as a dict, a list of 6, or just a total ("bst") plus a "spread" preset
  * evolutions as one-liners: "flarelord @ level 36", "x @ item fire_stone",
    "y @ friendship 160 + time night", "z @ trade holding metal_coat"
  * moves as {"1": "tackle, growl", "7": "ember", "egg": [...], "tm": "auto"}
  * drops as "minecraft:bone 0-2" / "cobblemon:oran_berry 5%"
  * sensible defaults for everything else (abilities, learnset, behaviour...)
"""

from __future__ import annotations

import re
from typing import Any

from .util import CobbleEffortError, as_list, move_id, num, qualify

TYPES = ["normal", "fire", "water", "grass", "electric", "ice", "fighting", "poison", "ground", "flying",
         "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
EXP_GROUPS = ["erratic", "fast", "medium_fast", "medium_slow", "slow", "fluctuating"]
EGG_GROUPS = ["monster", "water_1", "bug", "flying", "field", "fairy", "grass", "human_like", "water_3",
              "mineral", "amorphous", "water_2", "ditto", "dragon", "undiscovered"]
STATS = ["hp", "attack", "defence", "special_attack", "special_defence", "speed"]
STAT_ALIASES = {
    "hp": "hp", "health": "hp",
    "atk": "attack", "attack": "attack", "att": "attack",
    "def": "defence", "defense": "defence", "defence": "defence",
    "spa": "special_attack", "spatk": "special_attack", "sp_atk": "special_attack", "special_attack": "special_attack",
    "satk": "special_attack", "spattack": "special_attack",
    "spd": "special_defence", "spdef": "special_defence", "sp_def": "special_defence", "special_defence": "special_defence",
    "special_defense": "special_defence", "sdef": "special_defence", "spdefense": "special_defence",
    "spe": "speed", "speed": "speed", "spd_speed": "speed", "initiative": "speed",
}
SPREADS = {
    "balanced": [1, 1, 1, 1, 1, 1],
    "physical": [1.0, 1.4, 0.9, 0.6, 0.9, 1.2],
    "special": [1.0, 0.6, 0.9, 1.4, 0.9, 1.2],
    "mixed": [1.0, 1.2, 0.8, 1.2, 0.8, 1.0],
    "tank": [1.2, 0.8, 1.5, 0.6, 1.0, 0.7],
    "special_tank": [1.2, 0.6, 1.0, 0.8, 1.5, 0.7],
    "fast": [0.8, 1.1, 0.8, 1.1, 0.8, 1.6],
    "bulky": [1.6, 1.1, 1.0, 0.8, 1.0, 0.5],
    "glass_cannon": [0.7, 1.3, 0.6, 1.3, 0.6, 1.5],
}
DEFAULT_ABILITY = {
    "normal": ["runaway", "h:adaptability"], "fire": ["blaze", "h:flashfire"], "water": ["torrent", "h:swiftswim"],
    "grass": ["overgrow", "h:chlorophyll"], "electric": ["static", "h:motordrive"], "ice": ["icebody", "h:snowcloak"],
    "fighting": ["guts", "h:innerfocus"], "poison": ["poisonpoint", "h:stench"], "ground": ["sandveil", "h:sandforce"],
    "flying": ["keeneye", "h:bigpecks"], "psychic": ["synchronize", "h:magicguard"], "bug": ["shielddust", "h:swarm"],
    "rock": ["sturdy", "h:rockhead"], "ghost": ["levitate", "h:cursedbody"], "dragon": ["innerfocus", "h:multiscale"],
    "dark": ["intimidate", "h:moxie"], "steel": ["clearbody", "h:heavymetal"], "fairy": ["cutecharm", "h:pixilate"],
}
TYPE_MOVES = {  # early, mid, late signature moves per type
    "normal": ["quickattack", "headbutt", "bodyslam", "hypervoice"],
    "fire": ["ember", "flamewheel", "flamethrower", "fireblast"],
    "water": ["watergun", "waterpulse", "surf", "hydropump"],
    "grass": ["vinewhip", "razorleaf", "energyball", "solarbeam"],
    "electric": ["thundershock", "spark", "thunderbolt", "thunder"],
    "ice": ["powdersnow", "icefang", "icebeam", "blizzard"],
    "fighting": ["rocksmash", "brickbreak", "closecombat", "focusblast"],
    "poison": ["poisonsting", "acid", "sludgebomb", "gunkshot"],
    "ground": ["mudslap", "bulldoze", "earthpower", "earthquake"],
    "flying": ["gust", "wingattack", "airslash", "hurricane"],
    "psychic": ["confusion", "psybeam", "psychic", "futuresight"],
    "bug": ["bugbite", "strugglebug", "xscissor", "bugbuzz"],
    "rock": ["rockthrow", "rocktomb", "rockslide", "stoneedge"],
    "ghost": ["lick", "shadowsneak", "shadowball", "phantomforce"],
    "dragon": ["dragonbreath", "dragontail", "dragonpulse", "dracometeor"],
    "dark": ["bite", "snarl", "crunch", "darkpulse"],
    "steel": ["metalclaw", "ironhead", "flashcannon", "irontail"],
    "fairy": ["fairywind", "drainingkiss", "dazzlinggleam", "moonblast"],
}
GENERIC_TMS = ["protect", "rest", "sleeptalk", "substitute", "facade", "endure", "terablast", "helpinghand",
               "takedown", "gigaimpact", "hyperbeam"]
DEFAULT_RESTING = {"canSleep": True, "willSleepOnBed": True, "light": "0-4", "drowsyChance": 0.0333,
                   "rouseChance": 0.0042}
ARCHETYPES = ("walker", "flier", "swimmer", "floater", "amphibian")


# ------------------------------------------------------------------- stats


def parse_types(cfg: dict) -> list[str]:
    raw = cfg.get("types", cfg.get("type", "normal"))
    if isinstance(raw, str):
        raw = re.split(r"[/,\s]+", raw)
    types = [t.strip().lower() for t in raw if t and t.strip()]
    if not types:
        types = ["normal"]
    for t in types:
        if t not in TYPES:
            raise CobbleEffortError(f"Unknown type '{t}'. Valid: {', '.join(TYPES)}")
    if len(types) > 2:
        raise CobbleEffortError("A Pokemon can have at most 2 types")
    return types


def parse_stats(cfg: dict, default_bst: int) -> dict[str, int]:
    raw = cfg.get("stats")
    if isinstance(raw, (list, tuple)):
        if len(raw) != 6:
            raise CobbleEffortError("stats list must have 6 numbers: hp, atk, def, spa, spd, spe")
        return {k: int(v) for k, v in zip(STATS, raw)}
    if isinstance(raw, str) and re.fullmatch(r"[\d\s/,]+", raw):
        vals = [int(x) for x in re.split(r"[\s/,]+", raw.strip()) if x]
        return parse_stats({"stats": vals}, default_bst)
    if isinstance(raw, dict):
        out: dict[str, int] = {}
        for k, v in raw.items():
            key = STAT_ALIASES.get(k.lower().replace(" ", "_").replace(".", ""))
            if not key:
                raise CobbleEffortError(f"Unknown stat '{k}'. Use hp/atk/def/spa/spd/spe")
            out[key] = int(v)
        missing = [s for s in STATS if s not in out]
        if missing:
            raise CobbleEffortError(f"stats is missing {', '.join(missing)}")
        return {k: out[k] for k in STATS}
    bst = int(cfg.get("bst", default_bst))
    spread_name = str(cfg.get("spread", "balanced")).lower()
    if spread_name not in SPREADS:
        raise CobbleEffortError(f"Unknown spread '{spread_name}'. Options: {', '.join(SPREADS)}")
    weights = SPREADS[spread_name]
    total = sum(weights)
    vals = [max(1, round(bst * w / total)) for w in weights]
    vals[5] += bst - sum(vals)  # make the total exact
    return dict(zip(STATS, vals))


def default_ev_yield(stats: dict[str, int], stage: int) -> dict[str, int]:
    ev = {k: 0 for k in STATS}
    best = max(STATS, key=lambda s: stats[s])
    ev[best] = min(3, stage + 1)
    return ev


def parse_ev_yield(cfg: dict, stats: dict[str, int], stage: int) -> dict[str, int]:
    raw = cfg.get("ev_yield")
    if not raw:
        return default_ev_yield(stats, stage)
    ev = {k: 0 for k in STATS}
    for k, v in raw.items():
        key = STAT_ALIASES.get(k.lower())
        if not key:
            raise CobbleEffortError(f"Unknown EV stat '{k}'")
        ev[key] = int(v)
    return ev


# ------------------------------------------------------------------- moves


def parse_abilities(cfg: dict, types: list[str]) -> list[str]:
    raw = cfg.get("abilities")
    if not raw:
        return list(DEFAULT_ABILITY[types[0]])
    if isinstance(raw, dict):
        out = [move_id(a) for a in as_list(raw.get("normal", raw.get("regular", [])))]
        out += ["h:" + move_id(a) for a in as_list(raw.get("hidden", []))]
        return out
    out = []
    for a in as_list(raw):
        a = str(a).strip()
        hidden = a.lower().startswith("h:") or a.lower().startswith("hidden:")
        name = a.split(":", 1)[1] if hidden else a
        out.append(("h:" if hidden else "") + move_id(name))
    return out


def auto_moves(types: list[str], stage: int) -> list[str]:
    moves = ["1:tackle", "1:growl"]
    levels = [5, 14, 28, 42]
    primary = TYPE_MOVES[types[0]]
    for lvl, mv in zip(levels, primary):
        moves.append(f"{lvl}:{mv}")
    if len(types) > 1:
        sec = TYPE_MOVES[types[1]]
        moves += [f"9:{sec[0]}", f"22:{sec[1]}", f"36:{sec[2]}"]
    tms = set(GENERIC_TMS)
    for t in types:
        tms.update(TYPE_MOVES[t][1:])
    moves += [f"tm:{m}" for m in sorted(tms)]
    return moves


def parse_moves(cfg: dict, types: list[str], stage: int) -> list[str]:
    raw = cfg.get("moves", "auto")
    if raw in (None, "auto", "", []):
        return auto_moves(types, stage)
    out: list[str] = []
    if isinstance(raw, list):
        for m in raw:
            m = str(m).strip()
            if ":" not in m:
                raise CobbleEffortError(f"Move '{m}' needs a prefix like '1:{m}' or 'tm:{m}'")
            k, v = m.split(":", 1)
            out.append(f"{k.strip().lower()}:{move_id(v)}")
        return out
    if not isinstance(raw, dict):
        raise CobbleEffortError("moves must be 'auto', a list like ['1:tackle'], or a dict like {'1': 'tackle'}")
    def sort_key(k: str):
        return (0, int(k)) if str(k).isdigit() else (1, str(k))
    for key in sorted(raw.keys(), key=sort_key):
        val = raw[key]
        key_s = str(key).strip().lower()
        if key_s in ("level", "levels") and isinstance(val, dict):
            out += parse_moves({"moves": val}, types, stage)
            continue
        if key_s == "tm" and val == "auto":
            out += [m for m in auto_moves(types, stage) if m.startswith("tm:")]
            continue
        if key_s not in ("egg", "tm", "tutor", "legacy", "special", "evolution") and not key_s.isdigit():
            raise CobbleEffortError(f"moves key '{key}' must be a level number or egg/tm/tutor/legacy/special/evolution")
        for mv in as_list(val):
            out.append(f"{key_s}:{move_id(str(mv))}")
    return out


# --------------------------------------------------------------- evolutions

_ITEM_WORDS = ("item", "use", "stone", "with")


def parse_evolution(text: str | dict, source_id: str, ns: str, local_ids: set[str]) -> dict:
    """'flarelord @ level 36 + time night' -> Cobblemon evolution JSON."""
    if isinstance(text, dict):
        return text  # raw Cobblemon JSON passthrough
    if "@" not in text:
        raise CobbleEffortError(f"Evolution '{text}' needs the form 'target @ condition' e.g. 'ivysaur @ level 16'")
    target_raw, cond_raw = [p.strip() for p in text.split("@", 1)]
    target_parts = target_raw.split()
    target = target_parts[0]
    extra_props = " ".join(target_parts[1:])
    result = resolve_species_ref(target, ns, local_ids)
    if extra_props:
        result = f"{result} {extra_props}"
    variant = "level_up"
    reqs: list[dict] = []
    learn: list[str] = []
    consume = False
    required_context = None
    conds = [c.strip() for c in re.split(r"\s*(?:\+|&|,|\band\b)\s*", cond_raw) if c.strip()]
    for c in conds:
        words = c.split()
        head = words[0].lower()
        arg = " ".join(words[1:])
        if head.isdigit():
            reqs.append({"variant": "level", "minLevel": int(head)})
        elif head in ("level", "lvl", "lv", "l"):
            reqs.append({"variant": "level", "minLevel": int(arg)})
        elif head in _ITEM_WORDS:
            variant = "item_interact"
            required_context = qualify(arg.replace(" ", "_").lower())
        elif head.endswith("stone"):
            variant = "item_interact"
            required_context = qualify(head)
        elif head == "trade":
            variant = "trade"
            if len(words) > 2 and words[1].lower() in ("holding", "with", "held"):
                reqs.append({"variant": "held_item", "itemCondition": qualify(words[2].lower())})
                consume = True
        elif head in ("friendship", "happiness", "friend"):
            reqs.append({"variant": "friendship", "amount": int(arg) if arg else 160})
        elif head in ("time", "at"):
            rng = arg.lower() or "day"
            reqs.append({"variant": "time_range", "range": rng})
        elif head in ("day", "night", "dusk", "dawn", "morning", "noon", "midnight"):
            reqs.append({"variant": "time_range", "range": head})
        elif head in ("holding", "held", "hold"):
            reqs.append({"variant": "held_item", "itemCondition": qualify(arg.replace(" ", "_").lower())})
            consume = True
        elif head in ("move", "knows", "knowing"):
            reqs.append({"variant": "has_move", "move": move_id(arg)})
        elif head in ("biome", "in"):
            biome = arg.strip()
            if not biome.startswith("#") and ":" not in biome:
                biome = f"#cobblemon:is_{biome}"
            reqs.append({"variant": "biome", "biomeCondition": biome})
        elif head in ("rain", "raining"):
            reqs.append({"variant": "weather", "isRaining": True})
        elif head in ("thunder", "storm", "thundering"):
            reqs.append({"variant": "weather", "isThundering": True})
        elif head in ("male", "female"):
            reqs.append({"variant": "properties", "target": f"gender={head}"})
        elif head in ("gender",):
            reqs.append({"variant": "properties", "target": f"gender={arg.lower()}"})
        elif head in ("learns", "learn", "teach"):
            learn += [move_id(m) for m in re.split(r"[\s/]+", arg) if m]
        elif head in ("properties", "property", "props"):
            reqs.append({"variant": "properties", "target": arg})
        else:
            raise CobbleEffortError(f"Don't understand evolution condition '{c}' in '{text}'. "
                                    "Try: level N, item X, trade, friendship N, time night, holding X, move X, "
                                    "biome X, rain, male/female, learns X")
    if variant == "level_up" and not reqs:
        raise CobbleEffortError(f"Evolution '{text}' has no condition")
    evo: dict[str, Any] = {
        "id": f"{source_id}_{target.split(':')[-1].lower()}",
        "variant": variant,
        "result": result,
        "consumeHeldItem": consume,
        "learnableMoves": learn,
        "requirements": reqs,
    }
    if required_context:
        evo["requiredContext"] = required_context
    return evo


def resolve_species_ref(name: str, ns: str, local_ids: set[str]) -> str:
    """Pokemon in this project get our namespace; anything else defaults to cobblemon."""
    if ":" in name:
        return name.lower()
    sid = re.sub(r"[^a-z0-9]", "", name.lower())
    if sid in local_ids:
        return sid if ns == "cobblemon" else f"{ns}:{sid}"
    return sid


# ------------------------------------------------------------------ drops


def parse_drops(raw: Any) -> dict | None:
    if not raw:
        return None
    if isinstance(raw, dict) and "entries" in raw:
        return raw
    entries = []
    for d in as_list(raw):
        if isinstance(d, dict):
            entries.append(d)
            continue
        parts = str(d).split()
        e: dict[str, Any] = {"item": qualify(parts[0], "minecraft")}
        for p in parts[1:]:
            if p.endswith("%"):
                e["percentage"] = float(p[:-1])
            elif re.fullmatch(r"\d+-\d+", p):
                e["quantityRange"] = p
            elif p.isdigit():
                e["quantityRange"] = f"{p}-{p}"
        entries.append(e)
    return {"amount": max(1, len(entries)), "entries": entries}


# --------------------------------------------------------------- behaviour


def build_behaviour(archetype: str, types: list[str], walk_speed: float, cfg_behaviour: dict | None) -> dict:
    moving: dict[str, Any] = {}
    resting = dict(DEFAULT_RESTING)
    if archetype == "swimmer":
        moving = {"walk": {"avoidsLand": True}, "swim": {"swimSpeed": 0.2, "canBreatheUnderwater": True}}
        resting = {"canSleep": True, "times": ["any"], "drowsyChance": 0.0014, "rouseChance": 0.0042}
    elif archetype == "floater":
        moving = {"fly": {"canFly": True}, "walk": {"canWalk": False}, "swim": {"avoidsWater": True}}
        resting = {"canSleep": True, "light": "0-4", "times": ["any"], "drowsyChance": 0.0014, "rouseChance": 0.0042}
    elif archetype == "amphibian":
        moving = {"walk": {"walkSpeed": walk_speed},
                  "swim": {"swimSpeed": 0.2, "canBreatheUnderwater": True}}
    else:
        moving = {"walk": {"walkSpeed": walk_speed}}
        if archetype == "flier":
            moving["fly"] = {"canFly": True}
        if "water" not in types:
            moving["swim"] = {"avoidsWater": True}
    beh: dict[str, Any] = {"moving": moving, "resting": resting, "combat": {"willDefendOwner": True}}
    if "fire" in types:
        beh["fireImmune"] = True
    if cfg_behaviour:
        _deep_merge(beh, cfg_behaviour)
    return beh


def _deep_merge(dst: dict, src: dict) -> dict:
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _deep_merge(dst[k], v)
        else:
            dst[k] = v
    return dst


# ------------------------------------------------------------------ build


def build_species(*, cfg: dict, sid: str, ns: str, dex: int, stage: int, archetype: str, model_height_blocks: float,
                  model_width_blocks: float, local_ids: set[str], pre_evolution: str | None) -> dict:
    name = cfg["name"]
    types = parse_types(cfg)
    default_bst = {0: 320, 1: 420, 2: 525}.get(stage, 525) if cfg.get("_in_chain") else 450
    stats = parse_stats(cfg, default_bst)
    bst = sum(stats.values())
    scale = float(cfg.get("scale", 1.0))
    height_m = float(cfg.get("height_m", cfg.get("height", round(model_height_blocks * scale, 1))))
    weight_kg = float(cfg.get("weight_kg", cfg.get("weight", round(25 * height_m ** 3 + 2, 1))))

    gender = cfg.get("gender", cfg.get("male_ratio", 0.5))
    if isinstance(gender, str):
        g = gender.lower().replace("%", "")
        male_ratio = {"genderless": -1, "none": -1, "male": 1.0, "female": 0.0, "male_only": 1.0,
                      "female_only": 0.0}.get(g)
        if male_ratio is None:
            try:
                male_ratio = float(g) / (100 if float(g) > 1 else 1)
            except ValueError as e:
                raise CobbleEffortError(f"gender must be a male ratio 0-1, a percent, or 'genderless': {gender}") from e
    else:
        male_ratio = float(gender)

    exp_group = str(cfg.get("experience_group", "medium_slow" if cfg.get("_in_chain") else "medium_fast")).lower()
    if exp_group not in EXP_GROUPS:
        raise CobbleEffortError(f"experience_group must be one of {', '.join(EXP_GROUPS)}")
    egg_groups = [e.lower().replace(" ", "_") for e in as_list(cfg.get("egg_groups", ["field"]))]
    for e in egg_groups:
        if e not in EGG_GROUPS:
            raise CobbleEffortError(f"Unknown egg group '{e}'. Valid: {', '.join(EGG_GROUPS)}")

    walk_speed = float(cfg.get("walk_speed", 0.3))
    evolutions = [parse_evolution(e, sid, ns, local_ids) for e in as_list(cfg.get("evolutions"))
                  if not (isinstance(e, str) and not e.strip())]

    species: dict[str, Any] = {
        "implemented": True,
        "name": name,
        "nationalPokedexNumber": dex,
        "primaryType": types[0],
    }
    if len(types) > 1:
        species["secondaryType"] = types[1]
    species.update({
        "abilities": parse_abilities(cfg, types),
        "baseStats": stats,
        "evYield": parse_ev_yield(cfg, stats, stage),
        "catchRate": int(cfg.get("catch_rate", {0: 45, 1: 45, 2: 45}.get(stage, 45) if cfg.get("_in_chain") else 120)),
        "maleRatio": male_ratio,
        "shoulderMountable": bool(cfg.get("shoulder_mountable", model_height_blocks * scale < 0.9)),
        "baseExperienceYield": int(cfg.get("base_exp", round(bst * (0.2 + 0.1 * stage)))),
        "experienceGroup": exp_group,
        "eggCycles": int(cfg.get("egg_cycles", 20)),
        "eggGroups": egg_groups,
        "baseFriendship": int(cfg.get("base_friendship", 50)),
        "height": max(1, round(height_m * 10)),
        "weight": max(1, round(weight_kg * 10)),
        "baseScale": num(scale, 3),
        "hitbox": {
            "width": num(max(0.3, model_width_blocks * 0.6), 2),
            "height": num(max(0.3, model_height_blocks), 2),
            "fixed": False,
        },
        "labels": as_list(cfg.get("labels", ["custom"])),
        "pokedex": [f"{ns}.species.{sid}.desc"],
        "aspects": [],
        "moves": parse_moves(cfg, types, stage),
        "evolutions": evolutions,
        "behaviour": build_behaviour(archetype, types, walk_speed, cfg.get("behaviour_extra")),
    })
    if pre_evolution:
        species["preEvolution"] = pre_evolution
    drops = parse_drops(cfg.get("drops"))
    if drops:
        species["drops"] = drops
    if cfg.get("extra"):
        _deep_merge(species, cfg["extra"])  # raw Cobblemon fields, last word
    return species
