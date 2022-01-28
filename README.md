# schwarz_oder_rot_bot
A discord bot for playing the 'Schwarz oder Rot' drinking game


## Adding the API Token
- create a file named `.env` in the working directory
- add the line `API_TOKEN="<your_token>"` to the file and name exchange `<your_token>` with your actual token.

## Installing the bot (example on RPI)
1. install python3.10 (on RPI it needs to be built from source)
2. run `chmod +x discord_bot.sh` and `chmod +x main.py`
3. install requirements (ideally with `python3.10 -m pip install -r requirements.txt`, if this doesn't work just manuall install `discord` and `python-dotenv` packages with pip)
4. run the start script with `./discord_bot.sh start` (stop the bot with `./discord_bot.sh stop`).