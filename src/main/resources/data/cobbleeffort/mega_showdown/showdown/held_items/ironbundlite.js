({
  name: "Iron Bundlite",
  spritenum: 0,
  megaStone: { "Iron Bundle": "Iron Bundle-Mega" },
  itemUser: ["Iron Bundle"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9112,
  gen: 9,
  isNonstandard: "Past",
})
