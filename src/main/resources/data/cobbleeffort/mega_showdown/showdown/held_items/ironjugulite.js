({
  name: "Iron Jugulite",
  spritenum: 0,
  megaStone: { "Iron Jugulis": "Iron Jugulis-Mega" },
  itemUser: ["Iron Jugulis"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9114,
  gen: 9,
  isNonstandard: "Past",
})
