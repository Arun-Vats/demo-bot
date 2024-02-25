#(©)Codexbotz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT
from helper_func import subscribed, search_in_channel

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join Force Sub Channel & restart the Bot!")
                sys.exit()

    async def stop_and_restart(self):
        await self.stop()
        await self.start()

    async def send_message(self, message: Message, text: str):
        try:
            await self.send_message(chat_id=message.chat.id, text=text, reply_to_message_id=message.message_id)
        except Exception as e:
            LOGGER.error(e)

    async def search_messages(self, chat_id, query, filter, limit):
        try:
            messages = await self.search_messages(
                chat_id=chat_id,
                query=query,
                filter=filter,
                limit=limit
            )
            return messages
        except Exception as e:
            LOGGER.error(e)
            return None

Bot().run()

