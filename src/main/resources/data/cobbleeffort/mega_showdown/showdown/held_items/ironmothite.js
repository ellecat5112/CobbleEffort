({
  name: "Iron Mothite",
  spritenum: 0,
  megaStone: { "Iron Moth": "Iron Moth-Mega" },
  itemUser: ["Iron Moth"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9115,
  gen: 9,
  isNonstandard: "Past",
})
