({
  name: "Iron Handite",
  spritenum: 0,
  megaStone: { "Iron Hands": "Iron Hands-Mega" },
  itemUser: ["Iron Hands"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9113,
  gen: 9,
  isNonstandard: "Past",
})
