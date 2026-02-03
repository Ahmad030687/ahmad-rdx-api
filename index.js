const express = require("express");
const axios = require("axios");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get("/", (req, res) => {
  res.send("🦅 AHMAD RDX FB API LIVE");
});

// 🔥 MAIN DOWNLOAD ROUTE
app.get("/dl", async (req, res) => {
  let inputUrl = req.query.url;
  if (!inputUrl) return res.json({ status: false, msg: "URL missing" });

  try {
    // 🔹 STEP 1: Resolve share/redirect link
    const head = await axios.get(inputUrl, {
      maxRedirects: 5,
      headers: {
        "User-Agent":
          "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)",
      },
    });

    let finalUrl = head.request.res.responseUrl;

    // 🔹 Force mobile
    finalUrl = finalUrl.replace("www.facebook.com", "m.facebook.com");

    // 🔹 STEP 2: Puppeteer
    const browser = await puppeteer.launch({
      headless: "new",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
      ],
      executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || "/usr/bin/google-chrome-stable",
    });

    const page = await browser.newPage();
    await page.setUserAgent(
      "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)"
    );

    await page.goto(finalUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(4000);

    const videoUrl = await page.evaluate(() => {
      const v = document.querySelector("video");
      if (v && v.src && !v.src.startsWith("blob")) return v.src;

      const og = document.querySelector('meta[property="og:video"]');
      if (og) return og.content;

      return null;
    });

    await browser.close();

    if (!videoUrl) {
      return res.json({
        status: false,
        msg: "Video not found (FB blocked IP)",
      });
    }

    return res.json({
      status: true,
      brand: "AHMAD RDX",
      url: videoUrl,
    });
  } catch (e) {
    return res.json({
      status: false,
      error: e.message,
    });
  }
});

app.listen(PORT, "0.0.0.0", () =>
  console.log("AHMAD RDX API RUNNING on", PORT)
);
