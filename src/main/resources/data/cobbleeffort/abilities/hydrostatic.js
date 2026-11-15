{
onModifyMovePriority: -1,
onModifyMove(move) {
  if (move.type === 'Water') move.forceSTAB = true;
},
flags: {},
name: "Hydrostatic",
rating: 3,
num: -3071
}
