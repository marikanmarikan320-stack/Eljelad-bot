import os
import asyncio
import threading
from telethon import TelegramClient, events, Button
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰 إحداثيات القيادة العليا (مـنظومة جـيش الـتبليغ الـجزائري) ---
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
PASSWORD = os.environ.get('PASSWORD')
CUSTOM_HTML_BASE = os.environ.get('CUSTOM_HTML_BASE')

# --- 🌐 خادم الحفاظ على اليقظة (Web Server) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ALGERIAN REPORTING ARMY SYSTEM IS ONLINE")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# --- ⚔️ تشغيل محرك المنظومة ---
bot = TelegramClient('eljelad_session', API_ID, API_HASH)

@bot.on(events.NewMessage)
async def eljelad_core(event):
    if event.is_group: return
    sender = event.sender_id
    text = event.raw_text

    # 🎖️ نداء التحقق من هوية القائد
    if text == PASSWORD and sender == ADMIN_ID:
        await event.respond("<b>🦅 سـيادة الـقائد الـعام (الـجلاد الـجزائري).. مـنظومة جـيش الـتبليغ الـجزائري مـستعدة لـسحق الأهداف وبـدء الـقصف الـشامل!</b>", parse_mode='html')
        return

    # 🚀 رصد الأهداف وإرسال البلاغ القتالي
    if sender == ADMIN_ID and ("tiktok.com" in text or "http" in text):
        target_url = text.strip().split()[0]
        final_html_link = f"{CUSTOM_HTML_BASE}?target={target_url}"
        
        # 🌪️ الـرسالة الـحماسية لـلجنود
        msg = (
            "🌪️ <b>مـنظومة جـيش الـتبليغ الـجزائري</b> 🌪️\n"
            "👤 <b>بـقيادة الـقائد:</b> الـجلاد الـجزائـري\n\n"
            "🔥 <b>إلى أسُـود الـظـل وصـقـور الـجزائر الأبـرار..</b> 🔥\n\n"
            "⚠️ <b>صـدرت الأوامـر الـعـلـيـا لـسحق هـذا الـهدف الـخائن:</b>\n\n"
            "👊 <b>يـا أبطال، اقصفـوا بـلا رحـمة! زلـزلـوا الأرض بـبلاغاتكم!</b>\n"
            "نـحن فـي مـهمة مـقدسة مـن أجـل وطننا الـحبيب ووفـاءً لـدمـاء شـهدائنا الأبـرار. لا تـتركوا لـلخونة أثـراً!\n\n"
            "🛡️ <b>تـعليمات قـتالية هـامة لـلجنود:</b>\n"
            "<b>┌───────────────────┐</b>\n"
            "<b>⚠️ تـنبيه: يـجب إيـقاف خـيار (الـمتصفح الـداخلي) فـي إعـدادات تـيليجرام، لـكي تـفتح لـكم الـواجهة الـحربية فـي Chrome وتـعمل الـمنظومة بـكفاءة!</b>\n"
            "<b>└───────────────────┘</b>\n\n"
            "🇩🇿 <b>الـنـصر لـلـجـزائر.. الله أكـبـر!</b> 🇩🇿"
        )

        # 🔘 الأزرار الـقتالية
        buttons = [
            [Button.url("🚀 اقـصف الـهدف الآن (تـدمـير مباشر)", target_url)],
            [Button.url("📧 انـتقال إلـى الـواجهة الـحربية الـشاملة", final_html_link)]
        ]

        try:
            await bot.send_message(CHANNEL_ID, msg, buttons=buttons, link_preview=False, parse_mode='html')
            # 📟 رد الـبوت لـتأكيد الإرسـال
            await event.respond(f"✅ <b>تـم إرسـال الإحـداثيات لـلجيش! الـهدف مرصود فـي الـقناة الآن والـهجوم بـدأ يا سـيدي.</b>", parse_mode='html')
        except Exception as e:
            await event.respond(f"❌ <b>خـلل فـي تـوزيع الأوامـر:</b> {str(e)}")

async def main():
    # 🏁 تـفعيل الـخادم الـوهمي لـمنع الـخمول
    threading.Thread(target=run_web_server, daemon=True).start()
    
    await bot.start(bot_token=BOT_TOKEN)
    # 📢 رسـالة تـأكيد الاتـصال لـلقائد
    await bot.send_message(ADMIN_ID, "🦅 <b>تـم تـفعيل مـحرك مـنظومة جـيش الـتبليغ الـجزائري.. نـحن فـي وضـع الاسـتعداد الـدائم!</b>", parse_mode='html')
    print("System is Online and Waiting for Orders...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
