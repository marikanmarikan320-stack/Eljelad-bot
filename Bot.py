import os, time, threading
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import telebot
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰️ خادم الحفاظ على اليقظة ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ALIVE")

def run_keep_alive():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    server.serve_forever()

# --- 🎖️ إعدادات القيادة العليا ---
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
CHAT_ID = os.environ.get('ADMIN_ID')
PASSWORD = os.environ.get('PASSWORD')
is_authorized = False

# --- 🔍 محرك التحليل المؤسسي ---
def analyze_institutional():
    # سحب بيانات الذهب (GC=F) بفريم 15 دقيقة
    df = yf.download("GC=F", period="5d", interval="15m")
    
    # حساب أقوى المؤشرات المؤسسية
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # حساب VWAP يدوياً لضمان التوافق
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    last = df.iloc[-1]
    
    # استراتيجية الحيتان
    signal = "انتظار الفرصة"
    if last['Close'] > last['EMA200'] and last['Close'] > last['VWAP'] and last['RSI'] < 60:
        signal = "🚀 شراء (تأكيد حيتان)"
    elif last['Close'] < last['EMA200'] and last['Close'] < last['VWAP'] and last['RSI'] > 40:
        signal = "📉 بيع (تأكيد حيتان)"
    
    return signal, last

# --- 🌪️ المنظومة الآلية ---
def auto_engine():
    # رسالة ترحيب القائد عند النجاح
    welcome_msg = (
        f"🦅 <b>أهلاً بك يا قائد هاني دوحة.. في بوتك الأسطوري لتداول الذهب!</b>\n\n"
        f"أنت الآن القائد الأعلى لهذه المنظومة. لقد تم تفعيل كافة المحركات التقنية والمؤشرات المؤسسية.\n"
        f"استعد للسيطرة على السوق.. القائد هاني لا يهزم!"
    )
    bot.send_message(CHAT_ID, welcome_msg, parse_mode='HTML')
    
    while True:
        now = datetime.now()
        # الفترة الأمريكية (14:00 - 21:00)
        if 14 <= now.hour <= 21:
            # فلتر الأخبار (14:30)
            if now.hour == 14 and 25 <= now.minute <= 45:
                bot.send_message(CHAT_ID, "⚠️ <b>تحذير: وقت أخبار اقتصادية! توقف آلي للحماية.</b>", parse_mode='HTML')
                time.sleep(1200)
                continue
            
            signal, data = analyze_institutional()
            if "🚀" in signal or "📉" in signal:
                report = (f"🎯 <b>إشارة تداول فورية:</b>\n{signal}\n"
                          f"💰 السعر: {data['Close']:.2f}\n"
                          f"📊 الزخم (RSI): {data['RSI']:.2f}")
                bot.send_message(CHAT_ID, report, parse_mode='HTML')
        
        time.sleep(900) # فحص كل 15 دقيقة

# --- 🔐 نظام الحماية ---
@bot.message_handler(commands=['start'])
def start_gate(m):
    bot.send_message(CHAT_ID, "🦅 <b>مرحباً بك يا قائد هاني دوحة..</b>\nيرجى إدخال كلمة السر لفتح بوابات المنظومة:", parse_mode='HTML')

@bot.message_handler(func=lambda m: not is_authorized)
def auth(m):
    global is_authorized
    if m.text == PASSWORD:
        is_authorized = True
        threading.Thread(target=auto_engine, daemon=True).start()
    else:
        bot.reply_to(m, "❌ كلمة سر خاطئة!")

if __name__ == '__main__':
    threading.Thread(target=run_keep_alive, daemon=True).start()
    bot.polling(none_stop=True)
