import discord
from discord.ext.commands.bot import BotBase
from utils.context import Context


class CustomBotBase(BotBase):
    async def get_context(self, message: discord.Message, *, cls=Context):
        return await super().get_context(message, cls=cls)


class Bot(CustomBotBase, discord.Client):
    pass


class AutoShardedBot(CustomBotBase, discord.AutoShardedClient):
    pass
