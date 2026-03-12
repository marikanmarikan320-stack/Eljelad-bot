import os
import time
import asyncio
from market_engine import MarketEngine
from analysis_engine import AnalysisEngine
from ai_engine import AIEngine
from telegram_bot import TelegramEngine

BOT_NAME = "Hani Gold"
LEADER = "القائد هاني دوحه"

OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT = os.getenv("OANDA_ACCOUNT")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

AI_API_KEY = os.getenv("AI_API_KEY")

symbol = "XAU_USD"

market = MarketEngine(OANDA_API_KEY, OANDA_ACCOUNT)
analysis = AnalysisEngine()
ai = AIEngine(AI_API_KEY)
telegram = TelegramEngine(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)


async def startup_message():

    message = f"""
🚀 مرحباً بك في بوت

{BOT_NAME}

👑 بإدارة {LEADER}

🎯 أهداف البوت:

تحليل سوق الذهب مقابل الدولار

📊 الاستراتيجيات:

EMA
RSI
MACD
Bollinger Bands
ATR
Volume
Smart Money
Liquidity
Breakout
Candlestick Patterns

🤖 الذكاء الاصطناعي

LSTM
XGBoost
Random Forest

⚡ المزايا

تحليل متعدد الفريمات
تنبيهات فورية
تقارير كل 10 دقائق
فلتر أخبار
مراقبة السيولة

بالتوفيق في التداول 📈
"""

    await telegram.send(message)


async def main():

    await startup_message()

    await market.initialize_database()

    candles = await market.download_initial_candles(symbol)

    while True:

        try:

            data = await market.update_live_candles(symbol)

            indicators = analysis.calculate_indicators(data)

            patterns = analysis.detect_candles(data)

            signal = ai.generate_signal(indicators, patterns)

            if signal:

                message = f"""

🚨 فرصة تداول

الزوج: XAUUSD

الإشارة: {signal['type']}

الدخول: {signal['entry']}

TP: {signal['tp']}

SL: {signal['sl']}

الثقة: {signal['confidence']}

"""

                await telegram.send(message)

            await asyncio.sleep(5)

        except Exception as e:

            print("error", e)
            time.sleep(10)


if __name__ == "__main__":

    asyncio.run(main())
