import aiohttp
import os
from pyrogram import Client, filters
from pyrogram.types import Message

PASTY_API_URL = "https://pasty.lus.pm/api/v1/pastes"

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
        async with aiohttp.ClientSession() as session:
            async with session.post(
                PASTY_API_URL,
                json={"content": text_to_paste}
            ) as response:
                if response.status == 200:
                    paste_data = await response.json()
                    if "id" in paste_data:
                        paste_id = paste_data["id"]
                        paste_url = f"https://pasty.lus.pm/{paste_id}"
                        await pablo.edit(
                            f"**✅ Successfully pasted!**\n\n"
                            f"**🔗 Link:** [Click Here]({paste_url})",
                            disable_web_page_preview=True
                        )
                    else:
                        await pablo.edit("❌ Failed to get paste ID from response")
                else:
                    await pablo.edit(f"❌ Failed to paste text: {response.status}")
    except Exception as e:
        await pablo.edit(f"❌ Error: {str(e)}")