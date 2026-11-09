#!/usr/bin/env python3
"""
Writes dist/README.txt, the player guide shipped inside every release zip (build.gradle.kts distZip).

It is built from each collection's config (tools/collections/<name>.json: cosmetic_items, aspect and the "readme"
block) and the line lists the generator writes to tools/readme/<name>.json, so it always matches the build.
"@VERSION@" is replaced with mod_version when the zip is made. Runs at the end of `generate.py build`, or alone:

    python3 tools/make_readme.py
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
WIDTH = 100


def item_name(item_id: str) -> str:
    return item_id.split(":")[-1].replace("_", " ").title()


def wrap(text: str, indent: str = "", first: str | None = None) -> str:
    return textwrap.fill(text, WIDTH, initial_indent=first if first is not None else indent, subsequent_indent=indent)


def or_list(names: list[str]) -> str:
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " or " + names[-1]


def main():
    cols = []
    for f in sorted((TOOLS / "collections").glob("*.json")):
        cfg = json.loads(f.read_text())
        info = json.loads((TOOLS / "readme" / f.name).read_text())
        cols.append((cfg["readme"]["number"], cfg, info))
    cols.sort(key=lambda c: c[0])
    total = sum(info["pokemon"] for _, _, info in cols)

    out = []
    rule = "=" * WIDTH
    out += [rule, "CobbleEffort @VERSION@: extra cosmetic forms for Cobblemon".center(WIDTH), rule, ""]
    out.append(wrap(f"CobbleEffort adds {len(cols)} collections of cosmetic forms ({total} Pokemon) to Cobblemon"
                    + (f", plus {len(list((TOOLS / 'readme').glob('_new_*.json')))} new Pokemon" if list((TOOLS / 'readme').glob('_new_*.json')) else "") + ". "
                    "Each form is a new look for an existing Cobblemon model. Every cosmetic covers whole evolutionary "
                    "lines: if one stage has it, its pre-evolutions and evolutions have it too, and the look stays "
                    "through evolution, gender, regional forms, megas and shinies (shinies get their own version)."))
    out += ["", "INSTALL", "-------"]
    out.append(wrap("1. Unzip this file and put the .jar in your mods folder. It works on Fabric and NeoForge "
                    "(Minecraft 1.21.1, Cobblemon 1.7.0 or newer, built for 1.8.4).", "   ", ""))
    out.append(wrap("2. Remove any older cobbleeffort-*.jar first: two copies of the same mod stop the game "
                    "from starting.", "   ", ""))
    out.append(wrap("3. It must be installed on the server too (and in single player it just works).", "   ", ""))
    out += ["", "HOW TO GET A COSMETIC", "---------------------"]
    out.append(wrap("In survival: give a supported Pokemon the collection's item as its COSMETIC ITEM, the same way "
                    "as any Cobblemon cosmetic (hold the item, open the Pokemon's interaction menu and put it in the "
                    "cosmetic slot). Take the item back to remove the look. A Pokemon can wear one cosmetic at a time."))
    out.append("")
    out.append(wrap("With commands (creative / operators): /pokegive <pokemon> <form>, for example "
                    "/pokegive snorlax christmas or /pokegive snorlax christmas shiny. The <form> word for each "
                    "collection is listed below."))
    out += ["", "AT A GLANCE", "-----------"]
    rows = [(str(n), cfg["readme"]["title"].split(" (")[0], or_list([item_name(i) for i in cfg["cosmetic_items"]]),
             cfg["aspect"]) for n, cfg, _ in cols]
    widths = [max(len(r[i]) for r in rows + [("#", "Collection", "Cosmetic item", "Form word")]) + 2 for i in range(3)]
    for r in [("#", "Collection", "Cosmetic item", "Form word")] + rows:
        out.append("  " + "".join(c.ljust(w) for c, w in zip(r, widths)) + r[3])
    for n, cfg, info in cols:
        r = cfg["readme"]
        out += ["", rule, f"#{n}  {r['title'].upper()}  ({info['pokemon']} Pokemon)", rule]
        if r.get("warning"):
            out += [wrap(r["warning"]), ""]
        out.append(wrap(r["summary"]))
        out.append("")
        out.append(wrap(f"Cosmetic item: {or_list([item_name(i) for i in cfg['cosmetic_items']])}", "               ",
                        ""))
        out.append(f"Command:       /pokegive {r['example']} {cfg['aspect']}   (add 'shiny' for the shiny version)")
        out += ["", "The look:"]
        out += [wrap(l, "    ", "  * ") for l in r["looks"]]
        if r.get("specials"):
            out += ["", "Special costumes:"]
            for sp in r["specials"]:
                out.append(wrap(sp["line"], "    ", "  * "))
                out.append(wrap(sp["look"], "      "))
                out.append(wrap(f"Shiny: {sp['shiny']}", "      "))
        out += ["", "Pokemon (each line is a whole evolutionary family):"]
        out += [wrap(" > ".join(" / ".join(stage) for stage in line), "      ", "  - ") for line in info["lines"]]
    new = [json.loads(f.read_text()) for f in sorted((TOOLS / "readme").glob("_new_*.json"))]
    if new:
        out += ["", rule, "NEW POKEMON", rule]
        out.append(wrap("Pokemon Cobblemon has data for but no model, now with a model, animations and a way to get "
                        "them:"))
        for p in sorted(new, key=lambda p: p["dex"]):
            out += ["", f"#{p['dex']:04d} {p['name'].upper()}  ({p['types']}, {p['ability']})"]
            out.append(wrap(p["look"], "  ", "  "))
            out += [wrap(t, "    ", "  * ") for t in p["how"]]
    megas_file = TOOLS / "readme" / "_megas.json"
    if megas_file.exists():
        megas = json.loads(megas_file.read_text())
        out += ["", rule, "CUSTOM MEGA EVOLUTIONS (needs Mega Showdown)", rule]
        out.append(wrap("Five Ancient Paradox Pokemon can Mega Evolve in battle, the same way as Mega Showdown's megas: "
                        "hold the mega stone, wear a Mega Bracelet, and press Mega Evolve in battle. The base forms "
                        "come from Cobblemon: AllTheMons x Mega Showdown."))
        stat_names = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
        for sp, m in megas.items():
            out += ["", f"MEGA {m['display'].upper()}  ({' / '.join(t.title() for t in m['types'])}, "
                        f"{m['ability'].replace('toughclaws', 'Tough Claws').replace('magicbounce', 'Magic Bounce').replace('strongjaw', 'Strong Jaw').replace('levitate', 'Levitate').replace('moxie', 'Moxie')})"]
            out.append("  Stats: " + "  ".join(f"{n} {v}" for n, v in zip(stat_names, m["stats"])) + f"  (total {sum(m['stats'])})")
            r = m["recipe"]
            legend = ", ".join(f"{c} = {item_name(i)}" + (" (Mega Showdown's)" if i.startswith("mega_showdown:") else "")
                               for c, i in r["key"].items())
            out.append(f"  Stone: {m['stone_name']}, crafted like this:")
            out += [f"      [{row.replace(' ', '.')}]" for row in r["pattern"]]
            out.append(wrap(legend, "      ", "      "))
    out += ["", rule, "WORKS WITH", rule]
    out.append(wrap("CobbleEffort is built to run alongside Mega Showdown (+ Extra Megas, Ores), Cobblemon: AllTheMons "
                    "x Mega Showdown, Cobblemon Baby Legends, Cobblemon Lost Lore, Legendary Monuments, the Fully "
                    "Hisuian Starters resource pack and the Poke Costumes data pack. None of them is required."))
    out.append("")
    out += [wrap(t, "    ", "  * ") for t in [
        "Mega Showdown megas, Gigantamax and other forms of Pokemon in a collection get their own cosmetic look.",
        "Baby Legends' Xerfawn and Latot belong to their legendary's line (Backrooms and Easter).",
        "Forms from AllTheMons x Mega Showdown, Lost Lore, Fully Hisuian Starters and Poke Costumes keep their own "
        "look while the cosmetic is worn (their licences don't allow recoloured copies).",
    ]]
    out += ["", rule, "CREDITS AND LICENCE", rule]
    out.append(wrap("The textures are adaptations of Cobblemon's (CC BY-NC 3.0) and Mega Showdown's (CC BY-NC-SA 4.0) "
                    "assets. Non-commercial use only. Full credits are in CREDITS_cobbleeffort.md inside the jar. "
                    "Pokemon belongs to Nintendo, Game Freak and The Pokemon Company; The Backrooms to Kane Parsons; "
                    "Five Nights at Freddy's to Scott Cawthon; Naruto to Masashi Kishimoto. CobbleEffort is fan work "
                    "and not affiliated with any of them."))
    out += ["", "Source and issues: https://github.com/ellecat5112/CobbleEffort", ""]
    dest = ROOT / "dist" / "README.txt"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text("\n".join(out))
    print(f"wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
