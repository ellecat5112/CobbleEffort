const { chromium } = require('playwright');
// node render_fusion.js jobs.json  (serve this folder first: python3 -m http.server 8765 --bind 127.0.0.1)
// jobs: [{body_geo, body_tex, head_geo, head_tex, out}] (file paths). Renders fusions the way the Fusion add-on
// draws them (fusion.html); written by fusion/tools/preview_fusions.py.
const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
const size = Number(process.env.SIZE || 256), yaw = Number(process.env.YAW || 0), up = Number(process.env.CAM_UP || 15);
const dataUrl = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:8765/fusion.html');
  await page.waitForFunction(() => window.ready);
  for (const j of jobs) {
    const bg = JSON.parse(fs.readFileSync(j.body_geo)), hg = JSON.parse(fs.readFileSync(j.head_geo));
    const png = await page.evaluate(([a, b, c, d, s, y, u]) => window.renderFusion(a, b, c, d, s, y, u),
      [bg, dataUrl(j.body_tex), hg, dataUrl(j.head_tex), size, yaw, up]);
    fs.writeFileSync(j.out, Buffer.from(png.split(',')[1], 'base64'));
  }
  await browser.close();
})();
