import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yfinance as yf
import pandas as pd

# --- المتغيرات والإعدادات ---
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
PASSWORD = 'YOUR_SECRET_PASSWORD'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أنا بوت التداول الخاص بك. أدخل كلمة السر للبدء.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text == PASSWORD:
        await update.message.reply_text("تم التحقق! أنت الآن متصل. أرسل 'stat' للحصول على التقرير.")
    elif user_text == 'stat':
        await send_report(update, context)
    else:
        await update.message.reply_text("كلمة سر خاطئة أو أمر غير معروف.")

async def send_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # جلب بيانات الذهب (مثال)
    ticker = "GC=F"
    data = yf.download(ticker, period="1d", interval="1h")
    
    if not data.empty:
        last_price = data['Close'].iloc[-1]
        # منطق بسيط لاستراتيجية الحيتان (مقارنة السعر الحالي بمتوسط متحرك)
        moving_avg = data['Close'].rolling(window=5).mean().iloc[-1]
        
        report = f"📊 تقرير الساعة:\nالسعر الحالي: {last_price:.2f}\n"
        if last_price > moving_avg:
            report += "💡 نصيحة: اتجاه صعودي (شراء محتمل)"
        else:
            report += "⚠️ نصيحة: اتجاه هبوطي (بيع محتمل)"
        
        await update.message.reply_text(report)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
