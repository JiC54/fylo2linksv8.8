import aiohttp
import os
from pyrogram import Client, filters
from pyrogram.types import Message

# API endpoints
PASTY_BASE_URL = "https://pasty.lus.pm"
PASTY_API_URL = PASTY_BASE_URL  # Using base URL

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Content-Type": "application/json",
}

async def p_paste(text, extension=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{PASTY_API_URL}/api/v1/pastes", json={"content": text}, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    paste_id = data.get("id")
                    if paste_id:
                        purl = f"{PASTY_BASE_URL}/{paste_id}"
                        raw_url = f"{purl}/raw"
                        return {
                            "url": purl,
                            "raw": raw_url,
                            "bin": "Pasty",
                        }
                    else:
                        return {"error": "Unable to retrieve paste ID"}
                else:
                    return {"error": f"API request failed with status {response.status}"}
    except Exception as e:
        return {"error": str(e)}

@Client.on_message(filters.command("paste") & filters.private)
async def pasty(client: Client, message: Message):
    pablo = await message.reply_text("`Please wait...`")
    text = message.text
    message_s = text

    if not text:
        if not message.reply_to_message:
            await pablo.edit("`Only text and documents are supported.`")
            return

        if message.reply_to_message.text:
            message_s = message.reply_to_message.text
        elif message.reply_to_message.document:
            file_path = await message.reply_to_message.download()
            try:
                with open(file_path, "r") as file:
                    message_s = file.read()
            except Exception as e:
                await pablo.edit(f"❌ Error reading file: {str(e)}")
                os.remove(file_path)
                return
            os.remove(file_path)
        else:
            await pablo.edit("`Only text and documents are supported.`")
            return

    ext = "py"
    result = await p_paste(message_s, ext)

    if "error" in result:
        await pablo.edit(f"❌ Error: {result['error']}")
    else:
        p_link = result["url"]
        p_raw = result["raw"]
        pasted = f"**✅ Successfully Pasted to Pasty!**\n\n**🔗 Link:** [Click here]({p_link})\n\n**📄 Raw Link:** [Click here]({p_raw})"
        await pablo.edit(pasted, disable_web_page_preview=True)