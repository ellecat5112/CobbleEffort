#!/usr/bin/env python3
"""
Writes CobbleEffort: Distortion's battle data into common/src/main/resources (deterministic):

  twins      every move the distortable Pokémon can learn gets an inverted-type twin: an existing move that's its
             exact opposite (same category, power, accuracy, PP, priority, target, side effects; only the type
             differs, e.g. Ice Punch -> Fire Punch), otherwise a new move that's a copy with only its type and name
             changed (Cross Chop -> Psychic Chop). New moves are Cobblemon datapack moves
             (data/<ns>/moves/<id>.js, read by Cobblemon into Showdown and its move registry) built from the
             original's own Showdown data, so they keep every effect; their names go in the lang file.
  abilities  type-bound abilities (their code names the Pokémon's own type, or its type's weather) get a twin: an existing
             exact opposite (Blaze -> Torrent) or a new ability, the original's code with the types and weathers swapped
             (Solar Power -> Storm Power), a Cobblemon datapack ability (data/<ns>/abilities/<id>.js). Others stay.
  crystal    the Distortion Crystal's Showdown item (Mega Showdown's held-item scripts)
  engine     two Showdown scripts merged in by Mega Showdown's scripts loader
             (data/<ns>/mega_showdown/showdown/scripts/<side|queue|actions>.js):
               side.chooseMove     accepts "move N [target] distort" (once per battle per side, with the crystal;
                                   otherwise it's the plain move, so an AI's choice never fails)
               queue.resolveAction queues the distortion as its own action at Terastallization's priority
               (a Pokémon distorted outside battle starts in its -Distorted forme; it gets its twins at the start and
               counts as its side's distortion)
               actions.runDistort  distorts the Pokémon at the start of the turn: a permanent forme change to its
                                   "-Distorted" forme (inverted types; Cobblemon sees the detailschange and the
                                   add-on gives it the distorted look), its ability kept (or its inverted twin),
                                   every move swapped for its twin (runMove swaps the move it chose this turn)

Inputs: Showdown's moves and abilities dumped to JSON (dump_showdown.js) and Cobblemon's species data (its jar).
Usage: python3 tools/make_battle.py --moves <moves.json> --cobblemon-jar <Cobblemon-fabric-1.8.4.jar>
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RES = ROOT / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_distortion"

import sys  # noqa: E402
sys.path.insert(0, str(HERE))
from make_assets import DISTORTABLE, TYPE_CHART  # noqa: E402

# words in move names that stand for a type, replaced by the new type's name (Dragon Claw -> Fairy Claw)
TYPE_WORDS = {
    "normal": ["Normal", "Mega", "Giga", "Hyper"], "fire": ["Fire", "Flame", "Blaze", "Heat", "Ember", "Inferno", "Lava", "Magma", "Burn"],
    "water": ["Water", "Aqua", "Hydro", "Bubble", "Wave"], "grass": ["Grass", "Leaf", "Solar", "Petal", "Seed", "Wood", "Vine"],
    "electric": ["Electric", "Thunder", "Volt", "Spark", "Shock", "Zap", "Electro", "Charge"], "ice": ["Ice", "Icy", "Frost", "Blizzard", "Freeze"],
    "fighting": ["Fighting", "Focus", "Power-Up", "Brick", "Body"], "poison": ["Poison", "Sludge", "Toxic", "Acid", "Venom"],
    "ground": ["Ground", "Earth", "Mud", "Sand", "Dig", "Bulldoze"], "flying": ["Flying", "Air", "Aerial", "Sky", "Wing", "Aero"],
    "psychic": ["Psychic", "Psycho"], "bug": ["Bug", "X-Scissor", "Silver"],
    "rock": ["Rock", "Stone", "Ancient", "Meteor"], "ghost": ["Ghost", "Shadow", "Phantom", "Night", "Spirit", "Hex"],
    "dragon": ["Dragon", "Draco", "Dual", "Twister"], "dark": ["Dark", "Night", "Foul", "Sucker", "Crunch"],
    "steel": ["Steel", "Iron", "Metal", "Flash", "Mirror", "Gear"], "fairy": ["Fairy", "Moon", "Dazzling", "Misty", "Charm"],
}
# the signature moves get names written for them
NAME_OVERRIDES = {"roaroftime": "Radiance of Time", "spacialrend": "Fairy Rend", "shadowforce": "Dark Force",
                  "judgment": "Inverse Judgment",
                  # where the first-word rule loses the move's meaning, the type goes in front instead
                  "beatup": "Fairy Beat Up", "quickattack": "Fighting Quick Attack",
                  "helpinghand": "Fighting Helping Hand", "holdhands": "Fighting Hold Hands"}
SKIP = {"struggle", "hiddenpower"}

# abilities: one is type-bound when its code names one of the Pokémon's own types (Blaze: "Fire") or its type's weather
# (Solar Power: harsh sunlight for a Fire type). Its twin swaps those for the distorted type (and that type's weather):
# an existing ability when that's an exact match (Blaze -> Torrent), otherwise a new one (Solar Power -> Storm Power).
WEATHER = {"fire": ["sunnyday", "desolateland"], "water": ["raindance", "primordialsea"], "ice": ["hail", "snow"]}
WEATHER_NAMES = {"sunnyday": "harsh sunlight", "desolateland": "extremely harsh sunlight", "raindance": "rain",
                 "primordialsea": "heavy rain", "hail": "hail", "snow": "snow"}
ABILITY_NAMES = {"solarpower": "Storm Power", "flashfire": "Flash Flood"}    # new twins with names written for them
ABILITY_META = {"name", "num", "rating", "isNonstandard", "desc", "shortDesc"}


def toid(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def learnsets(jar):
    z = zipfile.ZipFile(jar)
    out = set()
    for sp in DISTORTABLE:
        for n in z.namelist():
            if n.startswith("data/cobblemon/species/") and n.endswith(f"/{sp}.json"):
                d = json.loads(z.read(n))
                for m in d.get("moves", []):
                    out.add(m.split(":", 1)[1])
                for f in d.get("forms", []):
                    for m in f.get("moves", []):
                        out.add(m.split(":", 1)[1])
    return sorted(out)


def species_info(jar):
    """Every distortable species' types and abilities (all forms but megas and Gigantamax)."""
    z = zipfile.ZipFile(jar)
    info = {}
    for sp in DISTORTABLE:
        for n in z.namelist():
            if n.startswith("data/cobblemon/species/") and n.endswith(f"/{sp}.json"):
                d = json.loads(z.read(n))
                types, abilities = set(), set()
                for f in [d] + [f for f in d.get("forms", []) if not set(f.get("aspects", [])) & {"mega", "mega_x", "mega_y", "gmax"}]:
                    pt = f.get("primaryType", d["primaryType"])
                    st = f.get("secondaryType", d.get("secondaryType") if "primaryType" not in f else None)
                    types |= {pt} | ({st} if st else set())
                    abilities |= {a.split(":", 1)[-1] for a in f.get("abilities", d["abilities"])}
                info[sp] = {"types": types, "abilities": abilities}
    return info


def substitute(text, own_types):
    """The ability's code with its own types (and their weathers) swapped for the distorted ones."""
    pairs = {}
    for t in own_types:
        pairs[f'"{t.title()}"'] = f'"{TYPE_CHART[t].title()}"'
        dst = WEATHER.get(TYPE_CHART[t], [])
        if dst:
            for i, w in enumerate(WEATHER.get(t, [])):
                pairs[f'"{w}"'] = f'"{dst[min(i, len(dst) - 1)]}"'
    if not pairs:
        return text, []
    rx = re.compile("|".join(re.escape(k) for k in sorted(pairs, key=len, reverse=True)))
    done = []
    out = rx.sub(lambda m: (done.append(m.group(0)), pairs[m.group(0)])[1], text)
    return out, sorted({(k.strip('"'), pairs[k].strip('"')) for k in done})


def normalize(text, name, aid):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"this\.debug\([^;]*\);", "", text)
    text = text.replace(f'"{name}', '"§NAME').replace(f": {name}", ": §NAME").replace(f'"{aid}"', '"§ID"')
    return re.sub(r"\s+", " ", text).strip()


def ability_body(ab, aid):
    return {k: normalize(v, ab["name"], aid) for k, v in ab["members"].items() if k not in ABILITY_META}


def build_ability_twins(abilities, info):
    twins, new = {}, {}
    num = -31100
    for sp in sorted(info):
        for aid in sorted(info[sp]["abilities"]):
            ab = abilities.get(aid)
            if not ab or aid in twins:
                continue
            members, changes = {}, []
            for k, v in ab["members"].items():
                members[k], ch = substitute(v, info[sp]["types"]) if k not in ABILITY_META else (v, [])
                changes += ch
            if not changes:
                continue                                    # not bound to its own type: it stays
            body = {k: normalize(v, ab["name"], aid) for k, v in members.items() if k not in ABILITY_META}
            match = sorted((o for o, oa in abilities.items() if o != aid and not oa["isNonstandard"] and ability_body(oa, o) == body),
                           key=lambda o: abilities[o]["num"])
            if match:
                twins[aid] = match[0]                       # Blaze -> Torrent
                continue
            name = ABILITY_NAMES.get(aid)
            if not name:
                frm, to = changes[0]
                words = ab["name"].split(" ")
                swapped = [to.title() if w in TYPE_WORDS.get(frm.lower(), []) else w for w in words]
                name = " ".join(swapped) if swapped != words else f"{to.title()} {ab['name']}"
            tid = toid(name)
            num -= 1
            out = {}
            for k, v in members.items():
                if k == "name":
                    v = f'"name": "{name}"'
                elif k == "num":
                    v = f'"num": {num}'
                else:
                    v = v.replace(f'"{aid}"', f'"{tid}"').replace(f"ability: {ab['name']}", f"ability: {name}")
                out[k] = v.replace("\r\n", "\n")
            out.setdefault("num", f'"num": {num}')
            new[tid] = {"from": aid, "name": name, "orig_name": ab["name"], "members": out, "changes": sorted(set(changes))}
            twins[aid] = tid
    return twins, new


def write_abilities(new):
    adir = RES / "data" / MOD / "abilities"
    if adir.exists():
        for f in adir.glob("*.js"):
            f.unlink()
    for tid, n in new.items():
        write(adir / f"{tid}.js", "{\n" + ",\n".join(n["members"].values()) + "\n}\n")


def signature(m):
    """Everything about a move except its type and name: two moves with the same signature are exact opposites."""
    sec = m["secondary"]
    return (m["category"], m["basePower"], m["accuracy"], m["pp"], m["priority"], m["target"],
            None if sec is None else (sec["chance"], bool(sec["status"]), bool(sec["volatileStatus"]), json.dumps(sec["boosts"], sort_keys=True), sec["hasSelf"]),
            m["secondaries"], m["self"], json.dumps(m["drain"]), json.dumps(m["recoil"]), json.dumps(m["multihit"]),
            m["critRatio"], json.dumps(m["boosts"], sort_keys=True), bool(m["status"]), bool(m["volatileStatus"]),
            tuple(sorted(m["fns"])), tuple(sorted(k for k, v in m["flags"].items() if v)))


def twin_name(m, new_type):
    if toid(m["name"]) in NAME_OVERRIDES:
        return NAME_OVERRIDES[toid(m["name"])]
    words = m["name"].split(" ")
    old = m["type"].lower()
    t = new_type.title()
    if len(words) == 1:
        return f"{t} {m['name']}"                       # one word: Earthquake -> Water Earthquake
    for i, w in enumerate(words):
        if w in TYPE_WORDS.get(old, []):
            words[i] = t                               # Dragon Claw -> Fairy Claw
            return " ".join(words)
    words[0] = t                                       # Cross Chop -> Psychic Chop
    return " ".join(words)


def build_twins(moves, learn):
    by_sig = {}
    for mid, m in moves.items():
        if m["isNonstandard"] or m["isZ"] or m["isMax"]:
            continue
        by_sig.setdefault((signature(m), m["type"].lower()), []).append(mid)
    twins, new = {}, {}
    num = -31000
    # the signature moves first, so their written names win (Phantom Force can't take "Dark Force")
    for mid in sorted(learn, key=lambda k: (k not in NAME_OVERRIDES, k)):
        m = moves.get(mid)
        if not m or mid in SKIP or m["isZ"] or m["isMax"]:
            continue
        new_type = TYPE_CHART[m["type"].lower()]
        if mid != "judgment":
            match = sorted(by_sig.get((signature(m), new_type), []), key=lambda k: moves[k]["num"])
            if match:
                twins[mid] = match[0]                      # an exact opposite already exists
                continue
        name = twin_name(m, new_type)
        tid = toid(name)
        if tid in moves or tid in new:                     # taken by another move (Dark Pulse, Dragon Pulse -> Fairy Pulse)
            name = f"{new_type.title()} {m['name']}"
            tid = toid(name)
        num -= 1
        new[tid] = {"from": mid, "name": name, "type": new_type.title(), "num": num, "orig_name": m["name"]}
        twins[mid] = tid
    return twins, new


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_moves(new):
    mdir = RES / "data" / MOD / "moves"
    if mdir.exists():
        for f in mdir.glob("*.js"):
            f.unlink()
    for tid, n in new.items():
        extra = ""
        if n["from"] == "judgment":
            # Judgment takes its type from Arceus' plate; its distorted twin takes the plate type's weakness
            chart = json.dumps({k.title(): v.title() for k, v in TYPE_CHART.items()})
            extra = (f', onModifyType(move, pokemon) {{ const chart = {chart}; const item = pokemon.getItem(); '
                     f'const t = item && item.onPlate && !item.zMoveType ? item.onPlate : "Normal"; move.type = chart[t] || "Fighting"; }}')
        write(mdir / f"{tid}.js",
              f'Object.assign({{}}, Dex.data.Moves["{n["from"]}"], {{num: {n["num"]}, name: "{n["name"]}", type: "{n["type"]}", '
              f'isNonstandard: null, zMove: undefined, maxMove: undefined{extra}}})\n')


def write_crystal():
    write(RES / "data" / MOD / "mega_showdown" / "showdown" / "held_items" / "distortioncrystal.js", """({
  name: "Distortion Crystal",
  spritenum: 0,
  num: -31000,
  gen: 9,
  onTakeItem(item, source) {
    return false;
  },
})
""")


def write_engine(twins, ability_twins):
    table = json.dumps(twins, sort_keys=True)
    # side: the choice. "move N [target] distort" reaches chooseMove with " distort" still on (choose() only strips
    # the gimmicks it knows): strip it, check, choose the move as usual, mark the Pokémon.
    write(RES / "data" / MOD / "mega_showdown" / "showdown" / "scripts" / "side.js", """({
  chooseMove(moveText, targetLoc, event) {
    const Side = require("./sim/side").Side;
    if (typeof moveText === "string" && / distort$/.test(moveText.trim())) {
      let text = moveText.trim().replace(/ distort$/, "").trim();
      if (targetLoc === undefined && /\\s(?:-|\\+)?[1-3]$/.test(text)) {
        targetLoc = parseInt(text.slice(-2));
        text = text.slice(0, -2).trim();
      }
      const index = this.getChoiceIndex();
      const pokemon = this.active[index];
      // can't distort (already did, or no crystal): the plain move, never an error (an AI's choice must not fail)
      if (!pokemon || this.distortUsed || this.choice.distort || !this.battle.actions.canDistort(pokemon)) {
        return Side.prototype.chooseMove.call(this, text, targetLoc, event);
      }
      const ok = Side.prototype.chooseMove.call(this, text, targetLoc, event);
      if (ok) {
        // the queue turns this into a distort action before the move (see queue.js)
        this.choice.actions[this.choice.actions.length - 1].distort = true;
        this.choice.distort = true;
      }
      return ok;
    }
    return Side.prototype.chooseMove.call(this, moveText, targetLoc, event);
  },
})
""")
    # queue: a chosen distort becomes its own action at Terastallization's priority (after switches, before moves),
    # an "event" action (a kind Showdown already runs) that a per-battle runAction hook turns into the distortion
    write(RES / "data" / MOD / "mega_showdown" / "showdown" / "scripts" / "queue.js", """({
  resolveAction(action, midTurn) {
    const BattleQueue = require("./sim/battle-queue").BattleQueue;
    const battle = this.battle;
    if (!battle.distortHooked) {
      battle.distortHooked = true;
      const runAction = battle.runAction;
      battle.runAction = function (a) {
        if (a.choice === "event" && a.event === "Distort") this.actions.runDistort(a.pokemon);
        // Pokémon distorted outside battle (the interaction wheel) start in their -Distorted forme: give them their twins
        if (a.choice === "start") this.actions.distortedAtStart();
        return runAction.call(this, a);
      };
    }
    const actions = BattleQueue.prototype.resolveAction.call(this, action, midTurn);
    if (!midTurn && action.choice === "move" && action.distort && !action.pokemon.distorted) {
      action.distort = false;
      actions.unshift(...BattleQueue.prototype.resolveAction.call(this,
        {choice: "event", event: "Distort", pokemon: action.pokemon, order: 106}, midTurn));
    }
    return actions;
  },
})
""")
    # actions: distorting happens right before the Pokémon's move, and the chosen move becomes its twin
    write(RES / "data" / MOD / "mega_showdown" / "showdown" / "scripts" / "actions.js", """({
  distortTwins: TWINS,
  distortAbilities: ABILITIES,
  distortChart: CHART,
  distortedSpecies(pokemon) {
    const species = this.dex.species.get(pokemon.species.name + "-Distorted");
    return species && species.exists ? species : null;
  },
  canDistort(pokemon) {
    // the Distortion Crystal; Arceus can use its plate instead (it can't hold both, and the plates are its power)
    const item = pokemon.getItem();
    const source = pokemon.item === "distortioncrystal" || (pokemon.species.num === 493 && item && item.onPlate);
    return !pokemon.distorted && !!source && !!this.distortedSpecies(pokemon);
  },
  distortMoves(pokemon) {
    // every move becomes its inverted twin, keeping its PP
    for (let i = 0; i < pokemon.moveSlots.length; i++) {
      const slot = pokemon.moveSlots[i];
      const twinId = this.distortTwins[slot.id];
      if (!twinId) continue;
      const twin = this.dex.moves.get(twinId);
      if (!twin || !twin.exists) continue;
      const moved = {move: twin.name, id: twin.id, pp: slot.pp, maxpp: slot.maxpp, target: twin.target,
                     disabled: slot.disabled, disabledSource: slot.disabledSource, used: slot.used, virtual: slot.virtual};
      pokemon.moveSlots[i] = moved;
      if (pokemon.baseMoveSlots[i] && pokemon.baseMoveSlots[i].id === slot.id) pokemon.baseMoveSlots[i] = moved;
    }
  },
  distortedAbility(pokemon) {
    const twin = this.distortAbilities[pokemon.baseAbility];
    return twin && this.dex.abilities.get(twin).exists ? twin : null;
  },
  distortedAtStart() {
    // before the leads are sent out, so their abilities start as their twins
    for (const side of this.battle.sides) {
      for (const pokemon of side.pokemon) {
        if (pokemon.distorted || !/-Distorted$/.test(pokemon.species.name)) continue;
        this.distortMoves(pokemon);
        const twin = this.distortedAbility(pokemon);
        if (twin) {
          pokemon.baseAbility = pokemon.ability = twin;
          pokemon.abilityState = {id: twin, target: pokemon};
        }
        pokemon.distorted = true;
        side.distortUsed = true;
      }
    }
  },
  runDistort(pokemon) {
    if (!pokemon.isActive || pokemon.fainted || !this.canDistort(pokemon)) return false;
    const species = this.distortedSpecies(pokemon);
    const ability = pokemon.ability;
    const twin = this.distortedAbility(pokemon);
    const source = this.dex.conditions.get("distortion");
    pokemon.formeChange(species, source && source.exists ? source : null, true);
    // the ability follows: its distorted twin if it's bound to the Pokémon's type (Blaze -> Torrent), else the same
    pokemon.setAbility(twin || ability, null, true);
    pokemon.baseAbility = twin || ability;
    if (twin) this.battle.add("-ability", pokemon, this.dex.abilities.get(twin).name);
    this.distortMoves(pokemon);
    pokemon.distorted = true;
    pokemon.side.distortUsed = true;
    this.battle.add("-message", `${pokemon.name} distorted!`);
    return true;
  },
  runMove(moveOrMoveName, pokemon, targetLoc, options) {
    const BattleActions = require("./sim/battle-actions").BattleActions;
    // the move was chosen (and queued) before the Pokémon distorted: use its twin, the move now in its slot
    if (pokemon.distorted) {
      const id = typeof moveOrMoveName === "string" ? this.dex.toID(moveOrMoveName) : moveOrMoveName.id;
      const twinId = this.distortTwins[id];
      if (twinId && !pokemon.moveSlots.some(s => s.id === id) && pokemon.moveSlots.some(s => s.id === twinId)) {
        moveOrMoveName = this.dex.moves.get(twinId);
      }
    }
    return BattleActions.prototype.runMove.call(this, moveOrMoveName, pokemon, targetLoc, options);
  },
})
""".replace("TWINS", table).replace("ABILITIES", json.dumps(ability_twins, sort_keys=True)).replace("CHART", json.dumps({k.title(): v.title() for k, v in TYPE_CHART.items()}, sort_keys=True)))


def write_lang(new, new_abilities):
    path = RES / "assets" / MOD / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data = {k: v for k, v in data.items() if not k.startswith(("cobblemon.move.", "cobblemon.ability."))}
    for tid, n in new_abilities.items():
        changes = " and ".join(f"{WEATHER_NAMES.get(b, b)} instead of {WEATHER_NAMES.get(a, a)}"
                               for a, b in sorted(n["changes"], key=lambda c: len(WEATHER_NAMES.get(c[0], c[0]))))
        data[f"cobblemon.ability.{tid}"] = n["name"]
        data[f"cobblemon.ability.{tid}.desc"] = f"The distorted twin of {n['orig_name']}: the same effect, with {changes}."
    for tid, n in new.items():
        data[f"cobblemon.move.{tid}"] = n["name"]
        data[f"cobblemon.move.{tid}.desc"] = (f"The distorted twin of {n['orig_name']}: the same move, but {n['type']}-type."
                                              if n["from"] != "judgment" else
                                              "The distorted twin of Judgment: its type is the weakness of Arceus' plate type.")
    path.write_text(json.dumps(dict(sorted(data.items())), indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--showdown", required=True, help="dump_showdown.js's output")
    ap.add_argument("--cobblemon-jar", required=True)
    a = ap.parse_args()
    dump = json.loads(Path(a.showdown).read_text())
    moves, abilities = dump["moves"], dump["abilities"]
    learn = learnsets(a.cobblemon_jar)
    twins, new = build_twins(moves, learn)
    ability_twins, new_abilities = build_ability_twins(abilities, species_info(a.cobblemon_jar))
    write_moves(new)
    write_abilities(new_abilities)
    write_crystal()
    write_engine(twins, ability_twins)
    write_lang(new, new_abilities)
    (RES / "data" / MOD / "distortion").mkdir(parents=True, exist_ok=True)
    (RES / "data" / MOD / "distortion" / "move_twins.json").write_text(json.dumps(twins, indent=2, sort_keys=True) + "\n")
    existing = sum(1 for v in twins.values() if v not in new)
    print(f"{len(learn)} learnable moves -> {len(twins)} twins ({existing} existing opposites, {len(new)} new moves)")
    print("ability twins:", ", ".join(f"{k} -> {v}{' (new)' if v in new_abilities else ''}" for k, v in sorted(ability_twins.items())))


if __name__ == "__main__":
    main()
