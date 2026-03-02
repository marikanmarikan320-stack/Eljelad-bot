import logging
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime, timedelta

# --- الإعدادات والمتغيرات ---
TOKEN = "ضغ_هنا_توكن_البوت"
PASSWORD = "كلمة_السر_التي_اتفقنا_عليها"
SYMBOL = "GC=F"  # رمز الذهب العالمي

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- دالة التحليل الفني العميق ---
def analyze_market():
    # جلب بيانات بأططر زمنية مختلفة
    data_1h = yf.download(SYMBOL, period="5d", interval="1h")
    
    # حساب المؤشرات السبعة المشهورة (RSI, MACD, Bollinger Bands, EMA, Fibonacci, ATR, Stochastic)
    data_1h.ta.rsi(length=14, append=True)
    data_1h.ta.macd(append=True)
    data_1h.ta.bbands(length=20, std=2, append=True)
    data_1h.ta.ema(length=50, append=True)
    
    last = data_1h.iloc[-1]
    rsi = last['RSI_14']
    macd_h = last['MACDH_12_26_9']
    close = last['Close']
    ema = last['EMA_50']
    
    # تحديد الاتجاه والتشبع
    signal = "انتظار ⏳"
    lot = "0.01 (إدارة مخاطر صارمة)"
    
    if rsi < 30 and close > ema:
        signal = "شراء قوي 🟢 (تشبع بيعي + اتجاه صاعد)"
        lot = "0.02"
    elif rsi > 70 and close < ema:
        signal = "بيع قوي 🔴 (تشبع شرائي + اتجاه هابط)"
        lot = "0.02"
        
    return {
        "price": close,
        "rsi": rsi,
        "signal": signal,
        "lot": lot,
        "trend": "صاعد" if close > ema else "هابط"
    }

# --- الأوامر والرسائل ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك يا هاني دوحه! 🫡\nالرجاء إدخال كلمة السر للولوج إلى النظام السيادي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == PASSWORD:
        welcome_msg = (
            "مرحباً بك أيها القائد هاني دوحه! 👑\n"
            "أنا بوتك الخاص بالتداول في صفقات الذهب.\n"
            "**'النجاح ليس نهائياً، والفشل ليس قاتلاً: إنها الشجاعة لمواصلة العمل هي التي تهم.'**\n"
            "أنا جاهز لتحليل السوق لك الآن. أرسل 'stat' للتقرير."
        )
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
        
    elif text.lower() == 'stat':
        analysis = analyze_market()
        report = (
            f"📊 **تقرير القائد هاني (الذهب - 1H):**\n"
            f"💰 السعر الحالي: {analysis['price']:.2f}\n"
            f"📈 الاتجاه العام: {analysis['trend']}\n"
            f"📉 مؤشر RSI: {analysis['rsi']:.2f}\n\n"
            f"💡 **توجيه البوت:** {analysis['signal']}\n"
            f"📏 اللوت المنصوح به: {analysis['lot']}\n"
            f"🚀 نصيحة: التزم بإدارة رأس المال دائماً."
        )
        await update.message.reply_text(report, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
