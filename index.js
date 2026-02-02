const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 - Mobile Bypass Active!'));

app.get('/ahmad-dl', async (req, res) => {
    let videoUrl = req.query.url;
    if (!videoUrl) return res.json({ status: false, msg: "Link missing!" });

    // 🚀 STEP 1: Desktop Link ko Mobile Link mein badlo
    if (videoUrl.includes("www.facebook.com")) {
        videoUrl = videoUrl.replace("www.facebook.com", "m.facebook.com");
    } else if (videoUrl.includes("facebook.com") && !videoUrl.includes("m.facebook.com")) {
        videoUrl = videoUrl.replace("facebook.com", "m.facebook.com");
    }

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--single-process'],
            headless: "new",
            executablePath: '/usr/bin/google-chrome-stable'
        });

        const page = await browser.newPage();
        
        // 🚀 STEP 2: Mobile Agent use karo taake FB ko lage iPhone hai
        await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1');
        
        await page.goto(videoUrl, { waitUntil: 'networkidle2', timeout: 60000 });

        // 🚀 STEP 3: SMART DETECTION (Wait for 5 seconds for video to render)
        await new Promise(r => setTimeout(r, 5000));

        const finalUrl = await page.evaluate(() => {
            // Mobile version mein video tags dhoondna asan hai
            const video = document.querySelector('video');
            if (video && video.src && !video.src.startsWith('blob:')) return video.src;

            // Agar reel hai to aksar meta tags mein asli link hota hai
            const metaOgVideo = document.querySelector('meta[property="og:video"]');
            if (metaOgVideo) return metaOgVideo.content;

            // Last resort: search all video sources
            const sources = Array.from(document.querySelectorAll('video source, a[href*=".mp4"]'));
            for (let s of sources) {
                let link = s.src || s.href;
                if (link && !link.startsWith('blob:')) return link;
            }
            return null;
        });

        await browser.close();

        if (finalUrl) {
            res.json({ status: true, brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", url: finalUrl });
        } else {
            res.json({ status: false, msg: "Facebook ne link block kar diya hai. Shayad Proxy ki zaroorat hai." });
        }

    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`RDX API Live on ${PORT}`));
