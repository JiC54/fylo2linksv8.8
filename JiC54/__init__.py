# JiC54

import os
from os import getenv, environ
from dotenv import load_dotenv
from aiohttp import ClientSession
from telethon.sessions import MemorySession
from telethon import TelegramClient
import logging
import time
StartTime = time.time()
__version__ = 1.1
aiohttpsession = ClientSession()

API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)


telethn = TelegramClient(MemorySession(), API_ID, API_HASH)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)
LOGGER = logging.getLogger('[JiC54]')
