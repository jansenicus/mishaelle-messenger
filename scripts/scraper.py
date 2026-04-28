import os
import asyncio
import sqlite3
from telethon import TelegramClient
from dotenv import load_dotenv
from parsers.index import PARSER_REGISTRY

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import load_env


# --- Load environment variables ---
api_id, api_hash = load_env()


client = TelegramClient("mishaelle_session", api_id, api_hash)


DUMP_DIR = "dumps"
os.makedirs(DUMP_DIR, exist_ok=True)

conn = sqlite3.connect(os.path.join(DUMP_DIR, "signals.db"))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    timestamp TEXT,
    symbol TEXT,
    direction TEXT,
    entry REAL,
    stop_loss REAL,
    take_profit TEXT,
    result TEXT
)
""")
conn.commit()


async def scrape_channel(channel_id, limit=1000):  # pragma: no cover
    parser = PARSER_REGISTRY.get(channel_id)
    if not parser:
        return
    async for msg in client.iter_messages(channel_id, limit=limit):
        parsed = parser(msg.text or "")
        if parsed:
            cursor.execute(
                """
                INSERT INTO signals (channel_id, timestamp, symbol, direction, entry, stop_loss, take_profit, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    channel_id,
                    msg.date.isoformat(),
                    parsed.get("symbol"),
                    parsed.get("direction"),
                    parsed.get("entry"),
                    parsed.get("stop_loss"),
                    str(parsed.get("take_profit")),
                    None,
                ),
            )
    conn.commit()
    print(f"✅ Historical scrape complete for channel {channel_id}")


async def main():
    await client.start()
    for channel_id in PARSER_REGISTRY.keys():
        count = cursor.execute(
            "SELECT COUNT(*) FROM signals WHERE channel_id=?", (channel_id,)
        ).fetchone()[0]
        if count == 0:  # only scrape once
            await scrape_channel(channel_id, limit=1000)
        else:
            print(f"⚡ Channel {channel_id} already scraped, skipping.")


if __name__ == "__main__":
    asyncio.run(main())
