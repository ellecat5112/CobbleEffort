{
onModifyMovePriority: -1,
onModifyMove(move) {
  if (move.type === 'Grass') move.forceSTAB = true;
},
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (target !== source && (move.flags['powder'] || move.id === 'leechseed')) {
    this.add('-immune', target, '[from] ability: Paleomycelium');
    return null;
  }
},
flags: {breakable: 1},
name: "Paleomycelium",
rating: 3,
num: -3004
}
