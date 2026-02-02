const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 - Render Engine is Live!'));

app.get('/ahmad-dl', async (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) return res.json({ status: false, msg: "Link missing hai!" });

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            headless: "new",
            executablePath: '/usr/bin/google-chrome-stable' // Render Docker path
        });

        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36');
        
        await page.goto(videoUrl, { waitUntil: 'networkidle2', timeout: 60000 });

        const finalUrl = await page.evaluate(() => {
            return document.querySelector('video')?.src;
        });

        await browser.close();
        res.json({ status: true, brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", url: finalUrl });

    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, () => console.log(`Server started on ${PORT}`));
