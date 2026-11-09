({
  name: "Iron Treadite",
  spritenum: 0,
  megaStone: { "Iron Treads": "Iron Treads-Mega" },
  itemUser: ["Iron Treads"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9111,
  gen: 9,
  isNonstandard: "Past",
})
