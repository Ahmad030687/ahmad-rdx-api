const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const qs = require('qs');

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => res.send('🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - Unlimited Universal DL is Live!'));

// 🎥 UNIVERSAL DOWNLOADER ENDPOINT
app.get('/rdx-dl', async (req, res) => {
    const url = req.query.url;
    if (!url) return res.json({ status: false, msg: "Link bhej Ahmad bhai!" });

    try {
        let result = null;

        // 1. TIKTOK LOGIC (No Watermark)
        if (url.includes("tiktok.com")) {
            const data = qs.stringify({ 'id': url, 'locale': 'en', 'tt': 'RFZueFoz' });
            const response = await axios.post('https://ssstik.io/abc?url=dl', data);
            const $ = cheerio.load(response.data);
            result = $('.download_link').first().attr('href');
        }

        // 2. INSTAGRAM LOGIC
        else if (url.includes("instagram.com")) {
            const data = qs.stringify({ 'q': url, 't': 'media', 'lang': 'en' });
            const response = await axios.post('https://v3.saveig.app/api/ajaxSearch', data);
            const $ = cheerio.load(response.data.data);
            result = $('.download-items__btn a').attr('href');
        }

        // 3. FACEBOOK LOGIC
        else if (url.includes("facebook.com") || url.includes("fb.watch")) {
            const data = qs.stringify({ 'q': url });
            const response = await axios.post('https://getmyfb.com/process', data);
            const $ = cheerio.load(response.data);
            result = $('.results-item-bundle a').first().attr('href');
        }

        if (result) {
            res.json({ status: true, brand: "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗", url: result });
        } else {
            res.json({ status: false, msg: "Video link nahi mil saka. Link public hai?" });
        }

    } catch (e) {
        res.json({ status: false, error: "Server Busy ya Link Expired!" });
    }
});

app.listen(PORT, '0.0.0.0', () => console.log(`RDX Universal API on ${PORT}`));
