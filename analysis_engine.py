
import pandas as pd
import pandas_ta as ta

class AnalysisEngine:

    def calculate_indicators(self, df):

        df["ema50"] = ta.ema(df["close"], length=50)
        df["ema200"] = ta.ema(df["close"], length=200)

        df["rsi"] = ta.rsi(df["close"], length=14)

        macd = ta.macd(df["close"])

        df["macd"] = macd["MACD_12_26_9"]

        bb = ta.bbands(df["close"])

        df["bb_upper"] = bb["BBU_20_2.0"]
        df["bb_lower"] = bb["BBL_20_2.0"]

        df["atr"] = ta.atr(df["high"], df["low"], df["close"])

        return df

    def detect_candles(self, df):

        patterns = []

        last = df.iloc[-1]

        if last["close"] > last["open"]:
            patterns.append("Bullish")

        else:
            patterns.append("Bearish")

        return patterns
