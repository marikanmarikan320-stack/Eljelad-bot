import os
import telebot
import yfinance as yf
import pandas as pd
import ta
import threading
import time
import hashlib
from datetime import datetime

# -------------------------
# 1️⃣ المتغيرات البيئية
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
PASSWORD = os.getenv("BOT_PASSWORD")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

active_users = {}
licensed_users = {}

# -------------------------
# 2️⃣ نظام التفعيل مدى الحياة
# -------------------------
def generate_license(user_id):
    raw = f"{user_id}-INSTITUTIONAL-GOLD-2026"
    return hashlib.sha256(raw.encode()).hexdigest()[:30]

# -------------------------
# 3️⃣ جلب بيانات الذهب
# -------------------------
def get_data(interval):
    df = yf.download("XAUUSD=X", interval=interval, period="5d", progress=False)
    return df

# -------------------------
# 4️⃣ تحليل الشموع اليابانية
# -------------------------
def detect_candles(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    body = abs(last["Close"] - last["Open"])
    candle_range = last["High"] - last["Low"]
    patterns = []

    if prev["Close"] < prev["Open"] and last["Close"] > last["Open"] and last["Close"] > prev["Open"]:
        patterns.append("Bullish Engulfing")
    if prev["Close"] > prev["Open"] and last["Close"] < last["Open"] and last["Close"] < prev["Open"]:
        patterns.append("Bearish Engulfing")
    if body < candle_range * 0.3:
        patterns.append("Pin Bar")
    if body < candle_range * 0.1:
        patterns.append("Doji")
    return patterns

# -------------------------
# 5️⃣ تحليل هيكل السوق
# -------------------------
def market_structure(df):
    highs = df["High"].rolling(5).max()
    lows = df["Low"].rolling(5).min()
    last_high = highs.iloc[-1]
    prev_high = highs.iloc[-2]
    last_low = lows.iloc[-1]
    prev_low = lows.iloc[-2]

    if last_high > prev_high:
        return "Bullish"
    elif last_low < prev_low:
        return "Bearish"
    else:
        return "Range"

# -------------------------
# 6️⃣ التحليل الكامل لكل فريم
# -------------------------
def analyze(interval):
    df = get_data(interval)
    df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], window=200)
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

    last = df.iloc[-1]

    buy_score = 0
    sell_score = 0

    if last["EMA50"] > last["EMA200"]:
        buy_score += 1
    else:
        sell_score += 1
    if last["RSI"] < 40:
        buy_score += 1
    elif last["RSI"] > 60:
        sell_score += 1

    structure = market_structure(df)
    candles = detect_candles(df)

    if "Bullish Engulfing" in candles:
        buy_score += 2
    if "Bearish Engulfing" in candles:
        sell_score += 2
    if structure == "Bullish":
        buy_score += 1
    elif structure == "Bearish":
        sell_score += 1

    return buy_score, sell_score, last["Close"], candles, structure

# -------------------------
# 7️⃣ إرسال تقرير كل 15 دقيقة
# -------------------------
def signal_loop():
    while True:
        try:
            intervals = ["5m", "15m", "1h", "4h", "1d"]
            total_buy = 0
            total_sell = 0
            price = 0
            candle_info = []
            structure_info = []

            for tf in intervals:
                buy, sell, price, candles, structure = analyze(tf)
                total_buy += buy
                total_sell += sell
                candle_info += candles
                structure_info.append(f"{tf}: {structure}")

            total = total_buy + total_sell
            strength = max(total_buy, total_sell) / total

            if total == 0:
                strength = 0

            if strength >= 0.7:
                direction = "BUY" if total_buy > total_sell else "SELL"
                report = f"""
🏦 INSTITUTIONAL GOLD REPORT

السعر الحالي: {price}
الاتجاه: {direction}
قوة الإشارة: {round(strength*100,2)}%

هيكل السوق:
{structure_info}

نماذج الشموع:
{set(candle_info)}

⏰ التوقيت: {datetime.utcnow()}

⚠️ استخدم إدارة رأس مال احترافية
"""
                for user in active_users:
                    if active_users[user]:
                        bot.send_message(user, report)

            # الانتظار 15 دقيقة قبل إرسال التقرير التالي
            time.sleep(900)

        except Exception as e:
            print("Error in signal loop:", e)
            time.sleep(60)

# -------------------------
# 8️⃣ أوامر Telegram
# -------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "🔐 ادخل كلمة السر")

@bot.message_handler(commands=["generate"])
def generate(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            code = generate_license(user_id)
            licensed_users[user_id] = code
            bot.send_message(message.chat.id, f"كود التفعيل مدى الحياة:\n{code}")
        except:
            bot.send_message(message.chat.id, "استخدم /generate USER_ID")

@bot.message_handler(commands=["price"])
def get_price(message):
    df = get_data("1m")
    last = df.iloc[-1]["Close"]
    bot.send_message(message.chat.id, f"💰 السعر اللحظي للذهب: {last}")

@bot.message_handler(commands=["stats"])
def get_stats(message):
    report = ""
    intervals = ["5m", "15m", "1h", "4h", "1d"]
    for tf in intervals:
        buy, sell, price, candles, structure = analyze(tf)
        report += f"{tf}: Buy {buy}, Sell {sell}, هيكل {structure}, شموع {set(candles)}\n"
    bot.send_message(message.chat.id, f"📊 إحصائيات التحليل:\n{report}")

@bot.message_handler(func=lambda m: True)
def verify(message):
    user_id = message.from_user.id

    if user_id in active_users and active_users[user_id]:
        return

    if message.text == PASSWORD:
        bot.send_message(user_id, "✅ ادخل كود التفعيل")
        active_users[user_id] = False
        return

    if user_id in licensed_users and message.text == licensed_users[user_id]:
        active_users[user_id] = True
        bot.send_message(user_id, "🚀 تم تفعيل النسخة المؤسسية مدى الحياة")
    else:
        bot.send_message(user_id, "❌ البيانات غير صحيحة")

# -------------------------
# 9️⃣ تشغيل البوت
# -------------------------
threading.Thread(target=signal_loop).start()
bot.polling(none_stop=True)
