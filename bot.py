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


    def check_info_reaction(self, reaction, user):
        """ Predicate used in wait_for_reaction. Bot only cares about
        reactions from anyone except the bot."""
        return user != self.user

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!hello"):
            await client.send_message(message.channel, content=(f"Hello! {message.author.mention}"))

        if message.content.startswith("!info"):
            fields = message.content.split()

            if len(fields) == 1:
                # user only said !info or no spaces "!infopython" and will not work
                await client.send_message(message.channel, content=self.resources.get_help_text())

            else:
                if fields[1] == "add":
                    # Possible change - Making sure user has permission to add urls to resource list
                    if len(fields) != 4:
                        # Not correct number of parameters
                        await client.send_message(message.channel, content=self.resources.get_help_text())
                        return
                    if not self.resources.add_url(fields[2], fields[3]):
                        # add_url wasn't able to confirm that url was in the right format
                        await client.add_reaction(message, '😡')
                        return
                    await client.add_reaction(message, '😍')
                else:
                    topic = fields[1]
                    msg_topic = f"Here are some resources for {topic}\n\n"
                    try:
                        urls = self.resources.get_urls(topic)
                        msg = '\n'.join([f"<{u}>" for u in self.resources.get_urls(topic)[:5]])
                        msg += "\nReact to this message to get the full list Private Message'd to you!"
                        bot_message = await client.send_message(message.channel, content=(msg_topic + msg))

                        # Add reaction and wait for any other reaction
                        await client.add_reaction(bot_message, '📚')
                        react = await client.wait_for_reaction(['📚'], message=bot_message, check=self.check_info_reaction)


                        await client.send_message(react.user, content=msg_topic + '\n'.join([f"<{u}>" for u in self.resources.get_urls(topic)]))
                    except KeyError:
                        await client.send_message(message.channel, content=self.resources.get_invalid_text())

client = MyClient()
client.run(TOKEN)
