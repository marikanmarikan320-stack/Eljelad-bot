import os
import asyncio
import requests
import pandas as pd
import pandas_ta as ta
import pytz
import sqlite3
import hmac
import hashlib
import mplfinance as mpf
from datetime import datetime, timedelta
from telethon import TelegramClient, events

# =========================
# 🔐 ENV
# =========================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MARKET_API = os.getenv("MARKET_API")
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PASSWORD = os.getenv("PASSWORD")
NEWS_API = os.getenv("NEWS_API")

bot = TelegramClient("gold_master_bot", API_ID, API_HASH)

AUTHORIZED = False

# =========================
# 🗄 DATABASE
# =========================

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, token TEXT)")
conn.commit()

def generate_token(user_id):
    return hmac.new(SECRET_KEY.encode(), str(user_id).encode(), hashlib.sha256).hexdigest()

# =========================
# 🕒 SESSION FILTER
# =========================

def is_us_session():
    tz = pytz.timezone("America/New_York")
    now = datetime.now(tz)
    return 7 <= now.hour <= 17

# =========================
# 📰 NEWS FILTER
# =========================

def high_impact_news():
    try:
        url=f"https://newsapi.org/v2/everything?q=USD&apiKey={NEWS_API}"
        r=requests.get(url).json()
        return False
    except:
        return False

# =========================
# 📊 FETCH DATA
# =========================

def get_data(interval):
    url=f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval={interval}&apikey={MARKET_API}&outputsize=200"
    r=requests.get(url).json()
    if "values" not in r:
        return None
    df=pd.DataFrame(r["values"])
    df=df.rename(columns={"datetime":"Date","open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"})
    df["Date"]=pd.to_datetime(df["Date"])
    df=df.set_index("Date")
    df=df.astype(float)
    df=df.sort_index()
    return df

# =========================
# 📈 ANALYSIS ENGINE
# =========================

def analyze(df):
    df["EMA50"]=ta.ema(df["Close"],50)
    df["EMA200"]=ta.ema(df["Close"],200)
    df["RSI"]=ta.rsi(df["Close"],14)
    df["ATR"]=ta.atr(df["High"],df["Low"],df["Close"],14)
    df["ADX"]=ta.adx(df["High"],df["Low"],df["Close"],14)["ADX_14"]

    last=df.iloc[-1]
    prev=df.iloc[-2]

    trend="Bullish" if last["EMA50"]>last["EMA200"] else "Bearish"
    strong=last["ADX"]>20
    volatility=last["ATR"]>1
    bos_up=last["High"]>prev["High"]
    bos_down=last["Low"]<prev["Low"]

    signal="WAIT"

    if trend=="Bullish" and strong and volatility and bos_up and last["RSI"]<70:
        signal="BUY"
    elif trend=="Bearish" and strong and volatility and bos_down and last["RSI"]>30:
        signal="SELL"

    return signal,trend,last

# =========================
# 📊 MULTI TF ANALYSIS
# =========================

def multi_timeframe_analysis():

    timeframes=["5min","15min","1h","4h","1day"]
    results={}

    for tf in timeframes:
        df=get_data(tf)
        if df is None:
            return None
        signal,trend,last=analyze(df)
        results[tf]={"signal":signal,"trend":trend,"price":last["Close"]}

    return results

# =========================
# 📷 CHART
# =========================

def create_chart(df):
    file="chart.png"
    mpf.plot(df.tail(100),type="candle",style="yahoo",savefig=file)
    return file

# =========================
# 🤖 COMMANDS
# =========================

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("🦅 مرحبا يا هاني، البوت يعمل الآن.\nأدخل كلمة السر لتفعيله.")

@bot.on(events.NewMessage)
async def handler(event):

    global AUTHORIZED

    if event.sender_id!=ADMIN_ID:
        return

    text=event.raw_text.strip()

    if text==PASSWORD:
        AUTHORIZED=True
        await event.respond("🔥 مرحبا بك يا قائد هاني دوحة.\nالبوت المؤسسي بدأ العمل.")
        return

    if text.lower()=="report" and AUTHORIZED:

        results=multi_timeframe_analysis()
        if results is None:
            await event.respond("API Limit reached.")
            return

        summary="📊 تقرير شامل متعدد الفريمات:\n\n"

        buy_count=0
        sell_count=0

        for tf,data in results.items():
            summary+=f"{tf} → {data['trend']} | {data['signal']} | السعر {data['price']}\n"
            if data["signal"]=="BUY":
                buy_count+=1
            if data["signal"]=="SELL":
                sell_count+=1

        final="WAIT"
        if buy_count>=3:
            final="BUY"
        elif sell_count>=3:
            final="SELL"

        summary+=f"\n🎯 القرار النهائي: {final}"

        df=get_data("15min")
        chart=create_chart(df)

        await bot.send_file(ADMIN_ID,chart,caption=summary)

# =========================
# ⏰ AUTO LOOP
# =========================

async def auto_loop():

    while True:

        if AUTHORIZED and is_us_session():

            if high_impact_news():
                await bot.send_message(ADMIN_ID,"⚠ خبر اقتصادي قوي قادم.\nالتداول متوقف مؤقتاً.")
                await asyncio.sleep(1800)
                continue

            results=multi_timeframe_analysis()
            if results:
                buy=sum(1 for tf in results if results[tf]["signal"]=="BUY")
                sell=sum(1 for tf in results if results[tf]["signal"]=="SELL")

                if buy>=3 or sell>=3:
                    decision="BUY" if buy>sell else "SELL"
                    await bot.send_message(ADMIN_ID,f"🚨 إشارة قوية: {decision}")

        await asyncio.sleep(900)

# =========================
# 🚀 RUN
# =========================

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.send_message(ADMIN_ID,"✅ تم تشغيل البوت بنجاح.\nأدخل /start.")
    asyncio.create_task(auto_loop())
    await bot.run_until_disconnected()

asyncio.run(main())
