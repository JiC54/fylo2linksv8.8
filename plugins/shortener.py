import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyshorteners import Shortener

# API Keys
BITLY_API = os.environ.get("BITLY_API", "8df1df8c23f719e5cf97788cc2d40321ea30092b")
CUTTLY_API = os.environ.get("CUTTLY_API", "8cb59cbecc2d349e4a0f31f05a8b020655b83")

async def shorten_url(url: str) -> str:
    """Shorten URL using multiple services"""
    shortened_urls = ["**📎 Shortened URLs**"]
    
    # Initialize shortener
    s = Shortener()
    
    # TinyURL (No API required)
    try:
        tiny_url = s.tinyurl.short(url)
        shortened_urls.append(f"\n**TinyURL:** {tiny_url}")
    except Exception as e:
        print(f"TinyURL error: {e}")
    
    # Bitly
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            bitly_url = s.bitly.short(url)
            shortened_urls.append(f"\n**Bitly:** {bitly_url}")
        except Exception as e:
            print(f"Bitly error: {e}")
    
    # Cuttly
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            cuttly_url = s.cuttly.short(url)
            shortened_urls.append(f"\n**Cuttly:** {cuttly_url}")
        except Exception as e:
            print(f"Cuttly error: {e}")

    # Da.gd
    try:
        s = Shortener()
        dagd_url = s.dagd.short(url)
        shortened_urls.append(f"\n**Dagd:** {dagd_url}")
    except Exception as e:
        print(f"Da.gd error: {e}")
    
    shortened_urls.append("\n\n**Note:** This feature is for donors only. Please /donate to continue using it.")
    return "\n".join(shortened_urls)

@Client.on_message(filters.command("short") & filters.regex(r'https?://[^\s]+'))
async def short_command(client: Client, message: Message) -> None:
    """Handle /short command"""
    try:
        # Send processing message
        progress_msg = await message.reply_text(
            "`🔄 Processing your link...`",
            quote=True
        )
        
        # Get URL from message
        url = message.matches[0].group(0)
        
        # Get shortened URLs
        result = await shorten_url(url)
        
        # Create buttons
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Shorten Another", callback_data="new_short"),
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ])
        
        # Edit progress message with results
        await progress_msg.edit_text(
            result,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        await progress_msg.edit_text(f"❌ Error: {str(e)}")

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    """Handle button callbacks"""
    try:
        if query.data == "new_short":
            await query.message.edit_text(
                "Send a new link with /short command\n"
                "Example: `/short https://example.com`"
            )
        elif query.data == "close":
            await query.message.delete()
    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)