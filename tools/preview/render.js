const { chromium } = require('playwright');
// Usage: npm install, serve this folder (python3 -m http.server 8765 --bind 127.0.0.1), then
//   node render.js <cobblemon>/common/src/main/resources ../../src/main/resources out
const fs = require('fs'), path = require('path');
const [ref, mod, outDir] = process.argv.slice(2);
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'backrooms_species.json')));
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  page.on('console', m => console.log('page:', m.text()));
  await page.goto('http://127.0.0.1:8765/index.html');
  await page.waitForFunction(() => window.ready);
  fs.mkdirSync(outDir, { recursive: true });
  const yaw = Number(process.env.YAW || 0);
  for (const e of cfg.species) {
    const geo = JSON.parse(fs.readFileSync(path.join(ref, 'assets/cobblemon/bedrock/pokemon/models', e.folder, e.species + '.geo.json')));
    for (const [tag, file] of [['orig', path.join(ref, 'assets/cobblemon/textures/pokemon', e.folder, e.species + '.png')],
                               ['still', path.join(mod, 'assets/cobbleeffort/textures/pokemon/backrooms', e.folder, e.species + '_backrooms.png')]]) {
      const url = 'data:image/png;base64,' + fs.readFileSync(file).toString('base64');
      const png = await page.evaluate(([g, u, y]) => window.renderModel(g, u, 320, y), [geo, url, yaw]);
      fs.writeFileSync(path.join(outDir, `${e.species}_${tag}.png`), Buffer.from(png.split(',')[1], 'base64'));
    }
  }
  await browser.close();
})();
