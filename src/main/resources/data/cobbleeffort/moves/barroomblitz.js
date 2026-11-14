{
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
