# YT Share Portal

A compliant promotional website to create shareable watch pages for YouTube links.

- Collects a YouTube URL, fetches oEmbed metadata, and generates a short link like `/watch/:id`
- Embeds the video via official YouTube iframe
- Tracks site visits to the watch page (not YouTube views)
- Provides social share links and optional Discord webhook announcement
- SQLite storage using better-sqlite3

## Important
- This project does not automate YouTube plays or interactions. It is designed for compliant sharing only.

## Getting started

1. Install dependencies:

```bash
npm install
```

2. Run in development mode (client + server):

```bash
npm run dev
```

- Client runs on `http://localhost:5173`
- API server runs on `http://localhost:3000`

3. Build and serve production bundle:

```bash
npm run build
npm start
```

Then open `http://localhost:3000`.

## Environment
Copy `.env.example` to `.env` to set any environment overrides.

## License
MIT