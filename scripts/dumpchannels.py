import os
import csv
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("mishaelle_session", api_id, api_hash)

DUMP_DIR = "dumps"
os.makedirs(DUMP_DIR, exist_ok=True)


async def dump_channels_groups():
    await client.start()
    dialogs = await client.get_dialogs()

    with open(
        os.path.join(DUMP_DIR, "channels_groups_dump.csv"),
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "ID", "Type"])
        for d in dialogs:
            if d.is_channel:
                writer.writerow([d.entity.title, d.entity.id, "Channel"])
            elif d.is_group:
                writer.writerow([d.entity.title, d.entity.id, "Group"])

    print("✅ Channels and Groups dumped into channels_groups_dump.csv")


if __name__ == "__main__":
    asyncio.run(dump_channels_groups())
