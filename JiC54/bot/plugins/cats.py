"""import asyncio
from JiC54.bot import StreamBot
from pyrogram import Client, filters
from pyrogram.types import Message
import httpx

timeout = httpx.Timeout(40, pool=None)
http = httpx.AsyncClient(http2=True, timeout=timeout)


@StreamBot.on_message(filters.command("cat"))
async def cat(c: Client, m: Message, strings):
    r = await http.get("https://api.thecatapi.com/v1/images/search")
    rj = r.json()

    if rj[0]["url"].endswith(".gif"):
        await m.reply_animation(rj[0]["url"], caption=strings("meow"))
    else:
        await m.reply_photo(rj[0]["url"], caption=strings("meow"))"""