{
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
