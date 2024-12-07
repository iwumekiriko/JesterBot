import disnake 
from disnake.ext import commands

from src.utils._embeds import EvalEmbed, ExceptionEmbed


class EvalCog(commands.Cog):
    async def cog_check(self, ctx: commands.Context) -> bool:
        return await ctx.bot.is_owner(ctx.author)
    

    def _prepare_response(self, variable) -> str:
        text = repr(variable)
        cutted_text = text[:1024]
        return f"```py\n{cutted_text}\n```"
    

    def _prepare_code(self, string: str) -> str:
        arr = string.strip("`").removeprefix('py\n').splitlines()
        return "".join(f"\n\t{i}" for i in arr)
    
    async def evaluate(self, ctx: commands.Context, code: str) -> None:
        code = self._prepare_code(code)
        args = {
            'disnake': disnake,
            'ctx': ctx
        }

        try:
            exec(f"async def func():{code}", args)
            response = await eval("func()", args)

            if response is None or isinstance(response, disnake.Message):
                return

            embed = EvalEmbed(
                title="Успешно выполнено!",
                description=self._prepare_response(response),
            ).set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed,
                           allowed_mentions=disnake.AllowedMentions(users=False))

        except Exception as error:
            embed = ExceptionEmbed(
                message=f"```{type(error).__name__}: {str(error)}```",
            ).set_thumbnail(url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed, 
                           allowed_mentions=disnake.AllowedMentions(users=False))

    @commands.command(aliases=['eval'])
    async def _eval(self, ctx, *, code: str) -> None:
        await self.evaluate(ctx, code)
