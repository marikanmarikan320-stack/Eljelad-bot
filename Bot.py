import os, time, threading, io
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import telebot
import matplotlib.pyplot as plt
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- الإعدادات ---
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
CHAT_ID = os.environ.get('ADMIN_ID')
PASSWORD = os.environ.get('PASSWORD')
is_authorized = False

# --- خادم الحفاظ على النشاط (لضمان عدم نوم البوت) ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"SYSTEM ACTIVE")

def run_keep_alive(): HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), KeepAliveHandler).serve_forever()

# --- استراتيجية الحيتان والتحليل المؤسسي ---
def analyze_market():
    # سحب بيانات الذهب مباشرة من السحابة
    df = yf.download("GC=F", period="5d", interval="15m")
    
    # المؤشرات المؤسسية (حيتان السوق)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])
    
    last = df.iloc[-1]
    
    # اتخاذ القرار
    signal = "انتظار"
    if last['Close'] > last['VWAP'] and last['Close'] > last['EMA200'] and last['RSI'] < 60:
        signal = "🚀 شراء (تأكيد حيتان)"
    elif last['Close'] < last['VWAP'] and last['Close'] < last['EMA200'] and last['RSI'] > 40:
        signal = "📉 بيع (تأكيد حيتان)"
    return signal, last

# --- المنظومة الذاتية للتحكم ---
def auto_engine():
    bot.send_message(CHAT_ID, "🦅 <b>تم تشغيل منظومة القائد هاني دوحة.. في وضع القتال!</b>", parse_mode='HTML')
    while True:
        if 14 <= datetime.now().hour <= 21: # الفترة الأمريكية
            # فلتر الأخبار (14:30)
            if datetime.now().hour == 14 and 30 <= datetime.now().minute <= 40:
                bot.send_message(CHAT_ID, "🚫 <b>أخبار عالمية، توقف آلي للحماية.</b>", parse_mode='HTML')
                time.sleep(900)
                continue
            
            signal, data = analyze_market()
            if signal != "انتظار":
                bot.send_message(CHAT_ID, f"🎯 <b>إشارة تداول:</b> {signal}\n💰 السعر: {data['Close']:.2f}", parse_mode='HTML')
        time.sleep(900)

@bot.message_handler(func=lambda m: not is_authorized)
def auth(m):
    global is_authorized
    if m.text == PASSWORD:
        is_authorized = True
        welcome_msg = ("🦅 <b>أهلاً بك يا قائد هاني دوحة.. في بوتك الأسطوري لتداول الذهب!</b>\n\n"
                       "أنت القائد الأعلى، أنت من يروض أسواق الذهب. المنظومة تعمل بكامل قوتها.")
        bot.reply_to(m, welcome_msg, parse_mode='HTML')
        threading.Thread(target=auto_engine, daemon=True).start()
    else: bot.reply_to(m, "❌ كلمة سر خاطئة.")

if __name__ == '__main__':
    threading.Thread(target=run_keep_alive, daemon=True).start()
    bot.polling(none_stop=True)
