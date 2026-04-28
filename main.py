# main.py
import asyncio
import os
from telethon import TelegramClient
from dotenv import load_dotenv
from banner import startup_banner
from shutdown import register_shutdown_handler
from logger import setup_logger

# --- Load environment variables ---
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# --- Setup logger ---
logger = setup_logger(level="INFO", log_file="mishaelle.log")

client = TelegramClient("mishaelle_session", api_id, api_hash)

async def main():
    await client.start()
    me = await client.get_me()
    logger.info(f"Logged in as: {me.first_name}")

    loop = asyncio.get_running_loop()
    register_shutdown_handler(loop, client, timeout=5)

    await client.run_until_disconnected()

if __name__ == "__main__":
    startup_banner()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("✧ CTRL+C pressed, disconnecting...")
