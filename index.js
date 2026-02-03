const express = require("express");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 10000;

app.get("/", (req, res) => {
  res.send("🦅 AHMAD RDX API – FB/IG Downloader LIVE");
});

app.get("/dl", async (req, res) => {
  let url = req.query.url;
  if (!url) return res.json({ status: false });

  // Force mobile
  url = url.replace("www.facebook.com", "m.facebook.com");

  try {
    const html = await axios.get(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
        "Accept-Language": "en-US,en;q=0.9"
      }
    });

    const match = html.data.match(/"browser_native_sd_url":"([^"]+)"/)
      || html.data.match(/"browser_native_hd_url":"([^"]+)"/);

    if (!match) return res.json({ status: false });

    const video = match[1].replace(/\\u0025/g, "%").replace(/\\/g, "");

    res.json({
      status: true,
      brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
      url: video
    });

  } catch {
    res.json({ status: false });
  }
});

app.listen(PORT, "0.0.0.0");
