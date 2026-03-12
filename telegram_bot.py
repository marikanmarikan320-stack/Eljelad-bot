
from telegram import Bot

class TelegramEngine:

    def __init__(self, token, chat):

        self.bot = Bot(token)
        self.chat = chat

    async def send(self, text):

        await self.bot.send_message(

            chat_id=self.chat,

            text=text

        )
