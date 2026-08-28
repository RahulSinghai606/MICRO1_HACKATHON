/* Playwright tour for the Matchpoint solution video.
 * Records 1920x1080 webm + writes timings.json (audio segment start offsets).
 * Run: node docs/demo/tour.js
 */
const path = require("path");
const fs = require("fs");
const { chromium } = require("/opt/homebrew/lib/node_modules/@playwright/mcp/node_modules/playwright");

const HERE = __dirname;
const DUR = JSON.parse(fs.readFileSync(path.join(HERE, "durations.json")));
const GAP = 0.9; // seconds of silence between narration segments

const DEMO_API = `
(() => {
  if (window.__demoInstalled) return; window.__demoInstalled = true;
  const cur = document.createElement('div');
  cur.id = '__cur';
  cur.style.cssText = 'position:fixed;left:0;top:0;width:22px;height:22px;z-index:2147483647;pointer-events:none;transition:opacity .3s;';
  cur.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 2l16 8.5-7 1.5-3.5 6.5z" fill="#fff" stroke="#000" stroke-width="1.4"/></svg>';
  const attach = () => document.body && document.body.appendChild(cur);
  document.body ? attach() : addEventListener('DOMContentLoaded', attach);
  let cx = 960, cy = 900;
  const ease = t => t < .5 ? 2*t*t : 1-Math.pow(-2*t+2,2)/2;
  window.demo = {
    cursor(x, y, ms=800) {
      return new Promise(res => {
        const sx=cx, sy=cy, t0=performance.now();
        const step = now => {
          const p = Math.min(1,(now-t0)/ms), e = ease(p);
          cx = sx+(x-sx)*e; cy = sy+(y-sy)*e;
          cur.style.transform = 'translate('+cx+'px,'+cy+'px)';
          p<1 ? requestAnimationFrame(step) : res();
        };
        requestAnimationFrame(step);
      });
    },
    async click(x, y) {
      await window.demo.cursor(x, y, 700);
      const ping = document.createElement('div');
      ping.style.cssText = 'position:fixed;left:'+(x-14)+'px;top:'+(y-14)+'px;width:28px;height:28px;border:2px solid #34d399;border-radius:50%;z-index:2147483646;pointer-events:none;animation:__ping .5s ease-out forwards';
      const st = document.createElement('style');
      st.textContent = '@keyframes __ping{from{transform:scale(.4);opacity:1}to{transform:scale(1.6);opacity:0}}';
      document.head.appendChild(st); document.body.appendChild(ping);
      const el = document.elementFromPoint(x, y);
      const target = el && (el.closest('button,a,input,[role=button]') || el);
      if (target) {
        for (const type of ['mousedown','mouseup','click'])
          target.dispatchEvent(new MouseEvent(type, {bubbles:true, cancelable:true, clientX:x, clientY:y}));
      }
      setTimeout(() => ping.remove(), 600);
    },
    scrollToEl(sel, offset=0, ms=900) {
      return new Promise(res => {
        const el = document.querySelector(sel);
        if (!el) return res();
        const y0 = scrollY, y1 = el.getBoundingClientRect().top + scrollY + offset;
        const t0 = performance.now();
        const step = now => {
          const p = Math.min(1,(now-t0)/ms);
          scrollTo(0, y0+(y1-y0)*ease(p));
          p<1 ? requestAnimationFrame(step) : res();
        };
        requestAnimationFrame(step);
      });
    },
    hideCursor(){ cur.style.opacity = '0'; }
  };
})();`;

const wait = s => new Promise(r => setTimeout(r, s * 1000));

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: path.join(HERE, "rec"), size: { width: 1920, height: 1080 } },
  });
  await context.addInitScript(DEMO_API);
  const page = await context.newPage();

  const t0 = Date.now();
  const timings = {};
  const mark = name => { timings[name] = (Date.now() - t0) / 1000; console.log(name, timings[name].toFixed(1) + "s"); };
  const demo = (fn, ...args) => page.evaluate(([f, a]) => window.demo[f](...a), [fn, args]);

  // ---- S1 title -----------------------------------------------------------
  await page.goto("http://localhost:8940/docs/demo/deck.html#s1", { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  mark("s1");
  await wait(DUR.s1 + GAP);

  // ---- S2 problem ---------------------------------------------------------
  mark("s2");
  await demo("scrollToEl", "#s2", 0, 900);
  await demo("cursor", 380, 560, 900);
  await wait(6);
  await demo("cursor", 380, 760, 900);
  await wait(8);
  await demo("cursor", 1450, 500, 1000);   // over the invoice image
  await wait(DUR.s2 + GAP - 17);

  // ---- S3 baseline --------------------------------------------------------
  mark("s3");
  await demo("scrollToEl", "#s3", 0, 900);
  await demo("cursor", 350, 640, 900);
  await wait(8);
  await demo("cursor", 1100, 560, 900);    // over the misses list
  await wait(9);
  await demo("cursor", 1100, 800, 900);
  await wait(DUR.s3 + GAP - 19);

  // ---- S4 execution -------------------------------------------------------
  mark("s4");
  await demo("scrollToEl", "#s4", 0, 900);
  await demo("cursor", 380, 620, 900);     // panel 1: extraction
  await wait(14);
  await demo("cursor", 960, 620, 900);     // panel 2: tool calls
  await wait(16);
  await demo("cursor", 1560, 560, 900);    // panel 3: verifier verdict
  await wait(14);
  await demo("cursor", 1560, 860, 800);    // baseline-approved-this card
  await wait(DUR.s4 + GAP - 46);

  // ---- S5 human queue + audit packet (live artifacts) ----------------------
  mark("s5");
  await page.goto("http://localhost:8765/", { waitUntil: "load" });
  await demo("cursor", 700, 520, 900);
  await wait(3.2);
  await demo("cursor", 300, 640, 700);     // hover Approve payment button area
  await wait(2.6);
  await page.goto("http://localhost:8940/out/audit_packet_agent_final.html", { waitUntil: "load" });
  await demo("scrollToEl", "#iNIS-2025-107", -140, 1100);
  await demo("cursor", 900, 480, 900);
  await wait(DUR.s5 + GAP - 8.5);

  // ---- S6 comparison ------------------------------------------------------
  mark("s6");
  await page.goto("http://localhost:8940/docs/demo/deck.html#s6", { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await demo("cursor", 700, 480, 900);
  await wait(7);
  await demo("cursor", 1050, 610, 900);    // missed defect row
  await wait(7);
  await demo("cursor", 1500, 480, 900);    // held-out column
  await wait(DUR.s6 + GAP - 15);

  // ---- S7 changelog -------------------------------------------------------
  mark("s7");
  await demo("scrollToEl", "#s7", 0, 900);
  await demo("cursor", 500, 470, 900);
  await wait(8);
  await demo("cursor", 500, 640, 900);     // v2 tools row
  await wait(8);
  await demo("cursor", 500, 560, 800);     // removed row
  await wait(DUR.s7 + GAP - 17);

  // ---- S8 hot take / close ------------------------------------------------
  mark("s8");
  await demo("scrollToEl", "#s8", 0, 900);
  await wait(3);
  await demo("hideCursor");
  await wait(DUR.s8 + 2.5 - 3);

  fs.writeFileSync(path.join(HERE, "timings.json"), JSON.stringify(timings, null, 2));
  await context.close();   // finalizes the video
  const files = fs.readdirSync(path.join(HERE, "rec")).filter(f => f.endsWith(".webm"));
  console.log("VIDEO:", files[0], "TOTAL:", ((Date.now() - t0) / 1000).toFixed(1) + "s");
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
