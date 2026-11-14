{
num: -3047,
accuracy: 100,
basePower: 80,
category: "Special",
name: "Effervescent Roar",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, sound: 1, bypasssub: 1, metronome: 1},
onAfterMove(source) {
  if (source.side.pokemon.some(ally => ally.status)) {
    this.add('-activate', source, 'move: Aromatherapy');
    for (const ally of source.side.pokemon) ally.cureStatus();
  }
  for (const side of source.side.foeSidesWithConditions()) side.addSideCondition('effervescentroar', source);
},
condition: {
  duration: 3,
  onSideStart(side) {
    this.add('-sidestart', side, 'move: Effervescent Roar');
  },
  onResidualOrder: 5,
  onResidualSubOrder: 1,
  onResidual(target) {
    this.damage(target.baseMaxhp / 16, target, null, this.dex.conditions.get('effervescentroar'));
  },
  onSideResidualOrder: 26,
  onSideResidualSubOrder: 13,
  onSideEnd(side) {
    this.add('-sideend', side, 'move: Effervescent Roar');
  }
},
secondary: null,
target: "allAdjacentFoes",
type: "Dragon",
desc: "Hits all adjacent foes and cures the status of every Pokemon in the user's party. For 3 turns, sparkling bubbles on the opposing side deal 1/16 of their maximum HP to each opposing Pokemon at the end of every turn.",
shortDesc: "Hits foes, cures party status; 3 turns of 1/16 residual on foes.",
contestType: "Beautiful"
}
