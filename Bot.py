import os, time, threading
import yfinance as yf
import pandas as pd
import telebot
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰️ خادم اليقظة ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"ACTIVE")
def run_keep_alive(): HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), KeepAliveHandler).serve_forever()

# --- 🎖️ الإعدادات ---
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
CHAT_ID = os.environ.get('ADMIN_ID')
PASSWORD = os.environ.get('PASSWORD')
is_authorized = False

# --- 🔍 المحرك الرياضي (المعادلات المدمجة) ---
def calculate_indicators(df):
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    return df.iloc[-1]

def get_market_data(interval):
    period = "5d" if interval in ['15m', '1h'] else "1mo"
    df = yf.download("GC=F", period=period, interval=interval)
    return calculate_indicators(df)

# --- 📊 تقرير الـ /status الشامل ---
@bot.message_handler(commands=['status'])
def report_status(m):
    if not is_authorized: return
    intervals = {'15 دقيقة': '15m', 'ساعة': '1h', '4 ساعات': '4h', 'يوم': '1d'}
    report = "📊 <b>التقرير المؤسسي الشامل:</b>\n"
    for name, code in intervals.items():
        data = get_market_data(code)
        report += f"\n📌 <b>فريم {name}:</b>\n💰 السعر: {data['Close']:.2f}\n📈 RSI: {data['RSI']:.2f}\n💎 VWAP: {data['VWAP']:.2f}\n"
    bot.reply_to(m, report, parse_mode='HTML')

# --- 🌪️ المنظومة الآلية ---
def auto_engine():
    bot.send_message(CHAT_ID, "🦅 <b>تم تفعيل المنظومة الأسطورية.. أنا في وضع القتال يا قائد هاني!</b>", parse_mode='HTML')
    while True:
        if 14 <= datetime.now().hour <= 21:
            # فلتر الأخبار (14:30)
            if datetime.now().hour == 14 and 30 <= datetime.now().minute <= 40:
                time.sleep(600)
                continue
            
            data = get_market_data('15m')
            # استراتيجية الحيتان
            if data['Close'] > data['VWAP'] and data['Close'] > data['EMA200']:
                bot.send_message(CHAT_ID, f"🚀 <b>فرصة شراء (حيتان):</b> السعر {data['Close']:.2f}", parse_mode='HTML')
            elif data['Close'] < data['VWAP'] and data['Close'] < data['EMA200']:
                bot.send_message(CHAT_ID, f"📉 <b>فرصة بيع (حيتان):</b> السعر {data['Close']:.2f}", parse_mode='HTML')
        time.sleep(900)

@bot.message_handler(commands=['start'])
def start_gate(m): bot.send_message(CHAT_ID, "🦅 <b>أهلاً بك يا قائد هاني.. أدخل كلمة السر:</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: not is_authorized)
def auth(m):
    global is_authorized
    if m.text == PASSWORD:
        is_authorized = True
        bot.reply_to(m, "🦅 <b>مرحباً يا قائد.. المنظومة الأسطورية جاهزة!</b>", parse_mode='HTML')
        threading.Thread(target=auto_engine, daemon=True).start()
    else: bot.reply_to(m, "❌ كلمة سر خاطئة.")

if __name__ == '__main__':
    threading.Thread(target=run_keep_alive, daemon=True).start()
    bot.polling(none_stop=True)
