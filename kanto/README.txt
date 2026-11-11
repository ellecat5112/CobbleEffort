CobbleEffort: Kanto @VERSION@
=============================

A Gen 1 adventure for Cobblemon: Gen 1 Bricks, a Gen 1-styled lab in villages with a glitchy PC, and the Kanto
dimension, where only Gen 1 Pokemon live, with eight gyms, an Elite Four, and Kantonian ore for armor and outfits.

WHAT'S IN IT
  - Gen 1 Bricks in black, white and grey (8 stone bricks around a black, white or grey dye make 8).
  - The lab: a Gen 1-styled research lab of Gen 1 Bricks that can generate in any village (plains, desert, savanna,
    snowy, taiga), with a glitchy PC on its back wall. It's a rare building: not every village has one.
  - Essence of Olde: a rare drop (5%) from any Gen 1 Pokemon you defeat in battle.
  - Kantonian Orb: craft a Distortion Crystal (from CobbleEffort: Distortion) with Essence of Olde. 16 uses.
  - The glitchy PC: use the Kantonian Orb on it to wake it up, then use it to travel to Kanto. You arrive at the same
    spot, on a small brick pad with a PC: use it to come back to where you left. You can also craft a glitchy PC
    (grey Gen 1 Bricks, a glass pane, iron and redstone), but it still needs an orb to wake.
  - Kanto: a world of its own (bigger biomes than the overworld) where only Gen 1 Pokemon spawn: anything else that
    would spawn there becomes a Gen 1 Pokemon of the same type instead (never a legendary or mythical).

THE GYMS AND THE ELITE FOUR (NEW in 0.2.0)
  The first time anyone arrives in Kanto, eight gyms and the Elite Four hall are built around Kanto's centre
  (x 0, z 0), about 320 blocks out, each door facing the centre. Kanto tells you where they are when you arrive, and
  /kanto gyms lists them any time. Each gym is Gen 1 Bricks with its type's colours and a leader at the back:
      Rock Gym (0, -320)      Shale       levels 12-15        Poison Gym (0, 320)     Nightshade  levels 34-38
      Water Gym (226, -226)   Brine       levels 18-21        Psychic Gym (-226, 226) Aura        levels 38-43
      Electric Gym (320, 0)   Volta       levels 21-24        Fire Gym (-320, 0)      Cinder      levels 42-47
      Grass Gym (226, 226)    Fern        levels 27-30        Ground Gym (-226, -226) Terra       levels 47-52
  Talk to a leader and pick "Battle!". Win and you get their badge (one each; the 8 badges are items you keep).
  The Elite Four hall is at Kanto's centre: Frost (Ice), Brawn (Fighting), Wisp (Ghost) and Wyrm (Dragon), levels
  54-62, one per room. They only battle trainers with all 8 badges. Beat all four for the Kanto Champion Ribbon.
  The leaders and the Elite Four are original characters (names, looks and teams), all with Gen 1 Pokemon.
  Operators: /kanto rebuild builds the gyms and their trainers again (e.g. after the world was edited).

KANTONIAN ORE AND ARMOR (NEW in 0.2.0)
  - Kantonian ore (stone and deepslate) is only found in Kanto, at iron's heights, a bit more common than iron
    (about 1.2x). Mine it with a stone pickaxe or better for Raw Kantonian; smelt that into Kantonian Ingots
    (9 make a Block of Kantonian).
  - Kantonian armor is between iron and diamond (17 armor in all, 1 toughness), enchantable and trimmable.
    Craft it from ingots in the usual shapes for the plain set.
  - OUTFITS: put a dye OR a wool block of an outfit's colour in the gap of the armor shape, and the piece comes out
    as that outfit (same stats, a different look):
        helmet      I I I       chestplate  I X I      leggings  I I I      boots   I X I
                    I X I                   I I I                I X I              I   I
                                            I I I                I   I
      red: Trainer (cap, red jacket, jeans)        blue: Ace (blue cap and coat, black trousers)
      white: Professor (lab coat, grey hair)       brown: Hiker (round hat, vest, shorts, boots)
      light blue: Swimmer (cap and goggles)        black: Biker (helmet with visor, studded jacket)
      lime: Bug Catcher (straw hat, shorts)        yellow: Engineer (hard hat, hi-vis vest, overalls)
      purple: Psychic (hood and robe)
    The outfits are original Kanto-flavoured looks for trainer classes, not copies of any game character's outfit.

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, CobbleEffort: Distortion 0.12.0+ (for the Distortion Crystal), Architectury API.
  Install it on the server too. Kanto is a new dimension: it's there in new and existing worlds.

PLEASE TEST AND REPORT
  0.2.0: battle a gym leader (do you get the badge?), try the Elite Four without and with 8 badges, find Kantonian
  ore in Kanto, craft an outfit and wear it. (/give @s cobbleeffort_kanto:rock_badge etc. to skip ahead.)
  Find a village with the lab (or /place template cobbleeffort_kanto:village/gen1_lab), craft or find a Kantonian
  Orb (/give @s cobbleeffort_kanto:kantonian_orb), wake the PC, travel to Kanto and back. Does only Gen 1 spawn
  there? Does Essence of Olde drop now and then? Send latest.log if anything goes wrong.

LICENCE
  CC BY-NC-SA 4.0 (non-commercial). All textures and buildings are original, by ellecat5112 / CobbleEffort, except
  the trainers' skins, which are recoloured from Cobblemon's trainer texture (Cobblemon's assets: CC BY-NC).

CHANGES
  0.2.0: the gyms, the Elite Four, badges and the Champion Ribbon; Kantonian ore, ingots and armor with 9 outfits;
         /kanto gyms and /kanto rebuild. Fabric fix: Kanto's Gen 1-only spawns and Essence of Olde drops failed on
         Fabric (a build problem); they work now.
  0.1.0: Gen 1 Bricks, the lab, Essence of Olde, the Kantonian Orb, the glitchy PC and Kanto.
