# JiC54
import os
import aiohttp
from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram import Client, filters
import time
import shutil, psutil
from utils_bot import *
from Adarsh import StartTime
from pyshorteners import Shortener
from pyrogram.handlers import MessageHandler
from urllib.parse import quote

BITLY_API = os.environ.get("BITLY_API", "8df1df8c23f719e5cf97788cc2d40321ea30092b")
CUTTLY_API = os.environ.get("CUTTLY_API", "f64dffbde033b6c307387dd50b7c76e505f1c")
SHORTCM_API = os.environ.get("SHORTCM_API", "pk_...NIZv")
GPLINKS_API = os.environ.get("GPLINKS_API", "008ccaedd6061ad1948838f410947603de9007a7")

START_TEXT = """ Your Telegram DC Is : `{}`  """
HELP_TEXT = """Everything has fully been explained very well in our website including About the bot, Features, FAQ, Copyright, Terms of use, Child Abuse Policy, DMCA and many more.
So, please consider visiting our website."""
ABOUT_TEXT = """With this service, you may post files to the internet by simply uploading or forwarding files to this bot and receive both a direct download link and a streamable URL for the contents.

Learn more about this service by visiting its website, click below."""
DONATE_TEXT = """ Dear {},

Right now, we're facing struggles to pay for servers to keep this service alive as well as to buy resources such as a domain for this services. We need just $10 a month to meet our goal whereby only $7 lets us run this bot a whole month on heroku and the reamining $3 is spent on databases.

Please donate <b>any little amount</b> today to ensure this service stays alive. Just click below and select a method.

Thank you for everything you do. We couldn’t do this without you.

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
MENU_TEXT = """Here is a list of all my commands."""
BITCOIN_TEXT = """<b>Use the following address to deposit ONLY Bitcoin (BTC):</b>

<code>38mRQgsPoRTZvcMUFpXGMf9HjL8MxjjUzE</code>"""
ETHEREUM_TEXT = """<b>Use the following address to deposit ONLY Ethereum (ETH):</b>

<code>0xa5c60C36422f3f77638B7C4875C6108641cCa77b</code>"""
TETHER_TEXT = """<b>Use the following address to deposit ONLY Tether (USDT):</b>

<code>TVekMwDh42vjXy5NbNrQPAKdBgzypDLRk6</code>"""
CRYPTO_TEXT = """<b>Please select a crypto currency.</b>"""
ID_MSG = """Your Telegram Id is <code>{}</code>"""
VERIFIED_TEXT = """You are a verified Telegram user"""
NOTVERIFIED_TEXT = """You are not a verified Telegram user"""
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
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('♻️ Update Channel', url='https://telegram.me/tellybots_4u'),
        InlineKeyboardButton('💬 Support Group', url='https://telegram.me/tellybots_support')
        ],[
        InlineKeyboardButton('♨️ Help', callback_data='help'),
        InlineKeyboardButton('🗑️ Close', callback_data='close')
        ]]
)
DONATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('PAYPAL', url='https://bit.ly/3BNvGAv'),
        InlineKeyboardButton('BUY ME A COFFEE', url='https://bit.ly/3SkoItT')
        ],[
        InlineKeyboardButton('CRYPTO', callback_data='crypto'),
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
        InlineKeyboardButton("HELP", callback_data="help"),
        InlineKeyboardButton("ABOUT", callback_data="about")
        ],[
        InlineKeyboardButton("COMMANDS", callback_data="command"),
        InlineKeyboardButton("CLOSE", callback_data="close")
        ]]
)
COMMAND_BUTTONS = InlineKeyboardMarkup(
        [[
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

Version:              9.8.0
Updated on:      Oct 03, 2022
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
        await update.message.edit_text(
            text=BITCOIN_TEXT,
            disable_web_page_preview=True,
            reply_markup=BITCOIN_BUTTONS
            )
    elif update.data=="ethereum":
        await update.message.edit_text(
            text=ETHEREUM_TEXT,
            disable_web_page_preview=True,
            reply_markup=ETHEREUM_BUTTONS
            )
    elif update.data=="tether":
        await update.message.edit_text(
            text=TETHER_TEXT,
            disable_web_page_preview=True,
            reply_markup=TETHER_BUTTONS
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
    shorten_urls = "**--Shorted URLs--**\n"
    
    # Bit.ly shorten
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bit.ly :-** {url}"
        except Exception as error:
            print(f"Bit.ly error :- {error}")
    
    # Chilp.it shorten
    try:
        s = Shortener()
        url = s.chilpit.short(link)
        shorten_urls += f"\n**Chilp.it :-** {url}"
    except Exception as error:
        print(f"Chilp.it error :- {error}")
    
    # Clck.ru shorten
    try:
        s = Shortener()
        url = s.clckru.short(link)
        shorten_urls += f"\n**Clck.ru :-** {url}"
    except Exception as error:
        print(f"Click.ru error :- {error}")
    
    # Cutt.ly shorten
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cutt.ly :-** {url}"
        except Exception as error:
            print(f"Cutt.ly error :- {error}")
    
    # Da.gd shorten
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**Da.gd :-** {url}"
    except Exception as error:
        print(f"Da.gd error :- {error}")
    
    # Is.gd shorten
    try:
        s = Shortener()
        url = s.isgd.short(link)
        shorten_urls += f"\n**Is.gd :-** {url}"
    except Exception as error:
        print(f"Is.gd error :- {error}")
    
    # Osdb.link shorten
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**Osdb.link :-** {url}"
    except Exception as error:
        print(f"Osdb.link error :- {error}")
    
    # Ow.ly shorten
    try:
        s = Shortener()
        url = s.owly.short(link)
        shorten_urls += f"\n**Ow.ly :-** {url}"
    except Exception as error:
        print(f"Ow.ly error :- {error}")
    
    # Po.st shorten
    try:
        s = Shortener()
        url = s.post.short(link)
        shorten_urls += f"\n**Po.st :-** {url}"
    except Exception as error:
        print(f"Po.st error :- {error}")
    
    # Qps.ru shorten
    try:
        s = Shortener()
        url = s.qpsru.short(link)
        shorten_urls += f"\n**Qps.ru :-** {url}"
    except Exception as error:
        print(f"Qps.ru error :- {error}")
    
    # Short.cm shorten
    if SHORTCM_API:
        try:
            s = Shortener(api_key=SHORTCM_API)
            url = s.shortcm.short(link)
            shorten_urls += f"\n**Short.cm :-** {url}"
        except Exception as error:
            print(f"Short.cm error :- {error}")
    
    # TinyURL.com shorten
    try:
        s = Shortener()
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**TinyURL.com :-** {url}"
    except Exception as error:
        print(f"TinyURL.com error :- {error}")
    
    # NullPointer shorten
    try:
        s = Shortener(domain='https://0x0.st')
        url = s.nullpointer.short(link)
        shorten_urls += f"\n**0x0.st :-** {url}"
    except Exception as error:
        print(f"NullPointer error :- {error}")
    
    # GPLinks shorten
    try:
        api_url = "https://gplinks.in/api"
        params = {'api': GPLINKS_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**GPLinks.in :-** {url}"
    except Exception as error:
        print(f"GPLink error :- {error}")
    
    # Send the text
    try:
        shorten_urls += "\n\ndon't forget to /donate"
        return shorten_urls
    except Exception as error:
        return error

