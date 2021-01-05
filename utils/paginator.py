import asyncio
from enum import Enum
from typing import List, Optional, Union

import discord
from discord.ext import commands


class NavigationSize(int, Enum):
    DELETE_ONLY = 1
    SMALL = 4
    FULL = 99


class NavigationEmojis(Enum):
    FIRST = "⏪"
    LEFT = "◀️"
    RIGHT = "▶️"
    LAST = "⏩"
    DELETE = "🗑️"

    @classmethod
    def values(cls, size: int = NavigationSize.FULL) -> List[str]:
        if size <= NavigationSize.DELETE_ONLY:
            return [cls.DELETE.value]
        if size <= NavigationSize.SMALL:
            return cls.small()
        return [n.value for n in NavigationEmojis]

    @classmethod
    def small(cls) -> List[str]:
        return [cls.LEFT.value, cls.RIGHT.value, cls.DELETE.value]


class EmbedPaginator:
    def __init__(
        self,
        ctx: commands.Context,
        embeds: List[discord.Embed],
        timeout: int = 120,
        disable_footer: bool = False,
    ):
        self.embeds = embeds
        self.timeout = timeout
        self.disable_footer = disable_footer
        self.pos = 0
        self.emojis: List[str] = NavigationEmojis.values(size=len(self.embeds))
        self.message: Optional[discord.Message] = None
        self.ctx: commands.Context = ctx
        self.task: Optional[asyncio.Task] = None

    async def start(self):
        self.message = await self.ctx.send(embed=self.current)
        await self._add_navigation()
        self.task = asyncio.create_task(self._run())

    @property
    def footer(self):
        f = f"Page {self.pos+1}/{len(self.embeds)}"
        embed = self._current_embed
        if embed.footer:
            f = f"{embed.footer.text} | {f}"
        return f

    @property
    def _current_embed(self) -> discord.Embed:
        if 0 > self.pos > len(self.embeds):
            self.pos = 0
        return self.embeds[self.pos]

    @property
    def current(self) -> discord.Embed:
        embed = self._current_embed
        if not self.disable_footer:
            embed.set_footer(text=self.footer)
        return embed

    async def _refresh(self):
        await self.message.edit(embed=self.current)

    def _reaction_check(
        self, reaction: discord.Reaction, user: Union[discord.User, discord.Member]
    ):
        return (
            reaction.message == self.message
            and reaction.emoji in self.emojis
            and self.ctx.author == user
        )

    async def _add_navigation(self):
        if not self.message:
            return
        await asyncio.gather(*[self.message.add_reaction(emoji) for emoji in self.emojis])

    def _first(self):
        self.pos = 0

    def _left(self):
        self.pos -= 1
        if self.pos < 0:
            self._first()

    def _right(self):
        self.pos += 1
        if self.pos >= len(self.embeds):
            self._last()

    def _last(self):
        self.pos = len(self.embeds) - 1

    async def _delete(self):
        await self.message.delete()
        await self.ctx.message.delete()
        if self.task:
            self.task.cancel()

    async def _navigate(self, reaction: discord.Reaction):
        try:
            nav = NavigationEmojis(reaction.emoji)
        except ValueError:
            return

        if nav is NavigationEmojis.FIRST:
            self._first()
        elif nav is NavigationEmojis.LEFT:
            self._left()
        elif nav is NavigationEmojis.RIGHT:
            self._right()
        elif nav is NavigationEmojis.LAST:
            self._last()
        elif nav is NavigationEmojis.DELETE:
            return await self._delete()

        await self._refresh()

    async def _teardown(self):
        if not self.message:
            return
        await asyncio.gather(
            *[self.message.remove_reaction(emoji, self.message.author) for emoji in self.emojis]
        )

    async def _run(self):
        try:
            while True:
                reaction, user = await self.ctx.bot.wait_for(
                    "reaction_add", check=self._reaction_check, timeout=self.timeout
                )
                await self._navigate(reaction)
                await self.message.remove_reaction(reaction.emoji, user)
        except asyncio.TimeoutError:
            await self._teardown()
