import discord
from discord import app_commands
import responses
import os
import league
from dotenv import load_dotenv, dotenv_values

load_dotenv()
token = os.getenv('token')
server_id = os.getenv('server_id')
print(f'Token: {token}')

class GitGudBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        
    async def send_message(self, message, user_message):
        try:
            private = True if message.content.startswith('!') else False
            response = responses.handle_response(user_message)
            print(f'Here is the response: {response}')
            if response == None: return
            if private:
                await message.author.send(response)
            else:
                await message.channel.send(response)
        except Exception as e:
            print(e)

    async def send_given_message(self, user_message, message):
        try:
            if message == None: return
            await user_message.author.send(message)
        except Exception as e:
            print(e)


    async def on_ready(self):
        print(f'Bot {self.user} is ready!')
        await self.wait_until_ready()
        if not self.synced:
            await command_tree.sync(guild = discord.Object(id=server_id))
            self.synced = True

    async def on_message(self, message):
        if message.author == self.user or message[0] == '/':
            return
        user = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{user} in {channel} sent: {user_message}')
        await self.send_message(message, user_message)



discord_bot = GitGudBot()        
command_tree = app_commands.CommandTree(discord_bot)

@command_tree.command(name='riot', description='Enter your Riot ID (Name and Tagline)', guild = discord.Object(id=server_id))
async def riot_id(interaction: discord.Interaction, name: str): 
    riot_name = name.split("#")[0]
    tagline = name.split("#")[1]
    print(name)
    print(f'Name: {riot_name}, Tagline: {tagline}')
    try:
        sum_info = league.get_summoner(riot_name, tagline)
        await interaction.response.send_message(f'Your Riot name is {riot_name} and your tagline is {tagline}!', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Sorry, I could not find your Riot info. Please try again.', ephemeral=True) 

