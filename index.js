const express = require("express");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get("/", (req, res) => {
  res.send("🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 API - FB Reel Engine Live");
});

app.get("/fb", async (req, res) => {
  let fbUrl = req.query.url;
  if (!fbUrl) return res.json({ status: false });

  // 🔁 Desktop → Mobile (MOST IMPORTANT)
  fbUrl = fbUrl
    .replace("www.facebook.com", "m.facebook.com")
    .replace("facebook.com", "m.facebook.com");

  let browser;
  let finalVideo = null;

  try {
    browser = await puppeteer.launch({
      headless: "new",
      executablePath: "/usr/bin/google-chrome-stable",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--single-process"
      ]
    });

    const page = await browser.newPage();

    // 📱 iPhone UA = FB gives cleaner video
    await page.setUserAgent(
      "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile Safari/604.1"
    );

    // 🔥 NETWORK SNIFFING (REAL MAGIC)
    await page.setRequestInterception(true);
    page.on("request", req => req.continue());

    page.on("response", async (response) => {
      try {
        const url = response.url();
        const headers = response.headers();

        if (
          !finalVideo &&
          url.includes(".mp4") &&
          headers["content-type"]?.includes("video")
        ) {
          finalVideo = url;
        }
      } catch {}
    });

    await page.goto(fbUrl, {
      waitUntil: "networkidle2",
      timeout: 60000
    });

    // ⏳ FB reels thora late load hoti hain
    await new Promise(r => setTimeout(r, 6000));

    // 🔁 DOM fallback (agar network miss ho jaye)
    if (!finalVideo) {
      finalVideo = await page.evaluate(() => {
        const v = document.querySelector("video");
        if (v && v.src && !v.src.startsWith("blob:")) return v.src;

        const og = document.querySelector('meta[property="og:video"]');
        if (og) return og.content;

        return null;
      });
    }

    await browser.close();

    // ❌ NO ERROR MESSAGE — SILENT FAIL
    if (!finalVideo) {
      return res.json({ status: false });
    }

    // ✅ SUCCESS
    return res.json({
      status: true,
      brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
      url: finalVideo
    });

  } catch {
    if (browser) await browser.close();
    return res.json({ status: false });
  }
});

app.listen(PORT, "0.0.0.0", () =>
  console.log(`🦅 AHMAD RDX FB Engine running on ${PORT}`)
);
