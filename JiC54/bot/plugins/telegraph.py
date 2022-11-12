#JiC54

import os
from JiC54.bot import StreamBot
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from urllib.parse import quote

@StreamBot.on_message(filters.command(["tgmedia", "tgraph", "telegraph"]))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("Reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4"),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("Not supported!")
        return
    download_location = await client.download_media(
        message=message.reply_to_message,
        file_name="root/downloads/",
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        await message.reply(
            f"<b>Link:-</b>\n\n <code>https://telegra.ph{response[0]}</code>",
            quote=True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="open link", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="share link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
                ],
                [InlineKeyboardButton(text="✗ Close ✗", callback_data="close_data")]
            ]
        )
    )
    finally:
        os.remove(download_location)

def share_link(text: str) -> str:
    return "**Here is Your Sharing Text 👇**\n\nhttps://t.me/share/url?url=" + quote(text)

@StreamBot.on_message(filters.command(["sharetext", "st", "stxt", "shtxt", "shtext"]))
async def share_text(client, message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Notice:**\n\n1. Reply Any Messages.\n2. No Media Support\n\n**Any Question Join Support Chat**",
            reply_to_message_id=reply_id
        )
        return
    await message.reply_text(share_link(input_text), reply_to_message_id=reply_id)