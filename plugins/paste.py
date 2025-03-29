import aiohttp
import os
from pyrogram import Client, filters
from pyrogram.types import Message

PASTY_API_URL = "https://pasty.lus.pm/api/v1/pastes"  # Pasty API URL

@Client.on_message(filters.command("paste") & filters.private)
async def paste_text(client: Client, message: Message):
    pablo = await message.reply_text("`Please wait...`")

    # Determine the text to paste
    if message.reply_to_message:
        if message.reply_to_message.text:
            text_to_paste = message.reply_to_message.text
        elif message.reply_to_message.document:
            file_path = await message.reply_to_message.download()
            with open(file_path, "r") as file:
                text_to_paste = file.read()
            os.remove(file_path)
        else:
            await pablo.edit("`Only text and documents are supported.`")
            return
    else:
        await pablo.edit("Reply to a message containing text or a document to paste it to Pasty.")
        return

    # Send the text to Pasty
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(PASTY_API_URL, json={"content": text_to_paste}) as response:
                if response.status in [200, 201]:  # Accept both 200 and 201 as success
                    paste_data = await response.json()
                    paste_url = paste_data.get("url")
                    if paste_url:
                        await pablo.edit(
                            f"✅ **Successfully pasted to Pasty!**\n\n🔗 [View Paste]({paste_url})",
                            disable_web_page_preview=True
                        )
                    else:
                        await pablo.edit("❌ Failed to retrieve the paste URL from the server response.")
                else:
                    await pablo.edit(f"❌ Failed to paste text. Server responded with status code {response.status}.")
    except Exception as e:
        await pablo.edit(f"❌ An error occurred while pasting the text: {e}")