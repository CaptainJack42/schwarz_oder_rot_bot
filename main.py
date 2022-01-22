import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')


class SoRClient(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        log_format = (
            '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s'
        )
        file_handler = logging.FileHandler('SoR-Log.log')
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.DEBUG)
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            filename=('debug.log')
        )
        self.logger = logging.getLogger('SoR-Logger')
        self.logger.addHandler(file_handler)

    async def on_ready(self):
        """doesn't work somehow
        but should be called on connect
        """
        guilds = discord.utils.get(client.guilds)
        self.logger.info(
            f'{self.user.display_name} connected'
        )

    @commands.command(name='sor', aliases=['schwarz', 'rot', 'schwarzoderrot', 'schwarz oder rot'])
    async def create_game(self, ctx):
        message = await ctx.send(f'{ctx.author.mention} will Schwarz oder Rot spielen, @everyone join in by clicking :heavy_plus_sign:!')
        await message.add_reaction(':heavy_plus_sign:')  # FIXME

    @commands.command(name='start')
    async def start_game(self, ctx):
        pass

    @commands.command(name='hey')
    async def hey(self, ctx):
        guild = ctx.guild
        channel = ctx.channel
        await ctx.send(f'Hello {ctx.author} and welcome to {channel} in {guild}')


if __name__ == '__main__':
    bot = commands.Bot('!')
    bot.add_cog(SoRClient(bot))
    bot.run(API_TOKEN)
