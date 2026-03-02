import yfinance as yf
import pandas_ta as ta
import pandas as pd
import asyncio
from telegram import Bot
from datetime import datetime
import time

# إعدادات البوت
TOKEN = "أدخل_توكن_البوت_الخاص_بك_هنا"
CHAT_ID = "أدخل_معرف_محادثتك_هنا"
bot = Bot(token=TOKEN)

# استراتيجية تحليل الحيتان والشموع
def analyze_market():
    symbol = "GC=F" # الذهب
    data = yf.download(symbol, period="1d", interval="15m")
    
    # استخدام pandas_ta للمؤشرات القوية
    data.ta.rsi(length=14, append=True)
    data.ta.macd(append=True)
    
    last_row = data.iloc[-1]
    
    # منطق الفلترة: هنا تضع شروط الاستراتيجيات السبع (مثلاً RSI < 30)
    signal = "انتظار إشارة قوية..."
    if last_row['RSI_14'] < 30:
        signal = "⚠️ إشارة شراء قوية (تشبع بيعي) - استراتيجية الحيتان"
    elif last_row['RSI_14'] > 70:
        signal = "⚠️ إشارة بيع قوية (تشبع شرائي)"
        
    return f"تقرير التداول:\nالسعر: {last_row['Close']:.2f}\nالتحليل: {signal}\nالوقت: {datetime.now().strftime('%H:%M')}"

async def send_report():
    report = analyze_market()
    await bot.send_message(chat_id=CHAT_ID, text=f"👋 أهلاً بك هاني!\n\n{report}")

# الدورة التكرارية (كل 15 دقيقة)
async def main():
    while True:
        # الفلترة الزمنية (الفترة الأمريكية تقريباً من 13:30 إلى 20:00 بتوقيت جرينتش)
        now = datetime.now()
        if 13 <= now.hour < 21: 
            await send_report()
        else:
            print("خارج نطاق الفترة الأمريكية - وضع السكون")
        
        await asyncio.sleep(900) # 15 دقيقة بالثواني

if __name__ == "__main__":
    asyncio.run(main())
