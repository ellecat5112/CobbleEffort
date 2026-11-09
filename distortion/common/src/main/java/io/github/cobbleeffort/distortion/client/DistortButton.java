package io.github.cobbleeffort.distortion.client;

import com.cobblemon.mod.common.api.moves.MoveTemplate;
import com.cobblemon.mod.common.api.moves.Moves;
import com.cobblemon.mod.common.battles.InBattleMove;
import com.cobblemon.mod.common.battles.MoveActionResponse;
import com.cobblemon.mod.common.client.gui.battle.subscreen.BattleBackButton;
import com.cobblemon.mod.common.client.gui.battle.subscreen.BattleMoveSelection;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import io.github.cobbleeffort.distortion.Distortion;
import io.github.cobbleeffort.distortion.DistortionBattle;
import io.wispforest.accessories.api.AccessoriesCapability;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import kotlin.Triple;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ItemStack;

/**
 * The Distort button on Cobblemon's move selection, next to its gimmick buttons. Shown when the trainer wears the
 * Distortion Band and the active Pokémon can distort (holds the Distortion Crystal, or is Arceus holding a plate,
 * and has Distorted forms) and hasn't yet. Toggled, the move tiles show each move's distorted twin and choosing one
 * sends the move with the "distort" gimmick.
 */
public final class DistortButton {
    public static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "textures/gui/battle/distort_button.png");
    private static final int WIDTH = 36, HEIGHT = 34;
    private static final float SCALE = 0.5F;
    private static Map<String, String> twins;

    public final float x, y;
    public final List<BattleMoveSelection.MoveTile> tiles;
    public boolean toggled;

    private DistortButton(float x, float y, List<BattleMoveSelection.MoveTile> tiles) {
        this.x = x;
        this.y = y;
        this.tiles = tiles;
    }

    /** The move -> twin table, from the jar (the same file the Showdown script is built from). */
    public static Map<String, String> twins() {
        if (twins == null) {
            try (InputStream in = DistortButton.class.getResourceAsStream("/data/" + Distortion.MOD_ID + "/distortion/move_twins.json")) {
                twins = in == null ? Collections.emptyMap()
                        : new Gson().fromJson(new InputStreamReader(in, StandardCharsets.UTF_8), new TypeToken<Map<String, String>>() {}.getType());
            } catch (Exception e) {
                twins = Collections.emptyMap();
            }
        }
        return twins;
    }

    /** A Distort button for this move selection, or null when the Pokémon can't distort now. */
    public static DistortButton create(BattleMoveSelection selection) {
        List<BattleMoveSelection.MoveTile> base = selection.getBaseTiles();
        if (base.isEmpty()) return null;
        Pokemon pokemon = base.get(0).getPokemon();
        if (pokemon == null || !canDistort(pokemon, base)) return null;
        List<BattleMoveSelection.MoveTile> tiles = new ArrayList<>();
        for (BattleMoveSelection.MoveTile tile : base) {
            tiles.add(new DistortTile(selection, tile.getMove(), tile.getX(), tile.getY()));
        }
        BattleBackButton back = selection.getBackButton();
        float x = back.getX() + BattleBackButton.WIDTH * 0.65F + 26 * selection.getGimmickButtons().size();
        return new DistortButton(x, back.getY(), tiles);
    }

    private static boolean canDistort(Pokemon pokemon, List<BattleMoveSelection.MoveTile> base) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player == null) return false;
        AccessoriesCapability capability = AccessoriesCapability.get(mc.player);
        if (capability == null || !capability.isEquipped(Distortion.BAND.get())) return false;
        ItemStack held = pokemon.heldItem();
        boolean source = held.is(Distortion.CRYSTAL.get())
                || (pokemon.getSpecies().getNationalPokedexNumber() == 493 && held.getItem().toString().endsWith("_plate"));
        if (!source) return false;
        boolean hasForm = false;
        for (FormData form : pokemon.getSpecies().getForms()) {
            if (form.getAspects().contains(DistortionBattle.ASPECT)) {
                hasForm = true;
                break;
            }
        }
        if (!hasForm) return false;
        // already distorted: its moves are twins now
        for (BattleMoveSelection.MoveTile tile : base) {
            if (twins().containsValue(tile.getMove().getId())) return false;
        }
        return true;
    }

    public boolean isHovered(double mouseX, double mouseY) {
        return mouseX >= x && mouseX <= x + WIDTH * SCALE && mouseY >= y && mouseY <= y + HEIGHT * SCALE;
    }

    public boolean toggle() {
        toggled = !toggled;
        Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.AMETHYST_BLOCK_CHIME, 1.0F));
        return toggled;
    }

    public void render(GuiGraphics graphics, int mouseX, int mouseY) {
        graphics.pose().pushPose();
        graphics.pose().scale(SCALE, SCALE, 1F);
        int v = (toggled || isHovered(mouseX, mouseY)) ? HEIGHT : 0;
        graphics.blit(TEXTURE, Math.round(x * 2), Math.round(y * 2), 0, v, WIDTH, HEIGHT, WIDTH, HEIGHT * 2);
        graphics.pose().popPose();
    }

    /** A move tile showing the move's distorted twin; choosing it distorts. */
    public static final class DistortTile extends BattleMoveSelection.MoveTile {
        public DistortTile(BattleMoveSelection selection, InBattleMove move, float x, float y) {
            super(selection, move, x, y);
            String twin = twins().get(move.getId());
            if (twin != null) {
                MoveTemplate template = Moves.getByNameOrDummy(twin);
                setMoveTemplate(template);
                int hue = template.getElementalType().getHue();
                setRgb(new Triple<>(((hue >> 16) & 255) / 255.0, ((hue >> 8) & 255) / 255.0, (hue & 255) / 255.0));
            }
        }

        @Override
        public MoveActionResponse getResponse() {
            return new MoveActionResponse(getMove().getId(), getTargetPnx(), DistortionBattle.GIMMICK);
        }
    }
}
