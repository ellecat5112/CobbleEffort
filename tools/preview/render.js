const { chromium } = require('playwright');
// Usage: npm install, serve this folder (python3 -m http.server 8765 --bind 127.0.0.1), then
//   node render.js <cobblemon>/common/src/main/resources ../../src/main/resources out manifest_<aspect>.json
// Renders every species in a manifest written by tools/generate.py: original vs. retextured.
const fs = require('fs'), path = require('path');
const [ref, mod, outDir, manifestFile = 'manifest_backrooms.json'] = process.argv.slice(2);
const size = Number(process.env.SIZE || 320);  // render size in px
const manifest = JSON.parse(fs.readFileSync(path.resolve(__dirname, manifestFile)));
// EXTRA_ROOTS (":"-separated resource roots, top-most first) are other mods' extracted jars, e.g. Mega Showdown for
// its megas or Baby Legends for a painted member's model. Read for previews only, never shipped.
const extraRoots = (process.env.EXTRA_ROOTS || '').split(':').filter(Boolean);
const texPath = (root, id) => {
  const [ns, p] = id.split(':');
  for (const r of (root === ref ? [...extraRoots, ref] : [root])) {
    const f = path.join(r, 'assets', ns, p);
    if (fs.existsSync(f)) return f;
  }
  throw new Error('texture not found: ' + id);
};
const yaw = Number(process.env.YAW || 0);       // turn the model (degrees)
const camUp = Number(process.env.CAM_UP || 15); // camera height above the model's centre (higher: seen from above)
// model folders: Cobblemon's, this mod's, plus EXTRA_MODEL_ROOTS (":"-separated) for other mods' models,
// e.g. an addon line's model (read for previews only, never shipped)
const cobblemonModels = [...extraRoots.map(r => path.join(r, 'assets/cobblemon/bedrock/pokemon/models')),
                         path.join(ref, 'assets/cobblemon/bedrock/pokemon/models'),
                         ...(process.env.EXTRA_MODEL_ROOTS || '').split(':').filter(Boolean)];
const modModels = [path.join(mod, 'assets/cobbleeffort/bedrock/pokemon/models')];
const findModel = (id) => {
  const want = id.split(':')[1] + '.json';
  const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) { const r = walk(p); if (r) return r; } else if (e.name === want) return p; } };
  for (const r of (id.startsWith('cobbleeffort:') ? modModels : cobblemonModels)) {
    const found = fs.existsSync(r) && walk(r);
    if (found) return found;
  }
  throw new Error('model not found: ' + id);
};
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:8765/index.html');
  await page.waitForFunction(() => window.ready);
  fs.mkdirSync(outDir, { recursive: true });
  for (const e of manifest) {
    const geoOrig = JSON.parse(fs.readFileSync(findModel(e.model)));
    // sprite collections swap the model too (tools/sprites.py)
    const geoNew = e.retextured_model ? JSON.parse(fs.readFileSync(findModel(e.retextured_model))) : geoOrig;
    const dataUrl = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
    for (const [tag, root, key] of [['orig', ref, 'original'], ['new', mod, 'retextured']]) {
      if (!e[key]) continue;   // e.g. an addon line has no Cobblemon original
      const url = dataUrl(texPath(root, e[key]));
      const layers = (e.layers || []).filter(l => l[key]).map(l => ({ url: dataUrl(texPath(root, l[key])), emissive: l.emissive }));
      const geo = tag === 'new' ? geoNew : geoOrig;
      const png = await page.evaluate(([g, u, ls, sz, yw, up]) => window.renderModel(g, u, sz, yw, ls, up), [geo, url, layers, size, yaw, camUp]);
      fs.writeFileSync(path.join(outDir, `${e.species}${e.form ? '_' + e.form : ''}_${tag}.png`), Buffer.from(png.split(',')[1], 'base64'));
    }
  }
  await browser.close();
})();
