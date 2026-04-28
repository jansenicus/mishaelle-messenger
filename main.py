# main.py
import asyncio
from telethon import TelegramClient, events
from banner import startup_banner
from shutdown import register_shutdown_handler
from logger import setup_logger
from parsers.index import PARSER_REGISTRY
from config import load_env  # centralized environment loader

# --- Load environment variables ---
api_id, api_hash = load_env()

# --- Setup logger ---
logger = setup_logger(level="INFO", log_file="mishaelle.log")

# --- Initialize client ---
client = TelegramClient("mishaelle_session", api_id, api_hash)


# --- Event handler for new signals ---
@client.on(events.NewMessage(chats=list(PARSER_REGISTRY.keys())))
async def signal_handler(event):
    parser = PARSER_REGISTRY.get(event.chat_id)
    if parser:
        parsed = parser(event.raw_text)
        logger.info(f"Parsed signal from {event.chat.title}: {parsed}")
        # TODO: save parsed dict into SQLite


# --- Main runtime loop ---
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
