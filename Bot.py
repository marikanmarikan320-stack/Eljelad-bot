import yfinance as yf
import pandas_ta as ta
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
from telegram import Bot
from datetime import datetime, timedelta

# إعدادات البوت (يتم جلبها من Railway Variables)
TOKEN = "YOUR_TOKEN" 
CHAT_ID = "YOUR_CHAT_ID"
bot = Bot(token=TOKEN)

def get_advanced_analysis():
    # جلب بيانات الذهب بدقة 15 دقيقة
    df = yf.download("GC=F", period="1d", interval="15m", progress=False)
    
    # 1. تحليل الشموع اليابانية (استراتيجية دوجي والمطرقة)
    df.ta.cdl_doji(append=True)
    df.ta.cdl_hammer(append=True)
    
    # 2. مؤشرات الزخم (RSI) والاتجاه (MACD)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    
    # 3. حساب القاع والقمة لليوم الحالي
    daily_high = df['High'].max()
    daily_low = df['Low'].min()
    
    # توليد صورة (سكرين شوت) للتحليل
    plt.figure(figsize=(10, 5))
    df['Close'].plot(title="تحليل الذهب الحي")
    plt.savefig('chart.png')
    
    return df.iloc[-1], daily_high, daily_low

async def send_status(update=False):
    last_candle, h, l = get_advanced_analysis()
    
    # منطق الاستراتيجية (دمج المؤشرات لاتخاذ القرار)
    decision = "انتظار تأكيد..."
    if last_candle['RSI_14'] < 30 and last_candle['MACD_12_26_9'] > 0:
        decision = "🚀 فرصة شراء قوية (استراتيجية الحيتان)"
    elif last_candle['RSI_14'] > 70:
        decision = "📉 فرصة بيع (تشبع شرائي)"

    msg = (f"📊 تقرير التداول اللحظي:\n"
           f"السعر الحالي: {last_candle['Close']:.2f}\n"
           f"القمة اليومية: {h:.2f} | القاع اليومي: {l:.2f}\n"
           f"القرار الفني: {decision}\n"
           f"الوقت: {datetime.now().strftime('%H:%M')}")
    
    await bot.send_message(chat_id=CHAT_ID, text=msg)
    await bot.send_photo(chat_id=CHAT_ID, photo=open('chart.png', 'rb'))

async def main():
    while True:
        # مراسلة دورية كل 15 دقيقة في الفترة الأمريكية
        now = datetime.now()
        if 13 <= now.hour < 21:
            await send_status()
        await asyncio.sleep(900)

if __name__ == "__main__":
    asyncio.run(main())
