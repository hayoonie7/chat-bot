import discord
from discord import app_commands
import responses
import os
import league
import mysql.connector

from dotenv import load_dotenv, dotenv_values

load_dotenv()
token = os.getenv('token')
server_id = os.getenv('server_id')
user = os.getenv('user')
host = os.getenv('host')
database = os.getenv('database')
password = os.getenv('password')
print(f'Token: {token}')

class GitGudBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True  # Ensure the guilds intent is enabled
        intents.messages = True  # Ensure the messages intent is enabled
        super().__init__(intents=intents)
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
        await self.connect_database()
        if not self.synced:
            await command_tree.sync(guild = discord.Object(id=server_id))
            self.synced = True
    
    async def on_guild_join(self, guild):
        print(f'Joined {guild.name}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        user = str(message.author)
        user_message = str(message.content)
        if user_message.startswith('/'):
            return
        channel = str(message.channel)
        print(f'{user} in {channel} sent: {user_message}')
        await self.send_message(message, user_message)

    
    async def connect_database(self):
        try:
            cnx = mysql.connector.connect(user=user, password=password,
                              host=host,
                              database=database, port=3306)
            if cnx.is_connected():
                db_Info = cnx.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            
        cnx.close()



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

