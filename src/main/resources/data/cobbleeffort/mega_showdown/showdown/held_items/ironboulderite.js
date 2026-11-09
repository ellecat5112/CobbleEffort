({
  name: "Iron Boulderite",
  spritenum: 0,
  megaStone: { "Iron Boulder": "Iron Boulder-Mega" },
  itemUser: ["Iron Boulder"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9120,
  gen: 9,
  isNonstandard: "Past",
})
