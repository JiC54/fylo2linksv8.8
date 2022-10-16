# JiC54
import os
import asyncio
import aiohttp
from JiC54.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram import Client, filters
import time
import shutil, psutil
from utils_bot import *
from JiC54 import StartTime
from pyshorteners import Shortener
from pyrogram.handlers import MessageHandler
from urllib.parse import quote

BITLY_API = os.environ.get("BITLY_API", "8df1df8c23f719e5cf97788cc2d40321ea30092b")
CUTTLY_API = os.environ.get("CUTTLY_API", "8cb59cbecc2d349e4a0f31f05a8b020655b83")
SHORTCM_API = os.environ.get("SHORTCM_API", "pk_...NIZv")
GPLINKS_API = os.environ.get("GPLINKS_API", "3f84819e8fd9f234b0150fb6d39e7ab9b6bf370c")

START_TEXT = """ Your Telegram DC Is : `{}`  """
HELP_TEXT = """Everything has fully been explained very well in our website including About the bot, Features, FAQ, Copyright, Terms of use, Child Abuse Policy, DMCA and many more.
So, please consider visiting our website."""
ABOUT_TEXT = """With this service, you may post files to the internet by simply uploading or forwarding files to this bot and receive both a direct download link and a streamable URL for the contents.

Learn more about this service by visiting its website, click below."""
DONATE_TEXT = """ Dear {},

I, the service's developer, am struggling to pay for servers in order to keep the service online. Running this service for a month costs $10. Whereby Only $7 is spent on Heroku, with the remaining $3 spent on databases. You can help keep this service alive today by donating any amount. Just click below and select a method.

Thank you for everything you do. I couldn’t do this without you.

All the best,

FilesToLinks"""
COMMAND_TEXT = """Here's a list of commands

/id check your telegram ID
/premium check if you're a premium TG user
/ping Check connection speed
/verified Check if you're a telegram verified user
/info Check bot's information
/feedback Send feedback to the developers
/dc Your Telegram Data Centre
"""
MENU_TEXT = """Here is a menu for this bot"""
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
TELEGRAPH_TEXT = """This feature, allows you to upload media on telegraph.

Just reply with /telegraph command to a media and the telegraph link will be generated and sent to you

<b>NOTE</b>
- Only videos and pictures can be uploaded to telegraph
- Maximum size of media that can be uploaded to telegraph is 5mb
- Supported media formats; .jpg, .jpeg, .png, .gif, .mp4"""
SHORTENER_TEXT = """This feature enables you to shorten links.
Just type /short command along with the link you want to shorten

For example;

<code>/short https://www.twosix5.blogspot.com</code>"""
EXTRA_TEXT = """Extra features are listed below. For the time being, all users may access these bonuses because they were created as a thank-you and a reward for supporters (donors).
However, this access will soon expire to all users who haven'nt made any donation. Therefore, /donate right now to be added to our donor list; further benefits are on the way for donors!"""
TELEGRAPH_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BACK', callback_data='extra'),
        InlineKeyboardButton('MENU', callback_data='menu'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
SHORTENER_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BACK', callback_data='extra'),
        InlineKeyboardButton('MENU', callback_data='menu'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('VISIT WEBSITE', url='https://bit.ly/3DgxO6h')
        ],[
        InlineKeyboardButton('BACK', callback_data='menu'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('WEBSITE', url='https://bit.ly/3DgxO6h')
        ],[
        InlineKeyboardButton('BACK', callback_data='menu'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
DONATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('PAYPAL', callback_data='paypal'),
        InlineKeyboardButton('BUY ME A COFFEE', callback_data='coffee')
        ],[
        InlineKeyboardButton('CRYPTO', callback_data='crypto'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
PAYPAL_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('DONATE VIA PAYPAL', url='https://bit.ly/3BNvGAv')
        ],[
        InlineKeyboardButton('BACK', callback_data='donate'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
BUYMEACOFFEE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BUY ME A COFFEE☕️', url='https://bit.ly/3SkoItT')
        ],[
        InlineKeyboardButton('BACK', callback_data='donate'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
)
CRYPTO_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BITCOIN [BTC]', callback_data='bitcoin'),
        InlineKeyboardButton('ETHEREUM [ETH]', callback_data='ethereum')
        ],[
        InlineKeyboardButton('TETHER [USDT]', callback_data='tether'),
        InlineKeyboardButton('BACK', callback_data='donate')
        ]]
)
BITCOIN_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BACK', callback_data='crypto')
        ]]
)
TETHER_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BACK', callback_data='crypto')
        ]]
)
ETHEREUM_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('BACK', callback_data='crypto')
        ]]
)
MENU_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("COMMANDS", callback_data="command"),
        InlineKeyboardButton("EXTRA", callback_data="extra")
        ],
        [
        InlineKeyboardButton("ABOUT", callback_data="about"),      
        InlineKeyboardButton("HELP", callback_data="help")
        ],
        [
        InlineKeyboardButton("CLOSE", callback_data="close")
        ]]
)
COMMAND_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("BACK", callback_data="menu"),
        InlineKeyboardButton("CLOSE", callback_data="close")
        ]]
)
EXTRA_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("TELEGRAPH", callback_data="telegraph"),
        InlineKeyboardButton("SHORTENER", callback_data="shortener")
        ],
        [
        InlineKeyboardButton("BACK", callback_data="menu"),
        InlineKeyboardButton("CLOSE", callback_data="close")
        ]]
)

@StreamBot.on_message(filters.command("maintainers") | filters.regex("maintainers😎"))
async def maintainers(b,m):
    try:
       await b.send_message(chat_id=m.chat.id,text="HELLO",quote=True)
    except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="This Bot was Coded and being maintained By [JiC54](https://t.me/jic54_official)",

                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Developer💻", url=f"https://t.me/jic54_official")
                            ]
                        ]
                    ),

                    disable_web_page_preview=True)


@StreamBot.on_message(filters.command("donate") | filters.regex("DONATE❤️"))
async def follow_user(b,m):
    try:
       await b.send_message(chat_id=m.chat.id,text="HELLO",quote=True)
    except Exception:
                donate = DONATE_TEXT.format(m.from_user.mention)
                await b.send_message(
                    chat_id=m.chat.id,
                    text=donate,
                    reply_markup=DONATE_BUTTONS,
                    disable_web_page_preview=True)


@StreamBot.on_message(filters.regex("DC"))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.dc_id)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        quote=True
    )



@StreamBot.on_message(filters.command("menu") | filters.regex("MENU📊"))
async def list(l, m):
    await l.send_message(chat_id = m.chat.id,
        text = MENU_TEXT, reply_markup=MENU_BUTTONS)


@StreamBot.on_message(filters.command("ping") | filters.regex("ping📡"))
async def ping(b, m):
    start_t = time.time()
    ag = await m.reply_text("....")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await ag.edit(f"Pong!\n{time_taken_s:.3f} ms")

@StreamBot.on_message(filters.private & filters.regex("status📊"))
async def stats(bot, update):
  currentTime = readable_time((time.time() - StartTime))
  total, used, free = shutil.disk_usage('.')
  total = get_readable_file_size(total)
  used = get_readable_file_size(used)
  free = get_readable_file_size(free)
  sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
  recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
  cpuUsage = psutil.cpu_percent(interval=0.5)
  memory = psutil.virtual_memory().percent
  disk = psutil.disk_usage('/').percent
  botstats = f'<b>Bot Uptime:</b> {currentTime}\n' \
            f'<b>Total disk space:</b> {total}\n' \
            f'<b>Used:</b> {used}  ' \
            f'<b>Free:</b> {free}\n\n' \
            f'📊Data Usage📊\n<b>Upload:</b> {sent}\n' \
            f'<b>Down:</b> {recv}\n\n' \
            f'<b>CPU:</b> {cpuUsage}% ' \
            f'<b>RAM:</b> {memory}% ' \
            f'<b>Disk:</b> {disk}%'
  await update.reply_text(botstats)

@StreamBot.on_message(filters.command("gist"))
async def gist(g, m):

    LIST_MSG = "Hi! {} Here is a list of all my commands \n \n 1 . `start⚡️` \n 2. `help📚` \n 3. `login🔑` \n 4.`follow❤️` \n 5. `ping📡` \n 6. `status📊` \n 7. `DC` this tells your telegram dc \n 8. `maintainers😎` "
    await g.send_message(chat_id = m.chat.id,
        text = LIST_MSG.format(m.from_user.mention(style="md")),
                    reply_markup=HELP_BUTTONS)
@StreamBot.on_message(filters.command("id"))
async def id(j, m):
    await j.send_message(chat_id = m.chat.id,
        text = ID_MSG.format(m.from_user.id))

@StreamBot.on_message(filters.command("verified"))
async def verified(v, m):
    verified = "You are a verified Telegram user: <b>{}</b>"
    await v.send_message(chat_id = m.chat.id,
        text = verified.format(m.from_user.is_verified))

@StreamBot.on_message(filters.command("premium"))
async def is_premium(p, m):
    premium = "You are a premium Telegram user: <b>{}</b>"
    await p.send_message(chat_id = m.chat.id,
        text = premium.format(m.from_user.is_premium))

@StreamBot.on_message(filters.command("info"))
async def info(i, m):
    info = """<b><u>Bot Info</u></b>

Version:              10.0.0
Updated on:      Oct 15, 2022
Offered By:        JiC54
Released on:     Feb 21, 2022"""
    await i.send_message(chat_id = m.chat.id,
        text = info)

@StreamBot.on_message(filters.command("feedback"))
async def feedback(f, m):
    feedback_text = """<b>How can we improve FilesToLinks so that it serves you the best?</b>
<i>Regarding anything, we want your opinion.</i>

Dear {},
We never stop striving to create FilesToLinks exactly what you require for your professional or domestic use. We need your input today to help us make FilesToLinks the best it can be.  Your feedback helps us decide which features to add and what enhancements should be made to our platform. To provide feedback, please click below."""
    feedback_buttons = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("GIVE FEEDBACK", url="https://t.me/jic54feedback")
        ]])
    await f.send_message(chat_id = m.chat.id,
        text = feedback_text.format(m.from_user.mention),
        reply_markup = feedback_buttons,
        disable_web_page_preview=False)

@StreamBot.on_message(filters.command("dc"))
async def dc(d, m):
    dcid = """<b>Your Telegram data centre is:</b> <code>{}</code>"""
    await d.send_message(chat_id = m.chat.id,
        text = dcid.format(m.from_user.dc_id))

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data=="donate":
        await update.message.edit_text(
            text=DONATE_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=DONATE_BUTTONS
            )
    elif update.data=="crypto":
        await update.message.edit_text(
            text=CRYPTO_TEXT,
            disable_web_page_preview=True,
            reply_markup=CRYPTO_BUTTONS
            )
    elif update.data=="bitcoin":
        close_bitcoin = await update.message.edit_text(
            text=BITCOIN_TEXT,
            disable_web_page_preview=True,
            reply_markup=BITCOIN_BUTTONS
            )
        await asyncio.sleep(150)
        await close_bitcoin.edit(
            text=DONATE_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=DONATE_BUTTONS
            )
    elif update.data=="ethereum":
        close_ethereum = await update.message.edit_text(
            text=ETHEREUM_TEXT,
            disable_web_page_preview=True,
            reply_markup=ETHEREUM_BUTTONS
            )
        await asyncio.sleep(150)
        await close_ethereum.edit(
            text=DONATE_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=DONATE_BUTTONS
            )
    elif update.data=="tether":
        close_tether = await update.message.edit_text(
            text=TETHER_TEXT,
            disable_web_page_preview=True,
            reply_markup=TETHER_BUTTONS
            )
        await asyncio.sleep(150)
        await close_tether.edit(
            text=DONATE_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=DONATE_BUTTONS
            )
    elif update.data=="menu":
        await update.message.edit_text(
            text=MENU_TEXT,
            disable_web_page_preview=True,
            reply_markup=MENU_BUTTONS
            )
    elif update.data=="command":
        await update.message.edit_text(
            text=COMMAND_TEXT,
            disable_web_page_preview=True,
            reply_markup=COMMAND_BUTTONS
            )
    elif update.data=="paypal":
        close_paypal = await update.message.edit_text(
            text=PAYPAL_TEXT,
            disable_web_page_preview=True,
            reply_markup=PAYPAL_BUTTONS
            )
        await asyncio.sleep(300)
        await close_paypal.edit(
            text=DONATE_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=DONATE_BUTTONS
            )
    elif update.data=="coffee":
        await update.message.edit_text(
            text=BUYMEACOFFEE_TEXT,
            disable_web_page_preview=True,
            reply_markup=BUYMEACOFFEE_BUTTONS
            )
    elif update.data=="telegraph":
        await update.message.edit_text(
            text=TELEGRAPH_TEXT,
            disable_web_page_preview=True,
            reply_markup=TELEGRAPH_BUTTONS
            )
    elif update.data=="shortener":
        await update.message.edit_text(
            text=SHORTENER_TEXT,
            disable_web_page_preview=True,
            reply_markup=SHORTENER_BUTTONS
            )
    elif update.data=="extra":
        await update.message.edit_text(
            text=EXTRA_TEXT,
            disable_web_page_preview=True,
            reply_markup=EXTRA_BUTTONS
            )
    elif update.data=="premium":
        hi = f"This user is a premium user: {update.from_user.is_premium}"
        await update.answer(text=hi, show_alert=True)
    else:
        await update.message.delete()
@StreamBot.on_message(filters.command(["short"]) & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        disable_web_page_preview=True
    )

@StreamBot.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0),
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            )
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--SHORTENED URLs--**\n"
    
    # Bit.ly shorten
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bitly : ** {url}"
        except Exception as error:
            print(f"Bit.ly error :- {error}")
    
    # Chilp.it shorten
    try:
        s = Shortener()
        url = s.chilpit.short(link)
        shorten_urls += f"\n**Chilpit : ** {url}"
    except Exception as error:
        print(f"Chilp.it error :- {error}")
    
    # Cutt.ly shorten
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cuttly : ** {url}"
        except Exception as error:
            print(f"Cutt.ly error :- {error}")
    
    # Da.gd shorten
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**Dagd : ** {url}"
    except Exception as error:
        print(f"Da.gd error :- {error}")
    
    
    # Osdb.link shorten
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**Osdblink : ** {url}"
    except Exception as error:
        print(f"Osdb.link error :- {error}")
    
    
    # Short.cm shorten
    if SHORTCM_API:
        try:
            s = Shortener(api_key=SHORTCM_API)
            url = s.shortcm.short(link)
            shorten_urls += f"\n**Shortcm : ** {url}"
        except Exception as error:
            print(f"Short.cm error :- {error}")
    
    # TinyURL.com shorten
    try:
        s = Shortener()
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**TinyURL : ** {url}"
    except Exception as error:
        print(f"TinyURL.com error :- {error}")
    
    # GPLinks shorten
    try:
        api_url = "https://gplinks.in/api"
        params = {'api': GPLINKS_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**GPLinks : ** {url}"
    except Exception as error:
        print(f"GPLink error :- {error}")
    
    # Send the text
    try:
        shorten_urls += "\n\nPlease note that this feature is for our donors, you may soon not be able to use it if you haven't made any donation, so please /donate to continue accessing this awesome feature."
        return shorten_urls
    except Exception as error:
        return error
