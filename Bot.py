import os
import asyncio
from telethon import TelegramClient, events, Button

# --- جلب البيانات من بيئة تشغيل Railway ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PASSWORD = os.getenv("PASSWORD")

CUSTOM_HTML_BASE = "https://marikanmarikan320-stack.github.io/EljeladD/eljelad.html"

bot = TelegramClient('eljelad_session', API_ID, API_HASH)

@bot.on(events.NewMessage)
async def eljelad_core(event):
    if event.is_group: return
    sender = event.sender_id
    text = event.raw_text

    if text == PASSWORD and sender == ADMIN_ID:
        await event.respond("<b>🦅 سـيادة القـائد.. الـمنظومة مـستعدة!</b>", parse_mode='html')
        return

    if sender == ADMIN_ID and ("tiktok.com" in text or "http" in text):
        target_url = text.strip().split()[0]
        final_html_link = f"{CUSTOM_HTML_BASE}?target={target_url}"
        
        msg = "🌪 <b>إعـصـار جـيـش الـتـبـلـيـغ:</b>\nالهدف مرصود وجاهز للاقتحام."
        buttons = [
            [Button.url("📍 اقـتـحام الـحساب", target_url)],
            [Button.url("📧 قـصف جـوي", final_html_link)]
        ]

        await event.respond(msg, buttons=buttons, parse_mode='html')

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.send_message(ADMIN_ID, "🦅 <b>الـمنظومة مـتصلة يا سـيدي.. بـانتظار الإشارة.</b>", parse_mode='html')
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
