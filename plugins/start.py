import random
import humanize
import selenium
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink
import os
import asyncio

# Text Constants in a dictionary for better organization
TEXTS = {
    "menu": "<b>Here is the menu for File To Links</b>",
    "help": "Everything has been explained on our website...",
    "about": "Upload files to get direct download and streaming links...",
    "bitcoin": """<b>Use the following address to deposit ONLY Bitcoin (BTC):</b>
<code>1Hahm7m65tsv6NMdrKJmyvsFFrE6orjUA9</code>""",
    "ethereum": """<b>Use the following address to deposit ONLY Ethereum (ETH):</b>
<code>0xa5c60C36422f3f77638B7C4875C6108641cCa77b</code>""",
    "tether": """Use the following address to deposit:
<b>ONLY USDT TRC20:</b>
<code>TYmPURwxpFUV8s7SS7qM2Wzujex2XK4CzA</code></b></b>
<b>ONLY USDT TON:</b>
<code>UQBG0ngZG3WYYR_cDuDgHlvHB6kN4mKbqzz5kqdxqyS7P_wV</code></b></b>""",
    "crypto": """Choose a cryptocurrency from the list below, and then use the address that appears. If the transaction was successful, snap a screenshot and send it to @jumahmw. We will add you to our donors list as a reward and way of saying "thank you" for your generosity, giving you access to extra services.

If you run across any problems while donating crypto, contact @jooma265 immediately.""",
    "paypal": """To make a donation, please use the button below. If the transaction was successful, snap a screenshot and send it to @jumahmw. We'll add you to our contributors list, where you'll be able to enjoy additional services as a reward and a 'thank you' for your support

Contact @jooma265 if you experience any difficulties while making a donation via PayPal.""",
    "buymeacoffee": """To donate, click the button below. Take a screenshot and send it to @jumahmw if the transaction was successful. As a reward and way of saying "thank you" for your donation, we will add you to our donors list, where you will have access to additional services.

Contact @jooma265 if you experience any difficulties while buying me a coffee""",
    "id_msg": """Your Telegram ID is <code>{}</code>""",
    "telegraph": """This feature allows you to upload media on telegraph.
Just reply with /telegraph command to a media and the telegraph link will be generated and sent to you.

<b>NOTE</b>
- Only videos and pictures can be uploaded to telegraph
- Maximum size of media that can be uploaded to telegraph is 5mb
- Supported media formats: .jpg, .jpeg, .png, .gif, .mp4""",
    "shortener": """This feature enables you to shorten links.
Just type /short command along with the link you want to shorten

<b>NOTE</b>
For example:
<code>/short https://www.twosix5.blogspot.com</code>""",
    "paste": """This feature allows to paste your text to Pasty
Just type /paste command along with the text you want to paste

For Example:
<code>/paste Hello, this is FilesToLinks</code>""",
    "webscreenshot": """This feature allows you to have a look of the specified website without opening the url, the bot does that for you, it opens the website and gives you the screenshot""",
    "imagetopdf": """This feature allows you to convert images to pdf. Simply just send an image as a document then reply it with /pdf""",
    "extra": """Extra features are listed below. For the time being, all users may access these bonuses because they were created as a thank-you and a reward for supporters (donors).
However, this access will soon expire to all users who haven't made any donation. Therefore, /donate right now to be added to our donor list; further benefits are on the way for donors!""",
    "donate": """Dear {},
I, the service's developer, am struggling to pay for servers in order to keep the service online. Running this service for a month costs $10. Whereby Only $7 is spent on Heroku, with the remaining $3 spent on databases. You can help keep this service alive today by donating any amount. Just click below and select a method.

Thank you for everything you do. I couldn't do this without you.

All the best,
FilesToLinks""",
    "start": """Your Telegram DC Is : `{}`""",
    "help": """Everything has fully been explained very well in our website including About the bot, Features, FAQ, Copyright, Terms of use, Child Abuse Policy, DMCA and many more.
So, please consider visiting our website.""",
    "about": """With this service, you may post files to the internet by simply uploading or forwarding files to this bot and receive both a direct download link and a streamable URL for the contents.

Learn more about this service by visiting its website, click below."""
}

# Button Configurations in a dictionary
BUTTONS = {
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("COMMANDS", "command"), InlineKeyboardButton("EXTRA", "extra")],
        [InlineKeyboardButton("ABOUT", "about"), InlineKeyboardButton("HELP", "help")],
        [InlineKeyboardButton("CLOSE", "close")]
    ]),
    "help": InlineKeyboardMarkup([
        [InlineKeyboardButton('VISIT WEBSITE', url='https://bit.ly/3DgxO6h')],
        [InlineKeyboardButton('BACK', callback_data='menu'), InlineKeyboardButton('CLOSE', callback_data='close')]
    ]),
    "command": InlineKeyboardMarkup([
        [InlineKeyboardButton("BACK", callback_data="menu"), InlineKeyboardButton("CLOSE", callback_data="close")]
    ]),
    "extra": InlineKeyboardMarkup([
        [InlineKeyboardButton("TELEGRAPH", callback_data="telegraph"), InlineKeyboardButton("SHORTENER", callback_data="shortener")],
        [InlineKeyboardButton("IMG TO PDF", callback_data="pdf"), InlineKeyboardButton("PASTE", callback_data="paste")],
        [InlineKeyboardButton("WEB SCREENSHOT", callback_data="webscreenshot")],
        [InlineKeyboardButton("BACK", callback_data="menu"), InlineKeyboardButton("CLOSE", callback_data="close")]
    ]),
    "about": InlineKeyboardMarkup([
        [InlineKeyboardButton('WEBSITE', url='https://bit.ly/3DgxO6h')],
        [InlineKeyboardButton('BACK', callback_data='menu'), InlineKeyboardButton('CLOSE', callback_data='close')]
    ]),
    "donate": InlineKeyboardMarkup([
        [InlineKeyboardButton('PAYPAL', callback_data='paypal'), InlineKeyboardButton('BUY ME A COFFEE', callback_data='coffee')],
        [InlineKeyboardButton('CRYPTO', callback_data='crypto'), InlineKeyboardButton('CLOSE', callback_data='close')]
    ]),
    "paypal": InlineKeyboardMarkup([
        [InlineKeyboardButton('DONATE VIA PAYPAL', url='https://bit.ly/3BNvGAv')],
        [InlineKeyboardButton('BACK', callback_data='donate'), InlineKeyboardButton('CLOSE', callback_data='close')]
    ]),
    "buymeacoffee": InlineKeyboardMarkup([
        [InlineKeyboardButton('BUY ME A COFFEE☕️', url='https://bit.ly/3SkoItT')],
        [InlineKeyboardButton('BACK', callback_data='donate'), InlineKeyboardButton('CLOSE', callback_data='close')]
    ]),
    "crypto": InlineKeyboardMarkup([
        [InlineKeyboardButton('BITCOIN [BTC]', callback_data='bitcoin'), InlineKeyboardButton('ETHEREUM [ETH]', callback_data='ethereum')],
        [InlineKeyboardButton('TETHER [USDT]', callback_data='tether'), InlineKeyboardButton('BACK', callback_data='donate')]
    ]),
    "bitcoin": InlineKeyboardMarkup([
        [InlineKeyboardButton('BACK', callback_data='crypto')]
    ]),
    "tether": InlineKeyboardMarkup([
        [InlineKeyboardButton('BACK', callback_data='crypto')]
    ]),
    "ethereum": InlineKeyboardMarkup([
        [InlineKeyboardButton('BACK', callback_data='crypto')]
    ])
}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    try:
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(
                message.from_user.id, message.from_user.mention))
        
        await client.send_photo(
            chat_id=message.from_user.id,
            photo="https://telegra.ph/file/4c096367043285a1a28d6.jpg",
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=ReplyKeyboardMarkup(
                [["MENU📊", "DONATE❤️"]],
                resize_keyboard=True
            ),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        print(f"Start command error: {e}")

@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id
    user_id = message.from_user.id
    username = message.from_user.mention

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )
    fileName = quote_plus(get_name(log_msg))
    if not SHORTLINK:
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
    else:
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = await get_shortlink(f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}")

    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᴍᴇ : {filename}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🚀 Download 🚀", url=download),
                 InlineKeyboardButton('🖥️ Watch 🖥️', url=stream)]
            ]
        )
    )

    rm = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download)
            ]
        ]
    )

    msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b> 🖥ᴡᴀᴛᴄʜ  :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

    await message.reply_text(
        text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(message)), download, stream),
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )

@Client.on_message(filters.command("help") & filters.incoming)
async def help_command(client, message):
    rm = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('VISIT WEBSITE', url='https://bit.ly/3DgxO6h')
            ],
            [
                InlineKeyboardButton('BACK', callback_data='menu'),
                InlineKeyboardButton('CLOSE', callback_data='close')
            ]
        ]
    )
    
    await client.send_message(
        chat_id=message.from_user.id,
        text=HELP_TEXT,
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )
    return

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    try:
        data = query.data
        
        # Handle text updates
        if data in TEXTS:
            await query.message.edit_text(
                text=TEXTS[data],
                reply_markup=BUTTONS.get(data),
                disable_web_page_preview=True
            )
            return
        
        # Handle special cases
        if data == "close":
            await query.message.delete()
        elif data == "donate":
            await query.message.edit_text(
                text=TEXTS["donate"].format(query.from_user.mention),
                reply_markup=BUTTONS["donate"],
                disable_web_page_preview=True
            )
        
    except Exception as e:
        print(f"Callback error: {e}")
        await query.answer("An error occurred!", show_alert=True)

# Add after existing handlers
@Client.on_message(filters.command("menu") | filters.regex("MENU📊"))
async def menu(client, message):
    try:
        await client.send_message(
            chat_id=message.chat.id,
            text=TEXTS["menu"],
            reply_markup=BUTTONS["menu"],
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Menu command error: {e}")

@Client.on_message(filters.command("donate") | filters.regex("DONATE❤️"))
async def donate(client, message):
    try:
        donate_text = TEXTS["donate"].format(message.from_user.mention)
        await client.send_message(
            chat_id=message.chat.id,
            text=donate_text,
            reply_markup=BUTTONS["donate"],
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Donate command error: {e}")