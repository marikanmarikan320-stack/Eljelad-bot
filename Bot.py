import os, time, threading
import yfinance as yf
import pandas as pd
import telebot
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🛰️ خادم اليقظة الدائم (Anti-Sleep) ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"COMMANDER SYSTEM IS ACTIVE")

def run_keep_alive():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), KeepAliveHandler).serve_forever()

# --- 🎖️ الإعدادات السرية ---
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
CHAT_ID = os.environ.get('ADMIN_ID')
PASSWORD = os.environ.get('PASSWORD')
is_authorized = False

# --- 🔍 المحرك الرياضي (استراتيجيات الحيتان) ---
def get_institutional_indicators(df):
    # 1. المتوسط المتحرك الأسي (الاتجاه العام)
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    # 2. مؤشر القوة النسبية (الزخم)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    # 3. مؤشر VWAP (منطقة دخول المؤسسات والحيتان)
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    return df.iloc[-1]

def analyze_all_frames():
    intervals = {'15 دقيقة': '15m', 'ساعة': '1h', '4 ساعات': '4h', 'يومي': '1d'}
    results = {}
    for name, code in intervals.items():
        # سحب بيانات الذهب GC=F
        df = yf.download("GC=F", period="5d" if code in ['15m', '1h'] else "1mo", interval=code, progress=False)
        results[name] = get_institutional_indicators(df)
    return results

# --- 🛡️ نظام الأوامر والمراسلة ---
@bot.message_handler(commands=['start'])
def welcome(m):
    bot.send_message(CHAT_ID, "🦅 <b>مرحباً يا قائد هاني دوحة..</b>\nأدخل كلمة السر لفتح بوابات المنظومة الأسطورية:", parse_mode='HTML')

@bot.message_handler(commands=['status'])
def send_status(m):
    if not is_authorized: return
    bot.reply_to(m, "🔄 جاري تحليل الفريمات الأربعة ومراقبة الحيتان..")
    stats = analyze_all_frames()
    report = "📊 <b>تقرير السيطرة على الذهب:</b>\n"
    for name, data in stats.items():
        trend = "📈 صاعد" if data['Close'] > data['EMA200'] else "📉 هابط"
        report += f"\n💎 <b>فريم {name}:</b>\n💰 السعر: {data['Close']:.2f}\n📊 الاتجاه: {trend}\n⚡ RSI: {data['RSI']:.2f}\n"
    bot.send_message(CHAT_ID, report, parse_mode='HTML')

@bot.message_handler(func=lambda m: not is_authorized)
def auth(m):
    global is_authorized
    if m.text == PASSWORD:
        is_authorized = True
        msg = (f"🦅 <b>أهلاً بك يا قائد هاني دوحة.. في بوتك الأسطوري!</b>\n\n"
               f"المنظومة نشطة الآن وتراقب الحيتان. القائد هاني لا يقهر!")
        bot.send_message(CHAT_ID, msg, parse_mode='HTML')
        threading.Thread(target=market_monitor, daemon=True).start()
    else:
        bot.reply_to(m, "❌ كلمة سر خاطئة!")

# --- 🌪️ حلقة المراقبة الآلية ---
def market_monitor():
    while True:
        now = datetime.now()
        # العمل فقط في الفترة الأمريكية (14:00 - 21:00) وتجنب الأخبار (14:30)
        if 14 <= now.hour <= 21:
            if now.hour == 14 and 25 <= now.minute <= 45:
                time.sleep(600)
                continue
            
            # تحليل فريم 15 دقيقة للبحث عن إشارات دخول
            df_15 = yf.download("GC=F", period="2d", interval="15m", progress=False)
            last = get_institutional_indicators(df_15)
            
            # استراتيجية القنص (السعر + VWAP + EMA200)
            if last['Close'] > last['VWAP'] and last['Close'] > last['EMA200'] and last['RSI'] < 60:
                bot.send_message(CHAT_ID, f"🚀 <b>إشارة شراء مؤسساتية:</b>\n💰 السعر: {last['Close']:.2f}\nاستعد للدخول يا قائد!")
            elif last['Close'] < last['VWAP'] and last['Close'] < last['EMA200'] and last['RSI'] > 40:
                bot.send_message(CHAT_ID, f"📉 <b>إشارة بيع مؤسساتية:</b>\n💰 السعر: {last['Close']:.2f}\nتحرك الآن يا قائد!")
        
        time.sleep(900) # فحص كل 15 دقيقة

if __name__ == '__main__':
    threading.Thread(target=run_keep_alive, daemon=True).start()
    bot.polling(none_stop=True)
