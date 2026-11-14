{
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (target !== source && move.type === 'Fire') {
    if (!this.heal(target.baseMaxhp / 4)) this.add('-immune', target, '[from] ability: Condenser');
    return null;
  }
},
flags: {breakable: 1},
name: "Condenser",
rating: 3.5,
num: -3055
}
