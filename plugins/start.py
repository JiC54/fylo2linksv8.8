import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink

# Text Constants
MENU_TEXT = """<b>Here is the menu for File To Links</b>"""
BITCOIN_TEXT = """<b>Use the following address to deposit ONLY Bitcoin (BTC):</b>
<code>38mRQgsPoRTZvcMUFpXGMf9HjL8MxjjUzE</code>"""
ETHEREUM_TEXT = """<b>Use the following address to deposit ONLY Ethereum (ETH):</b>
<code>0xa5c60C36422f3f77638B7C4875C6108641cCa77b</code>"""
TETHER_TEXT = """<b>Use the following address to deposit ONLY Tether (USDT):</b>
<code>TVekMwDh42vjXy5NbNrQPAKdBgzypDLRk6</code>"""
CRYPTO_TEXT = """Choose a cryptocurrency from the list below, and then use the address that appears. If the transaction was successful, snap a screenshot and send it to @jumahmw. We will add you to our donors list as a reward and way of saying "thank you" for your generosity, giving you access to extra services.

If you run across any problems while donating crypto, contact @jooma265 immediately."""
PAYPAL_TEXT = """To make a donation, please use the button below. If the transaction was successful, snap a screenshot and send it to @jumahmw. We'll add you to our contributors list, where you'll be able to enjoy additional services as a reward and a 'thank you' for your support

Contact @jooma265 if you experience any difficulties while making a donation via PayPal."""
BUYMEACOFFEE_TEXT = """To donate, click the button below. Take a screenshot and send it to @jumahmw if the transaction was successful. As a reward and way of saying "thank you" for your donation, we will add you to our donors list, where you will have access to additional services.

Contact @jooma265 if you experience any difficulties while buying me a coffee"""
ID_MSG = """Your Telegram ID is <code>{}</code>"""
TELEGRAPH_TEXT = """This feature allows you to upload media on telegraph.
Just reply with /telegraph command to a media and the telegraph link will be generated and sent to you.

<b>NOTE</b>
- Only videos and pictures can be uploaded to telegraph
- Maximum size of media that can be uploaded to telegraph is 5mb
- Supported media formats: .jpg, .jpeg, .png, .gif, .mp4"""
SHORTENER_TEXT = """This feature enables you to shorten links.
Just type /short command along with the link you want to shorten

<b>NOTE</b>
For example:
<code>/short https://www.twosix5.blogspot.com</code>"""
PASTE_TEXT = """This feature allows to paste your text to Pasty
Just type /paste command along with the text you want to paste

For Example:
<code>/paste Hello, this is FilesToLinks</code>"""
WEBSCREENSHOT_TEXT = """This feature allows you to have a look of the specified website without opening the url, the bot does that for you, it opens the website and gives you the screenshot"""
IMAGETOPDF_TEXT = """This feature allows you to convert images to pdf. Simply just send an image as a document then reply it with /pdf"""
EXTRA_TEXT = """Extra features are listed below. For the time being, all users may access these bonuses because they were created as a thank-you and a reward for supporters (donors).
However, this access will soon expire to all users who haven't made any donation. Therefore, /donate right now to be added to our donor list; further benefits are on the way for donors!"""
DONATE_TEXT = """Dear {},
I, the service's developer, am struggling to pay for servers in order to keep the service online. Running this service for a month costs $10. Whereby Only $7 is spent on Heroku, with the remaining $3 spent on databases. You can help keep this service alive today by donating any amount. Just click below and select a method.

Thank you for everything you do. I couldn't do this without you.

All the best,
FilesToLinks"""
START_TEXT = """Your Telegram DC Is : `{}`"""
HELP_TEXT = """Everything has fully been explained very well in our website including About the bot, Features, FAQ, Copyright, Terms of use, Child Abuse Policy, DMCA and many more.
So, please consider visiting our website."""
ABOUT_TEXT = """With this service, you may post files to the internet by simply uploading or forwarding files to this bot and receive both a direct download link and a streamable URL for the contents.

Learn more about this service by visiting its website, click below."""

# Button Markups
HELP_BUTTONS = InlineKeyboardMarkup(
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

MENU_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("COMMANDS", callback_data="command"),
            InlineKeyboardButton("EXTRA", callback_data="extra")
        ],
        [
            InlineKeyboardButton("ABOUT", callback_data="about"),      
            InlineKeyboardButton("HELP", callback_data="help")
        ],
        [
            InlineKeyboardButton("CLOSE", callback_data="close")
        ]
    ]
)

COMMAND_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("BACK", callback_data="menu"),
            InlineKeyboardButton("CLOSE", callback_data="close")
        ]
    ]
)

EXTRA_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("TELEGRAPH", callback_data="telegraph"),
            InlineKeyboardButton("SHORTENER", callback_data="shortener")
        ],
        [
            InlineKeyboardButton("IMG TO PDF", callback_data="pdf"),
            InlineKeyboardButton("PASTE", callback_data="paste")
        ],
        [
            InlineKeyboardButton("WEB SCREENSHOT", callback_data="webscreenshot")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="menu"),
            InlineKeyboardButton("CLOSE", callback_data="close")
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('WEBSITE', url='https://bit.ly/3DgxO6h')
        ],
        [
            InlineKeyboardButton('BACK', callback_data='menu'),
            InlineKeyboardButton('CLOSE', callback_data='close')
        ]
    ]
)

DONATE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('PAYPAL', callback_data='paypal'),
            InlineKeyboardButton('BUY ME A COFFEE', callback_data='coffee')
        ],
        [
            InlineKeyboardButton('CRYPTO', callback_data='crypto'),
            InlineKeyboardButton('CLOSE', callback_data='close')
        ]
    ]
)

PAYPAL_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('DONATE VIA PAYPAL', url='https://bit.ly/3BNvGAv')
        ],
        [
            InlineKeyboardButton('BACK', callback_data='donate'),
            InlineKeyboardButton('CLOSE', callback_data='close')
        ]
    ]
)

BUYMEACOFFEE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('BUY ME A COFFEE☕️', url='https://bit.ly/3SkoItT')
        ],
        [
            InlineKeyboardButton('BACK', callback_data='donate'),
            InlineKeyboardButton('CLOSE', callback_data='close')
        ]
    ]
)

CRYPTO_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('BITCOIN [BTC]', callback_data='bitcoin'),
            InlineKeyboardButton('ETHEREUM [ETH]', callback_data='ethereum')
        ],
        [
            InlineKeyboardButton('TETHER [USDT]', callback_data='tether'),
            InlineKeyboardButton('BACK', callback_data='donate')
        ]
    ]
)

BITCOIN_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('BACK', callback_data='crypto')
        ]
    ]
)

TETHER_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('BACK', callback_data='crypto')
        ]
    ]
)

ETHEREUM_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('BACK', callback_data='crypto')
        ]
    ]
)

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
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᴇ : {filename}",
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
    elif query.data == "command":
        await query.message.edit_text(
            text="Command information here",
            reply_markup=COMMAND_BUTTONS
        )
    elif query.data == "extra":
        await query.message.edit_text(
            text=EXTRA_TEXT,
            reply_markup=EXTRA_BUTTONS
        )
    elif query.data == "telegraph":
        await query.message.edit_text(
            text=TELEGRAPH_TEXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="extra")]])
        )
    elif query.data == "shortener":
        await query.message.edit_text(
            text=SHORTENER_TEXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="extra")]])
        )
    elif query.data == "pdf":
        await query.message.edit_text(
            text=IMAGETOPDF_TEXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="extra")]])
        )
    elif query.data == "paste":
        await query.message.edit_text(
            text=PASTE_TEXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="extra")]])
        )
    elif query.data == "webscreenshot":
        await query.message.edit_text(
            text=WEBSCREENSHOT_TEXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="extra")]])
        )
    elif query.data == "donate":
        donate_text = DONATE_TEXT.format(query.from_user.mention)
        await query.message.edit_text(
            text=donate_text,
            reply_markup=DONATE_BUTTONS,
            disable_web_page_preview=True
        )
    elif query.data == "paypal":
        await query.message.edit_text(
            text=PAYPAL_TEXT,
            reply_markup=PAYPAL_BUTTONS
        )
    elif query.data == "coffee":
        await query.message.edit_text(
            text=BUYMEACOFFEE_TEXT,
            reply_markup=BUYMEACOFFEE_BUTTONS
        )
    elif query.data == "crypto":
        await query.message.edit_text(
            text=CRYPTO_TEXT,
            reply_markup=CRYPTO_BUTTONS
        )
    elif query.data == "bitcoin":
        await query.message.edit_text(
            text=BITCOIN_TEXT,
            reply_markup=BITCOIN_BUTTONS
        )
    elif query.data == "ethereum":
        await query.message.edit_text(
            text=ETHEREUM_TEXT,
            reply_markup=ETHEREUM_BUTTONS
        )
    elif query.data == "tether":
        await query.message.edit_text(
            text=TETHER_TEXT,
            reply_markup=TETHER_BUTTONS
        )
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