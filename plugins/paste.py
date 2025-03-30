import aiohttp
import os
from pyrogram import Client, filters
from pyrogram.types import Message

# API endpoints based on https://github.com/lus/pasty/blob/master/API.md
PASTY_BASE_URL = "https://pasty.lus.pm"
PASTY_API_URL = f"{PASTY_BASE_URL}/api/v1/pastes"

@Client.on_message(filters.command("paste") & filters.private)
async def paste_text(client: Client, message: Message):
    pablo = await message.reply_text("`Please wait...`")

    # Determine the text to paste
    if message.reply_to_message:
        if message.reply_to_message.text:
            text_to_paste = message.reply_to_message.text
        elif message.reply_to_message.document:
            file_path = await message.reply_to_message.download()
            try:
                with open(file_path, "r") as file:
                    text_to_paste = file.read()
            except Exception as e:
                await pablo.edit(f"❌ Error reading file: {str(e)}")
                os.remove(file_path)
                return
            os.remove(file_path)
        else:
            await pablo.edit("`Only text and documents are supported.`")
            return
    else:
        await pablo.edit("Reply to a message containing text or a document to paste it to Pasty.")
        return

    try:
        # Create paste with proper JSON structure
        payload = {
            "content": text_to_paste,
            "title": "Untitled Paste"  # Optional title
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(PASTY_API_URL, json=payload) as response:
                if response.status == 200:
                    paste_data = await response.json()
                    
                    # Extract paste ID and create URLs according to API docs
                    paste_id = paste_data.get("id")
                    if paste_id:
                        view_url = f"{PASTY_BASE_URL}/{paste_id}"
                        raw_url = f"{PASTY_BASE_URL}/{paste_id}/raw"
                        
                        success_msg = (
                            "**✅ Successfully created paste!**\n\n"
                            f"**📎 View:** [Click Here]({view_url})\n"
                            f"**📄 Raw:** [Click Here]({raw_url})\n\n"
                            f"**🆔 Paste ID:** `{paste_id}`"
                        )
                        
                        await pablo.edit(
                            success_msg,
                            disable_web_page_preview=True
                        )
                    else:
                        await pablo.edit("❌ Failed to get paste ID from response")
                else:
                    error_response = await response.text()
                    await pablo.edit(f"❌ API Error: {response.status}\n{error_response}")
                    
    except Exception as e:
        await pablo.edit(f"❌ Error: {str(e)}")