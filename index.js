const express = require("express");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get("/", (req, res) => {
  res.send("🦅 AHMAD RDX DOWNLOADER API is LIVE");
});

/**
 * 🔥 FACEBOOK + INSTAGRAM DOWNLOADER
 * Usage:
 * /dl?url=VIDEO_LINK
 */
app.get("/dl", async (req, res) => {
  let url = req.query.url;
  if (!url) {
    return res.json({ status: false, msg: "Video URL missing" });
  }

  // 🔁 Facebook desktop → mobile (BEST bypass)
  if (url.includes("facebook.com") && !url.includes("m.facebook.com")) {
    url = url.replace("facebook.com", "m.facebook.com");
  }

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: "new",
      executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || "/usr/bin/google-chrome-stable",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--single-process"
      ]
    });

    const page = await browser.newPage();

    // 📱 Mobile UA (FB + IG both)
    await page.setUserAgent(
      "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile Safari/604.1"
    );

    await page.goto(url, {
      waitUntil: "networkidle2",
      timeout: 60000
    });

    await new Promise(r => setTimeout(r, 5000));

    const videoUrl = await page.evaluate(() => {
      // 1️⃣ direct video
      const v = document.querySelector("video");
      if (v && v.src && !v.src.startsWith("blob:")) return v.src;

      // 2️⃣ og:video
      const og = document.querySelector('meta[property="og:video"]');
      if (og) return og.content;

      // 3️⃣ source tags
      const sources = document.querySelectorAll("video source");
      for (let s of sources) {
        if (s.src && !s.src.startsWith("blob:")) return s.src;
      }

      // 4️⃣ mp4 links
      const links = document.querySelectorAll('a[href*=".mp4"]');
      for (let a of links) {
        return a.href;
      }

      return null;
    });

    await browser.close();

    if (!videoUrl) {
      return res.json({
        status: false,
        msg: "Video link blocked (proxy needed)"
      });
    }

    res.json({
      status: true,
      brand: "AHMAD RDX",
      url: videoUrl
    });

  } catch (err) {
    if (browser) await browser.close();
    res.json({ status: false, error: err.message });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log("RDX API running on port", PORT);
});
