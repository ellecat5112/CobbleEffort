{
onSourceInvulnerabilityPriority: 1,
onSourceInvulnerability(target, source, move) {
  if (move && source === this.effectState.target) return 0;
},
onSourceAccuracyPriority: -100,
onSourceAccuracy(accuracy, target, source, move) {
  if (move && source === this.effectState.target) return true;
  return accuracy;
},
flags: {},
name: "Blindsight",
rating: 3.5,
num: -3002
}
