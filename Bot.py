import os, time, threading
import yfinance as yf
import pandas as pd
import telebot
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰️ خادم اليقظة ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"ACTIVE")

def run_keep_alive():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), KeepAliveHandler).serve_forever()

# --- 🎖️ الإعدادات ---
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
CHAT_ID = os.environ.get('ADMIN_ID')
PASSWORD = os.environ.get('PASSWORD')
is_authorized = False

# --- 🔍 المحرك الرياضي المؤسسي ---
def get_indicators(df):
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    return df.iloc[-1]

def analyze_all():
    intervals = {'15 دقيقة': '15m', 'ساعة': '1h', '4 ساعات': '4h', 'يوم': '1d'}
    results = {}
    for name, code in intervals.items():
        df = yf.download("GC=F", period="5d" if code in ['15m', '1h'] else "1mo", interval=code)
        results[name] = get_indicators(df)
    return results

# --- 📊 الأوامر والردود ---
@bot.message_handler(commands=['start'])
def start_cmd(m): bot.send_message(CHAT_ID, "🦅 مرحباً يا قائد.. أدخل كلمة السر:")

@bot.message_handler(commands=['status'])
def status_cmd(m):
    if not is_authorized: return
    bot.reply_to(m, "جاري تحليل السوق المؤسسي.. لحظات يا قائد.")
    stats = analyze_all()
    report = "📊 <b>تقرير الحيتان الشامل:</b>\n"
    for name, data in stats.items():
        report += f"\n📌 <b>فريم {name}:</b>\n💰 السعر: {data['Close']:.2f} | RSI: {data['RSI']:.2f}\n"
    bot.reply_to(m, report, parse_mode='HTML')

@bot.message_handler(func=lambda m: not is_authorized)
def auth(m):
    global is_authorized
    if m.text == PASSWORD:
        is_authorized = True
        bot.reply_to(m, "🦅 <b>أهلاً بك يا قائد.. النظام جاهز!</b> استخدم /status للتقارير.", parse_mode='HTML')
    else: bot.reply_to(m, "❌ كلمة سر خاطئة.")

if __name__ == '__main__':
    threading.Thread(target=run_keep_alive, daemon=True).start()
    bot.polling(none_stop=True)
