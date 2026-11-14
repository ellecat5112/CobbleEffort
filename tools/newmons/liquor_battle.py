"""The Liquor Meadows' own abilities and moves (the user's design: 18 Pokémon inspired by brewing, distillation and
the culture of alcohol and spirits, living in CobbleEffort: Kanto's Liquor Meadows). Merged into build.py's
CUSTOM_ABILITIES / CUSTOM_MOVES; tested in node against Cobblemon's Showdown.
"""

LIQ_ABILITIES = {
    "aromaticharvest": {
        "name": "Aromatic Harvest",
        "js": """{
onResidualOrder: 5,
onResidualSubOrder: 4,
onResidual(pokemon) {
  if (!['sunnyday', 'desolateland', 'raindance', 'primordialsea'].includes(pokemon.effectiveWeather())) return;
  for (const ally of pokemon.alliesAndSelf()) {
    if (ally.hp && ally.hp < ally.maxhp) this.heal(ally.baseMaxhp / 16, ally, pokemon);
  }
},
flags: {},
name: "Aromatic Harvest",
rating: 2.5,
num: -3030
}
""",
        "lang": "In sun or rain its hop bracts give off a soothing scent: at the end of every turn it and its allies "
                "restore 1/16 of their maximum HP.",
    },
    "warminfusion": {
        "name": "Warm Infusion",
        "js": """{
onDamagingHit(damage, target, source, move) {
  if (move.type === 'Fire') this.boost({spa: 1}, target, target);
},
onStart(pokemon) {
  for (const ally of pokemon.side.pokemon) {
    if (ally.status === 'frz') {
      this.add('-activate', pokemon, 'ability: Warm Infusion');
      ally.cureStatus();
    }
  }
},
onResidualOrder: 5,
onResidualSubOrder: 3,
onResidual(pokemon) {
  for (const ally of pokemon.side.pokemon) {
    if (ally.status === 'frz') {
      this.add('-activate', pokemon, 'ability: Warm Infusion');
      ally.cureStatus();
    }
  }
},
onUpdate(pokemon) {
  if (pokemon.status === 'frz') pokemon.cureStatus();
},
onImmunity(type, pokemon) {
  if (type === 'frz') return false;
},
flags: {},
name: "Warm Infusion",
rating: 2.5,
num: -3031
}
""",
        "lang": "It swims in warmed waters: a Fire-type hit raises its Sp. Atk, it can't be frozen, and it thaws every "
                "frozen Pokémon in its party when it enters battle and at the end of each turn.",
    },
    "slowmelt": {
        "name": "Slow Melt",
        "js": """{
onSourceModifyDamage(damage, source, target, move) {
  if (move.type === 'Fire' && target.getMoveHitData(move).typeMod > 0) return this.chainModify(0.5);
},
onDamagingHit(damage, target, source, move) {
  if (move.type !== 'Fire') return;
  let activated = false;
  for (const foe of target.adjacentFoes()) {
    if (!activated) {
      this.add('-ability', target, 'Slow Melt');
      activated = true;
    }
    this.boost({spe: -1}, foe, target, null, true);
  }
},
flags: {breakable: 1},
name: "Slow Melt",
rating: 3,
num: -3032
}
""",
        "lang": "Dense ice that melts only slowly: super-effective Fire-type moves deal half damage, and when a "
                "Fire-type move hits it, its meltwater slicks the ground and lowers the Speed of every opposing Pokémon.",
    },
    "agedvintage": {
        "name": "Aged Vintage",
        "js": """{
onResidualOrder: 28,
onResidualSubOrder: 2,
onResidual(pokemon) {
  if (!pokemon.activeTurns) return;
  const stats = [];
  let s;
  for (s of ['atk', 'def', 'spa', 'spd', 'spe']) {
    if (pokemon.boosts[s] < 6) stats.push(s);
  }
  if (!stats.length) return;
  const boost = {};
  boost[this.sample(stats)] = 1;
  this.boost(boost, pokemon, pokemon);
},
flags: {},
name: "Aged Vintage",
rating: 4,
num: -3033
}
""",
        "lang": "It only gets better with age: at the end of every turn it stays in battle, one of its stats other "
                "than accuracy and evasion, picked at random, rises by 1 stage.",
    },
    "smokycask": {
        "name": "Smoky Cask",
        "js": """{
onStart(source) {
  this.field.addPseudoWeather('smokycask', source);
},
onBasePowerPriority: 21,
onBasePower(basePower, attacker, defender, move) {
  if (move.type === 'Fire' || move.type === 'Poison') return this.chainModify([5325, 4096]);
},
condition: {
  duration: 5,
  onFieldStart() {
    this.add('-fieldstart', 'ability: Smoky Cask');
  },
  onTryBoost(boost, target, source, effect) {
    if (source && target === source) return;
    let showMsg = false;
    let i;
    for (i in boost) {
      if (boost[i] < 0) {
        delete boost[i];
        showMsg = true;
      }
    }
    if (showMsg && !effect.secondaries && effect.id !== 'octolock') {
      this.add('-activate', target, 'ability: Smoky Cask');
    }
  },
  onFieldResidualOrder: 27,
  onFieldResidualSubOrder: 4,
  onFieldEnd() {
    this.add('-fieldend', 'ability: Smoky Cask');
  }
},
flags: {},
name: "Smoky Cask",
rating: 3.5,
num: -3034
}
""",
        "lang": "Its Fire- and Poison-type moves are 30% stronger, and when it enters battle it fills the field with "
                "thick peat smoke for five turns, in which no Pokémon's stats can be lowered by another.",
        "battle": {"cobblemon.battle.fieldstart.smokycask": "Thick, earthy peat smoke filled the field!",
                   "cobblemon.battle.fieldend.smokycask": "The peat smoke drifted away.",
                   "cobblemon.battle.activate.smokycask": "The peat smoke shields %1$s from losing its stats!"},
    },
    "oakmaturation": {
        "name": "Oak Maturation",
        "js": """{
onTryHeal(damage, target, source, effect) {
  if (effect && effect.isBerry) return this.chainModify(2);
},
onChangeBoost(boost, target, source, effect) {
  if (effect && effect.isBerry) {
    let b;
    for (b in boost) boost[b] *= 2;
  }
},
onSourceModifyDamagePriority: -1,
onSourceModifyDamage(damage, source, target, move) {
  if (target.abilityState.berryWeaken) {
    target.abilityState.berryWeaken = false;
    return this.chainModify(0.5);
  }
},
onTryEatItemPriority: -1,
onTryEatItem(item, pokemon) {
  this.add('-activate', pokemon, 'ability: Oak Maturation');
},
onEatItem(item, pokemon) {
  pokemon.abilityState.berryWeaken = !!item.onSourceModifyDamage;
  pokemon.abilityState.oakBerry = item.id;
  pokemon.abilityState.oakTurns = 0;
},
onResidualOrder: 28,
onResidualSubOrder: 3,
onResidual(pokemon) {
  const berry = pokemon.abilityState.oakBerry;
  if (!berry || pokemon.item) return;
  if (++pokemon.abilityState.oakTurns < 2) return;
  pokemon.abilityState.oakBerry = '';
  if (pokemon.setItem(berry)) {
    this.add('-item', pokemon, this.dex.items.get(berry), '[from] ability: Oak Maturation');
  }
},
flags: {},
name: "Oak Maturation",
rating: 3.5,
num: -3035
}
""",
        "lang": "Berries ripen inside its oak shell: a Berry it holds has twice the effect, and two turns after it "
                "eats one, a new one of the same kind has matured in its place.",
    },
    "liquidcourage": {
        "name": "Liquid Courage",
        "js": """{
onTryBoost(boost, target, source, effect) {
  if (effect.name === 'Intimidate' && boost.atk) {
    delete boost.atk;
    this.add('-fail', target, 'unboost', 'Attack', '[from] ability: Liquid Courage', '[of] ' + target);
  }
},
onAfterSetStatus(status, target, source, effect) {
  this.add('-ability', target, 'Liquid Courage');
  this.boost({atk: 1}, target, target);
},
onUpdate(pokemon) {
  if (pokemon.volatiles['confusion'] && !pokemon.abilityState.couraged) {
    pokemon.abilityState.couraged = true;
    this.add('-ability', pokemon, 'Liquid Courage');
    this.boost({atk: 1}, pokemon, pokemon);
  } else if (!pokemon.volatiles['confusion']) {
    pokemon.abilityState.couraged = false;
  }
},
flags: {breakable: 1},
name: "Liquid Courage",
rating: 3,
num: -3036
}
""",
        "lang": "A swig from its barrel steadies its nerve: it ignores Intimidate, and its Attack rises by 1 stage "
                "whenever it gets a status condition or becomes confused.",
    },
}

LIQ_MOVES = {
    "blueignition": {
        "base": "freezedry", "num": -3037, "name": "Blue Ignition", "type": "Fire", "category": "Special",
        "basePower": 75, "accuracy": 100, "pp": 15, "priority": 0,
        "flags": {"protect": 1, "mirror": 1, "metronome": 1}, "secondary": {"chance": 30, "status": "brn"},
        "contestType": "Beautiful",
        "desc": "This move's type effectiveness against Water is changed to be super effective no matter what this "
                "move's type is. 30% chance to burn the target.",
        "shortDesc": "Super effective on Water. 30% burn.",
        "lang": "The user sets its pure spirit ablaze in a cool, ghost-blue flame. It is super effective against "
                "Water types, and it may leave a burn.",
    },
    "zestshock": {
        "name": "Zest Shock",
        "js": """{
num: -3038,
accuracy: 100,
basePower: 50,
category: "Special",
name: "Zest Shock",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
self: {boosts: {spe: 2}},
onAfterMove(pokemon) {
  for (const active of this.getAllActive()) {
    if (active.status === 'slp') active.cureStatus();
  }
},
secondary: null,
target: "normal",
type: "Electric",
desc: "Raises the user's Speed by 2 stages. Every active Pokemon wakes up.",
shortDesc: "Raises the user's Speed by 2. Wakes every active Pokemon.",
contestType: "Cool"
}
""",
        "lang": "A jolt of electrified citrus zest: it sharply raises the user's Speed, and the crackle wakes every "
                "Pokémon on the field.",
    },
    "barroomblitz": {
        "name": "Barroom Blitz",
        "js": """{
num: -3039,
accuracy: 90,
basePower: 20,
category: "Physical",
name: "Barroom Blitz",
pp: 10,
priority: 0,
flags: {contact: 1, protect: 1, mirror: 1, punch: 1, metronome: 1},
multihit: [2, 5],
onBasePower(basePower, pokemon) {
  if (pokemon.volatiles['confusion']) return this.chainModify(2);
},
secondary: null,
target: "normal",
type: "Fighting",
desc: "Hits two to five times. Power doubles if the user is confused.",
shortDesc: "Hits 2-5 times. 2x power if the user is confused.",
contestType: "Tough"
}
""",
        "lang": "The user throws a flurry of wild haymakers, two to five of them. They hit twice as hard if the user "
                "is confused.",
    },
    "greenmuse": {
        "name": "Green Muse",
        "js": """{
num: -3040,
accuracy: 90,
basePower: 0,
category: "Status",
name: "Green Muse",
pp: 10,
priority: 0,
flags: {protect: 1, reflectable: 1, mirror: 1, metronome: 1},
onHit(target, source) {
  const confused = target.addVolatile('confusion', source);
  const lowered = this.boost({spd: -1}, target, source);
  return !!(confused || lowered);
},
self: {boosts: {spa: 1}},
secondary: null,
target: "normal",
type: "Psychic",
desc: "Confuses the target and lowers its Special Defense by 1 stage. Raises the user's Special Attack by 1 stage.",
shortDesc: "Confuses target, -1 SpD to it, +1 SpA to the user.",
contestType: "Beautiful"
}
""",
        "lang": "The user swirls a cloud of emerald mist round the target, confusing it and lowering its Sp. Def, "
                "and draws inspiration from it to raise its own Sp. Atk.",
    },
    "roastpress": {
        "name": "Roast & Press",
        "js": """{
num: -3041,
accuracy: 100,
basePower: 70,
category: "Physical",
name: "Roast & Press",
pp: 10,
priority: 0,
flags: {contact: 1, protect: 1, mirror: 1, metronome: 1},
onBasePower(basePower, pokemon, target) {
  const last = target.getLastAttackedBy();
  if (last && this.dex.moves.get(last.move).type === 'Fire') {
    this.debug('Roast & Press: target was roasted');
    return this.chainModify(2);
  }
},
secondary: null,
target: "normal",
type: "Ground",
desc: "Power doubles if the last move to hit the target was a Fire-type move.",
shortDesc: "2x power if the target was last hit by a Fire move.",
contestType: "Tough"
}
""",
        "lang": "The user crushes the target under its spiny core like an agave in the press. It hits twice as hard "
                "if the last move to hit the target was a Fire-type move.",
    },
    "popoff": {
        "name": "Pop Off",
        "js": """{
num: -3042,
accuracy: 100,
basePower: 80,
category: "Physical",
name: "Pop Off",
pp: 10,
priority: 0,
flags: {contact: 1, mirror: 1, metronome: 1},
breaksProtect: true,
critRatio: 2,
onTryHit(pokemon) {
  pokemon.side.removeSideCondition('reflect');
  pokemon.side.removeSideCondition('lightscreen');
  pokemon.side.removeSideCondition('auroraveil');
},
secondary: null,
target: "normal",
type: "Flying",
desc: "High critical hit ratio. Hits through Protect and similar moves, ending their effect, and shatters Reflect, Light Screen and Aurora Veil on the target's side.",
shortDesc: "High crit. Breaks Protect and screens.",
contestType: "Cool"
}
""",
        "lang": "The user corkscrews into the target and pops out with a loud thunk. It breaks through Protect and "
                "shatters Reflect, Light Screen and Aurora Veil, and lands critical hits more easily.",
    },
    "nectartoast": {
        "name": "Nectar Toast",
        "js": """{
num: -3043,
accuracy: true,
basePower: 0,
category: "Status",
name: "Nectar Toast",
pp: 5,
priority: 0,
flags: {heal: 1, bypasssub: 1, allyanim: 1, metronome: 1},
onHit(pokemon) {
  const healed = this.heal(this.modify(pokemon.maxhp, 0.5));
  const boosted = this.boost({atk: 1}, pokemon);
  return !!(healed || boosted);
},
secondary: null,
target: "allies",
type: "Bug",
desc: "The user and its allies on the field restore 1/2 of their maximum HP and raise their Attack by 1 stage.",
shortDesc: "User and allies: heal 50%, +1 Atk.",
contestType: "Cute"
}
""",
        "lang": "The user raises a toast of fermented nectar with its allies: it and every ally on the field restore "
                "half their HP and gain courage, raising their Attack.",
    },
    "hangover": {
        "name": "Hangover",
        "js": """{
num: -3044,
accuracy: 100,
basePower: 70,
category: "Special",
name: "Hangover",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
onBasePower(basePower, pokemon, target) {
  const last = target.lastMove;
  if (last && last.category === 'Status' && (last.boosts || (last.self && last.self.boosts))) {
    target.m.hangover = true;
    return this.chainModify(2);
  }
  target.m.hangover = false;
},
onHit(target) {
  if (target.m.hangover) {
    target.clearBoosts();
    this.add('-clearboost', target);
  }
  target.m.hangover = false;
},
secondary: null,
target: "normal",
type: "Ghost",
desc: "If the target's last move was a status move that raises stats, this move's power doubles and the target loses all its stat stages.",
shortDesc: "2x and clears boosts if the target last used a boosting move.",
contestType: "Clever"
}
""",
        "lang": "Haunted liquor's memory of the night before. If the target's last move was a status move that raised "
                "stats, it hits twice as hard and the target loses all its stat changes.",
    },
    "distill": {
        "name": "Distill",
        "js": """{
num: -3045,
accuracy: true,
basePower: 0,
category: "Status",
name: "Distill",
pp: 10,
priority: 0,
flags: {snatch: 1, metronome: 1},
onHit(pokemon) {
  let purified = 0;
  if (pokemon.status) {
    pokemon.cureStatus();
    purified++;
  }
  let s;
  for (s in pokemon.boosts) {
    if (pokemon.boosts[s] < 0) {
      pokemon.boosts[s] = 0;
      purified++;
    }
  }
  if (purified) this.add('-clearnegativeboost', pokemon, '[silent]');
  return this.boost({spa: purified ? 2 : 1}, pokemon, pokemon) !== false;
},
secondary: null,
target: "self",
type: "Steel",
desc: "The user is cured of its non-volatile status condition and loses its negative stat stages, then raises its Special Attack by 2 stages if anything was removed, otherwise by 1 stage.",
shortDesc: "Cures status and stat drops; +2 SpA if any were cleared, else +1.",
contestType: "Clever"
}
""",
        "lang": "The user boils away its impurities, curing its status condition and its lowered stats, and condenses "
                "them into pure energy: its Sp. Atk rises sharply if anything was purified, or by 1 stage otherwise.",
    },
    "contrabandswap": {
        "name": "Contraband Swap",
        "js": """{
num: -3046,
accuracy: 100,
basePower: 50,
category: "Physical",
name: "Contraband Swap",
pp: 10,
priority: 0,
flags: {contact: 1, protect: 1, mirror: 1, metronome: 1},
onAfterHit(target, source, move) {
  if (source.hp && !source.item && target.item) {
    const item = target.takeItem(source);
    if (item) {
      if (!source.setItem(item)) {
        target.item = item.id;
      } else {
        this.add('-enditem', target, item, '[silent]', '[from] move: Contraband Swap');
        this.add('-item', source, item, '[from] move: Contraband Swap', '[of] ' + target);
      }
    }
  }
  if (target.hp) target.addVolatile('contrabandswap', source);
},
condition: {
  duration: 2,
  onStart(pokemon) {
    this.add('-start', pokemon, 'Contraband Swap');
  },
  onResidualOrder: 13,
  onEnd(pokemon) {
    this.add('-end', pokemon, 'Contraband Swap');
    if (!pokemon.hp) return;
    const mod = Math.pow(2, Math.max(-2, Math.min(2, this.dex.getEffectiveness('Dark', pokemon))));
    this.damage(Math.max(1, Math.floor(pokemon.baseMaxhp / 4 * mod)), pokemon, null, this.dex.conditions.get('contrabandswap'));
  }
},
secondary: null,
target: "normal",
type: "Dark",
desc: "The user steals the target's held item if it has none, and leaves a volatile jug with the target that explodes at the end of the next turn, dealing 1/4 of its maximum HP adjusted by Dark-type effectiveness.",
shortDesc: "Steals item; jug explodes next turn: 1/4 HP x Dark effectiveness.",
contestType: "Clever"
}
""",
        "lang": "The user swipes the target's held item and slips it a volatile jug of moonshine instead. At the end "
                "of the next turn the jug explodes, dealing Dark-type damage.",
        "battle": {"cobblemon.battle.start.contrabandswap": "%1$s was handed a volatile jug!",
                   "cobblemon.battle.end.contrabandswap": "The jug %1$s was holding exploded!",
                   "cobblemon.battle.damage.contrabandswap": "%1$s was caught in the exploding jug!"},
    },
    "effervescentroar": {
        "name": "Effervescent Roar",
        "js": """{
num: -3047,
accuracy: 100,
basePower: 80,
category: "Special",
name: "Effervescent Roar",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, sound: 1, bypasssub: 1, metronome: 1},
onAfterMove(source) {
  if (source.side.pokemon.some(ally => ally.status)) {
    this.add('-activate', source, 'move: Aromatherapy');
    for (const ally of source.side.pokemon) ally.cureStatus();
  }
  for (const side of source.side.foeSidesWithConditions()) side.addSideCondition('effervescentroar', source);
},
condition: {
  duration: 3,
  onSideStart(side) {
    this.add('-sidestart', side, 'move: Effervescent Roar');
  },
  onResidualOrder: 5,
  onResidualSubOrder: 1,
  onResidual(target) {
    this.damage(target.baseMaxhp / 16, target, null, this.dex.conditions.get('effervescentroar'));
  },
  onSideResidualOrder: 26,
  onSideResidualSubOrder: 13,
  onSideEnd(side) {
    this.add('-sideend', side, 'move: Effervescent Roar');
  }
},
secondary: null,
target: "allAdjacentFoes",
type: "Dragon",
desc: "Hits all adjacent foes and cures the status of every Pokemon in the user's party. For 3 turns, sparkling bubbles on the opposing side deal 1/16 of their maximum HP to each opposing Pokemon at the end of every turn.",
shortDesc: "Hits foes, cures party status; 3 turns of 1/16 residual on foes.",
contestType: "Beautiful"
}
""",
        "lang": "A joyous, sparkling roar that hits every opposing Pokémon, cures its party's status conditions and "
                "leaves fizzing bubbles round the opposing side that hurt them at the end of each turn for three turns.",
        "battle": {
            "cobblemon.battle.sidestart.ally.effervescentroar": "Sparkling bubbles fizzed up around your team!",
            "cobblemon.battle.sidestart.opponent.effervescentroar": "Sparkling bubbles fizzed up around the opposing team!",
            "cobblemon.battle.sideend.ally.effervescentroar": "The bubbles around your team went flat!",
            "cobblemon.battle.sideend.opponent.effervescentroar": "The bubbles around the opposing team went flat!",
            "cobblemon.battle.damage.effervescentroar": "%1$s is buffeted by the sparkling bubbles!",
        },
    },
}
