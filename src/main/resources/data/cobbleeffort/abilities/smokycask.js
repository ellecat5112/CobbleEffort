{
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
