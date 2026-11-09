#!/usr/bin/env python3
"""
Writes CobbleEffort: Distortion's battle data into common/src/main/resources (deterministic):

  twins      every move the distortable Pokémon can learn gets an inverted-type twin: an existing move that's its
             exact opposite (same category, power, accuracy, PP, priority, target, side effects; only the type
             differs, e.g. Ice Punch -> Fire Punch), otherwise a new move that's a copy with only its type and name
             changed (Cross Chop -> Psychic Chop). New moves are Cobblemon datapack moves
             (data/<ns>/moves/<id>.js, read by Cobblemon into Showdown and its move registry) built from the
             original's own Showdown data, so they keep every effect; their names go in the lang file.
  crystal    the Distortion Crystal's Showdown item (Mega Showdown's held-item scripts)
  engine     two Showdown scripts merged in by Mega Showdown's scripts loader
             (data/<ns>/mega_showdown/showdown/scripts/<side|queue|actions>.js):
               side.chooseMove     accepts "move N [target] distort" (once per battle per side, with the crystal)
               queue.resolveAction queues the distortion as its own action at Terastallization's priority
               actions.runDistort  distorts the Pokémon at the start of the turn: a permanent forme change to its
                                   "-Distorted" forme (inverted types; Cobblemon sees the detailschange and the
                                   add-on gives it the distorted look), its ability kept (or its inverted twin),
                                   every move swapped for its twin (runMove swaps the move it chose this turn)

Inputs: Showdown's move data dumped to JSON (see dump_moves.js) and Cobblemon's species data (its jar).
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
from make_assets import FIRST_SET, TYPE_CHART  # noqa: E402

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
                  "judgment": "Inverse Judgment"}
SKIP = {"struggle", "hiddenpower"}


def toid(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def learnsets(jar):
    z = zipfile.ZipFile(jar)
    out = set()
    for sp in FIRST_SET:
        for n in z.namelist():
            if n.startswith("data/cobblemon/species/") and n.endswith(f"/{sp}.json"):
                d = json.loads(z.read(n))
                for m in d.get("moves", []):
                    out.add(m.split(":", 1)[1])
                for f in d.get("forms", []):
                    for m in f.get("moves", []):
                        out.add(m.split(":", 1)[1])
    return sorted(out)


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


def write_engine(twins):
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
      if (!pokemon) return this.emitChoiceError("Can't distort: no Pokemon");
      if (this.distortUsed || this.choice.distort) return this.emitChoiceError("Can't distort: you can only distort once per battle");
      if (!this.battle.actions.canDistort(pokemon)) return this.emitChoiceError(`Can't distort: ${pokemon.name} can't distort`);
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
  runDistort(pokemon) {
    if (!pokemon.isActive || pokemon.fainted || !this.canDistort(pokemon)) return false;
    const species = this.distortedSpecies(pokemon);
    const ability = pokemon.ability;
    const source = this.dex.conditions.get("distortion");
    pokemon.formeChange(species, source && source.exists ? source : null, true);
    // the ability stays what it was (inverted, if it's a type-bound one with a twin)
    pokemon.setAbility(ability, null, true);
    pokemon.baseAbility = ability;
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
""".replace("TWINS", table).replace("CHART", json.dumps({k.title(): v.title() for k, v in TYPE_CHART.items()}, sort_keys=True)))


def write_lang(new):
    path = RES / "assets" / MOD / "lang" / "en_us.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data = {k: v for k, v in data.items() if not k.startswith("cobblemon.move.")}
    for tid, n in new.items():
        data[f"cobblemon.move.{tid}"] = n["name"]
        data[f"cobblemon.move.{tid}.desc"] = (f"The distorted twin of {n['orig_name']}: the same move, but {n['type']}-type."
                                              if n["from"] != "judgment" else
                                              "The distorted twin of Judgment: its type is the weakness of Arceus' plate type.")
    path.write_text(json.dumps(dict(sorted(data.items())), indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--moves", required=True)
    ap.add_argument("--cobblemon-jar", required=True)
    a = ap.parse_args()
    moves = json.loads(Path(a.moves).read_text())
    learn = learnsets(a.cobblemon_jar)
    twins, new = build_twins(moves, learn)
    write_moves(new)
    write_crystal()
    write_engine(twins)
    write_lang(new)
    (RES / "data" / MOD / "distortion").mkdir(parents=True, exist_ok=True)
    (RES / "data" / MOD / "distortion" / "move_twins.json").write_text(json.dumps(twins, indent=2, sort_keys=True) + "\n")
    existing = sum(1 for v in twins.values() if v not in new)
    print(f"{len(learn)} learnable moves -> {len(twins)} twins ({existing} existing opposites, {len(new)} new moves)")


if __name__ == "__main__":
    main()
