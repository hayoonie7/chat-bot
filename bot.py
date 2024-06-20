import discord
from discord import app_commands
import pymongo.errors
import responses
import asyncio
import signal
import os
import league
import mysql.connector
import pymongo
from pymongo import MongoClient

from dotenv import load_dotenv, dotenv_values


class GitGudBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True  # Ensure the guilds intent is enabled
        intents.messages = True  # Ensure the messages intent is enabled
        super().__init__(intents=intents)
        load_dotenv()
        self.token = os.getenv('token')
        self.connection_string = os.getenv('connection_string')
        self.server_id = os.getenv('server_id')
        self.sql_user = os.getenv('user')
        self.host = os.getenv('host')
        self.database = os.getenv('database')
        self.password = os.getenv('password')
        print(f'Token: {self.token}')
        self.synced = False
        self.cnx = None
        self.database = None
        self.collection = None

        
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
        print(f'Bot {self.user} is ready! with id: {self.user.id}')
        await self.wait_until_ready()
        # await self.connect_database()
        discord_database = await self.get_database()
        self.database = discord_database
        self.collection = discord_database['Users']
        if not self.synced:
            await command_tree.sync(guild = discord.Object(id=self.server_id))
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
            self.cnx = mysql.connector.connect(user=self.sql_user, password=self.password,
                              host=self.host,
                              database=self.database, port=3306)
            if self.cnx.is_connected():
                db_Info = self.cnx.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
        except mysql.connector.Error as err:
                print(err)

    async def get_database(self):
        print('Connecting to MongoDB...')
        try:
            database_client = MongoClient(self.connection_string)
            db = database_client.list_database_names()
            print('Connected to MongoDB!')
            return database_client['DiscordBot']
            
        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to MongoDB: %s" % e)
        except pymongo.errors.OperationFailure as e:
            print("Authentication failed: %s" % e)
        
        # return database_client['']
    
    async def add_user(self, user):
        try:
            print('Adding user...')
            if self.collection.find_one(user):
                print('User already exists!')
                return
            self.collection.insert_one(user)
            print('User added!')
        except Exception as e:
            print(e)

    async def on_disconnect(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()
            print('Database connection closed.')
        print('Bot has disconnected.')

    async def on_close(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()
            print('Database connection closed.')
        print('Bot connection is closing.')



discord_bot = GitGudBot()        
command_tree = app_commands.CommandTree(discord_bot)


@command_tree.command(name='riot', description='Enter your Riot ID (Name and Tagline)', guild = discord.Object(id=discord_bot.server_id))
async def riot_id(interaction: discord.Interaction, name: str): 
    riot_name = name.split("#")[0]
    tagline = name.split("#")[1]
    print(name)
    print(f'Name: {riot_name}, Tagline: {tagline}')
    try:
        sum_info = league.get_summoner(riot_name, tagline)
        await interaction.response.send_message(f'Your Riot name is {riot_name} and your tagline is {tagline}!', ephemeral=True)
        user = interaction.user
        user_to_add = {
                'user_id': user.id,
                'name': user.name,
                'puuid': sum_info['puuid'],
                'riot_id': name
        }
        print(user_to_add)
        await discord_bot.add_user(user_to_add)
    except Exception as e:
        await interaction.response.send_message(f'Sorry, I could not find your Riot info. Please try again.', ephemeral=True) 

@command_tree.command(name='info', description='Display your riot info', guild = discord.Object(id=discord_bot.server_id))
async def get_riot_id(interaction: discord.Interaction):
    try:
        user_id = interaction.user.id
        user_document = discord_bot.collection.find_one({'user_id': user_id})
        if not user_document:
            await interaction.response.send_message(f'You have not entered your Riot ID yet!', ephemeral=True)
            return
        riot_id = user_document['riot_id']
        riot_name = riot_id.split("#")[0]
        tagline = riot_id.split("#")[1]
        puuid = user_document['puuid']
        await interaction.response.send_message(f'Your Riot name is {riot_name}.\nYour tagline is {tagline}\nAnd your puuid is {puuid}.', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Sorry, I could not find your Riot info. Please try again.', ephemeral=True)  
