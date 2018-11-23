# Start date November 17th, 2018
# Python v3.6

import json
import discord
from discord.ext import commands
from resources import Resources

# Ignore the following commented out code. Mods are discussing how we will handle hosting and the bot's token.

# cacheJSON = 'json/cache.json'

# try:
#     with open(cacheJSON, 'r') as foo:
#         contents = json.load(foo)
#         TOKEN = contents['token']

# except FileNotFoundError:
#     pass

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as: ')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.resources = Resources()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!hello"):
            await client.send_message(message.channel, content=(f"Hello! {message.author.mention}"))

        if message.content.startswith("!info"):
            topic_sep = message.content.split()
            if len(topic_sep) == 1:
                # user only said !info or !infopython and will not work
                return
            else:
                # only considers one-word info requests - "!info c plus plus" would not work
                topic = topic_sep[1]
                msg = '\n'.join([f"<{u}>" for u in self.resources.get_urls(topic)])
                await client.send_message(message.channel, content=(msg))


client = MyClient()
client.run(TOKEN)
