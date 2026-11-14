package io.github.cobbleeffort.kanto.client;

import dev.architectury.networking.NetworkManager;
import io.github.cobbleeffort.kanto.Kanto;
import io.github.cobbleeffort.kanto.Spawners;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.CycleButton;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.components.MultiLineEditBox;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;

import java.util.ArrayList;
import java.util.List;

/** The spawners' settings screen (like a command block's): text fields, on/off buttons, Done and Cancel. */
public final class SpawnerScreen extends Screen {
    private static final String K = Kanto.MOD_ID + ".spawner.";
    private final BlockPos pos;
    private final boolean trainer;
    private final CompoundTag config;
    private final List<Object[]> labels = new ArrayList<>();             // {text, x, y}

    private EditBox pokemon, name, level, scale, skin, skill;
    private MultiLineEditBox team;

    SpawnerScreen(BlockPos pos, boolean trainer, CompoundTag config) {
        super(Component.translatable(K + (trainer ? "trainer" : "pokemon") + ".title"));
        this.pos = pos;
        this.trainer = trainer;
        this.config = config.copy();
        if (!config.contains("level")) this.config.putInt("level", 50);
        if (!config.contains("scale")) this.config.putFloat("scale", 1F);
        if (!config.contains("skill")) this.config.putInt("skill", 3);
    }

    private EditBox box(int x, int y, int w, String label, String value, int max) {
        EditBox b = new EditBox(font, x, y, w, 18, Component.translatable(K + label));
        b.setMaxLength(max);
        b.setValue(value);
        addRenderableWidget(b);
        labels.add(new Object[]{Component.translatable(K + label), x, y - 11});
        return b;
    }

    private void toggle(int x, int y, int w, String key) {
        addRenderableWidget(CycleButton.onOffBuilder(config.getBoolean(key))
                .create(x, y, w, 20, Component.translatable(K + key), (button, value) -> config.putBoolean(key, value)));
    }

    @Override
    protected void init() {
        labels.clear();
        int w = Math.min(360, width - 20), x = (width - w) / 2, y = 34;
        int half = (w - 6) / 2, quarter = (w - 18) / 4;
        if (trainer) {
            name = box(x, y, half, "name", config.getString("name"), 64);
            skin = box(x + half + 6, y, quarter, "skin", config.getString("skin"), 16);
            level = box(x + half + quarter + 12, y, (quarter - 6) / 2 + 3, "level", String.valueOf(config.getInt("level")), 3);
            skill = box(x + w - (quarter - 6) / 2 - 3, y, (quarter - 6) / 2 + 3, "skill", String.valueOf(config.getInt("skill")), 1);
            y += 34;
            team = new MultiLineEditBox(font, x, y, w, 88, Component.translatable(K + "team.hint"), Component.translatable(K + "team"));
            team.setCharacterLimit(4000);
            team.setValue(config.getString("team"));
            addRenderableWidget(team);
            labels.add(new Object[]{Component.translatable(K + "team"), x, y - 11});
            y += 96;
            toggle(x, y, half, "battle");
            toggle(x + half + 6, y, half, "doubles");
            y += 24;
            toggle(x, y, half, "despawn");
            toggle(x + half + 6, y, half, "one");
        } else {
            pokemon = box(x, y, w, "pokemon", config.getString("pokemon"), 1000);
            y += 34;
            name = box(x, y, half, "name", config.getString("name"), 64);
            level = box(x + half + 6, y, quarter, "level", String.valueOf(config.getInt("level")), 3);
            scale = box(x + half + quarter + 12, y, w - half - quarter - 12, "scale", String.valueOf(config.getFloat("scale")), 5);
            y += 30;
            toggle(x, y, half, "uncatchable");
            toggle(x + half + 6, y, half, "glowing");
            y += 24;
            toggle(x, y, half, "battle");
            toggle(x + half + 6, y, half, "one");
        }
        y += 32;
        addRenderableWidget(Button.builder(Component.translatable("gui.done"), b -> save()).bounds(x, y, half, 20).build());
        addRenderableWidget(Button.builder(Component.translatable("gui.cancel"), b -> onClose()).bounds(x + half + 6, y, half, 20).build());
    }

    private static int number(EditBox b, int fallback) {
        try {
            return Integer.parseInt(b.getValue().trim());
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    private void save() {
        config.putString("name", name.getValue());
        config.putInt("level", number(level, 50));
        if (trainer) {
            config.putString("skin", skin.getValue());
            config.putInt("skill", number(skill, 3));
            config.putString("team", team.getValue());
        } else {
            config.putString("pokemon", pokemon.getValue());
            try {
                config.putFloat("scale", Float.parseFloat(scale.getValue().trim()));
            } catch (NumberFormatException e) {
                config.putFloat("scale", 1F);
            }
        }
        NetworkManager.sendToServer(new Spawners.SavePacket(pos, config));
        onClose();
    }

    @Override
    public void render(GuiGraphics g, int mouseX, int mouseY, float partial) {
        super.render(g, mouseX, mouseY, partial);
        g.drawCenteredString(font, title, width / 2, 8, 0xFFFFFF);
        g.drawCenteredString(font, Component.translatable(K + (trainer ? "trainer" : "pokemon") + ".help"), width / 2, 19, 0xA0A0A0);
        for (Object[] l : labels) g.drawString(font, (Component) l[0], (int) l[1], (int) l[2], 0xE0E0E0);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    /** Opens the screen for the spawner at pos with the settings the client has (synced from the block entity). */
    static void open(BlockPos pos, boolean trainer) {
        Minecraft mc = Minecraft.getInstance();
        CompoundTag config = mc.level != null && mc.level.getBlockEntity(pos) instanceof Spawners.SpawnerBlockEntity be
                ? be.config() : new CompoundTag();
        mc.setScreen(new SpawnerScreen(pos, trainer, config));
    }
}
