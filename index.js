const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 - Super-Lite is Live!'));

app.get('/ahmad-dl', async (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) return res.json({ status: false, msg: "Link missing!" });

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--single-process'],
            headless: "new",
            executablePath: '/usr/bin/google-chrome-stable' // Points to the Docker Chrome
        });

        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36');
        
        await page.goto(videoUrl, { waitUntil: 'networkidle2', timeout: 60000 });
        const finalUrl = await page.evaluate(() => document.querySelector('video')?.src);

        await browser.close();
        res.json({ status: true, brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", url: finalUrl });
    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`RDX API Live on ${PORT}`));
