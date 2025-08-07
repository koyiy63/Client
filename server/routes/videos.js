import express from 'express';
import axios from 'axios';
import { nanoid } from 'nanoid';

const router = express.Router();

function isValidYouTubeUrl(url) {
  try {
    const u = new URL(url);
    if (!['www.youtube.com', 'youtube.com', 'youtu.be', 'music.youtube.com', 'm.youtube.com'].includes(u.hostname)) return false;
    return true;
  } catch {
    return false;
  }
}

async function fetchOEmbed(url) {
  const oembedUrl = `https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`;
  const { data } = await axios.get(oembedUrl, { timeout: 8000 });
  return data; // { title, thumbnail_url, author_name, ... }
}

router.post('/', async (req, res) => {
  const db = req.app.get('db');
  const { url } = req.body || {};
  if (!url || !isValidYouTubeUrl(url)) return res.status(400).json({ error: 'Provide a valid YouTube URL' });
  try {
    const meta = await fetchOEmbed(url);
    const id = nanoid(10);
    const createdAt = new Date().toISOString();
    db.prepare(
      'INSERT INTO videos (id, url, title, thumbnail_url, author_name, created_at) VALUES (@id, @url, @title, @thumb, @author, @created)'
    ).run({ id, url, title: meta.title || null, thumb: meta.thumbnail_url || null, author: meta.author_name || null, created: createdAt });
    res.status(201).json({ id });
  } catch (e) {
    res.status(400).json({ error: 'Could not fetch video metadata' });
  }
});

router.get('/:id', (req, res) => {
  const db = req.app.get('db');
  const id = req.params.id;
  const video = db.prepare('SELECT * FROM videos WHERE id = ?').get(id);
  if (!video) return res.status(404).json({ error: 'Not found' });
  const visitCount = db.prepare('SELECT COUNT(*) as c FROM visits WHERE video_id = ?').get(id).c;
  res.json({ ...video, visitCount });
});

router.post('/:id/visit', (req, res) => {
  const db = req.app.get('db');
  const id = req.params.id;
  const video = db.prepare('SELECT id FROM videos WHERE id = ?').get(id);
  if (!video) return res.status(404).json({ error: 'Not found' });
  const ts = new Date().toISOString();
  const ua = req.headers['user-agent'] || null;
  const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').toString();
  db.prepare('INSERT INTO visits (video_id, ts, user_agent, ip) VALUES (?, ?, ?, ?)').run(id, ts, ua, ip);
  res.json({ ok: true });
});

router.post('/:id/announce', async (req, res) => {
  const db = req.app.get('db');
  const id = req.params.id;
  const { webhookUrl, publicBaseUrl } = req.body || {};
  if (!webhookUrl || !publicBaseUrl) return res.status(400).json({ error: 'webhookUrl and publicBaseUrl are required' });
  const video = db.prepare('SELECT * FROM videos WHERE id = ?').get(id);
  if (!video) return res.status(404).json({ error: 'Not found' });
  const watchUrl = `${publicBaseUrl.replace(/\/$/, '')}/watch/${id}`;
  try {
    await axios.post(webhookUrl, {
      content: `New watch page created: ${watchUrl}`,
      embeds: [
        {
          title: video.title || 'YouTube Video',
          url: watchUrl,
          description: video.author_name ? `by ${video.author_name}` : undefined,
          thumbnail: video.thumbnail_url ? { url: video.thumbnail_url } : undefined
        }
      ]
    }, { timeout: 8000 });
    res.json({ ok: true });
  } catch (e) {
    res.status(400).json({ error: 'Failed to send Discord webhook' });
  }
});

export default router;