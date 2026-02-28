import os
import asyncio
from telethon import TelegramClient, events, Button

# --- 🛰 إحداثيات القيادة العليا (تسحب من الخزنة السرية في رندر) ---
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
PASSWORD = os.environ.get('PASSWORD')
CUSTOM_HTML_BASE = os.environ.get('CUSTOM_HTML_BASE')

# تشغيل البوت
bot = TelegramClient('eljelad_session', API_ID, API_HASH)

@bot.on(events.NewMessage)
async def eljelad_core(event):
    if event.is_group: return
    sender = event.sender_id
    text = event.raw_text

    # 🎖 نظام التحقق من القائد
    if text == PASSWORD and sender == ADMIN_ID:
        await event.respond("<b>🦅 سـيادة القـائد.. الـمنظومة مـستعدة لـتلقي الإحـداثيات وبـدء الـهجوم!</b>", parse_mode='html')
        return

    # 🚀 استقبال الهدف وإرسال البلاغ للقناة
    if sender == ADMIN_ID and ("tiktok.com" in text or "http" in text):
        target_url = text.strip().split()[0]
        final_html_link = f"{CUSTOM_HTML_BASE}?target={target_url}"
        
        msg = (
            "🌪 <b>إعـصـار جـيـش الـتـبـلـيـغ الـجـزائـري</b> 🌪\n"
            "👤 <b>الـقـائد الـعـام:</b> الـجـلاد الـجـزائـري\n\n"
            "🔥 <b>إلى أسُـود الـظـل والـخـفاء.. إلى صـقـور الـجـزاء الـضـارية</b> 🔥\n\n"
            "⚠️ <b>صـدرت الأوامـر الـعـلـيـا لـلانـقـضاض والـقـصف الـشـامـل:</b>\n\n"
            "👊 <b>يـا أسـود، اضربـوا ولا تـبـالـوا! زلـزلـوا هـواتـفـكم بـالـبـلاغات!</b>\n"
            "حـطمـوا كـبـريـاء الـهـدف، ولا تـتـركوا لـه أثـراً.. الـنصر حـلـيـفـكم.\n\n"
            "🇩🇿 <b>الـنـصر لـلـجـزائر.. الله أكـبـر!</b> 🇩🇿"
        )

        buttons = [
            [Button.url("📍 اقـتـحام الـحساب وتـدمـيره", target_url)],
            [Button.url("📧 قـصف جـوي (عـبر الـجيمـيل)", final_html_link)]
        ]

        try:
            await bot.send_message(CHANNEL_ID, msg, buttons=buttons, link_preview=False, parse_mode='html')
            await event.respond("🚀 <b>تـم إرسـال الأوامـر لـلجيش.. الـهدف مرصود في الواجهة الآن!</b>", parse_mode='html')
        except Exception as e:
            await event.respond(f"❌ خـلل في الـمنظومة: {str(e)}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.send_message(ADMIN_ID, "🦅 <b>الـمنظومة مـتصلة يا سـيدي.. بـانتظار الإشارة.</b>", parse_mode='html')
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())            "🌪 <b>إعـصـار جـيـش الـتـبـلـيـغ الـجـزائـري</b> 🌪\n"
            "👤 <b>الـقـائد الـعـام:</b> الـجـلاد الـجـزائـري\n\n"
            "🔥 <b>إلى أسُـود الـظـل والـخـفاء.. إلى صـقـور الـجـزاء الـضـارية</b> 🔥\n\n"
            "⚠️ <b>صـدرت الأوامـر الـعـلـيـا لـلانـقـضاض والـقـصف الـشـامـل:</b>\n\n"
            "👊 <b>يـا أسـود، اضربـوا ولا تـبـالـوا! زلـزلـوا هـواتـفـكم بـالـبـلاغات!</b>\n"
            "حـطمـوا كـبـريـاء الـهـدف، ولا تـتـركوا لـه أثـراً.. الـنصر حـلـيـفـكم.\n\n"
            "🇩🇿 <b>الـنـصر لـلـجـزائر.. الله أكـبـر!</b> 🇩🇿"
        )

        # 🔘 الأزرار القتالية
        buttons = [
            [Button.url("📍 اقـتـحام الـحساب وتـدمـيره", target_url)],
            [Button.url("📧 قـصف جـوي (عـبر الـجيمـيل)", final_html_link)]
        ]

        try:
            await bot.send_message(CHANNEL_ID, msg, buttons=buttons, link_preview=False, parse_mode='html')
            await event.respond("🚀 <b>تـم إرسـال الأوامـر لـلجيش.. الـهدف مرصود في الواجهة الآن!</b>", parse_mode='html')
        except Exception as e:
            await event.respond(f"❌ خـلل في الـمنظومة: {str(e)}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.send_message(ADMIN_ID, "🦅 <b>الـمنظومة مـتصلة يا سـيدي.. بـانتظار الإشارة.</b>", parse_mode='html')
    await bot.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
