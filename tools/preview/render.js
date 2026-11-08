const { chromium } = require('playwright');
// Usage: npm install, serve this folder (python3 -m http.server 8765 --bind 127.0.0.1), then
//   node render.js <cobblemon>/common/src/main/resources ../../src/main/resources out manifest_<aspect>.json
// Renders every species in a manifest written by tools/generate.py: original vs. retextured.
const fs = require('fs'), path = require('path');
const [ref, mod, outDir, manifestFile = 'manifest_backrooms.json'] = process.argv.slice(2);
const manifest = JSON.parse(fs.readFileSync(path.resolve(__dirname, manifestFile)));
const texPath = (root, id) => { const [ns, p] = id.split(':'); return path.join(root, 'assets', ns, p); };
const modelsRoot = path.join(ref, 'assets/cobblemon/bedrock/pokemon/models');
const findModel = (id) => {
  const want = id.split(':')[1] + '.json';
  const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) { const r = walk(p); if (r) return r; } else if (e.name === want) return p; } };
  return walk(modelsRoot);
};
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:8765/index.html');
  await page.waitForFunction(() => window.ready);
  fs.mkdirSync(outDir, { recursive: true });
  for (const e of manifest) {
    const geo = JSON.parse(fs.readFileSync(findModel(e.model)));
    for (const [tag, file] of [['orig', texPath(ref, e.original)], ['new', texPath(mod, e.retextured)]]) {
      const url = 'data:image/png;base64,' + fs.readFileSync(file).toString('base64');
      const png = await page.evaluate(([g, u]) => window.renderModel(g, u, 320, 0), [geo, url]);
      fs.writeFileSync(path.join(outDir, `${e.species}_${tag}.png`), Buffer.from(png.split(',')[1], 'base64'));
    }
  }
  await browser.close();
})();
