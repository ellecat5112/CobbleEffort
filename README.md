# CobbleEffort

A Cobblemon sidemod that adds **extra cosmetic forms** for existing Cobblemon models, in the spirit of
[CobblemonMoreCosmetics](https://modrinth.com/resourcepack/cobblemonmorecosmetics). It changes no models:
each form is a new texture applied through Cobblemon's own cosmetic-slot and aspect system.

## Collection #1: Backrooms (Still Lifes)

18 Pokémon re-imagined as **Still Lifes** from Kane Pixels' *Backrooms*. A Still Life is an imperfect
copy of something real that the Backrooms rebuilt from memory. Here that means:

* colour drained into a sallow **plaster / wet-clay** palette, lit by Level 0's mono-yellow fluorescent light
* **damp blotches**, clay grain and wobbly **seams** where the "pieces" were pressed together
* rows that **slipped sideways**, like a bad copy
* **matte painted-on eyes** with a second, misplaced set just below and a **smear** running down from them
* no glow: emissive layers (Sizzlipede, Lokix) are switched off

Shiny Pokémon get their own Still Life, built from the shiny texture so a faint trace of the shiny colour shows through.

![Original vs. Still Life](docs/backrooms_preview.png)

| # | Pokémon | # | Pokémon | # | Pokémon |
|---|---------|---|---------|---|---------|
| 0082 | Magneton | 0394 | Prinplup | 0716 | Xerneas |
| 0138 | Omanyte | 0522 | Blitzle | 0844 | Sandaconda |
| 0292 | Shedinja | 0617 | Accelgor | 0850 | Sizzlipede |
| 0324 | Torkoal | 0662 | Fletchinder | 0861 | Grimmsnarl |
| 0348 | Armaldo | 0685 | Slurpuff | 0920 | Lokix |
| 0362 | Glalie | 0699 | Aurorus | 0943 | Mabosstiff |

The 18 were picked at random (`random.Random("kane-pixels-level-0").sample(...)`) from the 683 Cobblemon
species whose model never changes with aspects (no regional, gender or form model swaps). Because of that,
the Still Life texture always fits the model's UVs.

### How to get one

**Cosmetic slot (survival):** give a supported Pokémon one **Yellow Carpet** (Level 0's damp carpet) as its
*cosmetic item*, the same way you would put any Cobblemon cosmetic on it (open your Pokémon's interaction
menu while holding the carpet and choose the cosmetic slot). Take the carpet back to undo it.

**Commands (testing / servers):** the form is also a species feature, so it works anywhere Pokémon properties do:

```
/pokegive magneton backrooms
/pokegive glalie backrooms shiny
/spawnpokemon slurpuff backrooms
```

**Pack makers:** the accepted items come from the item tag `#cobbleeffort:backrooms_cosmetics`. Add items to it
with a datapack (`data/cobbleeffort/tags/item/backrooms_cosmetics.json`).

## Requirements & versions

| | |
|---|---|
| Loader | Fabric **or** NeoForge. It's a single jar with no code, so it works on both |
| Cobblemon | 1.7.0+ (built against **1.8.4**) |
| Minecraft | **1.21.1** (whatever version Cobblemon supports) |

> **About "Minecraft 1.26.1":** Minecraft moved to year-based version numbers in 2026 (26.1, 26.2, 26.3 …),
> and Cobblemon (latest 1.8.4) still only supports **1.21.1**. There is no Cobblemon build for the 26.x line yet,
> so this release targets 1.21.1. The mod is pure data, and its metadata only asks for "Minecraft ≥ 1.21.1 +
> Cobblemon ≥ 1.7.0". When Cobblemon ships for 26.x, the same content should load. At most it may need its
> metadata and `pack.mcmeta` bumped.

## Building

```
./gradlew build        # -> build/libs/cobbleeffort-<version>+1.21.1.zip  (contains the .jar; also runs validateData)
```

`validateData` checks that every JSON file parses and every texture a resolver points to exists.

### Regenerating / adding species

The textures, resolvers and data files are all generated from `tools/backrooms_species.json`:

```
pip install pillow
git clone --depth 1 --branch 1.8.4 https://gitlab.com/cable-mc/cobblemon.git
python3 tools/generate_backrooms.py --cobblemon cobblemon/common/src/main/resources
```

Add an entry (`folder` = Cobblemon's texture folder, e.g. `0025_pikachu`) and rerun. Pick species whose
resolver uses a single model. Each species has its own fixed seed, so reruns give byte-identical output.
`tools/preview/` renders original vs. Still Life models in headless Chromium (three.js) for a quick look.

## How it works (for future collections)

| File | Purpose |
|------|---------|
| `data/cobbleeffort/cosmetic_items/backrooms.json` | Yellow Carpet in the cosmetic slot → aspect `backrooms` |
| `data/cobbleeffort/species_features/backrooms_still_life.json` | flag feature `backrooms` (for `/pokegive … backrooms`) |
| `data/cobbleeffort/species_feature_assignments/backrooms_still_life.json` | which species get the flag |
| `data/cobbleeffort/tags/item/backrooms_cosmetics.json` | items accepted for the cosmetic |
| `assets/cobbleeffort/bedrock/pokemon/resolvers/<species>/9000_*_backrooms.json` | `order: 9000` variation that swaps the texture when the aspect is present |
| `assets/cobbleeffort/textures/pokemon/backrooms/<species>/` | the Still Life textures |

Cobblemon merges every resolver file for a species, sorted by `order`, and the **last** matching variation wins.
So the high order puts the Still Life texture on top of the base and shiny textures without touching Cobblemon's files.

## Credits & licence

See [CREDITS.md](CREDITS.md). In short: the code and data are MPL-2.0. The textures are **modified Cobblemon
assets** (CC BY-NC 3.0 where Cobblemon marks them so), so this mod is **non-commercial**. Pokémon belongs to
Nintendo / Game Freak / The Pokémon Company. *The Backrooms* Still Life concept belongs to Kane Parsons (Kane Pixels).
This project is not affiliated with any of them.
