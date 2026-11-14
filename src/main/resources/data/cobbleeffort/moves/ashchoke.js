{
num: -3058,
accuracy: 100,
basePower: 60,
category: "Special",
name: "Ash Choke",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
onBasePower(basePower, pokemon, target) {
  if (target.status === 'brn') return this.chainModify(2);
},
secondary: {chance: 100, boosts: {accuracy: -1}},
target: "normal",
type: "Poison",
desc: "Power doubles if the target is burned. Lowers the target's accuracy by 1 stage.",
shortDesc: "2x power if the target is burned. -1 accuracy.",
contestType: "Tough"
}
