import Database from 'better-sqlite3';

export function createDatabase(filePath) {
  const db = new Database(filePath);

  db.pragma('journal_mode = WAL');

  db.exec(`
    CREATE TABLE IF NOT EXISTS videos (
      id TEXT PRIMARY KEY,
      url TEXT NOT NULL,
      title TEXT,
      thumbnail_url TEXT,
      author_name TEXT,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS visits (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      video_id TEXT NOT NULL,
      ts TEXT NOT NULL,
      user_agent TEXT,
      ip TEXT,
      FOREIGN KEY (video_id) REFERENCES videos(id)
    );
  `);

  return db;
}