const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 - Smart Engine is Live!'));

app.get('/ahmad-dl', async (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) return res.json({ status: false, msg: "Link missing!" });

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--single-process', '--no-zygote'],
            headless: "new",
            executablePath: '/usr/bin/google-chrome-stable'
        });

        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36');
        
        // 1. Page load karo
        await page.goto(videoUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

        // 2. SMART WAIT: Jab tak video tag nazar na aaye, 10 second tak intezar karo
        try {
            await page.waitForSelector('video', { timeout: 15000 });
        } catch (e) {
            console.log("Video selector timeout");
        }

        // 3. 2-second ka extra sabr (Buffering ke liye)
        await new Promise(r => setTimeout(r, 2000));

        // 4. Link Extract karne ki Advanced Logic
        const finalUrl = await page.evaluate(() => {
            const getSrc = (el) => {
                if (!el) return null;
                return el.src && !el.src.startsWith('blob:') ? el.src : null;
            };

            // Pehle video tag check karo
            const video = document.querySelector('video');
            let src = getSrc(video);
            
            // Agar nahi mila to source tag check karo
            if (!src) {
                const source = document.querySelector('video source');
                src = getSrc(source);
            }
            
            return src;
        });

        await browser.close();

        if (finalUrl) {
            res.json({ status: true, brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", url: finalUrl });
        } else {
            res.json({ status: false, msg: "Video link detect nahi ho saka. Link shayad private hai ya expired." });
        }

    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`RDX API Live on ${PORT}`));
