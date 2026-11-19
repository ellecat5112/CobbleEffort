"""Lore sizes for the Digimon (the user's call, Digital 0.18.0: lore-accurate sizes replace the old "Greymon >= 15
blocks, +10 per stage" rule). One block = one metre. Digimon have no official height chart: wikimon's profiles state a
body size for exactly one (Valdurmon, a 30 m wingspan), so the heights come from how each Digimon is shown next to
people and other Digimon in the anime, manga and games (Agumon about a metre, Greymon a few storeys, the Royal Knights
not much taller than a man, Machinedramon and VenomVamdemon towering over buildings).

* LORE: hand-picked heights (metres, standing height as drawn) for the Digimon whose on-screen size is well known.
* Everyone else: their wikimon type (first listed; "Ancient X" counts as X) picks a body-plan group, and the group's
  height for their level (so a Holy Knight stays man-sized at Ultimate while a Dinosaur grows into a giant).

    python3 tools/digimon/sizes.py          # -> tools/digimon/data/sizes.json {slug: {"m": metres, "how": ...}}

Read by tools/newmons/digimon_gen.py (Pokédex height/weight) and build.py (baseScale = metres / model height).
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent

LEVELS = ["Baby I", "Baby II", "Child", "Adult", "Perfect", "Ultimate", "Super Ultimate"]
GROUPS = {  # metres for Baby I, Baby II, Child, Adult, Perfect, Ultimate, Super Ultimate
    "humanoid": (0.25, 0.4, 1.1, 2.0, 2.4, 2.8, 3.5),
    "small": (0.2, 0.35, 0.6, 1.0, 1.4, 1.8, 2.5),
    "dragon": (0.3, 0.45, 1.2, 6.0, 10.0, 15.0, 20.0),
    "dino": (0.3, 0.45, 1.0, 6.0, 9.0, 12.0, 16.0),
    "beast": (0.25, 0.4, 0.8, 2.2, 3.0, 4.0, 5.5),
    "bird": (0.25, 0.4, 0.8, 3.0, 5.0, 7.0, 9.0),
    "aqua": (0.25, 0.4, 0.8, 3.0, 5.0, 8.0, 12.0),
    "insect": (0.25, 0.4, 0.6, 3.0, 5.0, 8.0, 10.0),
    "plant": (0.25, 0.4, 0.8, 2.2, 2.6, 3.2, 4.0),
    "machine": (0.3, 0.45, 1.0, 2.6, 4.0, 6.0, 8.0),
    "element": (0.25, 0.4, 0.9, 2.4, 3.5, 5.0, 7.0),
    "reptile": (0.25, 0.4, 0.8, 2.0, 3.5, 5.0, 7.0),
    "undead": (0.25, 0.4, 0.8, 1.8, 2.6, 3.4, 4.5),
    "generic": (0.25, 0.4, 0.9, 2.2, 3.0, 4.0, 6.0),
}
TYPE_GROUP = [  # (regex on the wikimon type, group, factor); first match wins
    (r"^(small|baby) dragon$", "beast", 1.0),
    (r"dragon (man|warrior)", "humanoid", 1.15),
    (r"^demon lord$", "humanoid", 1.2),
    (r"dragon", "dragon", 1.0),
    (r"dinosaur|ankylosaur|ceratopsian|stegosaur|plesiosaur|pterosaur", "dino", 1.0),
    (r"fairy|puppet|small (devil|angel|bird)|^cherub$|card|musical|food|bulb|seed|lcd|chick|lesser|slime|larva|unique|smoke|spirit",
     "small", 1.0),
    (r"giant bird", "bird", 1.4),
    (r"bird man|beast man|aquatic beast man|reptile man|marine man", "humanoid", 1.0),
    (r"bird", "bird", 1.0),
    (r"beast|mammal", "beast", 1.0),
    (r"aquatic|mollusk|crustacean|shellfish|fish", "aqua", 1.0),
    (r"insect|parasite", "insect", 1.0),
    (r"plant", "plant", 1.0),
    (r"undead|ghost", "undead", 1.0),
    (r"mineral|ore|ice-snow|flame", "element", 1.0),
    (r"reptile|amphibian", "reptile", 1.0),
    (r"machine|cyborg|armor|weapon|enhancement|navigation|^mine$|holy sword", "machine", 1.0),
    (r"man$|knight|angel|seraph|warrior|oni|god|monk|magic|avatar|tath|ophan|dominion|principality|virtue|power|major|minor",
     "humanoid", 1.0),
]

LORE = {  # slug: metres, standing height as drawn next to people / other Digimon
    # Agumon line (CobbleEffort's own species, hand-built)
    "koromon": 0.3, "agumon": 1.0, "greymon": 6.0, "metalgreymon": 9.0, "blitzgreymon": 8.0,
    "omegamonalters": 4.0, "omegamonalterb": 4.5,
    # Adventure / 02
    "botamon": 0.2, "punimon": 0.2, "yuramon": 0.2, "pitchmon": 0.2, "bubbmon": 0.2, "poyomon": 0.2, "chicomon": 0.2,
    "leafmon": 0.2, "upamon": 0.3, "poromon": 0.3, "tokomon": 0.3, "tanemon": 0.3, "pukamon": 0.3, "tunomon": 0.3,
    "mochimon": 0.3, "nyaromon": 0.3, "pyocomon": 0.3, "minomon": 0.3, "chibimon": 0.4,
    "gabumon": 1.0, "patamon": 0.4, "tentomon": 0.6, "palmon": 1.0, "gomamon": 0.8, "piyomon": 0.9, "plotmon": 0.4,
    "vmon": 1.0, "wormmon": 0.5, "hawkmon": 0.6, "armadimon": 0.7,
    "garurumon": 2.5, "angemon": 2.2, "birdramon": 5.0, "kabuterimon": 5.0, "togemon": 3.0, "ikkakumon": 3.0,
    "tailmon": 0.5, "leomon": 2.3, "orgemon": 2.2, "devimon": 2.5, "meramon": 2.2, "monochromon": 4.0, "tyranomon": 6.0,
    "kuwagamon": 4.0, "unimon": 3.0, "centalmon": 2.5, "yukidarumon": 2.2,
    "mojyamon": 2.2, "numemon": 1.2, "scumon": 1.2, "gekomon": 1.3, "bakemon": 1.6, "cockatrimon": 3.5,
    "guardromon": 2.5, "xvmon": 2.3, "stingmon": 2.0, "aquilamon": 3.0, "ankylomon": 3.0, "wizarmon": 1.5,
    "elecmon": 0.8, "gottsumon": 1.0, "betamon": 0.6, "gizamon": 0.6, "floramon": 1.0, "mushmon": 0.8,
    "metalgreymonvirus": 9.0, "weregarurumon": 3.0, "holyangemon": 2.6, "angewomon": 2.2, "garudamon": 8.0,
    "atlurkabuterimonred": 9.0, "atlurkabuterimonblue": 9.0, "lilimon": 0.8, "zudomon": 4.5, "andromon": 2.6,
    "etemon": 1.8, "vamdemon": 2.4, "ladydevimon": 2.2, "skullgreymon": 10.0, "paildramon": 2.8, "silphymon": 2.2,
    "shakkoumon": 3.5, "dinobeemon": 2.4, "mamemon": 0.6, "bigmamemon": 1.2,
    "pumpmon": 1.8, "okuwamon": 7.0, "mummymon": 2.0, "archnemon": 2.0, "gesomon": 3.0,
    "monzaemon": 3.0, "warumonzaemon": 3.0, "triceramon": 6.0, "mammon": 6.0, "chimairamon": 15.0,
    "wargreymon": 3.0, "metalgarurumon": 3.5, "omegamon": 4.0, "seraphimon": 2.8, "ofanimon": 2.6, "rosemon": 2.0,
    "vikemon": 6.0, "heraklekabuterimon": 12.0, "hououmon": 8.0, "mugendramon": 30.0, "piemon": 2.0,
    "pinochimon": 1.3, "venomvamdemon": 50.0, "blackwargreymon": 3.0, "demon": 8.0,
    "imperialdramonfightermode": 10.0, "imperialdramonpaladinmode": 10.0,
    "valkyrimon": 2.2, "diablomon": 4.0, "armagemon": 50.0, "kuramon": 0.15, "tsumemon": 0.3, "keramon": 0.6,
    "infermon": 3.0, "apocalymon": 30.0, "millenniumon": 8.0, "moonmillenniumon": 15.0, "zeedmillenniumon": 50.0,
    # Tamers
    "guilmon": 1.2, "terriermon": 0.5, "renamon": 1.8, "impmon": 0.8, "lopmon": 0.5, "culumon": 0.4, "kudamon": 0.2,
    "growmon": 3.5, "galgomon": 1.8, "kyubimon": 2.2, "turuiemon": 1.8, "megalogrowmon": 6.0, "rapidmonperfect": 2.0,
    "taomon": 2.6, "andiramon": 2.5, "dukemon": 3.0, "dukemoncrimsonmode": 3.0, "saintgalgomon": 12.0,
    "sakuyamon": 2.3, "beelzebumon": 2.4, "beelzebumonblastmode": 2.6, "justimonaccelarm": 2.2, "justimonblitzarm": 2.2, "justimoncriticalarm": 2.2, "megidramon": 30.0,
    "cherubimonvirtue": 8.0, "cherubimonvice": 8.0,
    # Frontier
    "agnimon": 1.9, "vritramon": 3.0, "wolfmon": 1.9, "garummon": 2.5, "chackmon": 1.8, "blizzarmon": 3.0,
    "fairimon": 1.7, "shutumon": 2.5, "blitzmon": 1.9, "bolgmon": 3.2, "duskmon": 1.9, "velgrmon": 3.5,
    "grottomon": 1.8, "gigasmon": 3.0, "arbormon": 1.9, "petaldramon": 8.0, "ranamon": 1.7, "calamaramon": 4.0,
    "mercurymon": 2.0, "sephirothmon": 6.0, "lucemon": 1.4, "lucemonfalldownmode": 4.0, "susanoomon": 15.0,
    "kaisergreymon": 3.2, "magnagarurumon": 3.5,
    # Savers / Xros Wars / Appmon-era and the Seven Great Demon Lords, Royal Knights, Olympos XII
    "geogreymon": 7.0, "rizegreymon": 4.0, "shinegreymon": 10.0, "gaomon": 1.0, "gaogamon": 2.2,
    "machgaogamon": 2.6, "miragegaogamon": 3.0, "lalamon": 0.6, "sunflowmon": 1.8, "lilamon": 1.8, "lotusmon": 2.4,
    "falcomon": 0.8, "peckmon": 1.9, "yatagaramon": 2.6, "ravmon": 3.0, "shoutmon": 0.7, "ballistamon": 2.5,
    "belphemonsleepmode": 3.0, "belphemonragemode": 30.0, "barbamon": 2.0, "lilithmon": 2.0,
    "alphamon": 3.0, "gankoomon": 2.2, "jesmon": 2.5, "craniummon": 3.0, "magnamon": 2.2, "dynasmon": 3.0,
    "lordknightmon": 2.6, "sleipmon": 4.0, "ulforcevdramon": 2.5, "duftmon": 3.0,
    "valdurmon": 10.0,                                   # wikimon: six wings spanning 30 m (the only stated size)
    "goddramon": 15.0, "holydramon": 15.0, "griffomon": 8.0, "boltmon": 3.5, "titamon": 15.0,
    "ebemon": 1.5, "seadramon": 6.0, "metalseadramon": 10.0, "megaseadramon": 8.0, "airdramon": 6.0, "megadramon": 10.0,
    "gigadramon": 10.0,                                  # serpents/flying dragons built coiled or rearing: heights
    "examonxantibody": 3.5, "cyberdramon": 2.5,                              # the upright knight, not the dragon "lucemonsatanmode": 30.0, "lucemonlarva": 0.5, "ravmonburstmode": 3.2, "demonsuperultimate": 20.0,
}
LENGTH = {  # slug: metres nose to tail, for long bodies (whales, sea serpents, flying dragons): the height follows the model
    "whamon": 40.0, "leviamon": 60.0, "examon": 40.0, "plesiomon": 25.0, "gesomon": 6.0, "imperialdramondragonmode": 40.0,
}
# variants (X-Antibody, Black, G Erosion Mode...) stand as tall as the form they vary
VARIANT = re.compile(r"(xantibody|black|red|blue|violet|gerosionmode|zwartdefeat|zwart|burstmode|mercifulmode)$")


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def group_of(wtype):
    t = (wtype or "").lower().replace("ancient ", "").strip()
    t = re.sub(r"<!--.*?-->", "", t)
    for pat, g, k in TYPE_GROUP:
        if re.search(pat, t):
            return g, k
    return "generic", 1.0


GEO = HERE.parents[1] / "digital" / "common" / "src" / "main" / "resources" / "assets" / "cobbleeffort" / "bedrock" / "pokemon" / "models"


def proportions(sp):
    """(height, front-to-back length) of the built model in model units, or None."""
    fs = sorted(GEO.glob(f"*_{sp}/{sp}.geo.json"))
    if not fs:
        return None
    lo, hi = [1e9] * 3, [-1e9] * 3
    for b in json.loads(fs[0].read_text())["minecraft:geometry"][0]["bones"]:
        for c in b.get("cubes", []):
            for i in range(3):
                lo[i] = min(lo[i], c["origin"][i])
                hi[i] = max(hi[i], c["origin"][i] + c["size"][i])
    h = hi[1] - max(lo[1], 0)
    return (h, hi[2] - lo[2]) if h > 0 else None


def build():
    sys.path.insert(0, str(HERE))
    import roster
    facts = json.loads((HERE / "data" / "wikimon.json").read_text())
    sys.path.insert(0, str(HERE.parent / "newmons"))
    from digimon_gen import stage_of
    out, used = {}, set()
    for e in roster.ROSTER:
        sp = slug(e["name"])
        f = facts.get(e.get("wikimon", e["name"]), {})
        stage = stage_of(e, f)
        base = sp
        while base not in LORE and VARIANT.search(base) and VARIANT.sub("", base):
            base = VARIANT.sub("", base)
        hl = proportions(sp)
        if base in LENGTH:                               # a lore length -> the height that makes the model that long
            m = LENGTH[base] * (hl[0] / max(hl[0], hl[1]) if hl else 0.4)
            out[sp] = {"m": round(m, 2), "how": f"lore length {LENGTH[base]} m" + ("" if base == sp else f" ({base})")}
            used.add(base)
            continue
        if base in LORE:
            out[sp] = {"m": LORE[base], "how": "lore" if base == sp else f"lore ({base})"}
            used.add(base)
            continue
        wtype = (f.get("types") or [""])[0]
        g, k = group_of(wtype)
        if g in ("dragon", "dino") and hl and hl[1] < 0.75 * hl[0]:
            g, k = "humanoid", 1.3                       # an upright dragon-man (V-dramon, Slayerdramon), not a kaiju
        elif g == "machine" and hl and hl[1] < 0.6 * hl[0]:
            g, k = "humanoid", 1.15                      # a slim upright cyborg (Andromon-like), not a war machine
        m = GROUPS[g][LEVELS.index(stage)] * k
        if hl and hl[1] > 1.8 * hl[0]:                   # a long body: the group size is its bulk, not its height
            m *= 1.8 * hl[0] / hl[1]
        out[sp] = {"m": round(m, 2), "how": f"{g} {stage}" + (f" ({wtype})" if wtype else "")}
    for sp in ("koromon", "agumon", "greymon", "metalgreymon", "blitzgreymon", "omegamonalters", "omegamonalterb"):
        out[sp] = {"m": LORE[sp], "how": "lore"}
        used.add(sp)
    missing = sorted((set(LORE) | set(LENGTH)) - used)
    (HERE / "data" / "sizes.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    return out, missing


if __name__ == "__main__":
    out, missing = build()
    print(f"{len(out)} Digimon sized; {sum(v['how'] == 'lore' for v in out.values())} by lore")
    if missing:
        print("LORE names not in the roster:", ", ".join(missing))
