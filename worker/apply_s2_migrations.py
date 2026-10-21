"""Apply pipeline SQLite schema and force strip2-only settings."""
from __future__ import annotations

from peach_db import SCHEMA_PATH, db_conn


def apply_migrations() -> None:
    if not SCHEMA_PATH.is_file():
        raise RuntimeError(f"missing schema: {SCHEMA_PATH}")
    with db_conn() as conn:
        conn.execute(
            """
            INSERT INTO app_settings (key, value, description, updated_at)
            VALUES (
              'parser.primary_source',
              'strip2',
              'Catalog source (strip2 only)',
              datetime('now')
            )
            ON CONFLICT (key) DO UPDATE SET
              value = 'strip2',
              updated_at = datetime('now')
            """
        )
        conn.execute(
            """
            INSERT INTO app_settings (key, value, description, updated_at)
            VALUES (
              'strip2.source_origin',
              'https://vps402.strip2.co',
              'strip2 mirror origin',
              datetime('now')
            )
            ON CONFLICT (key) DO UPDATE SET
              value = 'https://vps402.strip2.co',
              updated_at = datetime('now')
            """
        )
        conn.execute(
            """
            INSERT INTO app_settings (key, value, description, updated_at)
            VALUES (
              'namevids.caption_link',
              'https://telegram.dog/home6on',
              's2 pipeline caption TG channel',
              datetime('now')
            )
            ON CONFLICT (key) DO UPDATE SET
              value = 'https://telegram.dog/home6on',
              description = 's2 pipeline caption TG channel',
              updated_at = datetime('now')
            """
        )
        row = conn.execute(
            "SELECT count(*) AS n FROM sqlite_master WHERE type='table'"
        ).fetchone()
        print(
            f"migrations: sqlite schema ready ({(row or {}).get('n', 0)} tables), source=strip2"
        )
        conn.commit()


if __name__ == "__main__":
    apply_migrations()
