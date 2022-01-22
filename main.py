import os
import discord
from dotenv import load_dotenv
import logging

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')


class SoRClient(discord.Client):
    def __init__(self) -> None:
        super().__init__()
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
        guilds = discord.utils.get(client.guilds)
        self.logger.info(
            f'{self.user.display_name} connected'
        )


if __name__ == '__main__':
    client = SoRClient()
    client.run(API_TOKEN)
