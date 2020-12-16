import asyncio
import inspect
from typing import Union, Any, Optional, Callable

import discord
from discord.ext import commands


class Context(commands.Context):
    DEFAULT_COLOR = discord.Colour.dark_teal()

    async def ask(
        self,
        question: str,
        timeout: int = 120,
        parser: Optional[Union[Callable[[str], Any]]] = None,
        use_embed: bool = True,
        embed_color: Optional[discord.Color] = None,
        delete_question: bool = True,
        delete_answer: bool = True,
    ) -> Union[Optional[str], Any]:
        """
        Ask the user a question, returns the response as string or whatever parser returns
        :param question: Question as string
        :param timeout: Defaults to 120. Timeout for the question in seconds.
        :param parser: Optional. A callable or coroutine that gets the answer as a string ask will return
        :param use_embed: Defaults to True. Set to False to disable embeds
        :param embed_color: Optional. Custom color for the embed
        :param delete_question: Defaults to True. Delete the question before returning
        :param delete_answer: Defaults to True. Delete the answer before returning
        :return: Answer as string or whatever parser returns
        """
        if use_embed:
            if embed_color is None:
                embed_color = self.DEFAULT_COLOR
            embed = discord.Embed(description=question, colour=embed_color)
            question = await self.send(embed=embed)
        else:
            question = await self.send(question)

        def check(m: discord.Message) -> bool:
            return m.author == self.author and m.channel == self.channel

        message = None
        try:
            message = await self.bot.wait_for("message", check=check, timeout=timeout)
        except asyncio.TimeoutError:
            pass

        if delete_question:
            await question.delete()
        if message is None:
            return None

        reply = message.content
        if parser is not None:
            if inspect.isfunction(parser):
                reply = parser(message.content)
            elif inspect.iscoroutine(parser):
                reply = await parser(message.content)

        if delete_answer:
            await message.delete()

        return reply
