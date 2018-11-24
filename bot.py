# Start date November 17th, 2018
# Python v3.6

import discord
import re
from discord.ext import commands
import projectslist
from projectslist import ProjectInfo
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
        self.project_channel = client.get_channel("515799506231492610")

    async def extract_project_info(self) -> [(str, str)]:
        links = []
        async for log in client.logs_from(self.project_channel):
            try:
                text = str(log.content)
                title = re.findall(r"\*\*([^:]+)\*\*\n", text)[0]
                channel_id = re.findall(r"<#(\d+)>", text)[0]
                url = re.findall(r"\*\* (\S+github\S+)\n", text)[0]
                links.append(ProjectInfo(title, channel_id, url))
            except AttributeError:
                pass

        return links

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!hello"):
            await client.send_message(message.channel, content=(f"Hello! {message.author.mention}"))


        if message.content.startswith("!github"):
            all_links = await self.extract_project_info()
            fields = message.content.split()
            if len(fields) > 1:
                if (fields[-1].lower() == "help"):
                    await client.send_message(message.channel, content='Usage:\n\t"!github" in a channel where a project exists.\n\t"!github [project_name]" otherwise')
                    return
                # user has asked for a specific project, try to search it
                links = projectslist.get_by_name(fields[-1], all_links)
            else:
                # get the project that is assigned with users channel
                links = projectslist.get_by_channel(message.channel.id, all_links)
            if len(links) < 1:
                await client.add_reaction(message, '😡')
                return
            msg = "\n".join(["{0}: {1}".format(project, url) for project, _, url in links])
            await client.send_message(message.channel, content=msg)




client = MyClient()
client.run(TOKEN)
