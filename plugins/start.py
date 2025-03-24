import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, ReplyKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink

# Text Constants
START_TEXT = """Your Telegram DC Is : `{}`"""
HELP_TEXT = """Everything has fully been explained very well in our website including About the bot, Features, FAQ, Copyright, Terms of use, Child Abuse Policy, DMCA and many more.
So, please consider visiting our website."""
ABOUT_TEXT = """With this service, you may post files to the internet by simply uploading or forwarding files to this bot and receive both a direct download link and a streamable URL for the contents.

Learn more about this service by visiting its website, click below."""
# ...add other text constants...

# Button Markups
HELP_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('VISIT WEBSITE', url='https://bit.ly/3DgxO6h')
    ],[
        InlineKeyboardButton('BACK', callback_data='menu'),
        InlineKeyboardButton('CLOSE', callback_data='close')
    ]]
)
# ...add other button markups...

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    
    await client.send_photo(
        chat_id=message.from_user.id,
        photo="https://telegra.ph/file/4c096367043285a1a28d6.jpg",
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=ReplyKeyboardMarkup(
            [
                ["MENU📊", "DONATE❤️"]
            ],
            resize_keyboard=True
        ),
        parse_mode=enums.ParseMode.HTML
    )
    return


@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    user_id = message.from_user.id
    username =  message.from_user.mention 

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )
    fileName = {quote_plus(get_name(log_msg))}
    if SHORTLINK == False:
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
    else:
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = await get_shortlink(f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}")
        
    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᴇ : {fileName}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Download 🚀", url=download),  # we download Link
                                            InlineKeyboardButton('🖥️ Watch 🖥️', url=stream)]])  # web stream Link
    )
    rm=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download)
            ]
        ] 
    )
    msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b> 🖥ᴡᴀᴛᴄʜ  :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

    await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(message)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)

@Client.on_message(filters.command("help") & filters.incoming)
async def help_command(client, message):
    rm = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('VISIT WEBSITE', url='https://bit.ly/3DgxO6h')
        ],
        [
            InlineKeyboardButton('BACK', callback_data='menu'),
            InlineKeyboardButton('CLOSE', callback_data='close')
        ]
    ])
    
    await client.send_message(
        chat_id=message.from_user.id,
        text=HELP_TEXT,
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )
    return

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "menu":
        await query.message.edit_text(
            text=MENU_TEXT,
            reply_markup=MENU_BUTTONS
        )
    elif query.data == "help":
        await query.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS
        )
    elif query.data == "about":
        await query.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS
        )
    # ...add other callback cases...
    elif query.data == "close":
        await query.message.delete()

# Add after existing handlers

@Client.on_message(filters.command("menu") | filters.regex("MENU📊"))
async def menu(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text=MENU_TEXT,
        reply_markup=MENU_BUTTONS
    )

@Client.on_message(filters.command("donate") | filters.regex("DONATE❤️"))
async def donate(client, message):
    donate_text = DONATE_TEXT.format(message.from_user.mention)
    await client.send_message(
        chat_id=message.chat.id,
        text=donate_text,
        reply_markup=DONATE_BUTTONS,
        disable_web_page_preview=True
    )

# ...add other command handlers...
