const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const qs = require('qs');

const app = express();
const PORT = process.env.PORT || 10000; // Render isi port ka intezar karta hai

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐔𝐋𝐓𝐑𝐀-𝐋𝐈𝐓𝐄 - Ready to Fly!'));

app.get('/rdx-dl', async (req, res) => {
    const url = req.query.url;
    if (!url) return res.json({ status: false, msg: "Link missing!" });

    try {
        let videoUrl = null;

        // 🟢 Facebook/Instagram/TikTok Bypass Logic
        const data = qs.stringify({ 'q': url, 'lang': 'en' });
        const config = {
            method: 'post',
            url: 'https://v3.saveig.app/api/ajaxSearch', // Multi-downloader endpoint
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            data: data
        };

        const response = await axios(config);
        const $ = cheerio.load(response.data.data);
        videoUrl = $('.download-items__btn a').attr('href');

        if (videoUrl) {
            res.json({ status: true, brand: "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗", url: videoUrl });
        } else {
            res.json({ status: false, msg: "Video link not found. Try another link!" });
        }
    } catch (e) {
        res.json({ status: false, error: "Server busy! Try again." });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`🚀 RDX API Live on port ${PORT}`));
