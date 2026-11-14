{
num: -3059,
accuracy: 100,
basePower: 40,
category: "Special",
name: "Twin-Coil Surge",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
multihit: 2,
onAfterMove(source) {
  this.field.addPseudoWeather('twincoilsurge', source);
},
condition: {
  duration: 5,
  onFieldStart() {
    this.add('-fieldstart', 'move: Twin-Coil Surge');
  },
  onModifyAccuracyPriority: -1,
  onModifyAccuracy(accuracy, target, source, move) {
    if (typeof accuracy !== 'number' || !target.hasType('Flying')) return;
    return this.chainModify([3277, 4096]);
  },
  onFieldResidualOrder: 27,
  onFieldResidualSubOrder: 5,
  onFieldEnd() {
    this.add('-fieldend', 'move: Twin-Coil Surge');
  }
},
secondary: null,
target: "normal",
type: "Electric",
desc: "Hits twice. Then a thick vapour fills the field for 5 turns: moves aimed at Flying-type Pokemon are 20% less accurate.",
shortDesc: "Hits 2 times. 5 turns: Flying types are harder to hit.",
contestType: "Cool"
}
