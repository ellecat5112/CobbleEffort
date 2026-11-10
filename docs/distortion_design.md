# Distortion (typing inversion): design

A new battle gimmick, separate from Mega Evolution, Z-Moves, Dynamax and Terastallization. The Pokémon holds the
**Distortion Crystal** (one crystal for every Pokémon); the trainer wears a **Distortion Band** in its own accessory slot. In battle the
Pokémon **distorts**: its types turn into their weaknesses, its ability and moves follow, and its colours invert.
It also gets its own entry in the interaction wheel (the radial menu, next to Mega Showdown's).

Built for Cobblemon 1.8.4, Mega Showdown 1.3.3 and Accessories 1.1.0-beta.54 on Minecraft 1.21.1.

## Ships as an add-on: "CobbleEffort: Distortion"

A separate jar that needs CobbleEffort, Cobblemon, Mega Showdown and Accessories. Unlike CobbleEffort (data and
assets, one loader-independent jar), this is a real code mod: it hooks into Cobblemon's battle screen and server-side
move validation, Cobblemon's interaction wheel and the Showdown battle engine, so it's built per loader (Fabric
and NeoForge) against those mods. A bug in it can't break the cosmetics. Each Cobblemon or Mega Showdown update may
need it updated.

## How the parts work

| Part | How |
|---|---|
| Distortion Band | A registered item, worn in a new **distortion** accessory slot. Accessories reads slot definitions and slot tags from data (`data/<ns>/accessories/slot/distortion.json`, `#accessories:distortion_slot`); rendered on the wrist like Mega Showdown's bracelets. |
| Distortion Crystal | One registered item for every Pokémon (Arceus distorts with its plate instead, since it can only hold one item). Its Showdown item is Mega Showdown held-item data (`data/<ns>/mega_showdown/showdown/held_items/distortioncrystal.js`, can't be knocked off); a Cobblemon `HeldItemProvider` maps the item to it. |
| Battle engine | Cobblemon runs Showdown in GraalJS; Mega Showdown's scripts loader merges the add-on's `side`, `queue`, `pokemon` and `actions` scripts (`data/<ns>/mega_showdown/showdown/scripts/`, written by `tools/make_battle.py`). `move N [target] distort` is parsed by `side.chooseMove` (a Pokémon that can't toggle just uses the move); `queue.resolveAction` queues the toggle as its own action at Terastallization's priority (after switches, before moves); `actions.setDistorted` turns the types into their weaknesses (the species stays real; `pokemon.setSpecies` re-inverts after form changes), swaps the ability for its twin if type-bound and every move for its twin (PP kept), or back; `runMove` swaps the move chosen that turn. Tested in Cobblemon's Showdown with Mega Showdown's patches (node). |
| Toggle and stacking (0.6.0) | Distorting is a free toggle: "move N distort" distorts, or reverts a distorted Pokémon, any turn. A distorted Pokémon keeps its real species in the engine (a `pokemon` script re-inverts its types after any species change), so every form change that doesn't need another held item works and stays distorted: Dynamax/Gigantamax, Battle Bond's Ash-Greninja, move megas (Dragon Ascent), ability forms. The client hears `-formechange` to "<species>-Distorted" / "<species>-Reverted" (FORME_CHANGE "distorted" / "reverted": the aspect on / off). Forms needing a held item (stone megas, primals) get no distorted copy; Gmax and Ash do. |
| Server validation | Cobblemon only accepts known gimmick ids (`VALID_GIMMICK_IDS`): a mixin on `MoveActionResponse.isValid` accepts `distort` when the move is otherwise valid and the trainer wears the band. |
| Battle button | Cobblemon's gimmick buttons come from a fixed enum; a client mixin adds a Distort button (own icon) to the move selection when the player wears the band and the Pokémon holds the crystal (Arceus: a plate) and has a distorted form; toggling it shows the twin moves (names, types) on the move tiles, and their responses carry `distort`. |
| Radial menu | Mega Showdown's entries come from Cobblemon's `POKEMON_INTERACTION_GUI_CREATION` event, so the add-on adds its own **Distort** entry (own icon) there, no mixin: shown when the player wears the band and the Pokémon holds the crystal (Arceus: a plate), or as **Revert Distortion** when it's distorted. It sends a packet (`DistortPacket`); the server checks again (party, band, item, not battling, one distorted Pokémon per party) and toggles the `distorted` flag feature (saved with the Pokémon), with reverse-portal particles. Taking the crystal away reverts it (`HELD_ITEM_POST`). A Pokémon distorted this way enters battle in its -Distorted forme; the Showdown scripts give it its twin moves at the start and count it as the side's distortion. |
| Distorted forms | `species_additions` forms "Distorted" (aspect `distorted`) per Pokémon, with inverted types. In battle the aspect is forced until the battle ends; out of battle the wheel toggles the `distorted` flag feature, which gives the same aspect. |
| Moves | (`tools/make_battle.py`, for every move the distortable Pokémon can learn) Each move maps to its inverted-type twin: an existing move that's an exact equivalent (same category, power, accuracy, effect), otherwise a new move made from the original with only its type changed and a name to match (Cross Chop → Psychic Chop). New moves are data (`data/<ns>/moves/*.js`, read by Cobblemon) with lang names. |
| Abilities | (`tools/make_battle.py`) An ability is type-bound when its Showdown code names the Pokémon's own type, or its type's weather. Its twin swaps those for the distorted type and that type's weather: an existing ability when it's an exact match (Blaze → Torrent), otherwise a new Cobblemon datapack ability (`data/<ns>/abilities/*.js`; Solar Power → Storm Power, the same in rain). Others stay. The engine swaps it when the Pokémon distorts (announced with `-ability`), or at the start for one distorted outside battle. |
| Look | Each distorted Pokémon gets inverted colours (every hue to its complement) and, where it fits, new parts (`tools/parts/`, the part kit): e.g. the Charmander line's flame tail becomes a mermaid tail (a model copy in the add-on's namespace with the flame planes emptied, a fluke on the tail tip and scales, painted in an added part of the texture; the flame layer dropped). Resolver variations (order 9100) with the `distorted` aspect, mirroring Cobblemon's and Mega Showdown's. |

## Type chart: each type becomes its weakness

| Type | Becomes | | Type | Becomes |
|---|---|---|---|---|
| Normal | Fighting | | Flying | Electric |
| Fire | Water | | Psychic | Dark |
| Water | Grass | | Bug | Flying |
| Grass | Fire | | Rock | Fighting |
| Electric | Ground | | Ghost | Dark |
| Ice | Fire | | Dragon | Fairy |
| Fighting | Psychic | | Dark | Fairy |
| Poison | Ground | | Steel | Ground |
| Ground | Water | | Fairy | Steel |

## First set: the Distortion World's champion and the creation trio

| Pokémon | Types | Distorted | Notes |
|---|---|---|---|
| Giratina (Altered, Origin) | Ghost / Dragon | Dark / Fairy | Pressure / Levitate stay (not type-bound). Shadow Force → a Dark twin; Dragon moves → Fairy twins. |
| Dialga (and Origin) | Steel / Dragon | Ground / Fairy | Roar of Time → a Fairy twin. |
| Palkia (and Origin) | Water / Dragon | Grass / Fairy | Spacial Rend → a Fairy twin. |
| Arceus (all 18 plate types) | its type | its type's weakness | Distorts with its plate (no crystal). Judgment → Inverse Judgment (the weakness of the plate's type). |

## Gen 1 legendary and mythical Pokémon

Articuno, Zapdos and Moltres (and their Galarian forms) follow the chart. Mew and Mewtwo are specialised distortions
by the user's design (`TYPE_OVERRIDES` in make_assets.py, `CHART_OVERRIDES` in make_battle.py, per-species twin
tables in the engine and `move_twins.json`): both Normal/Fighting; Mew's Psychic moves turn Normal, Mewtwo's Fighting.
Mew: the unborn, in a translucent veined orb (the placenta, a pulsing translucent layer) with its tail turned to the
front as the umbilical cord. Mewtwo: the bodybuilder, Conkeldurr's arm geometry (from Cobblemon's model) fitted to its
joints in translucent pink, bulked chest and thighs. Mega Mewtwo needs a Mega Stone, so it doesn't distort.

## Gen 2 legendary and mythical Pokémon

By the chart, with themed looks: Raikou a sandstorm (Ground), Entei a lionfish (Water: striped spines, pearl crest),
Suicune a weeping willow (Grass: vine ribbons, wisteria mane), Lugia a storm at night (Dark/Electric: RECOLOUR
"negative", electric plates), Ho-Oh an aurora (Water/Electric: GLOW_DST), Celebi an ember sprite (Dark/Fire). Raikou,
Entei and Suicune are Mega Showdown's models. Celebi is modelled only by AllTheMons x Mega Showdown (no derivatives):
an ADDON module paints an original texture on its UV layout (`parts/layouts/atm_celebi_layout.json`, from
`tools/addons/extract_layout.py`, no art read), set by texture alone so the resolver names no model.

## The DNA machine (0.11.0)

The user's design: a way to get Mewtwo. `dna/DnaMachineBlock` (two halves like a door, facing the placer; the
lower holds `DnaMachineBlockEntity`): click with Mew DNA to fill it (16; sneak pours the stack), then with Mew
selected in the party bar (the client sends `DnaInsertPacket` with the selected Pokémon, since the selection is
client-side) Mew goes in (saved as NBT with its owner and start time); after 5 minutes (server ticker, by game time)
it becomes Mewtwo (same level, shininess); clicking gives it to the owner (party, else PC). Unbreakable while
occupied. `dna/MewDna`: on BATTLE_FAINTED, each player on the other side with a Mew in their party gets 3-8 Mew DNA,
dropped at the defeated Pokémon (or given). Client: `DnaMachineRenderer` draws the glowing fluid (rising with the
fill) and the Pokémon inside as a client-only display PokemonEntity (as Cobblemon's habitat block does); glass is
translucent (`render_type` in the model for NeoForge, RenderTypeRegistry for Fabric). Assets and data (textures,
models, blockstates, loot, recipe, pickaxe tag, names): `tools/make_dna_machine.py` (run by make_assets.py).

## The crystal distorts by itself (0.10.0)

The user's direction: holding the Distortion Crystal IS the distortion outside battle. `DistortionWheel.sync` on
Cobblemon's HELD_ITEM_POST (and POKEMON_SENT_POST, for a crystal given another way): a distortable Pokémon given the
crystal gets the `distorted` flag feature (form + look) at once, no band needed; taking it (and, for Arceus, its plate)
away clears it. Since 0.10.1 that also swaps its stored moves and ability for their twins (`DistortionTwins`, from
`distortion/move_twins.json` + `ability_twins.json`, originals kept in the Pokémon's persistent data and put back on
revert; a move learned meanwhile stays); the engine recognises a pre-swapped Pokémon at battle start (`preswapped`:
a move with no twin of its own that is some move's twin, or such an ability) and only records the pairs. An in-battle
revert undoes it, and after the battle a Pokémon still holding the crystal distorts again. It enters battle distorted (as before for a wheel distortion); the band still gates the in-battle
toggle and the wheel.

## Every Gen 1 Pokémon (0.9.0)

The other 70 Gen 1 lines, whole (later-generation members too: Pichu, Crobat, Eevee's evolutions...; 174 species),
by the chart, with looks themed on each Pokémon's (and each regional / Gigantamax form's) NEW types:
`tools/parts/gen1.py` (lines in `gen1_lines.json`) on `tools/parts/_themes.py`, one motif per new type placed by
bone names (head, torso/body, tail tip, wings, arms, legs, ears; on the back face when the head sits on the body):
Fighting a brawler (bulk + headband with ribbons), Water sea life (back fin, tail fluke, flames to sea life), Grass
overgrowth (leaves, fern fronds, moss), Fire flames, Ground a cluster of jagged rocks + sandstone, Psychic a forehead
gem + halo, Electric lightning through wings/tail (bolts otherwise), Dark shadow wisps, Flying feathered wings, Fairy
a petal crown, Steel riveted plates. The first new type gets the full motif, the second an accent; the main colour
moves to the new primary type's (a Normal type's most saturated colour). `make_assets.types_for` gives each model's
form types (Alolan Vulpix: Ice -> Fire). Ability twins now depend on the holder's types (`distortAbilities[ability]
[types]`): Thick Fat is Blubber on Fire types, Insulation on Ice types; ordinary weathers never turn primal (Snow
Warning's twin sets sun, not Desolate Land).

## Second set: every starter line (Gen 1-9)

Water starters distort into plant-inspired forms, grass starters into natural disasters, fire starters into sea life
(the per-line looks are in the add-on's README and `distortion/tools/parts/<first stage>.py`). Built with the part kit
(`tools/parts/_kit.py`, `_materials.py`): model copies with hidden, reskinned and added parts (boxes, planes, crossed
planes), UVs in an added lower part of the texture, materials (animated emissive flames, charred and lava rock,
prototaxite bands, cut-out leaves, petals, flytraps, fins, coral/anemone/jellyfish ramps, sea-life conversion of
emissive flame layers), and a type-hue recolour (the old type's colour moved to the new type's, other colours kept).

### The Charmander line (first)

| Pokémon | Types | Distorted | Notes |
|---|---|---|---|
| Charmander, Charmeleon | Fire | Water | Blaze → Torrent, Solar Power → Storm Power; the flame tail becomes a mermaid tail. |
| Charizard | Fire / Flying | Water / Electric | As above; Mega X/Y and Gigantamax don't distort. |

## Phases

1. Add-on project (Fabric + NeoForge), the band, the crystals, the accessory slot, the distorted forms and their
   looks for the first set. Testable in-game: items, slot, forms via command.
2. The battle gimmick: engine patch, server validation, battle button, inverted moves (abilities: later, when a
   Pokémon with a type-bound one joins). One crystal for every Pokémon (changed from one per type).
3. The radial-menu entry (done in 0.3.0).
4. Ability twins, the Charmander line with its mermaid tail, wild and NPC Pokémon distorting (0.4.0): an AI actor's
   first move gets `distort` when its Pokémon can (`AIDistortMixin` on `BattleActor.setActionResponses`); the side
   script turns a distort that isn't allowed into the plain move, so an AI's choice never fails.

Each phase needs an in-game test round (crash logs or screenshots back), since none of this can be run here.
