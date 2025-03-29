import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

PASTY_API_URL = "https://pasty.lus.pm/api/v1/pastes"  # Pasty API URL

@Client.on_message(filters.command("paste") & filters.private)
async def paste_text(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply_text(
            "Reply to a message containing text to paste it to Pasty.",
            quote=True
        )
        return

    text_to_paste = message.reply_to_message.text

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(PASTY_API_URL, json={"content": text_to_paste}) as response:
                if response.status == 201:  # HTTP 201 Created
                    paste_data = await response.json()
                    paste_url = paste_data.get("url")
                    await message.reply_text(
                        f"✅ Text successfully pasted!\n\n🔗 [View Paste]({paste_url})",
                        disable_web_page_preview=True,
                        quote=True
                    )
                else:
                    await message.reply_text(
                        f"❌ Failed to paste text. Server responded with status code {response.status}.",
                        quote=True
                    )
    except Exception as e:
        await message.reply_text(
            f"❌ An error occurred while pasting the text: {e}",
            quote=True
        )