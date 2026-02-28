import asyncio
from telethon import TelegramClient, events, Button

# --- 🛰 إحداثيات القيادة العليا ---
API_ID = 38225499 
API_HASH = '6f367ce0c263c959b84da22c7d5180e0' 
BOT_TOKEN = '8585074322:AAE9EsEABVzsDiRVKY8kXq940g7CBNysjkQ' 
ADMIN_ID = 6113400824 
CHANNEL_ID = -1003803200793 
PASSWORD = "ELJELADDZ2025###"

# 🚩 الرابط الأساسي لواجهتك على GitHub
CUSTOM_HTML_BASE = "https://marikanmarikan320-stack.github.io/EljeladD/eljelad.html"

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
        
        # 🔗 دمج الرابط بالواجهة لاستقبال آلاف الأهداف تلقائياً
        final_html_link = f"{CUSTOM_HTML_BASE}?target={target_url}"
        
        # 🌪 الرسالة التحفيزية (تم التأكد من إغلاق كافة علامات التنصيص)
        msg = (
            "🌪 <b>إعـصـار جـيـش الـتـبـلـيـغ الـجـزائـري</b> 🌪\n"
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
