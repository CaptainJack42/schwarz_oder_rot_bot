from ast import alias
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

from ressource.card_deck import CardDeck

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')


class SoRGameClient(commands.Bot):
    def __init__(self, command_prefix, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command, description, **options)
        self.__setup_logger()
        self.__register_commands()
        self.init_msg_id: int = None
        self.players: list[discord.User] = []
        self.card_deck: CardDeck = None
        
    def __register_commands(self):
        self.create_sor_game = self.command(name='sor', aliases=['schwarz', 'rot', 'schwarzoderrot', 'schwarz oder rot'], pass_context=True)(self.create_game)
        self.start_sor_game = self.command(name='start', aliases=['go', 'play'], pass_context=True)(self.start_game)

    async def on_ready(self):
        guilds = discord.utils.get(self.guilds)
        self.logger.info(
            f'{self.user.display_name} connected in [{guilds}]'
        )

    async def create_game(self, ctx: commands.Context):
        message: discord.Message = await ctx.send(f'{ctx.author.mention} will Schwarz oder Rot spielen, @everyone join in by clicking :beers:!')
        await message.add_reaction('🍻')
        self.init_msg_id = message.id
        
    async def start_game(self, ctx: commands.Context):
        self.logger.debug(f'{ctx.author} tried to start the game')
        if len(self.players) <= 1:
            await ctx.send(f'Nicht genug Mitspieler... @everyone join in! :beers: !!!')
            return
        
        # TODO: start the game
        self.card_deck = CardDeck()
        self.init_msg_id = None

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.init_msg_id and self.init_msg_id != None:
            return
        if payload.user_id == self.user.id:
            return
        
        user = self.get_user(payload.user_id)
        if user == None:
            user = await self.fetch_user(payload.user_id)
        self.players.append(user)
        self.logger.debug(f'{user} joined the game')
        
            
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
    bot = SoRGameClient(command_prefix='!', description='!SchwarzOderRot')
    bot.run(API_TOKEN)
