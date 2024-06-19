from bot import discord_bot
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
token = os.getenv('token')

if __name__ == "__main__":
    discord_bot.run(token)