({
  name: "Iron Valiantite",
  spritenum: 0,
  megaStone: { "Iron Valiant": "Iron Valiant-Mega" },
  itemUser: ["Iron Valiant"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9117,
  gen: 9,
  isNonstandard: "Past",
})
