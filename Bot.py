import os
import asyncio
import threading
from telethon import TelegramClient, events, Button
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰 إحداثيات القيادة العليا ---
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
PASSWORD = os.environ.get('PASSWORD')
CUSTOM_HTML_BASE = os.environ.get('CUSTOM_HTML_BASE')

# --- 🌐 خادم ويب وهمي (لإصلاح خطأ Port Binding في Render) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"System is Live")

def run_web_server():
    # Render يمرر المنفذ تلقائياً عبر متغير بيئة يسمى PORT
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# --- إعداد البوت ---
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
        msg = "🌪 <b>إعـصـار جـيـش الـتـبـلـيـغ الـجـزائـري</b> 🌪"
        buttons = [[Button.url("📍 اقتحام", target_url)], [Button.url("📧 قصف", final_html_link)]]
        try:
            await bot.send_message(CHANNEL_ID, msg, buttons=buttons, link_preview=False, parse_mode='html')
        except Exception as e:
            print(f"Error: {e}")

async def main():
    # تشغيل الخادم الوهمي في خلفية الكود لإرضاء Render
    threading.Thread(target=run_web_server, daemon=True).start()
    await bot.start(bot_token=BOT_TOKEN)
    print("المنظومة متصلة بنجاح!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
