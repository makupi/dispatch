import discord
from discord.ext import commands
from utils.context import Context


class Bot(commands.Bot):
    async def get_context(self, message: discord.Message, *, cls=Context):
        return await super().get_context(message, cls=cls)


class AutoShardedBot(commands.AutoShardedBot):
    async def get_context(self, message: discord.Message, *, cls=Context):
        return await super().get_context(message, cls=cls)
