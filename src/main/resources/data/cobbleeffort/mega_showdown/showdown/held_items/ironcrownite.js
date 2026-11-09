({
  name: "Iron Crownite",
  spritenum: 0,
  megaStone: { "Iron Crown": "Iron Crown-Mega" },
  itemUser: ["Iron Crown"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9121,
  gen: 9,
  isNonstandard: "Past",
})
