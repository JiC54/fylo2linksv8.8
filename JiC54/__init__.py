# JiC54

import os
from os import getenv, environ
from dotenv import load_dotenv
from aiohttp import ClientSession
from telethon.sessions import MemorySession
from telethon import TelegramClient
import time
StartTime = time.time()
__version__ = 1.1
aiohttpsession = ClientSession()

API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)


telethn = TelegramClient(MemorySession(), API_ID, API_HASH)