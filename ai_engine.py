import random

class AIEngine:

    def __init__(self, key):

        self.key = key

    def generate_signal(self, indicators, patterns):

        if random.random() > 0.95:

            return {

                "type": "BUY",

                "entry": 2000,

                "tp": 2010,

                "sl": 1990,

                "confidence": "78%"

            }

        return None
