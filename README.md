# CobbleEffort

A Cobblemon sidemod that adds **extra cosmetic forms** for existing Cobblemon models, in the spirit of
[CobblemonMoreCosmetics](https://modrinth.com/resourcepack/cobblemonmorecosmetics). It changes no models:
each form is a new texture applied through Cobblemon's own cosmetic-slot and aspect system.

**Collections so far:** #1 Backrooms (41 Pokémon) · #2 Thanksgiving (37 Pokémon) · #3 Halloween (33 Pokémon) · #4 Christmas (40 Pokémon) · #5 Easter (40 Pokémon) · #6 Five Nights at Freddy's (40 Pokémon) · #7 Ice Sculptures (42 Pokémon) · #8 Stone Statues (41 Pokémon) · #9 Naruto (35 Pokémon + Xurkitree).

**House rule: every cosmetic covers whole evolutionary lines.** If one stage gets a form, every pre-evolution,
evolution and branch of that Pokémon gets it too. The generator enforces this (see [Collection rules](#collection-rules)).

**Built for a mod stack (since v0.10.0).** CobbleEffort is made to run alongside Mega Showdown (+ Extra Megas,
Ores), Cobblemon: AllTheMons x Mega Showdown, Cobblemon Baby Legends, Cobblemon Lost Lore, Legendary Monuments,
the Fully Hisuian Starters resource pack and the Poke Costumes data pack. Megas, Gigantamax and other new forms keep
the cosmetic, and other mods' model replacements don't break it. See [Compatibility](#compatibility).

## Collection #1: Backrooms (Still Lifes)

18 evolutionary lines (**41 Pokémon**) re-imagined as **Still Lifes** from Kane Pixels' *Backrooms*. A Still Life is an imperfect
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
| Xerneas | Xerfawn (Baby Legends), Xerneas |
| Silicobra | Silicobra → Sandaconda |
| Sizzlipede | Sizzlipede → Centiskorch |
| Impidimp | Impidimp → Morgrem → Grimmsnarl |
| Nymble | Nymble → Lokix |
| Maschiff | Maschiff → Mabosstiff |

The 18 lines were picked at random (`random.Random("kane-pixels-level-0").sample(...)`) and then expanded to
their full evolutionary families from Cobblemon's species data. Torkoal has no evolutions; Xerneas' line includes Baby Legends' Xerfawn.

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

## Collection #3: Halloween (Nightmare) ⚠️ gore

> **Content warning:** this collection is deliberately horrific. It has blood, gore, rotting flesh, wounds and
> body horror. Players who don't want it simply never use the Carved Pumpkin cosmetic.

18 evolutionary lines (**33 Pokémon**) turned into nightmares. These are **animated textures** (4 frames, 5 fps):

* colour drained and darkened, mottled with **bruise-purple and rot-green**, grime along every edge
* swollen **bruised lumps**, **torn patches of raw flesh**, some crudely **stitched** shut
* **blood splatters** with drips running down, and a drop that creeps further each frame
* **lots of extra, misplaced eyes**: bloodshot, with darting pupils, some blinking, some weeping blood
* the Pokémon's own eyes turn blood red, and **misplaced copies** of them grow elsewhere on the body
* **mouths full of jagged, yellowed, bloody teeth that gnash** open and shut
* shiny → **pale corpse**: cold grey-blue skin, so the blood stands out more
* glowing parts become a sickly **ghost-green**. Full-body glow layers (Shinx line) keep only their hottest spots,
  so they don't hide the gore

**Charmander line ("Bone-Rot"):** Charmander, Charmeleon and Charizard are **skeletons with flesh rotting off the
bones**: cracked ivory bone, an exposed **rib cage** where the belly was, ragged rotting flesh with blood, ichor and
maggots, hollow eye sockets with a flickering pink ember, a gnashing skeletal grin, and the tail fire burning
**pink**. Shiny Charmanders have charred black bones.

![Original vs. Nightmare](docs/halloween_preview.png)

![Gnashing animation](docs/halloween_animation.gif)

| Line | Pokémon |
|------|---------|
| **Charmander** (Bone-Rot) | Charmander → Charmeleon → Charizard |
| Koffing | Koffing → Weezing (incl. Galarian) |
| Sentret | Sentret → Furret |
| Misdreavus | Misdreavus → Mismagius |
| Absol | Absol |
| Shinx | Shinx → Luxio → Luxray |
| Glameow | Glameow → Purugly |
| Timburr | Timburr → Gurdurr → Conkeldurr |
| Sigilyph | Sigilyph |
| Ducklett | Ducklett → Swanna |
| Pancham | Pancham → Pangoro |
| Comfey | Comfey |
| Komala | Komala |
| Dracovish | Dracovish |
| Tarountula | Tarountula → Spidops |
| Nacli | Nacli → Naclstack → Garganacl |
| Klawf | Klawf |
| Veluza | Veluza |

The Charmander line was chosen by request. The other 17 were picked with
`generate.py pick --count 17 --seed halloween-2026` from the 398 remaining eligible lines.

Models aren't changed (this mod only retextures). The deformities, extra eyes and mouths are painted onto the
existing models.

### How to get one

Give a supported Pokémon a **Carved Pumpkin** as its cosmetic item. With commands: `/pokegive charmander halloween`,
`/pokegive tarountula halloween shiny`. Pack makers can extend the item tag `#cobbleeffort:halloween_cosmetics`.

## Collection #4: Christmas

18 evolutionary lines (**40 Pokémon**). Four of them have their own costume:

| Line | Look |
|------|------|
| **Munchlax → Snorlax** | **Santa Claus**: red suit, a red coat front with white fur trim, a black belt with a gold buckle, and a white fluffy beard and cuffs. Shiny: an old-world **Father Christmas** in green |
| **Turtwig → Grotle → Torterra** | **Christmas tree**: every leafy part becomes a pine tree hung with baubles and gold tinsel, wound with **twinkling fairy lights**, and topped with snow. Shiny: a white **flocked** tree |
| **Trubbish → Garbodor** | **Christmas gift**: wrapped in candy-stripe paper with a green satin ribbon, a bow and a gift tag. Shiny: gold foil with a red ribbon |
| **Phantump → Trevenant** | **Krampus**: shaggy black goat fur, ridged ram's horns, **red eyes that glow in the dark**, a long red tongue, and iron chains hung with gold bells. Shiny: a white-furred Krampus with gold horns |

The other 14 lines get the **Festive** look: a Christmas palette (crimson, gold, pine, icy blue, berry, with snowy
whites), snow settled on top of every surface, snowflakes, and strings of **fairy lights that glow in the dark and
twinkle**. Shiny: **Frosted** (silver, ice and snow).

Weedle → Kakuna → Beedrill · Mankey → Primeape → Annihilape · Shellder → Cloyster · Girafarig → Farigiraf ·
Pineco → Forretress · Heracross · Makuhita → Hariyama · Spiritomb · Skorupi → Drapion ·
Sewaddle → Swadloon → Leavanny · Yamask (incl. Galarian) → Cofagrigus / Runerigus · Larvesta → Volcarona ·
Litleo → Pyroar · Dreepy → Drakloak → Dragapult

The four costume lines were chosen by request; the other 14 were picked with
`generate.py pick --count 14 --seed christmas-2026` from the 377 remaining eligible lines.

![Original vs. Christmas](docs/christmas_preview.png)

![Twinkling lights](docs/christmas_lights.gif)

### How to get one

Give a supported Pokémon a **Snowball** as its cosmetic item. With commands: `/pokegive snorlax christmas`,
`/pokegive turtwig christmas shiny`. Pack makers can extend the item tag `#cobbleeffort:christmas_cosmetics`.

## Collection #5: Easter

18 evolutionary lines (**40 Pokémon**). Two of them have their own costume:

| Line | Look |
|------|------|
| **Togepi → Togetic → Togekiss** | **Easter egg**: the white shell and body become a hand-painted egg with pastel bands of solid colour, zigzags, polka dots and white pin-stripes. Togepi's red and blue triangles are repainted raspberry and periwinkle as part of the decoration. Shiny: a **golden Fabergé egg** set with ruby, sapphire, emerald and pearl |
| **Buneary → Lopunny** | **Easter Bunny**: soft white bunny fur with a lavender shadow, pastel-pink fluffy ears, spring daisies and a painted-egg ribbon. Shiny: a **chocolate bunny** in milk and white chocolate with a dark drizzle and gold-foil trim |

The other 16 lines get the **Pastel** look: every colour becomes its soft pastel version, plus a hand-painted
zigzag ribbon like the decoration round an Easter egg and little spring daisies. Shiny: **chocolate** with rainbow
candy sprinkles.

Jigglypuff (incl. Igglybuff, Wigglytuff) · Diglett → Dugtrio · Aerodactyl · Chinchou → Lanturn ·
Mareep → Flaaffy → Ampharos · Smeargle · Slakoth → Vigoroth → Slaking · Latot (Baby Legends) → Latias / Latios · Drifloon → Drifblim ·
Roggenrola → Boldore → Gigalith · Litten → Torracat → Incineroar · Cutiefly → Ribombee · Snom → Frosmoth ·
Eternatus · Wattrel → Kilowattrel · Finizen → Palafin

Togepi and Lopunny were chosen by request. The other 16 were picked with `generate.py pick --count 16 --seed easter-2027`
from the 361 remaining eligible lines.

![Original vs. Easter](docs/easter_preview.png)

![Easter eggs and bunnies, normal and shiny](docs/easter_specials.png)

### How to get one

Give a supported Pokémon an **Egg** as its cosmetic item. With commands: `/pokegive togepi easter`,
`/pokegive lopunny easter shiny`. Pack makers can extend the item tag `#cobbleeffort:easter_cosmetics`.

## Collection #6: Five Nights at Freddy's (Animatronics)

18 evolutionary lines (**40 Pokémon**) rebuilt as pizzeria animatronics, with **eyes that glow in the dark**
(an extra emissive layer). Three of them are the classic cast:

| Line | Look | Shiny |
|------|------|-------|
| **Teddiursa → Ursaring → Ursaluna** | **Classic Freddy**: brown felt bear, pale muzzle, black top hat, bow tie, animatronic grin, glowing blue eyes | **Golden Freddy** |
| **Torchic → Combusken → Blaziken** | **Classic Chica**: yellow felt chicken, orange beak and feet, the "LET'S EAT!!!" bib, teeth, glowing violet eyes | **Toy Chica**: brighter, with rosy cheeks |
| **Sandile → Krokorok → Krookodile** | **Classic Foxy**: rust-red fox suit torn open to the metal endoskeleton, eye patch with strap, sharp teeth, one glowing amber eye | **Mangle**: white and pink |

The other 15 lines each wear the look of one game (dealt round-robin):

| Game | Look | Lines |
|------|------|-------|
| FNAF 1 | **Classic**: worn felt, stitched seams, rivets, square teeth, white pinprick eyes | Seel, Pidove, Fidough |
| FNAF 2 | **Withered**: faded, filthy, torn to the endoskeleton and wires, one eye dark | Horsea, Audino |
| FNAF 2 | **Toy**: glossy plastic, brighter colours, rosy cheeks, shiny eyes | Sunkern, Maractus |
| FNAF 3 | **Springtrap**: rotten olive-yellow suit, stains, wires | Murkrow, Zorua |
| FNAF 4 | **Nightmare**: near-black, jagged tears lined with teeth, red pinprick eyes | Unown, Gothita |
| FNAF 5 | **Funtime**: white glossy plating, pink/purple panels, faceplate seams, rosy cheeks | Finneon, Vanillite |
| FNAF 6 | **Scrap**: rusted and patched with mismatched panels, burns and wires | Patrat, Helioptile |

(each with its whole evolutionary line). Shinies of the generic looks are **Golden** animatronics.

Teddiursa, Torchic and Sandile were chosen by request. The other 15 were picked with `generate.py pick --count 15 --seed fnaf-1987`.

![Freddy, Chica and Foxy](docs/fnaf_characters.png)

![Original vs. animatronic](docs/fnaf_preview.png)

### How to get one

Give a supported Pokémon a **Clock** (the night shift, 12 to 6 AM) as its cosmetic item. With commands:
`/pokegive teddiursa animatronic`, `/pokegive sandile animatronic shiny`. Pack makers can extend the item tag
`#cobbleeffort:animatronic_cosmetics`.

## Collection #7: Ice Sculptures

18 evolutionary lines (**42 Pokémon**) carved out of a block of ice:

* recoloured in clear **glacier-ice blues**, mapped from each Pokémon's own light and shade, so every marking
  is still there, chiselled into the ice
* **faceted chisel planes** that each catch the light differently, **light streaks** refracting through,
  hairline **cracks** and trapped **air bubbles**
* a **frosted rim** along every edge, and **eyes carved** as deeper-blue hollows
* a layer of **glints that twinkle and glow in the dark** (4-frame emissive layer)
* glowing parts (Crocalor's and Skeledirge's fire, for example) turn into an **icy cyan glow**
* shiny: **Aurora Ice**, the same sculpture shimmering teal-to-violet like the northern lights

Zubat → Golbat → Crobat · Oddish → Gloom → Vileplume / Bellossom · Drowzee → Hypno · Lickitung → Lickilicky ·
Shuckle · Whismur → Loudred → Exploud · Cranidos → Rampardos · Hippopotas → Hippowdon · Snover → Abomasnow ·
Axew → Fraxure → Haxorus · Skiddo → Gogoat · Dedenne · Poipole → Naganadel · Sobble → Drizzile → Inteleon ·
Wooloo → Dubwool · Sprigatito → Floragato → Meowscarada · Fuecoco → Crocalor → Skeledirge · Toedscool → Toedscruel

Picked with `generate.py pick --count 18 --seed ice-sculpture-2026` from the 327 remaining eligible lines.

![Original vs. ice sculpture](docs/ice_sculpture_preview.png)

![Normal and shiny Aurora Ice](docs/ice_sculpture_closeup.png)

![Twinkling glints](docs/ice_sculpture_glints.gif)

### How to get one

Give a supported Pokémon **Ice, Packed Ice or Blue Ice** as its cosmetic item. With commands:
`/pokegive axew ice_sculpture`, `/pokegive sprigatito ice_sculpture shiny`. Pack makers can extend the item tag
`#cobbleeffort:ice_sculpture_cosmetics`.

## Collection #8: Stone Statues

18 evolutionary lines (**41 Pokémon**) turned into solid stone statues:

* **granite-grey stone**, mapped from each Pokémon's own light and shade, so its markings remain as carved relief
* mottled **stone grain** with speckles and fine **chisel strokes**
* **weathering**: sunlit top edges, shadowed undersides, small chips, dark **cracks** and the odd patch of
  **moss and lichen**
* **blank, carved eyes**, like a real statue
* **no glow**: flames, lights and other glowing parts are turned off or turned to stone (Quilava's and
  Typhlosion's flames become carved stone flames)
* shiny: polished white **marble** with flowing grey veins and **gold-leaf eyes**

Pidgey → Pidgeotto → Pidgeot · Goldeen → Seaking · Tauros (incl. Paldean breeds) · Cyndaquil → Quilava → Typhlosion
(incl. Hisuian) · Qwilfish → Overqwil · Phanpy → Donphan · Aron → Lairon → Aggron · Trapinch → Vibrava → Flygon ·
Cherubi → Cherrim · Deerling → Sawsbuck (all seasons) · Fennekin → Braixen → Delphox · Rowlet → Dartrix → Decidueye ·
Rookidee → Corvisquire → Corviknight · Rolycoly → Carkol → Coalossal · Stonjourner · Regidrago ·
Tadbulb → Bellibolt · Capsakid → Scovillain

Picked with `generate.py pick --count 18 --seed stone-statue-2026` from the 309 remaining eligible lines.

![Original vs. stone statue](docs/stone_statue_preview.png)

![Stone and shiny marble](docs/stone_statue_closeup.png)

### How to get one

Give a supported Pokémon **Stone, Smooth Stone or Chiseled Stone Bricks** as its cosmetic item. With commands:
`/pokegive aron stone_statue`, `/pokegive fennekin stone_statue shiny`. Pack makers can extend the item tag
`#cobbleeffort:stone_statue_cosmetics`.

## Collection #9: Naruto / Naruto Shippuden / Boruto (Shinobi)

18 evolutionary lines (**35 Pokémon, plus Xurkitree**) as shinobi. Two of them are characters:

| Line | Look | Shiny |
|------|------|-------|
| **Vulpix → Ninetales** (incl. Alolan) | **Kurama**, the Nine-Tails: orange fox fur, black eye markings and ear tips, red slit eyes, and an orange chakra glow flickering on every edge | **Kurama Link Mode**: gold with black seal lines |
| **Xurkitree** ⚠️ *needs AllTheMons x Mega Showdown (or Cobblemon Ultra-Beasts) for its model* | **Sasuke Uchiha**: spiky blue-black star "hair", glowing Sharingan eyes, the Uchiha crest on the back, navy sleeves and trousers with white shin wraps, a purple rope belt, and **Chidori** lightning crackling on both claws (glowing, animated) | Rinnegan purple, with purple-black lightning |

The other 16 lines each get one look:

| Look | What it is | Lines |
|------|------------|-------|
| **Akatsuki** | black cloak with red, white-edged clouds; glowing Sharingan eyes | Venonat, Swinub, Cetoddle |
| **Leaf Shinobi** | navy-toned uniform, olive flak vest with scroll pockets, Leaf forehead protector | Onix, Mantine, Iron Leaves |
| **ANBU** | grey armour, white porcelain mask with red markings | Voltorb, Solrock |
| **Sage Mode** | orange sage pigment, glowing toad eyes, red cloak hem with black flames | Cubone, Popplio |
| **Uzumaki** | Naruto's orange and black, whisker marks, red swirl, forehead protector | Hoothoot, Toxel |
| **Byakugan** | pale lavender robes, pupil-less glowing eyes, bulging veins | Spinarak, Cufant |
| **Karma** (Boruto) | a bold black Karma seal and one glowing blue Jōgan eye | Dunsparce, Rellor |

(each with its whole evolutionary line). Vulpix was chosen by request. The other 16 were picked with
`generate.py pick --count 16 --seed naruto-shippuden`.

**About Xurkitree:** Cobblemon 1.8.4 has no Xurkitree model. **Cobblemon: AllTheMons x Mega Showdown** ships one,
and so does **Cobblemon Ultra-Beasts** (by BileulDevs). ATM's is the same model with a few small glow bulbs added.
CobbleEffort doesn't include either model or any of their art: the Sasuke texture is painted from scratch onto the
union of both UV layouts, so it fits whichever one is installed. Without either mod it does nothing.

![Kurama and Sasuke](docs/naruto_kurama_sasuke.png)

![Original vs. shinobi](docs/naruto_preview.png)

### How to get one

Give a supported Pokémon **Flint** (a kunai) as its cosmetic item. With commands: `/pokegive vulpix shinobi`,
`/pokegive xurkitree shinobi shiny`. Pack makers can extend the item tag `#cobbleeffort:shinobi_cosmetics`.

## Compatibility

CobbleEffort is built to be used alongside this mod stack, and every update is generated against it:

| Mod | What CobbleEffort does with it |
|-----|--------------------------------|
| **Mega Showdown** | Every mega, Gigantamax, Eternamax and mode form (e.g. Mega Charizard X/Y, Gmax Snorlax, Xerneas' active mode) of a Pokémon in a collection gets its own cosmetic texture, adapted from Mega Showdown's (CC BY-NC-SA 4.0). Where Mega Showdown replaces a Cobblemon model or texture (Audino, Latias, Xerneas…), the cosmetic follows its version |
| **Mega Showdown: Extra Megas** | Its megas (Torterra, Luxray, Gogoat, Annihilape…) get cosmetic textures too |
| **Mega Showdown Ores** | Nothing to change (no Pokémon visuals) |
| **AllTheMons x Mega Showdown** | It replaces some Cobblemon models (Absol, Typhlosion, Rolycoly line, Bounsweet line, Frosmoth, Runerigus, Incineroar…). A cosmetic texture is painted for Cobblemon's model, so CobbleEffort ships Cobblemon's model, poser and animations for those Pokémon under its own name and the cosmetic uses them. ATM's own forms show unchanged under the cosmetic (its licence doesn't allow recoloured copies). Also provides Xurkitree's model for the Sasuke cosmetic |
| **Cobblemon Baby Legends** | Its babies join their legendary's evolutionary line: Xerfawn (→ Xerneas) is in Backrooms, Latot (→ Latias / Latios) in Easter. Its art is All Rights Reserved, so their cosmetic textures are painted from scratch on the model's UV layout, in the evolved form's colours |
| **Cobblemon Lost Lore** | Its forms on collection Pokémon (snowman Snorlax/Munchlax, crystal Onix/Steelix, clone Charmander/Squirtle lines, coloured Kecleon) show unchanged under the cosmetic, since its licence doesn't allow modified copies |
| **Legendary Monuments**, **Fully Hisuian Starters**, **Poke Costumes** | No conflicts known. Not yet checked against their files |

How it works: every cosmetic variation pins the model and poser it was painted for, so another mod replacing the
base model at a lower resolver order can't put the cosmetic texture on the wrong model. Forms added by mods whose
licence doesn't allow adapted art get a "passthrough" copy that restores exactly what the game shows without the
cosmetic. The cosmetic steps aside in that form rather than looking broken.

![Mega Showdown forms and Baby Legends babies, original vs. cosmetic](docs/compat_forms_preview.png)

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

`validateData` checks that every JSON file parses, that every texture a resolver points to exists, and that every
pinned `cobbleeffort:` model, poser and animation group exists.

### Regenerating / adding collections

Each collection is a config in `tools/collections/<name>.json` (aspect, cosmetic item, `lines`, optional
`line_styles` to give one line its own look) plus a texture style in `tools/styles/<style>.py`. A style can set
`FRAMES`/`FPS` to make every texture an animation (Halloween does), and `EXTRA_LAYERS` + `extra_layer()` to add
its own layers on top of the body, such as Christmas's glowing, twinkling fairy lights. A style that sets
`WANTS_HINTS` is told where the model's head front/top and torso front faces are in the texture (read from the
`.geo.json`). FNAF uses this to put Freddy's hat on top of his head and Chica's bib on her chest. Everything under `assets/cobbleeffort` and `data/cobbleeffort` is generated:

The generator reads the mod stack from `tools/compat/mods.json`. Put each mod's jar (or a directory of its
resources) in `tools/compat/jars/`, which is gitignored: other mods' files are never committed. Pass `--no-compat`
to build against Cobblemon alone.

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

### Addon lines (Pokémon modelled by another mod)

A collection can list `addon_lines` for Pokémon Cobblemon doesn't model but another mod does (Xurkitree, from
Cobblemon Ultra-Beasts). The model's UV layout, with no art, is extracted with
`python3 -I tools/addons/extract_layout.py <their .geo.json> tools/addons/<name>_layout.json`. A builder in
`tools/addons/` then paints an original texture onto it. The resolver only swaps textures and layers, so the
cosmetic is active only when that mod is installed. To preview it, pass the other mod's model folder with
`EXTRA_MODEL_ROOTS=...`.

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
5. **Built for the mod stack.** Families include other mods' pre-evolutions and evolutions. Other mods' forms are
   retextured where their licence allows, and passed through otherwise. Models are pinned (and vendored when a mod
   overwrites one). See [Compatibility](#compatibility).

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
