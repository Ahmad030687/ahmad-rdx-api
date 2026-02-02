const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐏𝐈 - Pro Engine (FB/IG/TT) is Live!'));

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
        
        // --- 🛡️ ENGINE CONFIGURATION ---
        if (videoUrl.includes("facebook.com") || videoUrl.includes("fb.watch")) {
            videoUrl = videoUrl.replace("www.facebook.com", "m.facebook.com");
            await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1');
        } 
        else if (videoUrl.includes("instagram.com")) {
            // Instagram needs a very specific Mobile Safari header to avoid login wall
            await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1');
        } 
        else if (videoUrl.includes("tiktok.com")) {
            await page.setUserAgent('Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36');
        }

        // Navigate to URL
        await page.goto(videoUrl, { waitUntil: 'networkidle2', timeout: 80000 });

        // Platform-specific wait times
        const waitTime = videoUrl.includes("instagram.com") ? 7000 : 5000;
        await new Promise(r => setTimeout(r, waitTime));

        const finalUrl = await page.evaluate(() => {
            // Helper function to extract URL
            const getSrc = (el) => (el && el.src && !el.src.startsWith('blob:')) ? el.src : null;

            // 1. General Video Tag Search
            const video = document.querySelector('video');
            let src = getSrc(video);

            // 2. Instagram/Facebook Meta Tag Check (Very effective for Reels)
            if (!src) {
                const metaOgVideo = document.querySelector('meta[property="og:video"]');
                if (metaOgVideo) src = metaOgVideo.content;
            }

            // 3. TikTok / Deep Source Search
            if (!src) {
                const allSources = Array.from(document.querySelectorAll('video source, video, a[href*=".mp4"]'));
                for (let s of allSources) {
                    let link = s.src || s.href;
                    if (link && !link.startsWith('blob:')) {
                        src = link;
                        break;
                    }
                }
            }
            return src;
        });

        await browser.close();

        if (finalUrl) {
            res.json({ 
                status: true, 
                brand: "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗", 
                platform: videoUrl.includes("fb") ? "Facebook" : videoUrl.includes("ig") ? "Instagram" : "TikTok",
                url: finalUrl 
            });
        } else {
            res.json({ status: false, msg: "Video detect nahi ho saka. Shayad private account ho?" });
        }

    } catch (e) {
        if (browser) await browser.close();
        res.json({ status: false, error: e.message });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`Pro RDX API Live on ${PORT}`));
