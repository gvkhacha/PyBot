# Start date November 17th, 2018
# Python v3.6

import discord
from discord.ext import commands
# Ignore the following commented out code. Mods are discussing how we will handle hosting and the bot's token.

# cacheJSON = 'json/cache.json'

# try:
#     with open(cacheJSON, 'r') as foo:
#         contents = json.load(foo)
#         TOKEN = contents['token']

# except FileNotFoundError:
#     pass

def extract_github_urls(channel: str, message: str) -> [(str, str)]:
    """ Given a single message from project_lists, finds
    projects that matches original {channel} and returns a 
    2-tuple  (project, url) """
    print(message.content)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as: ')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.project_channel = client.get_channel("515799506231492610")

    async def extract_github_urls(self, channel:str) -> [(str, str)]:
        links = []
        async for log in client.logs_from(self.project_channel):
            if f"<#{channel}>" in log.content:
                fields = log.content.split("\n")
                for f in fields:
                    if f.startswith("**Github"):
                        links.append((fields[0], f.split()[-1]))
                        break
        return links

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!hello"):
            await client.send_message(message.channel, content=(f"Hello! {message.author.mention}"))

        if message.content.startswith("!github"):
            links = await self.extract_github_urls(message.channel.id)
            msg = "\n".join(["{0}: {1}".format(project, url) for project, url in links])
            await client.send_message(message.channel, content=msg)




client = MyClient()
client.run(TOKEN)
