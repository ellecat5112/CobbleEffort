({
  name: "Iron Thornite",
  spritenum: 0,
  megaStone: { "Iron Thorns": "Iron Thorns-Mega" },
  itemUser: ["Iron Thorns"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9116,
  gen: 9,
  isNonstandard: "Past",
})
