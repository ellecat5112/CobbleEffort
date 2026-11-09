({
  name: "Flutter Manite",
  spritenum: 0,
  megaStone: { "Flutter Mane": "Flutter Mane-Mega" },
  itemUser: ["Flutter Mane"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9103,
  gen: 9,
  isNonstandard: "Past",
})
