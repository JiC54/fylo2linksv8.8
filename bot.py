# Updated main file of the bot
import sys, glob, importlib, logging, pytz, asyncio
from pathlib import Path
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

ppath = "plugins/*.py"
files = glob.glob(ppath)

async def start():
    print('\n')
    print('Initializing Your Bot')
    
    # Start the TechVJBot client
    await TechVJBot.start()
    print("TechVJBot client started successfully.")
    
    bot_info = await TechVJBot.get_me()
    await initialize_clients()
    
    # Load plugins
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[f"plugins.{plugin_name}"] = load
            print(f"Tech VJ Imported => {plugin_name}")
    
    # Start ping server if on Heroku
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    
    # Set bot details in temp
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    
    # Send restart message
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    
    # Start the web server
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    
    # Keep the bot running
    await idle()

    # Stop the client when idle ends
    await TechVJBot.stop()
    print("TechVJBot client stopped.")

if __name__ == '__main__':
    try:
        asyncio.run(start())  # Use asyncio.run() to start the bot
    except KeyboardInterrupt:
        logging.info('Service Stopped. Bye 👋')
    except Exception as e:
        logging.error(f"Fatal error: {e}")

