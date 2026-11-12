#!/usr/bin/env python3
"""
One-off: choose each region's league (8 gym types + 4 Elite Four types) and its trainers' teams from that generation's
Pokédex only, using Cobblemon's species data (implemented species; no legendaries, mythicals, Ultra Beasts or
paradoxes). Writes tools/league_teams.json, which make_leagues.py reads (committed, so the normal build needs no jar).

Usage: python3 tools/make_league_teams.py --cobblemon-jar <Cobblemon-fabric-1.8.4+1.21.1.jar>
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RANGES = {"johto": (152, 251), "hoenn": (252, 386), "sinnoh": (387, 493), "unova": (494, 649), "kalos": (650, 721),
          "alola": (722, 809), "galar": (810, 905), "paldea": (906, 1025)}
# each region's preferred league types, in gym order then the Elite Four (taken while the dex has enough of them)
PREFS = {
    "johto": ["flying", "bug", "normal", "ghost", "fighting", "steel", "ice", "dragon", "psychic", "poison", "dark", "fire", "water", "grass"],
    "hoenn": ["rock", "fighting", "electric", "fire", "normal", "flying", "psychic", "water", "dark", "ghost", "ice", "dragon", "grass", "steel"],
    "sinnoh": ["rock", "grass", "fighting", "water", "ghost", "steel", "ice", "electric", "bug", "ground", "fire", "psychic", "poison", "dark"],
    "unova": ["grass", "normal", "bug", "electric", "ground", "flying", "ice", "dragon", "ghost", "dark", "psychic", "fighting", "water", "fire"],
    "kalos": ["bug", "rock", "fighting", "grass", "electric", "fairy", "psychic", "ice", "fire", "water", "steel", "dragon", "dark", "ghost", "normal", "flying"],
    "alola": ["normal", "water", "fire", "grass", "electric", "ghost", "fairy", "ground", "steel", "rock", "dark", "flying", "psychic", "bug", "fighting", "dragon", "poison"],
    "galar": ["grass", "water", "fire", "fighting", "ghost", "fairy", "rock", "ice", "dark", "dragon", "psychic", "steel", "electric", "ground", "bug", "poison"],
    "paldea": ["bug", "grass", "electric", "water", "normal", "ghost", "psychic", "ice", "rock", "steel", "fairy", "dragon", "flying", "fighting", "dark", "fire", "ground"],
}
GYM_SIZE = [3, 3, 3, 4, 4, 4, 5, 5]
GYM_LEVEL = [14, 19, 24, 29, 34, 39, 44, 48]


def load(jar):
    z = zipfile.ZipFile(jar)
    out = {}
    for n in z.namelist():
        if not re.match(r"data/cobblemon/species/[^/]+/[^/]+\.json$", n):
            continue
        d = json.loads(z.read(n))
        if not d.get("implemented"):
            continue
        labels = set(d.get("labels", []))
        if labels & {"legendary", "mythical", "ultra_beast", "paradox", "restricted"}:
            continue
        types = [t for t in (d.get("primaryType"), d.get("secondaryType")) if t]
        bst = sum(d.get("baseStats", {}).values())
        out[Path(n).stem] = {"dex": d.get("nationalPokedexNumber"), "types": types, "bst": bst, "name": d.get("name")}
    return out


def pick(cands, n, frac):
    """n species from cands (sorted by strength) around the given fraction of the way up, the ace the strongest."""
    if not cands:
        return []
    i = int(round(frac * (len(cands) - 1)))
    lo = max(0, min(len(cands) - n, i - n // 2))
    return cands[lo:lo + n]                     # a smaller team when the type has fewer species (no repeats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cobblemon-jar", required=True)
    species = load(ap.parse_args().cobblemon_jar)
    leagues = {}
    for region, (a, b) in RANGES.items():
        local = {k: v for k, v in species.items() if v["dex"] and a <= v["dex"] <= b}
        by_type = {}
        for k, v in local.items():
            for t in v["types"]:
                by_type.setdefault(t, []).append(k)
        types = [t for t in PREFS[region] if len(by_type.get(t, [])) >= 3][:12]
        if len(types) < 12:
            types += sorted((t for t in by_type if t not in types), key=lambda t: -len(by_type[t]))[:12 - len(types)]
        trainers = []
        for k, t in enumerate(types):
            cands = sorted(by_type[t], key=lambda s: (local[s]["bst"], s))
            if k < 8:
                team = pick(cands, GYM_SIZE[k], k / 7 * 0.85)
                levels = [GYM_LEVEL[k] + i for i in range(len(team))]
            else:
                team = pick(cands, 5, 1.0)
                levels = [54 + (k - 8) * 2 + i for i in range(len(team))]
            trainers.append({"type": t, "team": [f"{s} level={lv}" for s, lv in zip(team, levels)]})
        leagues[region] = trainers
        if region == "alola":                                    # each trial's totem: the type's strongest wild Pokémon
            starters = {"rowlet", "dartrix", "decidueye", "litten", "torracat", "incineroar", "popplio", "brionne", "primarina"}
            used, totems = set(), {}
            for t in types[:8]:
                options = sorted((x for x in by_type[t] if x not in starters and x not in used),
                                 key=lambda s_: (-local[s_]["bst"], s_))
                totems[t] = options[0]
                used.add(options[0])
            leagues["alola_totems"] = totems
        print(region, [t["type"] for t in trainers])
    (HERE / "league_teams.json").write_text(json.dumps(leagues, indent=1) + "\n")


if __name__ == "__main__":
    main()
