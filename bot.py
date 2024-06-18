import discord
import responses
import keys

token = keys.token

async def send_message(message, user_message):
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

async def send_given_message(user_message, message):
    try:
        if message == None: return
        await user_message.author.send(message)
    except Exception as e:
        print(e)


def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'Bot {client.user} is ready!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{user} in {channel} sent: {user_message}')

        await send_message(message, user_message)

    client.run(token)