({
  name: "Scream Tailite",
  spritenum: 0,
  megaStone: { "Scream Tail": "Scream Tail-Mega" },
  itemUser: ["Scream Tail"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9101,
  gen: 9,
  isNonstandard: "Past",
})
