# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, idle 
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients
from pyrogram.errors import FloodWait

ppath = "plugins/*.py"
files = glob.glob(ppath)
# Remove or comment out this line since we're starting the bot in the main block
# TechVJBot.start()
loop = asyncio.get_event_loop()

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FileToLink",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"Bot {me.first_name} started")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped")

async def main():
    bot = Bot()
    try:
        await bot.start()
        await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")

