{
onSourceModifyDamage(damage, source, target, move) {
  if (move.flags['contact']) return this.chainModify(0.7);
},
flags: {breakable: 1},
name: "Frothy Guard",
rating: 3,
num: -3053
}
