{
num: -3004,
accuracy: true,
basePower: 0,
category: "Status",
name: "Devonian Drift",
pp: 15,
priority: 0,
flags: {reflectable: 1, metronome: 1},
sideCondition: "devoniandrift",
condition: {
  duration: 5,
  onSideStart(side) {
    this.add('-sidestart', side, 'move: Devonian Drift');
  },
  onResidualOrder: 5,
  onResidualSubOrder: 1,
  onResidual(target) {
    if (target.hasType('Poison') || target.hasType('Steel') || !target.isGrounded()) return;
    this.damage(target.baseMaxhp / 8, target, null, this.dex.conditions.get('devoniandrift'));
    this.boost({spe: -1}, target, null, null, true);
  },
  onSideResidualOrder: 26,
  onSideResidualSubOrder: 12,
  onSideEnd(side) {
    this.add('-sideend', side, 'move: Devonian Drift');
  }
},
secondary: null,
target: "foeSide",
type: "Poison",
desc: "For 5 turns, heavy ancient spores cover the opposing side: at the end of each turn, every grounded opponent that is not Poison or Steel type loses 1/8 of its maximum HP and its Speed falls by 1 stage.",
shortDesc: "5 turns: grounded non-Poison/Steel foes lose 1/8 HP and -1 Spe each turn.",
contestType: "Clever"
}
