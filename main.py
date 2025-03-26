import discord
from discord.ext import commands
from collections import defaultdict

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to keep track of messages
message_tracker = defaultdict(list)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Track the message content and author
    message_tracker[message.content].append(message)

    # Check if the same message has been sent more than once
    if len(message_tracker[message.content]) > 1:
        # If it's a bot, ban it
        if message.author.bot:
            try:
                await message.author.ban(reason="Sent duplicate messages")
                print(f"Banned bot: {message.author.name}")
            except discord.Forbidden:
                print("Bot does not have permission to ban.")
            except discord.HTTPException:
                print("Failed to ban the bot.")

        # Delete all duplicate messages
        for msg in message_tracker[message.content]:
            try:
                await msg.delete()
                print(f"Deleted message: {msg.content} from {msg.author.name}")
            except discord.Forbidden:
                print("Bot does not have permission to delete messages.")
            except discord.HTTPException:
                print("Failed to delete the message.")

        # Clear the tracked messages for this content
        del message_tracker[message.content]

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    # Remove the message from the tracker if it gets deleted
    if message.content in message_tracker:
        message_tracker[message.content].remove(message)
        if not message_tracker[message.content]:
            del 
