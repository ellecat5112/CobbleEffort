{
num: -3023,
accuracy: 100,
basePower: 75,
category: "Physical",
name: "Spittoon Slug",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1, bullet: 1},
onBasePower(basePower, source, target, move) {
  if (target.item) return this.chainModify(1.5);
},
secondary: null,
target: "normal",
type: "Fighting",
desc: "Power is multiplied by 1.5 if the target is holding an item.",
shortDesc: "1.5x damage if the target holds an item.",
contestType: "Tough"
}
