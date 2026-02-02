const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 IS LIVE!'));

app.get('/ahmad-dl', async (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) return res.json({ status: false, msg: "Link kahan hai jani?" });

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            headless: "new",
            executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || null
        });

        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36');
        
        await page.goto(videoUrl, { waitUntil: 'networkidle2', timeout: 60000 });

        // Asli Video Link nikalne ki koshish
        const finalUrl = await page.evaluate(() => {
            const video = document.querySelector('video');
            return video ? video.src : null;
        });

        await browser.close();
        
        if (finalUrl) {
            res.json({ status: true, brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", url: finalUrl });
        } else {
            res.json({ status: false, msg: "Video link detect nahi ho saka." });
        }
    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, () => console.log(`RDX API live on ${PORT}`));
                      
