# CobbleEffort

A Cobblemon sidemod that adds **extra cosmetic forms** for existing Cobblemon models, in the spirit of
[CobblemonMoreCosmetics](https://modrinth.com/resourcepack/cobblemonmorecosmetics). It changes no models:
each form is a new texture applied through Cobblemon's own cosmetic-slot and aspect system.

**Collections so far:** #1 Backrooms (40 Pokémon) · #2 Thanksgiving (37 Pokémon).

**House rule: every cosmetic covers whole evolutionary lines.** If one stage gets a form, every pre-evolution,
evolution and branch of that Pokémon gets it too. The generator enforces this (see [Collection rules](#collection-rules)).

## Collection #1: Backrooms (Still Lifes)

18 evolutionary lines (**40 Pokémon**) re-imagined as **Still Lifes** from Kane Pixels' *Backrooms*. A Still Life is an imperfect
copy of something real that the Backrooms rebuilt from memory. Here that means:

* colour drained into a sallow **plaster / wet-clay** palette, lit by Level 0's mono-yellow fluorescent light
* **damp blotches**, clay grain and wobbly **seams** where the "pieces" were pressed together
* rows that **slipped sideways**, like a bad copy
* **matte painted-on eyes** with a second, misplaced set just below and a **smear** running down from them
* no glow: emissive layers (Magnezone, Sizzlipede, Centiskorch, Nymble, Lokix) are switched off

Shiny Pokémon get their own Still Life, built from the shiny texture so a faint trace of the shiny colour shows through.

![Original vs. Still Life](docs/backrooms_preview.png)

| Line | Pokémon |
|------|---------|
| Magnemite | Magnemite → Magneton → Magnezone |
| Omanyte | Omanyte → Omastar |
| Nincada | Nincada → Ninjask / Shedinja |
| Torkoal | Torkoal |
| Anorith | Anorith → Armaldo |
| Snorunt | Snorunt → Glalie / Froslass |
| Piplup | Piplup → Prinplup → Empoleon |
| Blitzle | Blitzle → Zebstrika |
| Shelmet | Shelmet → Accelgor |
| Fletchling | Fletchling → Fletchinder → Talonflame |
| Swirlix | Swirlix → Slurpuff |
| Amaura | Amaura → Aurorus |
| Xerneas | Xerneas |
| Silicobra | Silicobra → Sandaconda |
| Sizzlipede | Sizzlipede → Centiskorch |
| Impidimp | Impidimp → Morgrem → Grimmsnarl |
| Nymble | Nymble → Lokix |
| Maschiff | Maschiff → Mabosstiff |

The 18 lines were picked at random (`random.Random("kane-pixels-level-0").sample(...)`) and then expanded to
their full evolutionary families from Cobblemon's species data. Torkoal and Xerneas have no evolutions.

### How to get one

**Cosmetic slot (survival):** give a supported Pokémon one **Yellow Carpet** (Level 0's damp carpet) as its
*cosmetic item*, the same way you would put any Cobblemon cosmetic on it (open your Pokémon's interaction
menu while holding the carpet and choose the cosmetic slot). Take the carpet back to undo it.

**Commands (testing / servers):** the form is also a species feature, so it works anywhere Pokémon properties do:

```
/pokegive magnemite backrooms
/pokegive glalie backrooms shiny
/spawnpokemon slurpuff backrooms
```

**Pack makers:** the accepted items come from the item tag `#cobbleeffort:backrooms_cosmetics`. Add items to it
with a datapack (`data/cobbleeffort/tags/item/backrooms_cosmetics.json`).

## Collection #2: Thanksgiving (Harvest)

18 more evolutionary lines (**37 Pokémon**) dressed for a Thanksgiving table:

* colours moved onto a **harvest palette** that keeps the original markings readable: deep reds become cranberry,
  pinks peach, oranges pumpkin, yellows maize gold, greens sage, blues and cyans chestnut and toasted squash,
  purples plum
* greys, whites and blacks turned into warm neutrals: **pie-crust cream, cinnamon, dark roast**
* a golden-brown **roast glaze** along the edges of each painted area
* a few **fallen maple leaves** (pumpkin, amber, gold) stuck to the fur
* **eyes keep their original colours**, so every Pokémon still looks like itself
* **shiny → golden harvest**: everything pulled toward honey-gold
* glowing parts keep glowing, recoloured like candlelight

![Original vs. Harvest](docs/thanksgiving_preview.png)

| Line | Pokémon |
|------|---------|
| Squirtle | Squirtle → Wartortle → Blastoise |
| Meowth | Meowth (incl. Alolan & Galarian) → Persian / Perrserker |
| Porygon | Porygon → Porygon2 → Porygon-Z |
| Corsola | Corsola (incl. Galarian) → Cursola |
| Miltank | Miltank |
| Kecleon | Kecleon |
| Bagon | Bagon → Shelgon → Salamence |
| Croagunk | Croagunk → Toxicroak |
| Carnivine | Carnivine |
| Munna | Munna → Musharna |
| Tirtouga | Tirtouga → Carracosta |
| Ferroseed | Ferroseed → Ferrothorn |
| Mienfoo | Mienfoo → Mienshao |
| Grubbin | Grubbin → Charjabug → Vikavolt |
| Bounsweet | Bounsweet → Steenee → Tsareena |
| Pyukumuku | Pyukumuku |
| Squawkabilly | Squawkabilly (all four plumages) |
| Wiglett | Wiglett → Wugtrio |

Picked with `generate.py pick --count 18 --seed thanksgiving-2026`: 18 random lines out of the 417 that are fully
modelled in Cobblemon and not already in another collection.

### How to get one

Give a supported Pokémon one **Pumpkin Pie** as its cosmetic item. With commands: `/pokegive miltank thanksgiving`,
`/pokegive squirtle thanksgiving shiny`. Pack makers can extend the item tag `#cobbleeffort:thanksgiving_cosmetics`.

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

### Regenerating / adding collections

Each collection is a config in `tools/collections/<name>.json` (aspect, cosmetic item, `lines`) plus a texture
style in `tools/styles/<style>.py`. Everything under `assets/cobbleeffort` and `data/cobbleeffort` is generated:

```
pip install pillow
git clone --depth 1 --branch 1.8.4 https://gitlab.com/cable-mc/cobblemon.git
python3 tools/generate.py --cobblemon cobblemon/common/src/main/resources build              # every collection
python3 tools/generate.py --cobblemon cobblemon/common/src/main/resources build thanksgiving # just one
python3 tools/generate.py --cobblemon cobblemon/common/src/main/resources pick --count 18 --seed <text>
```

`pick` randomly chooses new evolutionary lines that are fully modelled and not used by any collection yet. Put
its first column into a new config's `lines`. Each species has a fixed seed per collection, so reruns give
byte-identical output, and each collection's generated folders are wiped and rebuilt on every run.
`tools/preview/` renders original vs. retextured models in headless Chromium (three.js) for a quick look.

### Collection rules

These hold for every collection, now and in future:

1. **Whole evolutionary lines only.** Configs list lines, never single stages. The generator works out each family
   (pre-evolutions, evolutions, branches, forms' evolution links) from Cobblemon's `data/cobblemon/species`, and
   **stops with an error** if any member of a line has no Cobblemon model to retexture. Evolutions Cobblemon's data
   doesn't link can be joined with `extra_links`.
2. **Every vanilla variation is mirrored.** For each species, every variation in Cobblemon's resolver
   (shiny, gender, regional forms, model swaps, animated textures, extra layers) is copied with the cosmetic aspect
   added and its textures retextured. So the form keeps working through evolution, gender, regional and shiny changes.
3. **No overlap.** A species belongs to at most one collection, and each collection has its own cosmetic item.
   The generator refuses to build otherwise.
4. **Releases are zips.** `./gradlew build` puts the jar inside `build/libs/<name>.zip`.

## How it works (for future collections)

Per collection (`<aspect>` = `backrooms`, `thanksgiving`, …):

| File | Purpose |
|------|---------|
| `data/cobbleeffort/cosmetic_items/<aspect>.json` | the collection's item in the cosmetic slot → aspect `<aspect>` |
| `data/cobbleeffort/species_features/<feature>.json` | flag feature (for `/pokegive … <aspect>`) |
| `data/cobbleeffort/species_feature_assignments/<feature>.json` | which species get the flag |
| `data/cobbleeffort/tags/item/<aspect>_cosmetics.json` | items accepted for the cosmetic |
| `assets/cobbleeffort/bedrock/pokemon/resolvers/<aspect>/<species>/9000_*.json` | `order: 9000` copies of every vanilla variation with the aspect added |
| `assets/cobbleeffort/textures/pokemon/<aspect>/<species>/` | the retextured textures |

Cobblemon merges every resolver file for a species, sorted by `order`, and the **last** matching variation wins.
So the high order, combined with mirroring the vanilla variations in order, puts the right texture on top in every
combination (base, shiny, female, regional…) without touching Cobblemon's files.

## Credits & licence

See [CREDITS.md](CREDITS.md). In short: the code and data are MPL-2.0. The textures are **modified Cobblemon
assets** (CC BY-NC 3.0 where Cobblemon marks them so), so this mod is **non-commercial**. Pokémon belongs to
Nintendo / Game Freak / The Pokémon Company. *The Backrooms* Still Life concept belongs to Kane Parsons (Kane Pixels).
This project is not affiliated with any of them.
