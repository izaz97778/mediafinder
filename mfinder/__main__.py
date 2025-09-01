import uvloop
import asyncio
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer
from mfinder import APP_ID, API_HASH, BOT_TOKEN

from flask import Flask
import threading

# ---------------- Flask Health Server ---------------- #
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "MediaFinder Bot is running!", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

# ----------------------------------------------------- #

uvloop.install()

async def main():
    plugins = dict(root="mfinder/plugins")
    app = Client(
        name="mfinder",
        api_id=APP_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins,
    )
    async with app:
        me = await app.get_me()
        print(
            f"{me.first_name} - @{me.username} - Pyrogram v{__version__} (Layer {layer}) - Started..."
        )
        await idle()
        print(f"{me.first_name} - @{me.username} - Stopped !!!")

if __name__ == "__main__":
    # Run Flask server in background thread
    threading.Thread(target=run_flask).start()

    # Run bot with uvloop
    uvloop.run(main())
