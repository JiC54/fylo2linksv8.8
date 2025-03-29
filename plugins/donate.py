from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Donation Texts
DONATE_TEXT = """Dear {},

I, the service's developer, am struggling to pay for servers in order to keep the service online. Running this service for a month costs $10. Whereby Only $7 is spent on Heroku, with the remaining $3 spent on databases. You can help keep this service alive today by donating any amount. Just click below and select a method.

Thank you for everything you do. I couldn’t do this without you.

All the best,

FilesToLinks"""

BITCOIN_TEXT = """<b>Use the following address to deposit ONLY Bitcoin (BTC):</b>

<code>1Hahm7m65tsv6NMdrKJmyvsFFrE6orjUA9</code>"""
ETHEREUM_TEXT = """<b>Use the following address to deposit ONLY Ethereum (ETH):</b>

<code>0xa5c60C36422f3f77638B7C4875C6108641cCa77b</code>"""
TETHER_TEXT = """<b>Use the following address to deposit ONLY Tether (USDT):</b>

<code>TYmPURwxpFUV8s7SS7qM2Wzujex2XK4CzA</code>"""
CRYPTO_TEXT = """Choose a cryptocurrency from the list below, and then use the address that appears. If the transaction was successful, snap a screenshot and send it to @jumahmw. We will add you to our donors list as a reward and way of saying "thank you" for your generosity, giving you access to extra services.

If you run across any problems while donating crypto, contact @jooma265 immediately."""
PAYPAL_TEXT = """To make a donation, please use the button below. If the transaction was successful, snap a screenshot and send it to @jumahmw. We'll add you to our contributors list, where you'll be able to enjoy additional services as a reward and a 'thank you' for your support.

Contact @jooma265 if you experience any difficulties while making a donation via PayPal."""
BUYMEACOFFEE_TEXT = """To donate, click the button below. Take a screenshot and send it to @jumahmw if the transaction was successful. As a reward and way of saying "thank you" for your donation, we will add you to our donors list, where you will have access to additional services.

Contact @jooma265 if you experience any difficulties while buying me a coffee."""

# Inline Buttons
DONATE_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('PAYPAL', callback_data='paypal'),
        InlineKeyboardButton('BUY ME A COFFEE', callback_data='coffee')
    ], [
        InlineKeyboardButton('CRYPTO', callback_data='crypto'),
        InlineKeyboardButton('CLOSE', callback_data='close')
    ]]
)
PAYPAL_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('DONATE VIA PAYPAL', url='https://bit.ly/3BNvGAv')
    ], [
        InlineKeyboardButton('BACK', callback_data='donate'),
        InlineKeyboardButton('CLOSE', callback_data='close')
    ]]
)
BUYMEACOFFEE_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('BUY ME A COFFEE☕️', url='https://bit.ly/3SkoItT')
    ], [
        InlineKeyboardButton('BACK', callback_data='donate'),
        InlineKeyboardButton('CLOSE', callback_data='close')
    ]]
)
CRYPTO_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('BITCOIN [BTC]', callback_data='bitcoin'),
        InlineKeyboardButton('ETHEREUM [ETH]', callback_data='ethereum')
    ], [
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

# Command Handler
@Client.on_message(filters.command("donate") & filters.private)
async def donate(client: Client, message: Message):
    donate = DONATE_TEXT.format(message.from_user.mention)
    await message.reply_text(
        text=donate,
        reply_markup=DONATE_BUTTONS,
        disable_web_page_preview=True
    )

# Callback Query Handler
@Client.on_callback_query()
async def handle_donate_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    if data == "paypal":
        await callback_query.message.edit_text(
            text=PAYPAL_TEXT,
            reply_markup=PAYPAL_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "coffee":
        await callback_query.message.edit_text(
            text=BUYMEACOFFEE_TEXT,
            reply_markup=BUYMEACOFFEE_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "crypto":
        await callback_query.message.edit_text(
            text=CRYPTO_TEXT,
            reply_markup=CRYPTO_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "bitcoin":
        await callback_query.message.edit_text(
            text=BITCOIN_TEXT,
            reply_markup=BITCOIN_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "ethereum":
        await callback_query.message.edit_text(
            text=ETHEREUM_TEXT,
            reply_markup=ETHEREUM_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "tether":
        await callback_query.message.edit_text(
            text=TETHER_TEXT,
            reply_markup=TETHER_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "donate":
        await callback_query.message.edit_text(
            text=DONATE_TEXT.format(callback_query.from_user.mention),
            reply_markup=DONATE_BUTTONS,
            disable_web_page_preview=True
        )
    elif data == "close":
        await callback_query.message.delete()