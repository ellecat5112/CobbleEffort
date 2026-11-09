# Credits & licensing

## Cobblemon assets (modified)

Every texture under `src/main/resources/assets/cobbleeffort/textures/pokemon/` (except the `compat/` folders
described further down, and the Xurkitree addon textures, which are original) is an **adaptation** of a texture
from [Cobblemon](https://gitlab.com/cable-mc/cobblemon) (tag `1.8.4`, `common/src/main/resources/assets/cobblemon/textures/pokemon/`),
made by the Cobblemon team and contributors.

**Changes made:** `tools/generate.py` transforms the originals with one style per collection:

* **Backrooms** (`tools/styles/backrooms.py`, textures under `.../pokemon/backrooms/`): colours remapped to a
  plaster/clay palette; stain, grain, seam and row-shift effects added; eyes repainted, duplicated and smeared,
  located with Cobblemon's `*_alpha.png` eye masks.
* **Thanksgiving** (`tools/styles/thanksgiving.py`, textures under `.../pokemon/thanksgiving/`): colours remapped to
  an autumn harvest palette; edge "glaze" darkening and small maple-leaf stamps added; eyes left as in the original.
* **Halloween** (`tools/styles/halloween.py`, `halloween_skeleton.py`, `_horror.py`; textures under
  `.../pokemon/halloween/`): colours darkened and mottled; wounds, stitches, lumps, blood splatters and drips,
  extra eyes and toothed mouths painted on and animated across 4 frames; the Charmander line repainted as bone,
  ribs and rotting flesh, with its flame layer recoloured pink.
* **Christmas** (`tools/styles/christmas*.py`, `_festive.py`; textures under `.../pokemon/christmas/`): colours
  remapped to a Christmas palette; snow, snowflakes and light garlands added, with an extra emissive layer of
  twinkling bulbs; the Snorlax, Turtwig, Trubbish and Phantump lines repainted as Santa Claus, Christmas trees,
  wrapped gifts and Krampus.
* **Easter** (`tools/styles/easter*.py`, `_spring.py`; textures under `.../pokemon/easter/`): colours turned
  pastel (or chocolate for shinies); painted-egg bands, zigzag ribbons, daisies and sprinkles added; the Togepi
  line repainted as Easter eggs (golden Fabergé for shinies) and the Lopunny line as the Easter Bunny (a chocolate
  bunny for shinies).
* **Five Nights at Freddy's** (`tools/styles/fnaf_*.py`, `_animatronic.py`; textures under `.../pokemon/animatronic/`):
  colours remapped per look (classic, withered, toy, springtrap, nightmare, funtime, scrap); felt, seams, rivets,
  grime, endoskeleton tears, teeth and glowing eyes added; the Teddiursa, Torchic and Sandile lines repainted after
  Freddy, Chica and Foxy.
* **Ice Sculptures** (`tools/styles/ice_sculpture.py`; textures under `.../pokemon/ice_sculpture/`): colours remapped
  to an ice palette by lightness; facets, refraction streaks, cracks, bubbles and a frosted rim added; eyes darkened;
  an extra emissive layer of twinkling glints; shinies tinted teal-to-violet.
* **Stone Statues** (`tools/styles/stone_statue.py`; textures under `.../pokemon/stone_statue/`): colours remapped to
  stone by lightness; grain, speckles, chisel strokes, weathered edges, cracks, moss and lichen added; shinies remapped
  to veined white marble with gilded eyes.
* **Naruto** (`tools/styles/naruto_*.py`, `_shinobi.py`; textures under `.../pokemon/shinobi/`): colours remapped per
  look; clouds, flak vests, forehead protectors, masks, sage pigment, flame hems, whiskers, swirls, veins, Karma
  seals and glowing eyes added; the Vulpix line repainted as Kurama with a flickering chakra layer.
* **Trans Pride** (`tools/styles/trans_pride.py`; textures under `.../pokemon/trans_pride/`): recoloured into the
  transgender pride flag's five stripes by height on the model, keeping the original's shading, outlines and eyes;
  shinies get pastel glitter and an extra emissive layer of twinkling sparkles.

Cobblemon ships many of its Pokémon models and textures under the **Creative Commons
Attribution-NonCommercial 3.0** licence (see the `license` files next to the models in Cobblemon's repository,
e.g. `assets/cobblemon/bedrock/pokemon/models/0082_magneton/license`):
<https://creativecommons.org/licenses/by-nc/3.0/>.
The adapted textures are shared under those same terms. **No commercial use.**

The `docs/*_preview.png` images show Cobblemon models rendered with both the original and the adapted
textures, and are covered by the same terms. `docs/compat_forms_preview.png` also shows Mega Showdown's models and
textures (CC BY-NC-SA 4.0) and the painted Baby Legends members (no Baby Legends texture is shown).

## Mega Showdown assets (modified): CC BY-NC-SA 4.0

Textures under `src/main/resources/assets/cobbleeffort/textures/pokemon/<aspect>/compat/mega_showdown/` are
**adaptations** of textures from [Mega Showdown](https://github.com/yajatkaul/CobblemonMegaShowdown) by yajatkaul and
contributors (version 1.3.3 for Cobblemon 1.8.4 / Minecraft 1.21.1). These are its mega, Gigantamax, Eternamax and
mode forms, plus the Cobblemon textures it replaces. They were changed by the same collection styles as above.
Mega Showdown's assets are licensed under the
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0** licence
(<https://creativecommons.org/licenses/by-nc-sa/4.0/>), and these adapted textures are shared under that same
licence. **No commercial use.**

## Mega Showdown: Extra Megas assets (modified)

Textures under `.../<aspect>/compat/msdextramegas/` are adaptations of textures from **MSD Extra Megas**
(<https://modrinth.com/mod/msd-extra-megas>), released under the Unlicense. Changed by the collection styles as above.

## Vendored Cobblemon models, posers and animations

**Cobblemon: AllTheMons x Mega Showdown** replaces some of Cobblemon's models, posers and animations with its own.
The cosmetic textures are painted for Cobblemon's models, so unmodified copies of Cobblemon's files for those
Pokémon are included under `src/main/resources/assets/cobbleeffort/bedrock/pokemon/{models,posers,animations}/<aspect>/`.
Animation groups are renamed `ce_<name>` because Cobblemon keys animation groups by file name. Some posers are JSON
conversions of Cobblemon's Kotlin posers (`tools/kotlin_poser.py`). These copies are covered by Cobblemon's terms:
CC BY-NC 3.0 for the models and animations, MPL-2.0 for the code the posers were converted from.

A few **Mega Showdown** models, posers and animations (Mega Absol / Mega Absol Z, Gmax Garbodor, Gmax Coalossal,
Bloodmoon Ursaluna, Xerneas' neutral mode) are copied, unmodified apart from renamed animation groups, into the same
folders. A resolver may only name models that always exist, so these copies ensure CobbleEffort never depends on
another mod being installed. They remain under Mega Showdown's **CC BY-NC-SA 4.0** licence, credited to yajatkaul
and contributors.

## Other mods (referenced, never copied)

* **Xurkitree as Sasuke** is made for the Xurkitree model shipped by **Cobblemon: AllTheMons x Mega Showdown**
  (<https://github.com/Lvnatic-T/AllTheMons-x-Mega-Showdown>) and by **Cobblemon Ultra-Beasts** by BileulDevs
  (<https://github.com/BileulDevs/cobblemon-ultra-beasts>). Neither model nor any of their textures is included in
  CobbleEffort. Only the UV layouts (cube positions, no art) are stored in `tools/addons/atm_xurkitree_layout.json` and
  `tools/addons/ultrabeasts_xurkitree_layout.json`, so an original texture can be painted to fit either.
* **Cobblemon Baby Legends** (All Rights Reserved): the cosmetic textures for **Xerfawn** and **Latot** are painted
  from scratch (`tools/painter.py`) onto the UV layout of that mod's models, in colours taken from Cobblemon's Xerneas,
  Latios and Latias textures (so they are Cobblemon adaptations, CC BY-NC 3.0). No Baby Legends texture is read or
  included.
* **Cobblemon: AllTheMons x Mega Showdown** (ALLTHEMONS LICENSE v3.2), **Cobblemon Lost Lore** (Lvnatic's General
  License 1.3), **Fully Hisuian Starters** by its author and **Poke Costumes** by RedRibbon (no licence stated): their
  forms are only referenced by id in "passthrough" resolver entries, so they show unchanged under a cosmetic. None of
  their files is included or modified.
* **Legendary Monuments** by JorgaoMC (All Rights Reserved) is read only to confirm it doesn't touch Pokémon visuals.
* The generator reads these mods' jars locally at build time (`tools/compat/`, gitignored). They are never committed.

## New Pokémon models

* **Iron Boulder** (`assets/cobbleeffort/bedrock/pokemon/models/1022_ironboulder/`, its textures, animations and
  poser): converted from a 3D model made by ellecat5112 with **Tripo AI**. `tools/models/ironboulder.py` voxelizes
  the mesh at one voxel per model unit, quantizes its colours, merges the voxels into boxes and paints a box-UV
  texture; the animations, poser and shiny colours are original. Iron Boulder's game data (types, stats, ability,
  moves) is Cobblemon's own; CobbleEffort only marks it implemented and adds its spawns.
* **Celesteela** (`.../models/0797_celesteela/`, its textures, animations and poser): converted from an untextured 3D
  model made by ellecat5112 with **Tripo AI** by `tools/models/celesteela.py`. It is painted in the colour scheme of a
  reference picture ellecat5112 provided (no pixels of it are used); the glow layer, animations, poser and shiny are original. Its game data is Cobblemon's own.

## Code and data

The build scripts, generator, data and resolver JSON are licensed under the
[Mozilla Public License 2.0](LICENSE), the same licence Cobblemon's code uses.

## Inspiration

* **CobblemonMoreCosmetics** (Archaeus) set the "more cosmetic forms through the cosmetic slot" model this mod follows.
* **The Backrooms** by Kane Parsons (Kane Pixels) is the source of the Still Lifes and the Level 0 look. This is fan
  work; no footage or art from the series is used.

* **Five Nights at Freddy's** by Scott Cawthon inspired collection #6 (fan work; no art or assets from the games
  are used).

* The **transgender pride flag** was designed by Monica Helms (1999) and inspired collection #10.

* **Naruto**, **Naruto Shippuden** and **Boruto** by Masashi Kishimoto (and Mikio Ikemoto / Ukyo Kodachi) inspired
  collection #9 (fan work; no art from the series is used).

Pokémon and all related names are trademarks of Nintendo, Game Freak and The Pokémon Company.
CobbleEffort is not affiliated with or endorsed by them, the Cobblemon team, or Kane Parsons / A24.
