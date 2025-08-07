import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { createDatabase } from './lib/db.js';
import videosRouter from './routes/videos.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(cors({ origin: [/^http:\/\/localhost:\d+$/], credentials: false }));

// Initialize DB
const db = createDatabase(path.join(__dirname, 'data.db'));
app.set('db', db);

// Health
app.get('/api/health', (_req, res) => res.json({ ok: true }));

// API routes
app.use('/api/videos', videosRouter);

// Static assets (production)
const publicDir = path.join(__dirname, 'public');
app.use(express.static(publicDir));

// SPA fallback
app.get('*', (req, res) => {
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({ error: 'Not found' });
  }
  res.sendFile(path.join(publicDir, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});