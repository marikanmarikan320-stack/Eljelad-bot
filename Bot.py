import os, time, threading
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import telebot
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰️ خادم اليقظة (Keep Alive) ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SYSTEM IS ACTIVE")

def run_keep_alive():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), KeepAliveHandler).serve_forever()

# --- 🎖️ إعدادات القيادة ---
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
CHAT_ID = os.environ.get('ADMIN_ID')
PASSWORD = os.environ.get('PASSWORD')
is_authorized = False

# --- 🔍 محرك التحليل المؤسسي (استراتيجية الحيتان) ---
def analyze_institutional():
    # سحب بيانات الذهب (GC=F)
    df = yf.download("GC=F", period="5d", interval="15m")
    
    # حساب المؤشرات المؤسسية (خفيفة ومستقرة)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # VWAP مبسط
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    last = df.iloc[-1]
    
    # اتخاذ القرار (استراتيجية الحيتان)
    signal = "انتظار"
    if last['Close'] > last['VWAP'] and last['Close'] > last['EMA200']:
        signal = "🚀 شراء (تأكيد حيتان)"
    elif last['Close'] < last['VWAP'] and last['Close'] < last['EMA200']:
        signal = "📉 بيع (تأكيد حيتان)"
    return signal, last

# --- 🌪️ المنظومة الآلية ---
def auto_engine():
    bot.send_message(CHAT_ID, "🦅 <b>تم تفعيل المنظومة الأسطورية بنجاح.. أنا في وضع القتال يا قائد هاني دوحة!</b>", parse_mode='HTML')
    while True:
        # فلتر الفترة الأمريكية (14:00 - 21:00)
        if 14 <= datetime.now().hour <= 21:
            # فلتر الأخبار (14:30)
            if datetime.now().hour == 14 and 30 <= datetime.now().minute <= 40:
                time.sleep(600)
                continue
            
            signal, data = analyze_institutional()
            if signal != "انتظار":
                bot.send_message(CHAT_ID, f"🎯 <b>إشارة:</b> {signal}\n💰 السعر: {data['Close']:.2f}", parse_mode='HTML')
        time.sleep(900) # فحص كل 15 دقيقة

@bot.message_handler(func=lambda m: not is_authorized)
def auth(m):
    global is_authorized
    if m.text == PASSWORD:
        is_authorized = True
        bot.reply_to(m, "🦅 <b>مرحباً يا قائد.. القوة في يدك!</b>", parse_mode='HTML')
        threading.Thread(target=auto_engine, daemon=True).start()
    else: bot.reply_to(m, "❌ كلمة سر خاطئة.")

if __name__ == '__main__':
    threading.Thread(target=run_keep_alive, daemon=True).start()
    bot.polling(none_stop=True)
