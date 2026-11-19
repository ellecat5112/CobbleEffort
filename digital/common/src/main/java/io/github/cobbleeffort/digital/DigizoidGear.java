package io.github.cobbleeffort.digital;

import dev.architectury.event.EventResult;
import dev.architectury.event.events.common.EntityEvent;
import dev.architectury.event.events.common.TickEvent;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.ChatFormatting;
import net.minecraft.Util;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Chrome Digizoid gear, the tier above Netherite, in four lore metals (smithing: a Netherite piece + a coloured
 * Digizoid Ingot + the Digizoid Upgrade template):
 * Red Digizoid: the heaviest armor (most defense, strong knockback resistance) and the hardest-hitting sword.
 * Blue Digizoid: light armor (each piece +4% speed) and a quick sword (much faster attacks).
 * Gold Digizoid: wearing two or more pieces reflects a third of projectiles back and takes a quarter less magic/beam
 * damage.
 * Black Digizoid: with the full set, sneaking while sprinting phases you six blocks ahead; the sword blinks you where
 * you look (right-click). Both have a cooldown.
 */
public final class DigizoidGear {
    public enum Metal {
        RED(new int[]{4, 7, 9, 4}, 4.0F, 0.3F, 5, -2.6F),
        BLUE(new int[]{3, 6, 8, 3}, 3.0F, 0.1F, 3, -1.6F),
        GOLD(new int[]{3, 7, 8, 3}, 3.5F, 0.15F, 4, -2.4F),
        BLACK(new int[]{3, 6, 8, 3}, 3.0F, 0.1F, 4, -2.3F);

        final int[] defense;     // boots, leggings, chestplate, helmet
        final float toughness, knockback, attackSpeed;
        final int damage;

        Metal(int[] defense, float toughness, float knockback, int damage, float attackSpeed) {
            this.defense = defense;
            this.toughness = toughness;
            this.knockback = knockback;
            this.damage = damage;
            this.attackSpeed = attackSpeed;
        }

        public String id() {
            return name().toLowerCase(java.util.Locale.ROOT) + "_digizoid";
        }
    }

    public static final DeferredRegister<ArmorMaterial> MATERIALS = DeferredRegister.create(Digital.MOD_ID, Registries.ARMOR_MATERIAL);
    public static final Map<Metal, RegistrySupplier<ArmorMaterial>> MATERIAL = new EnumMap<>(Metal.class);
    public static final Map<Metal, List<RegistrySupplier<Item>>> ARMOR = new EnumMap<>(Metal.class);
    public static final Map<Metal, RegistrySupplier<Item>> SWORDS = new EnumMap<>(Metal.class);
    public static final Map<Metal, RegistrySupplier<Item>> INGOTS = new EnumMap<>(Metal.class);
    public static RegistrySupplier<Item> TEMPLATE;
    private static final Map<UUID, Long> COOLDOWN = new HashMap<>();
    private static final Map<UUID, Boolean> WAS_SNEAKING = new HashMap<>();
    private static boolean rehurting;

    private DigizoidGear() {
    }

    record DigizoidTier(Metal metal) implements Tier {
        @Override
        public int getUses() {
            return 2600;
        }

        @Override
        public float getSpeed() {
            return 10F;
        }

        @Override
        public float getAttackDamageBonus() {
            return metal.damage;
        }

        @Override
        public net.minecraft.tags.TagKey<Block> getIncorrectBlocksForDrops() {
            return BlockTags.INCORRECT_FOR_NETHERITE_TOOL;
        }

        @Override
        public int getEnchantmentValue() {
            return 16;
        }

        @Override
        public Ingredient getRepairIngredient() {
            return Ingredient.of(INGOTS.get(metal).get());
        }
    }

    /** Called from Digital's static setup, before the registers register. */
    static void register(java.util.function.BiFunction<String, java.util.function.Supplier<Item>, RegistrySupplier<Item>> item) {
        TEMPLATE = item.apply("digizoid_upgrade_smithing_template", () -> new TooltipItem(new Item.Properties().rarity(Rarity.RARE)));
        for (Metal m : Metal.values()) {
            INGOTS.put(m, item.apply(m.id() + "_ingot", () -> new Item(new Item.Properties().rarity(Rarity.EPIC))));
            RegistrySupplier<ArmorMaterial> mat = MATERIALS.register(m.id(), () -> new ArmorMaterial(
                    Util.make(new EnumMap<>(ArmorItem.Type.class), map -> {
                        map.put(ArmorItem.Type.BOOTS, m.defense[0]);
                        map.put(ArmorItem.Type.LEGGINGS, m.defense[1]);
                        map.put(ArmorItem.Type.CHESTPLATE, m.defense[2]);
                        map.put(ArmorItem.Type.HELMET, m.defense[3]);
                        map.put(ArmorItem.Type.BODY, m.defense[2]);
                    }), 16, SoundEvents.ARMOR_EQUIP_NETHERITE, () -> Ingredient.of(INGOTS.get(m).get()),
                    List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, m.id()))), m.toughness, m.knockback));
            MATERIAL.put(m, mat);
            List<RegistrySupplier<Item>> pieces = new ArrayList<>();
            for (ArmorItem.Type type : new ArmorItem.Type[]{ArmorItem.Type.HELMET, ArmorItem.Type.CHESTPLATE, ArmorItem.Type.LEGGINGS, ArmorItem.Type.BOOTS}) {
                pieces.add(item.apply(m.id() + "_" + type.getName(), () -> {
                    Item.Properties p = new Item.Properties().fireResistant().rarity(Rarity.EPIC)
                            .durability(type.getDurability(42));
                    if (m == Metal.BLUE) p = p.attributes(blueArmor(type));
                    return new GearArmor(mat, type, p, m);
                }));
            }
            ARMOR.put(m, pieces);
            SWORDS.put(m, item.apply(m.id() + "_sword", () -> new GearSword(new DigizoidTier(m), new Item.Properties().fireResistant().rarity(Rarity.EPIC)
                    .attributes(SwordItem.createAttributes(new DigizoidTier(m), 3, m.attackSpeed)), m)));
        }
    }

    static ItemAttributeModifiers blueArmor(ArmorItem.Type type) {
        // vanilla armor modifiers come from the material; ours adds speed on top
        EquipmentSlotGroup group = EquipmentSlotGroup.bySlot(type.getSlot());
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, "blue_digizoid_" + type.getName());
        Metal m = Metal.BLUE;
        int def = switch (type) {
            case BOOTS -> m.defense[0];
            case LEGGINGS -> m.defense[1];
            case HELMET -> m.defense[3];
            default -> m.defense[2];
        };
        return ItemAttributeModifiers.builder()
                .add(Attributes.ARMOR, new AttributeModifier(id.withSuffix("_armor"), def, AttributeModifier.Operation.ADD_VALUE), group)
                .add(Attributes.ARMOR_TOUGHNESS, new AttributeModifier(id.withSuffix("_toughness"), m.toughness, AttributeModifier.Operation.ADD_VALUE), group)
                .add(Attributes.KNOCKBACK_RESISTANCE, new AttributeModifier(id.withSuffix("_knockback"), m.knockback, AttributeModifier.Operation.ADD_VALUE), group)
                .add(Attributes.MOVEMENT_SPEED, new AttributeModifier(id.withSuffix("_speed"), 0.04, AttributeModifier.Operation.ADD_MULTIPLIED_BASE), group)
                .build();
    }

    static class GearArmor extends ArmorItem {
        final Metal metal;

        GearArmor(Holder<ArmorMaterial> material, Type type, Properties properties, Metal metal) {
            super(material, type, properties);
            this.metal = metal;
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            lines.add(Component.translatable(Digital.MOD_ID + ".gear." + metal.id()).withStyle(ChatFormatting.AQUA));
        }
    }

    static class GearSword extends SwordItem {
        final Metal metal;

        GearSword(Tier tier, Properties properties, Metal metal) {
            super(tier, properties);
            this.metal = metal;
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (metal != Metal.BLACK) return InteractionResultHolder.pass(stack);
            if (!level.isClientSide && player instanceof ServerPlayer sp && blink(sp, 8)) {
                player.getCooldowns().addCooldown(this, 60);
                stack.hurtAndBreak(1, player, hand == InteractionHand.MAIN_HAND ? EquipmentSlot.MAINHAND : EquipmentSlot.OFFHAND);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            lines.add(Component.translatable(Digital.MOD_ID + ".gear." + metal.id() + "_sword").withStyle(ChatFormatting.AQUA));
        }
    }

    static int pieces(Player p, Metal m) {
        int n = 0;
        for (ItemStack s : p.getArmorSlots()) if (s.getItem() instanceof GearArmor g && g.metal == m) n++;
        return n;
    }

    /** Phases the player up to `reach` blocks along where they look, to the last open spot. */
    static boolean blink(ServerPlayer p, int reach) {
        ServerLevel level = p.serverLevel();
        Vec3 eye = p.getEyePosition(), look = p.getLookAngle();
        HitResult hit = level.clip(new net.minecraft.world.level.ClipContext(eye, eye.add(look.scale(reach)),
                net.minecraft.world.level.ClipContext.Block.COLLIDER, net.minecraft.world.level.ClipContext.Fluid.NONE, p));
        Vec3 to = hit.getType() == HitResult.Type.BLOCK ? hit.getLocation().subtract(look.scale(0.6)) : eye.add(look.scale(reach));
        BlockPos feet = BlockPos.containing(to.x, to.y - 1.4, to.z);
        if (!level.getBlockState(feet).getCollisionShape(level, feet).isEmpty()) feet = feet.above();
        if (!level.getBlockState(feet).getCollisionShape(level, feet).isEmpty()
                || !level.getBlockState(feet.above()).getCollisionShape(level, feet.above()).isEmpty()) return false;
        level.sendParticles(ParticleTypes.PORTAL, p.getX(), p.getY() + 1, p.getZ(), 40, 0.3, 0.6, 0.3, 0.2);
        p.teleportTo(feet.getX() + 0.5, feet.getY(), feet.getZ() + 0.5);
        level.sendParticles(ParticleTypes.REVERSE_PORTAL, p.getX(), p.getY() + 1, p.getZ(), 40, 0.3, 0.6, 0.3, 0.1);
        level.playSound(null, p.blockPosition(), SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 0.7F, 1.6F);
        return true;
    }

    static void init() {
        MATERIALS.register();
        EntityEvent.LIVING_HURT.register((entity, source, amount) -> {
            if (!(entity instanceof Player p) || p.level().isClientSide || rehurting) return EventResult.pass();
            if (pieces(p, Metal.GOLD) >= 2 && reduce(p, source, amount) < amount) {
                rehurting = true;
                try {
                    p.hurt(source, reduce(p, source, amount));
                } finally {
                    rehurting = false;
                }
                return EventResult.interruptFalse();
            }
            if (pieces(p, Metal.GOLD) >= 2) {
                if (source.getDirectEntity() instanceof Projectile proj && p.getRandom().nextFloat() < 0.34F) {
                    proj.setDeltaMovement(proj.getDeltaMovement().scale(-1));
                    proj.setOwner(p);
                    p.level().playSound(null, p.blockPosition(), SoundEvents.SHIELD_BLOCK, SoundSource.PLAYERS, 0.8F, 1.4F);
                    return EventResult.interruptFalse();
                }
            }
            return EventResult.pass();
        });
        TickEvent.PLAYER_POST.register(player -> {
            if (!(player instanceof ServerPlayer sp)) return;
            boolean sneak = sp.isShiftKeyDown(), was = WAS_SNEAKING.getOrDefault(sp.getUUID(), false);
            WAS_SNEAKING.put(sp.getUUID(), sneak);
            if (sneak && !was && sp.isSprinting() && pieces(sp, Metal.BLACK) == 4) {
                long now = sp.serverLevel().getGameTime();
                Long cd = COOLDOWN.get(sp.getUUID());
                if (cd == null || now >= cd) {
                    if (blink(sp, 6)) COOLDOWN.put(sp.getUUID(), now + 100);
                }
            }
        });
    }

    /** Gold Digizoid: a quarter less magic and beam (indirect magic, sonic, explosion) damage. */
    static float reduce(Player p, DamageSource source, float amount) {
        if (pieces(p, Metal.GOLD) >= 2 && (source.is(DamageTypeTags.WITCH_RESISTANT_TO) || source.is(DamageTypeTags.IS_EXPLOSION))) {
            return amount * 0.75F;
        }
        return amount;
    }
}
