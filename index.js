const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 - Universal Engine (FB/IG/TT) is Live!'));

app.get('/ahmad-dl', async (req, res) => {
    let videoUrl = req.query.url;
    if (!videoUrl) return res.json({ status: false, msg: "Link missing!" });

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--single-process', '--no-zygote'],
            headless: "new",
            executablePath: '/usr/bin/google-chrome-stable'
        });

        const page = await browser.newPage();
        
        // --- 🚀 PLATFORM DETECTION & LOGIC ---
        
        // 1. FACEBOOK BYPASS
        if (videoUrl.includes("facebook.com") || videoUrl.includes("fb.watch")) {
            videoUrl = videoUrl.replace("www.facebook.com", "m.facebook.com");
            await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1');
        } 
        
        // 2. INSTAGRAM BYPASS
        else if (videoUrl.includes("instagram.com")) {
            await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1');
        } 
        
        // 3. TIKTOK BYPASS
        else if (videoUrl.includes("tiktok.com")) {
            // TikTok mobile version is very bot-friendly
            await page.setUserAgent('Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36');
        }

        await page.goto(videoUrl, { waitUntil: 'networkidle2', timeout: 60000 });

        // Smart Wait: Har platform ko load hone ke liye 4-5 second chahiye
        await new Promise(r => setTimeout(r, 5000));

        const finalUrl = await page.evaluate(() => {
            const video = document.querySelector('video');
            if (video && video.src && !video.src.startsWith('blob:')) return video.src;

            // Meta Tag Check (Backup for IG/FB Reels)
            const metaVideo = document.querySelector('meta[property="og:video"]');
            if (metaVideo) return metaVideo.content;

            // TikTok specific: checking for download/play links
            const sources = Array.from(document.querySelectorAll('video source, a[href*=".mp4"]'));
            for (let s of sources) {
                let link = s.src || s.href;
                if (link && !link.startsWith('blob:')) return link;
            }
            return null;
        });

        await browser.close();

        if (finalUrl) {
            res.json({ 
                status: true, 
                brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", 
                platform: videoUrl.includes("fb") ? "FB" : videoUrl.includes("ig") ? "IG" : "TT",
                url: finalUrl 
            });
        } else {
            res.json({ status: false, msg: "Link detect nahi ho saka." });
        }

    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`Universal RDX API Live on ${PORT}`));
