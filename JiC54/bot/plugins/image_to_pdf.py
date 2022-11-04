from io import BytesIO
from os import path, remove
from time import time
import img2pdf
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message
from JiC54.bot import StreamBot as app
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
import sys
import traceback
from functools import wraps
import logging

LOGGER = logging.getLogger('[ImageToPDF]')

n = "\n"
w = " "


bold = lambda x: f"**{x}:** "
bold_ul = lambda x: f"**--{x}:**-- "

mono = lambda x: f"`{x}`{n}"


def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:

    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        text += (
            indent * w
            + bold(key)
            + ((value[0] + n) if isinstance(value, list) else mono(value))
        )
    return text

def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await app.send_message(LOGGER, x)
            raise err

    return capture

async def convert(
    main_message: Message,
    reply_messages,
    status_message: Message,
    start_time: float,
):
    m = status_message

    documents = []

    for message in reply_messages:
        if not message.document:
            return await m.edit("Not document, ABORTED!")

        if message.document.mime_type.split("/")[0] != "image":
            return await m.edit("Invalid mime type!")

        if message.document.file_size > 5000000:
            return await m.edit("Size too large, ABORTED!")
        documents.append(await message.download())

    for img_path in documents:
        img = Image.open(img_path).convert("RGB")
        img.save(img_path, "JPEG", quality=100)

    pdf = BytesIO(img2pdf.convert(documents))
    pdf.name = "NaoRobot.pdf"

    if len(main_message.command) >= 2:
        pdf.name = main_message.text.split(None, 1)[1]

    elapsed = round(time() - start_time, 2)

    await main_message.reply_document(
        document=pdf,
        caption=section(
            "IMG2PDF",
            body={
                "Title": pdf.name,
                "Size": f"{pdf.__sizeof__() / (10**6)}MB",
                "Pages": len(documents),
                "Took": f"{elapsed}s",
            },
        ),
    )

    await m.delete()
    pdf.close()
    for file in documents:
        if path.exists(file):
            remove(file)


@app.on_message(filters.command("pdf"))
@capture_err
async def img_to_pdf(_, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            "Reply to an image (as document) or group of images."
        )

    m = await message.reply_text("Converting..")
    start_time = time()

    if reply.media_group_id:
        messages = await app.get_media_group(
            message.chat.id,
            reply.message_id,
        )
        return await convert(message, messages, m, start_time)

    return await convert(message, [reply], m, start_time)
