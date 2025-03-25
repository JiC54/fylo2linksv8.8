import os
import json
import aiohttp
from typing import Dict, Optional
from pyrogram import Client, filters
from pyrogram.types import Message

# Headers for API requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Content-Type": "application/json",
}

async def paste_to_pasty(content: str, extension: Optional[str] = None) -> Dict:
    """
    Upload content to pasty.lus.pm
    Args:
        content: Text content to paste
        extension: File extension (optional)
    Returns:
        Dict containing URLs or error
    """
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": content}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=siteurl, json=data, headers=HEADERS) as response:
                if response.status == 200:
                    response_data = await response.json()
                    ext = extension or "txt"
                    return {
                        "url": f"https://pasty.lus.pm/{response_data['id']}.{ext}",
                        "raw": f"https://pasty.lus.pm/{response_data['id']}/raw",
                        "bin": "Pasty"
                    }
        except Exception as e:
            return {"error": str(e)}
    
    return {"error": "Unable to reach pasty.lus.pm"}

@Client.on_message(filters.command("paste"))
async def paste_command(client: Client, message: Message) -> None:
    """Handle /paste command"""
    progress_msg = await message.reply_text("`Processing...`")
    
    try:
        # Get text content
        if message.reply_to_message:
            if message.reply_to_message.document:
                file = await message.reply_to_message.download()
                try:
                    with open(file, "r") as f:
                        content = f.read()
                finally:
                    os.remove(file)
            else:
                content = message.reply_to_message.text or message.reply_to_message.caption
        else:
            content = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else None

        if not content:
            await progress_msg.edit("`Please provide some text or reply to a message/document.`")
            return

        # Upload to pasty
        extension = "py" if message.reply_to_message and message.reply_to_message.document else "txt"
        result = await paste_to_pasty(content, extension)

        if "error" in result:
            await progress_msg.edit(f"`Failed to paste: {result['error']}`")
            return

        # Send success message
        response_text = (
            "**Successfully Pasted to Pasty**\n\n"
            f"**Link:** [Click Here]({result['url']})\n"
            f"**Raw Link:** [Click Here]({result['raw']})"
        )
        await progress_msg.edit(
            response_text,
            disable_web_page_preview=True
        )

    except Exception as e:
        await progress_msg.edit(f"`Error: {str(e)}`")