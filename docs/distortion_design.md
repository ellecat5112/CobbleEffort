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
| Battle engine | Cobblemon runs Showdown in GraalJS; Mega Showdown's scripts loader merges the add-on's `side`, `queue` and `actions` scripts (`data/<ns>/mega_showdown/showdown/scripts/`). `move N [target] distort` is parsed by `side.chooseMove` (once per battle per side); `queue.resolveAction` queues the distortion as its own action at Terastallization's priority (after switches, before moves); `actions.runDistort` does a permanent forme change to the "-Distorted" forme (inverted types; `detailschange` reaches Cobblemon, whose `FORME_CHANGE` event gives the Pokémon the `distorted` aspect until the battle ends), keeps the ability and swaps every move for its twin (PP kept); `runMove` swaps the move chosen that turn. Tested in Cobblemon's Showdown with Mega Showdown's patches (node). |
| Server validation | Cobblemon only accepts known gimmick ids (`VALID_GIMMICK_IDS`): a mixin on `MoveActionResponse.isValid` accepts `distort` when the move is otherwise valid and the trainer wears the band. |
| Battle button | Cobblemon's gimmick buttons come from a fixed enum; a client mixin adds a Distort button (own icon) to the move selection when the player wears the band and the Pokémon holds the crystal (Arceus: a plate) and has a distorted form; toggling it shows the twin moves (names, types) on the move tiles, and their responses carry `distort`. |
| Radial menu | Mega Showdown's entries come from Cobblemon's `POKEMON_INTERACTION_GUI_CREATION` event, so the add-on adds its own **Distort** entry (own icon) there, no mixin: shown when the player wears the band and the Pokémon holds the crystal (Arceus: a plate), or as **Revert Distortion** when it's distorted. It sends a packet (`DistortPacket`); the server checks again (party, band, item, not battling, one distorted Pokémon per party) and toggles the `distorted` flag feature (saved with the Pokémon), with reverse-portal particles. Taking the crystal away reverts it (`HELD_ITEM_POST`). A Pokémon distorted this way enters battle in its -Distorted forme; the Showdown scripts give it its twin moves at the start and count it as the side's distortion. |
| Distorted forms | `species_additions` forms "Distorted" (aspect `distorted`) per Pokémon, with inverted types. In battle the aspect is forced until the battle ends; out of battle the wheel toggles the `distorted` flag feature, which gives the same aspect. |
| Moves | (`tools/make_battle.py`, for every move the distortable Pokémon can learn) Each move maps to its inverted-type twin: an existing move that's an exact equivalent (same category, power, accuracy, effect), otherwise a new move made from the original with only its type changed and a name to match (Cross Chop → Psychic Chop). New moves are data (`data/<ns>/moves/*.js`, read by Cobblemon) with lang names. |
| Abilities | (`tools/make_battle.py`) An ability is type-bound when its Showdown code names the Pokémon's own type, or its type's weather. Its twin swaps those for the distorted type and that type's weather: an existing ability when it's an exact match (Blaze → Torrent), otherwise a new Cobblemon datapack ability (`data/<ns>/abilities/*.js`; Solar Power → Storm Power, the same in rain). Others stay. The engine swaps it when the Pokémon distorts (announced with `-ability`), or at the start for one distorted outside battle. |
| Look | Each distorted Pokémon gets inverted colours (every hue to its complement) and, where it fits, new parts (`tools/make_parts.py`): the Charmander line's flame tail becomes a mermaid tail (a model copy in the add-on's namespace with the flame planes emptied, a fluke on the tail tip and scales, painted in an added lower half of the texture; the flame layer dropped). Resolver variations (order 9100) with the `distorted` aspect, mirroring Cobblemon's and Mega Showdown's. |

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

## Second set: the Charmander line

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
