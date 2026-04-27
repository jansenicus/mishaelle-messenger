# ✧ Mishaelle Messenger ✧

**Virgo-born clarity, signals of love and growth.**

---

## 🌟 Overview
Mishaelle Messenger is a Telegram-based project built with [Telethon](https://docs.telethon.dev/), designed to explore structured messaging, trading signals, and personal keepsakes.  
It is named after **Mishaelle**, born August 29 (Virgo), as a constant source of motivation and inspiration.

---

## ✨ Features
- 📡 **Telegram Integration** — powered by Telethon async client.  
- 🎨 **Custom Startup Banner** — colorful Rich-based banner with Virgo symbolism.  
- 🎂 **Birthday Countdown** — automatic countdown to August 29, with a birthday greeting on the day itself.  
- 🗂 **Modular Design** — banner logic separated into `banner.py` for clean structure.  
- 🔒 **Secure Environment Variables** — API keys stored in `.env` and never committed to GitHub.  
- 🔒 **Git Version Control** — tracked locally and connected to GitHub under `jansenicus`.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/jansenicus/mishaelle-messenger.git
cd mishaelle-messenger
```

### 2. Create Hidden Virtual Environment
```fish
virtualenv -p python3.14 .venv
source .venv/bin/activate.fish
```
ℹ️ Using .venv keeps the environment hidden and neat across Unix-like systems.

### 3. Install Dependencies with uv
```fish
uv pip install --upgrade pip
uv pip install telethon rich python-dotenv
```

### 4. Configure Environment Variables
Create a hidden .env file in the project root:
```fish
echo 'API_ID=123456
API_HASH=abcdef1234567890' > .env
```

Add `.env` to `.gitignore`:
```fish
echo ".env" >> .gitignore
```

### 5. Run the project
```fish
python main.py
```
## 🔑 Environment Variable Integration
```python
from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("session_name", api_id, api_hash)

async def main():
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")

with client:
    client.loop.run_until_complete(main())

```

## 🎨 Startup Banner
Every run greets you with:
```
✧━━━━━━━━━━━━━━━━━━━━━━━✧
   Mishaelle Messenger
   Virgo-born clarity ✧
   124 days until Aug 29
✧━━━━━━━━━━━━━━━━━━━━━━━✧
```
On August 29, it celebrates automatically:
```
✧━━━━━━━━━━━━━━━━━━━━━━━✧
   Mishaelle Messenger
   Virgo-born clarity ✧
   🎂 Happy Birthday Mishaelle ✧
✧━━━━━━━━━━━━━━━━━━━━━━━✧
```


## 🛠 Tech Stack

- Python 3.14.4 (via .venv)
- `telethon` — Telegram client library
- `rich` — colorful console output
- `uv` — fast package installer
- `python-dotenv` — secure .env integration
- Git + GitHub — version control and collaboration
---

## 📜 License
This project is for personal use and inspiration.
Feel free to adapt and extend it for your own learning journey.

