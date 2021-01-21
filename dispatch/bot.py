from pathlib import Path
from typing import Optional, Type

import discord
from discord.ext.commands.bot import BotBase
from dispatch.context import Context
from dispatch.settings import Settings


class CustomBotBase(BotBase):
    def __init__(
        self,
        cogs_path: Optional[str] = None,
        command_prefix: Optional[str] = None,
        settings: Type[Settings] = Settings,
        *args,
        **kwargs,
    ):
        self.settings = settings()
        if command_prefix is None:
            command_prefix = self.settings.prefix
        super().__init__(command_prefix, *args, **kwargs)
        self.cogs_path = cogs_path
        if self.cogs_path is not None:
            self.cogs_path = Path(cogs_path)
            self._load_extensions()

    @property
    def token(self) -> str:
        return self.settings.token

    def _load_extensions(self):
        for file in self.cogs_path.rglob("*.py"):
            ext = file.as_posix()[:-3].replace("/", ".")
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
    def run(self, token: Optional[str] = None):
        if token is not None:
            super().run(token)
        super().run(self.token)


class AutoShardedBot(CustomBotBase, discord.AutoShardedClient):
    def run(self, token: Optional[str] = None):
        if token is not None:
            super().run(token)
        super().run(self.token)
