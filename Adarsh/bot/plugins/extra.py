from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import shutil, psutil
from utils_bot import *
from Adarsh import StartTime


START_TEXT = """ Your Telegram Data Centre Is : `{}`  """


@StreamBot.on_message(filters.command("maintainers") | filters.regex("maintainers😎"))
async def maintainers(b,m):
    try:
       await b.send_message(chat_id=m.chat.id,text="HELLO",quote=True)
    except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="This Bot was Coded and being maintained By [JiC54](https://t.me/JiC54)",
                    
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Developer💻", url=f"https://t.me/JiC54_SERIES_Bot")
                            ]
                        ]
                    ),
                    parse_mode="markdown",
                    disable_web_page_preview=True)
            
         
 
@StreamBot.on_message(filters.command("maintainers") | filters.regex("maintainers😎"))
async def maintainers(b,m):
    try:
       await b.send_message(chat_id=m.chat.id,text="HELLO",quote=True)
    except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**v8.8 Changelog**\n●Fixed link buttons in channels:\n There was an issue where the bot could not create valid links in channels, this has now been fixed\n
                    ●Standard keyboard rearranged to suit small screens\n●Fixed streaming page for small screens\n●Added changelog command\n●All bugs in previous version fixed\n
                    \n**v8.6 Changelog**\n
                    •Superfast download and stream links. Download speeds up to 20mbps depending on your internet bandwidth.\n
                    •No ads in generated links.\n
                    •Superfast interface.\n
                    •Along with the links that can be copied with a single tap you also get file information like name, size ,etc.\n
                    •Support command. Get support from our team, and you can also report issues and bugs as well as sending feedback to the team.\n
                    •Password Protection. Added login command. This feature has just been introduced and will be useful in future versions.\n
                    •User Friendly Interface.\n
                    •Ping check.\n
                    •User Data Centre check.\n
                    •Real time CPU, RAM, Internet usage check.\n
                    •Channel supported. Just add bot Channel as Admin. If any new file comes in Channel it will edit it with stream and Download Link Button.\n
                    •Supports audio streaming.\n
                    •Enhanced Video streaming. Added new video player that supports many media formats and codecs. This new player also support pop up play, Fullscreen ability, download button and also allows the user to   customize settings via settings button. All these features on the video player.\n
                    •Customizable streaming page. The ability to change day & night mode added.\n
                    •Updated terms and conditions of use\n
                    •Fixed all bugs in previous version.",
                    
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Terms & Conditions", url=f"bit.ly/3xgjGWf")
                            ]
                        ]
                    ),
                    parse_mode="markdown",
                    disable_web_page_preview=True)
        
        
@StreamBot.on_message(filters.command("follow") | filters.regex("follow❤️"))
async def follow_user(b,m):
    try:
       await b.send_message(chat_id=m.chat.id,text="HELLO",quote=True)
    except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>HERE'S THE FOLLOW LINK</b>",
                    
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("FOLLOW ME", url=f"https://t.me/JiC54_dax")
                            ]
                        ]
                    ),
                    parse_mode="HTML",
                    disable_web_page_preview=True)
            
                     
        
        
@StreamBot.on_message(filters.command("dc") | filters.regex("DC"))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.dc_id)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        quote=True
    )

    
    
@StreamBot.on_message(filters.command("list"))
async def list(l, m):
    LIST_MSG = "**Hi! {} Here is a list of all my commands** \n \n **1.** `start⚡️` \n **2.** `help📚` \n **3.** `login🔑` \n **4.** `follow❤️` \n **5.** `ping📡` \n **6.** `status📊` check bot status \n **7.** `DC` this tells your telegram data center \n **8.** `maintainers😎` "
    await l.send_message(chat_id = m.chat.id,
        text = LIST_MSG.format(m.from_user.mention(style="md")),
        reply_to_message_id = m.message_id,
        parse_mode="markdown"
    )
    
    
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
