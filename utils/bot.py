from pathlib import Path
from typing import Optional

import discord
from discord.ext.commands.bot import BotBase
from utils.context import Context


class CustomBotBase(BotBase):
    def __init__(self, cogs_path: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cogs_path = cogs_path
        if self.cogs_path is not None:
            self.cogs_path = Path(cogs_path)
            self._load_extensions()

    def _load_extensions(self):
        for file in self.cogs_path.rglob("*.py"):
            ext = str(file)[:-3].replace("/", ".")
            try:
                self.load_extension(ext)
            except Exception as ex:
                print(f"Failed to load extension {ext}. Exception: {ex}")

    def load_extensions(self, cogs_path: str = "bot/cogs"):
        self.cogs_path = Path(cogs_path)
        self._load_extensions()

    async def get_context(self, message: discord.Message, *, cls=Context):
        return await super().get_context(message, cls=cls)


class Bot(CustomBotBase, discord.Client):
    pass


class AutoShardedBot(CustomBotBase, discord.AutoShardedClient):
    pass
