
import pandas as pd
import sqlite3
import requests
import datetime

class MarketEngine:

    def __init__(self, api, account):

        self.api = api
        self.account = account
        self.db = sqlite3.connect("market.db")

    async def initialize_database(self):

        cursor = self.db.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS candles(

        time TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL

        )

        """)

        self.db.commit()

    async def download_initial_candles(self, symbol):

        print("Downloading history...")

    async def update_live_candles(self, symbol):

        print("Updating candles...")

        return pd.DataFrame()
