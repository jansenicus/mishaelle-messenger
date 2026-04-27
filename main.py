# main.py
from telethon import TelegramClient
import asyncio
import os
from banner import startup_banner   # Import banner function
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")


client = TelegramClient("session_name", api_id, api_hash)

# Show banner at startup
startup_banner()

async def main():
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")

with client:
    client.loop.run_until_complete(main())
