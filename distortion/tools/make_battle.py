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
  engine     Showdown scripts merged in by Mega Showdown's scripts loader
             (data/<ns>/mega_showdown/showdown/scripts/<side|queue|pokemon|actions>.js; see write_engine): "move N
             [target] distort" toggles distortion (any turn, both ways) as its own action before moves; a distorted
             Pokémon keeps its real species (so item-free form changes work: Ash-Greninja, Gigantamax, Dragon
             Ascent) with inverted types, twin moves and ability; the client hears "-Distorted"/"-Reverted"

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
from make_assets import DISTORTABLE, GEN1_LINES, TYPE_CHART, TYPE_OVERRIDES  # noqa: E402
GEN1 = {sp for line in GEN1_LINES for sp in line}

# specialised distortions: their moves of these types turn into these instead (Mew's Psychic moves turn Normal, the
# unborn; Mewtwo's turn Fighting, the bodybuilder); the rest follow the chart
CHART_OVERRIDES = {"mew": {"psychic": "normal"}, "mewtwo": {"psychic": "fighting"}}

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
ABILITY_NAMES = {"solarpower": "Storm Power", "flashfire": "Flash Flood", "thickfat": "Blubber",   # new twins with
                 "liquidvoice": "Blossom Voice", "scrappy": "Scrappy Mind", "snowcloak": "Heat Haze",    # names written for them
                 "drought": "Deluge", "galvanize": "Tectonize", "icebody": "Sun Bask", "lightningrod": "Sinkhole",
                 "magnetpull": "Quagmire", "motordrive": "Tremor Drive", "overcoat": "Sunscreen", "pixilate": "Metallize",
                 "rattled": "Jittery", "sandforce": "Tide Force", "slushrush": "Heat Rush", "snowwarning": "Heat Warning",
                 "steelyspirit": "Earthen Spirit", "swarm": "Flock", "waterabsorb": "Root Absorb",
                 # a second twin where the holder's types differ ("<ability>:<its types the code names>")
                 "scrappy:normal": "Scrappy Fists", "thickfat:ice": "Insulation", "sandforce:ground,steel": "Silt Force"}
PRIMAL = {"desolateland": "sunnyday", "primordialsea": "raindance"}
ABILITY_META = {"name", "num", "rating", "isNonstandard", "desc", "shortDesc"}


def toid(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def learnsets(jar, only=None):
    z = zipfile.ZipFile(jar)
    out = set()
    for sp in (only or DISTORTABLE):
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
    """Every distortable species' types and abilities (all forms but the item ones: stone megas, primals)."""
    z = zipfile.ZipFile(jar)
    info = {}
    for sp in DISTORTABLE:
        for n in z.namelist():
            if n.startswith("data/cobblemon/species/") and n.endswith(f"/{sp}.json"):
                d = json.loads(z.read(n))
                forms = []
                for f in [d] + [f for f in d.get("forms", []) if not set(f.get("aspects", [])) & {"mega", "mega_x", "mega_y", "primal"}]:
                    pt = f.get("primaryType", d["primaryType"])
                    st = f.get("secondaryType", d.get("secondaryType") if "primaryType" not in f else None)
                    forms.append({"types": tuple(sorted({pt.lower()} | ({st.lower()} if st else set()))),
                                  "abilities": {a.split(":", 1)[-1] for a in f.get("abilities", d["abilities"])}})
                info[sp] = forms
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
    for primal, normal in PRIMAL.items():
        if primal not in text:                      # an ordinary weather never turns primal (Snow Warning: sun, not
            out = out.replace(f'setWeather("{primal}")', f'setWeather("{normal}")')     # Desolate Land)
    return out, sorted({(k.strip('"'), pairs[k].strip('"')) for k in done})


def normalize(text, name, aid):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"this\.debug\([^;]*\);", "", text)
    text = text.replace(f'"{name}', '"§NAME').replace(f": {name}", ": §NAME").replace(f'"{aid}"', '"§ID"')
    return re.sub(r"\s+", " ", text).strip()


def ability_body(ab, aid):
    return {k: normalize(v, ab["name"], aid) for k, v in ab["members"].items() if k not in ABILITY_META}


def build_ability_twins(abilities, info):
    """aid -> {holder's types ("Fire", "Ice/Water"): twin}: a type-bound ability's twin depends on which of the
    holder's types its code names (Thick Fat on a Fire type: Blubber, resisting Water and Ice; on an Ice type, Fire)."""
    table, new, variant = {}, {}, {}
    num = -31100
    order = sorted(info, key=lambda sp: (sp in GEN1, sp))       # earlier lines first: their twins keep their names
    for sp in order:
      for form in info[sp]:
        for aid in sorted(form["abilities"]):
            ab = abilities.get(aid)
            if not ab:
                continue
            key = "/".join(t.title() for t in form["types"])
            members, changes = {}, []
            for k, v in ab["members"].items():
                members[k], ch = substitute(v, form["types"]) if k not in ABILITY_META else (v, [])
                changes += ch
            if not changes:
                continue                                    # not bound to its own type: it stays
            vkey = (aid, tuple(sorted(set(changes))))
            if vkey in variant:
                table.setdefault(aid, {})[key] = variant[vkey]
                continue
            body = {k: normalize(v, ab["name"], aid) for k, v in members.items() if k not in ABILITY_META}
            match = sorted((o for o, oa in abilities.items() if o != aid and not oa["isNonstandard"] and ability_body(oa, o) == body),
                           key=lambda o: abilities[o]["num"])
            if match:
                variant[vkey] = table.setdefault(aid, {})[key] = match[0]     # Blaze -> Torrent
                continue
            frm, to = sorted(set(changes))[0]
            froms = ",".join(sorted({f.lower() for f, _ in changes}))
            name = ABILITY_NAMES.get(f"{aid}:{froms}") or (ABILITY_NAMES.get(aid) if aid not in {n["from"] for n in new.values()} else None)
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
            variant[vkey] = table.setdefault(aid, {})[key] = tid
    return table, new


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


def build_twins(moves, learn, chart=TYPE_CHART, new=None, only_types=None):
    by_sig = {}
    for mid, m in moves.items():
        if m["isNonstandard"] or m["isZ"] or m["isMax"]:
            continue
        by_sig.setdefault((signature(m), m["type"].lower()), []).append(mid)
    twins = {}
    new = {} if new is None else new
    num = -31000 - len(new)
    # the signature moves first, so their written names win (Phantom Force can't take "Dark Force")
    for mid in sorted(learn, key=lambda k: (k not in NAME_OVERRIDES, k)):
        m = moves.get(mid)
        if not m or mid in SKIP or m["isZ"] or m["isMax"]:
            continue
        if only_types is not None and m["type"].lower() not in only_types:
            continue
        new_type = chart[m["type"].lower()]
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


def strip_line_comments(js: str) -> str:
    """JavaScript without its // comments (strings, template literals and regex literals kept). Mega Showdown's script
    and held-item loaders join a file's lines with no separator (content.replace("\n", "")), so a // comment would
    swallow the rest of the file ("Expected } but found eof" when the world loads)."""
    out, i, n = [], 0, len(js)
    quote, prev = None, ""
    while i < n:
        ch = js[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(js[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"`":
            quote = ch
        elif ch == "/" and js.startswith("//", i):
            while i < n and js[i] != "\n":
                i += 1
            continue
        elif ch == "/" and prev in "(,=:[!&|?{};" and not js.startswith("/*", i):
            j = i + 1                                       # a regex literal: copy it whole
            while j < n and js[j] != "/" and js[j] != "\n":
                j += 2 if js[j] == "\\" else 1
            out.append(js[i:j + 1])
            i = j + 1
            prev = "/"
            continue
        out.append(ch)
        if not ch.isspace():
            prev = ch
        i += 1
    return "".join(out)


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".js":
        text = strip_line_comments(text)
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


def write_engine(twins, ability_twins, by_species):
    """The Showdown side of distorting (Mega Showdown's scripts loader merges these into the battle engine).

    A distorted Pokémon keeps its real species (so every form change that doesn't need a held item works as usual:
    Battle Bond's Ash-Greninja, Dynamax and Gigantamax, a move-triggered mega like Dragon Ascent, ability forms) and is
    flagged `distorted`: its types are its species' types turned into their weaknesses (re-applied after any species
    change), its moves are their twins and its ability its twin (if type-bound). Choosing a move with the "distort"
    gimmick toggles it, freely, any turn: distort, or revert to normal. The client is told with a -formechange to
    "<species>-Distorted" / "<species>-Reverted", which Cobblemon posts as FORME_CHANGE ("distorted" / "reverted"),
    and the add-on gives or takes the "distorted" aspect (the look). A Pokémon distorted outside battle starts in its
    "-Distorted" species; it's set back to its real one, already distorted, before the leads are sent out."""
    table = json.dumps(twins, sort_keys=True)
    scripts = RES / "data" / MOD / "mega_showdown" / "showdown" / "scripts"
    # side: "move N [target] distort" reaches chooseMove with " distort" still on (choose() only strips the gimmicks
    # it knows): strip it and tag the move action; if the Pokémon can't toggle, it's the plain move (an AI's choice
    # must never fail)
    write(scripts / "side.js", """({
  chooseMove(moveText, targetLoc, event) {
    const Side = require("./sim/side").Side;
    if (typeof moveText === "string" && / distort$/.test(moveText.trim())) {
      let text = moveText.trim().replace(/ distort$/, "").trim();
      if (targetLoc === undefined && /\\s(?:-|\\+)?[1-3]$/.test(text)) {
        targetLoc = parseInt(text.slice(-2));
        text = text.slice(0, -2).trim();
      }
      const pokemon = this.active[this.getChoiceIndex()];
      if (!pokemon || !this.battle.actions.canToggleDistortion(pokemon)) {
        return Side.prototype.chooseMove.call(this, text, targetLoc, event);
      }
      const ok = Side.prototype.chooseMove.call(this, text, targetLoc, event);
      if (ok) this.choice.actions[this.choice.actions.length - 1].distort = true;
      return ok;
    }
    return Side.prototype.chooseMove.call(this, moveText, targetLoc, event);
  },
})
""")
    # queue: the toggle is its own action at Terastallization's priority (after switches, before moves): an "event"
    # action (a kind Showdown already runs) that a per-battle runAction hook carries out
    write(scripts / "queue.js", """({
  resolveAction(action, midTurn) {
    const BattleQueue = require("./sim/battle-queue").BattleQueue;
    const battle = this.battle;
    if (!battle.distortHooked) {
      battle.distortHooked = true;
      const runAction = battle.runAction;
      battle.runAction = function (a) {
        if (a.choice === "event" && a.event === "Distort") this.actions.toggleDistortion(a.pokemon);
        // Pokémon distorted outside battle (the interaction wheel) start in their -Distorted species
        if (a.choice === "start") this.actions.distortedAtStart();
        return runAction.call(this, a);
      };
    }
    const actions = BattleQueue.prototype.resolveAction.call(this, action, midTurn);
    if (!midTurn && action.choice === "move" && action.distort) {
      action.distort = false;
      actions.unshift(...BattleQueue.prototype.resolveAction.call(this,
        {choice: "event", event: "Distort", pokemon: action.pokemon, order: 106}, midTurn));
    }
    return actions;
  },
})
""")
    # pokemon: after any species change (switching, Gigantamax, Ash-Greninja...), a distorted Pokémon's types are
    # inverted again
    write(scripts / "pokemon.js", """({
  setSpecies(rawSpecies, source, isTransform) {
    const Pokemon = require("./sim/pokemon").Pokemon;
    const species = Pokemon.prototype.setSpecies.call(this, rawSpecies, source, isTransform);
    if (species && this.distorted && !isTransform) this.battle.actions.applyDistortTypes(this);
    return species;
  },
})
""")
    write(scripts / "actions.js", """({
  distortTwins: TWINS,
  distortTwinsBySpecies: SPECIES_TWINS,
  distortTypesBySpecies: SPECIES_TYPES,
  distortAbilities: ABILITIES,
  distortChart: CHART,
  distortBase(pokemon) {
    return pokemon.baseSpecies.baseSpecies || pokemon.baseSpecies.name;
  },
  twinOf(pokemon, id) {
    const own = this.distortTwinsBySpecies[this.distortBase(pokemon)];
    return (own && own[id]) || this.distortTwins[id];
  },
  hasDistortion(pokemon) {
    return this.dex.species.get(this.distortBase(pokemon) + "-Distorted").exists;
  },
  canToggleDistortion(pokemon) {
    if (pokemon.distorted) return true;          // reverting needs nothing more
    // the Distortion Crystal; Arceus can use its plate instead (it can't hold both, and the plates are its power)
    const item = pokemon.getItem();
    const source = pokemon.item === "distortioncrystal" || (pokemon.species.num === 493 && item && item.onPlate);
    return !!source && this.hasDistortion(pokemon);
  },
  applyDistortTypes(pokemon) {
    // specialised distortions have their own types (Mew and Mewtwo: Normal/Fighting); the rest follow the chart
    const types = this.distortTypesBySpecies[this.distortBase(pokemon)] ||
      [...new Set(pokemon.species.types.map(t => this.distortChart[t] || t))];
    pokemon.setType(types, true);
  },
  distortedAbility(pokemon) {
    const twins = this.distortAbilities[pokemon.baseAbility];
    if (!twins) return null;
    const twin = twins[[...pokemon.species.types].sort().join("/")];
    return twin && this.dex.abilities.get(twin).exists ? twin : null;
  },
  swapSlot(pokemon, i, move) {
    const slot = pokemon.moveSlots[i];
    const moved = {move: move.name, id: move.id, pp: slot.pp, maxpp: slot.maxpp, target: move.target,
                   disabled: slot.disabled, disabledSource: slot.disabledSource, used: slot.used, virtual: slot.virtual};
    if (pokemon.baseMoveSlots[i] && pokemon.baseMoveSlots[i].id === slot.id) pokemon.baseMoveSlots[i] = moved;
    pokemon.moveSlots[i] = moved;
  },
  distortMoves(pokemon) {
    // every move becomes its inverted twin, keeping its PP; the pairs are kept to turn them back
    pokemon.distortPairs = [];
    for (let i = 0; i < pokemon.moveSlots.length; i++) {
      const slot = pokemon.moveSlots[i];
      const twinId = this.twinOf(pokemon, slot.id);
      const twin = twinId && this.dex.moves.get(twinId);
      if (!twin || !twin.exists) continue;
      pokemon.distortPairs.push([slot.id, twin.id]);
      this.swapSlot(pokemon, i, twin);
    }
  },
  undistortMoves(pokemon) {
    for (const [orig, twin] of pokemon.distortPairs || []) {
      const i = pokemon.moveSlots.findIndex(s => s.id === twin);
      const move = this.dex.moves.get(orig);
      if (i >= 0 && move.exists) this.swapSlot(pokemon, i, move);
    }
  },
  setDistorted(pokemon, on, silent) {
    const name = pokemon.species.name;
    if (on) {
      pokemon.distorted = true;
      pokemon.distortOrigAbility = pokemon.baseAbility;
      const twin = this.distortedAbility(pokemon);
      this.applyDistortTypes(pokemon);
      const want = twin || pokemon.baseAbility;
      if (pokemon.ability !== want) {
        if (silent) {
          pokemon.ability = want;
          pokemon.abilityState = {id: want, target: pokemon};
        } else {
          pokemon.setAbility(want, null, true);
        }
      }
      pokemon.baseAbility = want;
      this.distortMoves(pokemon);
      if (!silent) {
        this.battle.add("-formechange", pokemon, name + "-Distorted");
        if (twin) this.battle.add("-ability", pokemon, this.dex.abilities.get(twin).name);
        this.battle.add("-message", `${pokemon.name} distorted!`);
      }
    } else {
      pokemon.distorted = false;
      pokemon.setType(pokemon.species.types, true);
      const orig = pokemon.distortOrigAbility || pokemon.baseAbility;
      const changed = pokemon.ability !== orig;
      if (changed) pokemon.setAbility(orig, null, true);
      pokemon.baseAbility = orig;
      this.undistortMoves(pokemon);
      this.battle.add("-formechange", pokemon, name + "-Reverted");
      if (changed) this.battle.add("-ability", pokemon, this.dex.abilities.get(orig).name);
      this.battle.add("-message", `${pokemon.name} returned to normal!`);
    }
    return true;
  },
  toggleDistortion(pokemon) {
    if (!pokemon.isActive || pokemon.fainted || !this.canToggleDistortion(pokemon)) return false;
    return this.setDistorted(pokemon, !pokemon.distorted, false);
  },
  distortedAtStart() {
    // before the leads are sent out: back to the real species, already distorted
    for (const side of this.battle.sides) {
      for (const pokemon of side.pokemon) {
        if (pokemon.distorted || !/-Distorted$/.test(pokemon.species.name)) continue;
        const real = this.dex.species.get(pokemon.species.name.replace(/-Distorted$/, ""));
        if (real.exists) {
          pokemon.baseSpecies = real;
          pokemon.setSpecies(real);
          pokemon.details = pokemon.details.replace(/-Distorted(?=,|$)/, "");
        }
        this.setDistorted(pokemon, true, true);
      }
    }
  },
  runMove(moveOrMoveName, pokemon, targetLoc, options) {
    const BattleActions = require("./sim/battle-actions").BattleActions;
    // the move was chosen before the toggle ran: use the one now in its slot (the twin, or back to the original)
    const id = typeof moveOrMoveName === "string" ? this.dex.toID(moveOrMoveName) : moveOrMoveName.id;
    if (pokemon.distortPairs && !pokemon.moveSlots.some(s => s.id === id)) {
      const pair = pokemon.distortPairs.find(p => p[0] === id || p[1] === id);
      const other = pair && (pair[0] === id ? pair[1] : pair[0]);
      if (other && pokemon.moveSlots.some(s => s.id === other)) moveOrMoveName = this.dex.moves.get(other);
    }
    return BattleActions.prototype.runMove.call(this, moveOrMoveName, pokemon, targetLoc, options);
  },
})
""".replace("SPECIES_TWINS", json.dumps(by_species, sort_keys=True)).replace("SPECIES_TYPES", json.dumps(
        {sp.title(): [t.title() for t in ts] for sp, ts in TYPE_OVERRIDES.items()}, sort_keys=True)).replace(
        "TWINS", table).replace("ABILITIES", json.dumps(ability_twins, sort_keys=True)).replace(
        "CHART", json.dumps({k.title(): v.title() for k, v in TYPE_CHART.items()}, sort_keys=True)))


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
    by_species = {}
    for sp, over in CHART_OVERRIDES.items():
        chart = dict(TYPE_CHART, **over)
        t, _ = build_twins(moves, learnsets(a.cobblemon_jar, [sp]), chart, new, set(over))
        by_species[sp.title()] = t
    ability_twins, new_abilities = build_ability_twins(abilities, species_info(a.cobblemon_jar))
    write_moves(new)
    write_abilities(new_abilities)
    write_crystal()
    write_engine(twins, ability_twins, by_species)
    write_lang(new, new_abilities)
    (RES / "data" / MOD / "distortion").mkdir(parents=True, exist_ok=True)
    (RES / "data" / MOD / "distortion" / "move_twins.json").write_text(
        json.dumps({"default": twins, "species": {k.lower(): v for k, v in by_species.items()}}, indent=2, sort_keys=True) + "\n")
    existing = sum(1 for v in twins.values() if v not in new)
    print(f"{len(learn)} learnable moves -> {len(twins)} twins ({existing} existing opposites, {len(new)} new moves)")
    print("ability twins:", ", ".join(f"{k} -> {'/'.join(sorted(set(v.values())))}" for k, v in sorted(ability_twins.items())),
          f"({len(new_abilities)} new)")


if __name__ == "__main__":
    main()
