{
onStart(source) {
  this.field.addPseudoWeather('cloudchaser', source);
},
condition: {
  duration: 5,
  onFieldStart(field, source) {
    this.add('-fieldstart', 'ability: Cloud Chaser');
  },
  onBasePowerPriority: 6,
  onBasePower(basePower, attacker, defender, move) {
    if (move.type === 'Electric') return this.chainModify([5325, 4096]);
  },
  onModifyAccuracyPriority: -1,
  onModifyAccuracy(accuracy, target, source, move) {
    if (typeof accuracy !== 'number' || !source || source.hasType('Electric')) return;
    return this.chainModify([3277, 4096]);
  },
  onFieldResidualOrder: 27,
  onFieldResidualSubOrder: 3,
  onFieldEnd() {
    this.add('-fieldend', 'ability: Cloud Chaser');
  }
},
flags: {},
name: "Cloud Chaser",
rating: 3,
num: -3013
}
