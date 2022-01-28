from ast import alias
from enum import IntEnum
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import logging
import ressource.card_deck as card_deck

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')


class SoRMainClient(commands.Bot):
    def __init__(self, command_prefix, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command, description, **options)
        self.__setup_logger()
        self.__register_commands()
        self.init_msg_id: int = None
        self.game_channel: commands.Context = None
        self.game: SoRGame = None

    def __register_commands(self):
        self.create_sor_game = self.command(name='sor', aliases=[
                                            'schwarz', 'rot', 'schwarzoderrot', 'schwarz oder rot', 'new', 'neu'], pass_context=True)(self.create_game)
        self.start_sor_game = self.command(
            name='start', aliases=['go', 'play'], pass_context=True)(self.start_game)

    async def on_ready(self):
        guilds = discord.utils.get(self.guilds)
        self.logger.info(
            f'{self.user.display_name} connected in [{guilds}]'
        )

    async def create_game(self, ctx: commands.Context):
        message: discord.Message = await ctx.send(f'{ctx.author.mention} will Schwarz oder Rot spielen, @everyone macht mit indem ihr auf :beers: klickt!')
        await message.add_reaction('🍻')
        self.game = SoRGame(self, self.logger)
        self.init_msg_id = message.id
        self.game_channel = ctx

    async def start_game(self, ctx: commands.Context):
        self.logger.debug(f'{ctx.author} tried to start the game')
        if len(self.game.players) <= 0:
            await ctx.send(f'Nicht genug Mitspieler... @everyone macht mit! :beers: :beers: :beers:')
            return
        self.init_msg_id = None
        await self.game.run()

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.init_msg_id and self.init_msg_id != None:
            return
        if payload.user_id == self.user.id:
            return

        user = self.get_user(payload.user_id)
        if user == None:
            user = await self.fetch_user(payload.user_id)

        await self.game.add_player(user)
        self.logger.debug(f'{user} joined the game')

    async def send_msg_and_await_reaction(self, msg: str, curr_player: discord.User, possible_reacts: list[str]):
        message: discord.Message = await self.game_channel.send(msg)
        for emoji in possible_reacts:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == curr_player and str(reaction.emoji) in possible_reacts

        try:
            reaction, user = await self.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            await self.game_channel.send(
                f'{curr_player.mention} hat nicht reagiert und wird nun aus dem Spiel entfernt.')
            await self.game.remove_player(curr_player)
        else:
            return str(reaction)

    async def send_msg(self, msg: str):
        await self.game_channel.send(msg)

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


class SoRGame:
    MESSAGES_MAP: dict = {
        0: 'Schwarz oder Rot?',
        1: 'Höher, Tiefer oder Gleich?',
        2: 'Innerhalb oder Außerhalb? \n ✅ : innerhalb \n ❌ : außerhalb \n 🌗 : gleich',
        3: 'Hast du oder hast du nicht? \n ✅ : hab ich \n ❌ : hab ich nicht',
    }

    REACTION_MAP: dict = {
        0: ['⚫', '🔴'],
        1: ['⏫', '⏬', '🌗'],
        2: ['✅', '❌', '🌗'],
        3: ['✅', '❌'],
    }

    def __init__(self, client: SoRMainClient, logger: logging.Logger) -> None:
        self.players: list[discord.User] = list()
        self.player_cards: list[list[card_deck.Card]] = list()
        self.logger: logging.Logger = logger
        self.client: SoRMainClient = client
        self.deck = card_deck.CardDeck()

    async def add_player(self, player: discord.User):
        if player not in self.players:
            self.players.append(player)
            self.player_cards.append(list())
            self.logger.debug(f'{player} joined the game')

    async def remove_player(self, player: discord.User):
        if player in self.players:
            idx = self.players.index(player)
            self.player_cards.remove(self.player_cards[idx])
            self.players.remove(player)

    async def run(self):
        await self.phase_1()
        await self.phase_2()
        await self.phase_3()
        await self.phase_4()

    async def phase_1(self):
        for player in self.players:
            msg = f'{player.mention} \n {self.MESSAGES_MAP.get(0)}'
            reaction = await self.client.send_msg_and_await_reaction(msg, player, self.REACTION_MAP.get(0))
            if reaction == None:
                continue
            
            self.logger.debug(
                f'{player.name} reacted with {reaction} to Schwarz oder Rot. This is viable: ({str(reaction) in self.REACTION_MAP.get(0)})')
            
            card: card_deck.Card = self.deck.draw_card()
            
            msg = f'{player.mention} deine Karte ist die {self.deck.CARD_VALUE_MAP.get(card.value)} of {card.color._name_}.'
            
            if await self.parse_phase_1(card, reaction):
                msg += '\n Das ist richtig! Wähle jemanden aus der trinkt!'
            else:
                msg += '\n Das ist falsch! Trink!'
                
            await self.client.send_msg(msg)
            
    async def parse_phase_1(self, card: card_deck.Card, reaction: str) -> bool:
        if reaction == '⚫':
            if card.color == card_deck.CardColor.SPADES or card.color == card_deck.CardColor.CLUBS:
                return True
            else:
                return False
        elif reaction == '🔴':
            if card.color == card_deck.CardColor.HEARTS or card.color == card_deck.CardColor.DIAMONDS:
                return True
            else:
                return False

    async def phase_2(self):
        for (idx, player) in enumerate(self.players):
            msg = f'{player.mention} \n {self.MESSAGES_MAP.get(1)}'
            reaction = await self.client.send_msg_and_await_reaction(msg, player, self.REACTION_MAP.get(1))
            if reaction == None:
                continue
            
            self.logger.debug(
            f'{player.name} reacted with {reaction} to Schwarz oder Rot. This is viable: ({str(reaction) in self.REACTION_MAP.get(0)})')

    async def phase_3(self):
        pass

    async def phase_4(self):
        pass


if __name__ == '__main__':
    bot = SoRMainClient(command_prefix='!', description='!SchwarzOderRot')
    bot.run(API_TOKEN)
