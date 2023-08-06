import nextcord
from nextcord.ext import commands, tasks
import random
import re
import json

TOKEN = ""  #Type your discord token here

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

message_storage = []


def load_messages():
    try:
        with open('message_storage.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_messages():
    with open('message_storage.json', 'w') as f:
        json.dump(message_storage, f)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip():
        message_storage.append(message.content)

    if bot.user in message.mentions:     #You can mess with most of these values.
        # Choose a random number of words (between 3 and 10 or the number of messages, whichever is smaller)
        num_words = min(random.randint(3, 10), len(message_storage))

        # Randomly select words from the storage
        random_words = random.sample(message_storage, num_words)

        # Use regex to find words in each random message
        words = [re.findall(r'\S+', random_message) for random_message in random_words]

        # Flatten the list of words
        flat_words = [word for sublist in words for word in sublist]

        # Shuffle the words randomly
        random.shuffle(flat_words)

        # Send the shuffled words as a single string
        allowed_mentions = nextcord.AllowedMentions(users=True, roles=True, everyone=True)
        await message.channel.send(' '.join(flat_words), allowed_mentions=allowed_mentions)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = nextcord.Game("with humans")
    await bot.change_presence(status=nextcord.Status.online, activity=game)

message_storage = load_messages()


@tasks.loop(minutes=1.0)
async def save_messages_task():
    save_messages()

save_messages_task.start()

bot.run(TOKEN)
