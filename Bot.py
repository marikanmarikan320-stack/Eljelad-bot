import logging
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime, time, timedelta

# --- المتغيرات التي اتفقنا عليها (تُضاف في Railway كـ Variables) ---
TOKEN = "ضغ_هنا_توكن_البوت"
PASSWORD = "كلمة_السر_الخاصة_بك"
TELEGRAM_ID = "معرف_حسابك"
SYMBOL = "GC=F"

logging.basicConfig(level=logging.INFO)

# --- دالة التحليل الفني (الاستراتيجية المعتمدة) ---
def get_analysis():
    df = yf.download(SYMBOL, period="2d", interval="1h")
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    df.ta.ema(length=50, append=True)
    
    last = df.iloc[-1]
    
    # التحليل الفني الاحترافي
    if last['RSI_14'] < 30 and last['Close'] > last['EMA_50']:
        return "شراء 🟢", "0.02"
    elif last['RSI_14'] > 70 and last['Close'] < last['EMA_50']:
        return "بيع 🔴", "0.02"
    return "انتظار ⏳", "0.00"

# --- دالة التحقق من التوقيت (الفترة الأمريكية + تجنب وقت الأخبار) ---
def is_market_safe():
    now = datetime.now().time()
    # 1. نطاق الفترة الأمريكية (من 13:00 إلى 21:00)
    in_american_session = time(13, 0) <= now <= time(21, 0)
    
    # 2. تجنب وقت الأخبار (مثال: إذا صدر خبر قوي الساعة 14:30، نتوقف من 14:15 إلى 15:00)
    # يمكنك إضافة تواريخ الأخبار هنا يدوياً أو ربطها بـ API
    news_time_start = time(14, 15)
    news_time_end = time(15, 0)
    is_news_time = news_time_start <= now <= news_time_end
    
    return in_american_session and not is_news_time

# --- الأوامر ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك يا هاني دوحه! أدخل كلمة السر للولوج إلى النظام السيادي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == PASSWORD:
        await update.message.reply_text("مرحباً بك أيها القائد هاني دوحه! أنا بوتك الخاص بالتداول.. 'النجاح يصنع بالصبر والعلم'.")
    elif text.lower() == 'stat':
        if not is_market_safe():
            await update.message.reply_text("⚠️ النظام في وضع الحماية: إما أننا خارج الفترة الأمريكية أو نقترب من موعد صدور أخبار اقتصادية. لا تدخل صفقات الآن.")
            return
        
        signal, lot = get_analysis()
        report = f"📊 تقرير القائد هاني:\nالنصيحة: ادخل صفقة {signal}\nاللوت المقترح: {lot}\nنحن في فترة تداول آمنة."
        await update.message.reply_text(report)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("نظام EljeladDZ يعمل الآن بكامل طاقته...")
    app.run_polling()
