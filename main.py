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
api_id_str = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
if not api_hash:
    raise ValueError(
        "API_HASH environment variable is not set. Please set it in your .env file."
    )
if not api_id_str:
    raise ValueError("Environment variable 'API_ID' must be set to a valid integer.")
api_id = int(api_id_str)

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


def run_app():
    startup_banner()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("✧ CTRL+C pressed, disconnecting...")


if __name__ == "__main__":  # pragma: no cover
    run_app()
