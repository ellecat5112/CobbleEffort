({
  name: "Iron Leafite",
  spritenum: 0,
  megaStone: { "Iron Leaves": "Iron Leaves-Mega" },
  itemUser: ["Iron Leaves"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9119,
  gen: 9,
  isNonstandard: "Past",
})
