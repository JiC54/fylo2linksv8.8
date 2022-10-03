#JiC54
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Any, Optional
from pyrogram.file_id import FileId
from pyrogram.raw.types.messages import Messages
from Adarsh.server.exceptions import FIleNotFound

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size


db = Database(Var.DATABASE_URL, Var.name)


MY_PASS = os.environ.get("MY_PASS",None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("login🔑") | filters.command("login")) , group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("Now send me password.\n\n If You don't know check the MY_PASS Variable in heroku \n\n(You can use /cancel command to cancel the process)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp=="/cancel":
                   await ag.edit("Process Cancelled Successfully")
                   return
            else:
                return
        except TimeoutError:
            await ag.edit("I can't wait more for password, try again")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "yeah! you entered the password correctly"
        else:
            ag_text = "Wrong password, try again"
        await ag.edit(ag_text)
    except Exception as e:
        print(e)

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) , group=4)
async def private_receive_handler(c: Client, m: Message):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass== None:
            await m.reply_text("Login first using /login cmd \n don\'t know the pass? request it from the Developer")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ : \n\n Nᴀᴍᴇ : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ.__\n\n  **Cᴏɴᴛᴀᴄᴛ Dᴇᴠᴇʟᴏᴘᴇʀ [JiC54](https://t.me/JiC54)\n ʜᴇ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                    
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>𝙹𝙾𝙸𝙽 UPDATES CHANNEL 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴 🔐</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ʙᴏss** [JiC54](https://t.me/jic54_official)",
                
                disable_web_page_preview=True)
            return
    try:
        
        uploading_text0 = """
<b>Uploading</b>
[▱▱▱▱▱▱▱▱▱▱] 0%
EAT: -/-s
        """
        gy = await m.reply_text(text=uploading_text0, quote=True)
        await asyncio.sleep(2)
        uploading_text1 = """
<b>Uploading</b>
[▰▱▱▱▱▱▱▱▱▱] 10%
EAT: 8s
        """
        gy1 = await gy.edit(text=uploading_text1)
        uploading_text2 = """
<b>Uploading</b>
[▰▰▱▱▱▱▱▱▱▱] 20%
EAT: 8s
        """
        gy2 = await gy1.edit(text=uploading_text2)
        uploading_text3 = """
<b>Uploading</b>
[▰▰▰▱▱▱▱▱▱▱] 30%
EAT: 7s
        """
        gy11 = await gy2.edit(text=uploading_text3)
        await asyncio.sleep(2)
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        await asyncio.sleep(2)
        uploading_text5 = """
<b>Uploading</b>
[▰▰▰▰▰▱▱▱▱▱] 50%
EAT: 3s
        """
        gy12 = await gy11.edit(text=uploading_text5)
        uploading_text6 = """
<b>Uploading</b>
[▰▰▰▰▰▰▱▱▱▱] 60%
EAT: 3s
        """
        gy13 = await gy12.edit(text=uploading_text6)
        uploading_text7 = """
<b>Uploading</b>
[▰▰▰▰▰▰▰▱▱▱] 70%
EAT: 2s
        """
        gy14 = await gy13.edit(text=uploading_text7)
        uploading_text8 = """
<b>Uploading</b>
[▰▰▰▰▰▰▰▰▱▱] 80%
EAT: 2s
        """
        gy15 = await gy14.edit(text=uploading_text8)
        uploading_text9 = """
<b>Uploading</b>
[▰▰▰▰▰▰▰▰▰▱] 90%
EAT: 1s
        """
        gy16 = await gy15.edit(text=uploading_text9)
        uploading_text10 = """
<b>Uploading</b>
[▰▰▰▰▰▰▰▰▰▰] 99%
EAT: 1s
        """
        gy17 = await gy16.edit(text=uploading_text10)
        await asyncio.sleep(2)
        uploading_textup = """
<b>Sending...</b>
        """
        gyy = await gy17.edit(text=uploading_textup)
        await asyncio.sleep(2)
        await gyy.delete()
        
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

        msg_text ="""
<b><u>Your Link Has Been Generated Successfully!</u></b>

<b>📂FILE NAME:</b> {}

<b>💾FILE SIZE:</b> {}

<b>🔗DOWNLOAD LINK:</b> <code>{}</code>

<b>🔗WATCH LINK:</b> <code>{}</code>

<b>⚠️THESE LINKS WON'T EXPIRE IF YOU COMPLY WITH OUR <a href='https://bit.ly/3yaIvUw'>TERMS & CONDITIONS</a></b>"""

        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Stream ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True,  quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥STREAM", url=stream_link), #Stream Link
                                                InlineKeyboardButton('DOWNLOAD📥', url=online_link)], #Download Link
                                                [InlineKeyboardButton('SHARE STREAM LINK⌲', url=f"https://t.me/share/url?url={stream_link}")
                                                ]]) 
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True)


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.audio)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("Login first using /login cmd \n don\'t know the pass? request it from developer!")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong password, login again")
            await pass_db.delete_user(broadcast.chat.id)
            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        await asyncio.sleep(5)
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            quote=True
        )
        await asyncio.sleep(5)
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🖥STREAM ", url=stream_link),
                     InlineKeyboardButton('DOWNLOAD📥', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.x)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Give me edit permission in updates and bin Chanell{e}**")