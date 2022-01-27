import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')


class MainClient(commands.Bot):
    def __init__(self, command_prefix, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command, description, **options)
        self.__setup_logger()
        self.__register_commands()
        self.relevant_msg: discord.Message = None
        self.players: list[discord.User]
        
    def __register_commands(self):
        self.start_sor_game = self.command(name='sor', aliases=['schwarz', 'rot', 'schwarzoderrot', 'schwarz oder rot'], pass_context=True)(self.create_sor_game)

    async def on_ready(self):
        guilds = discord.utils.get(self.guilds)
        self.logger.info(
            f'{self.user.display_name} connected in [{guilds}]'
        )

    async def create_sor_game(self, ctx):
        message = await ctx.send(f'{ctx.author.mention} will Schwarz oder Rot spielen, @everyone join in by clicking :beers:!')
        await message.add_reaction('🍻')
        self.relevant_msg = message

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.relevant_msg.id:
            return
        if payload.user_id == self.user.id:
            return
        print('reacted')
        
            
    def __setup_logger(self):
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

if __name__ == '__main__':
    bot = MainClient(command_prefix='!', description='!SchwarzOderRot')
    bot.run(API_TOKEN)
