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
        if user == self.user:
            return False
        return True

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
                msg = 'I can give you some information depending on the topics available.\nHere are the available topics:\n'
                msg += 'Ask for a topic by saying \"!info {topic}\"\n```'
                msg += '\n'.join(self.resources.get_keys())
                await client.send_message(message.channel, content=(msg + '```'))

            else:
                if fields[1] == "add":
                    # Possible change - Making sure user has permission to add urls to resource list
                    if len(fields) != 4:
                        # Not correct number of parameters
                        await client.send_message(message.channel, content=('To add a URL resource to our topics, use the following command:\n\t"!info add {topic} {url}"'))
                        return
                    if not self.resources.add_url(fields[2], fields[3]):
                        # add_url wasn't able to confirm that url was in the right format
                        await client.send_message(message.channel, content=("That is not a valid URL!"))
                        return
                    await client.send_message(message.channel, content=("Thank you for your contribution."))
                else:
                    topic = fields[1]
                    msg = f"Here are some resources for {topic}\n\n"
                    try:
                        msg += '\n'.join([f"<{u}>" for u in self.resources.get_urls(topic)[:5]])
                        bot_message = await client.send_message(message.channel, content=(msg))
                        await client.add_reaction(bot_message, '👍')
                        react = await client.wait_for_reaction(['👍', '👎'], message=bot_message, check=self.check_info_reaction)
                        await client.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(react))
                    except KeyError:
                        await client.send_message(message.channel, content=('That topic does not exist. If you wish to start the list of resources, use the following command:\n\t"!info add {topic} {url}"'))



client = MyClient()
client.run(TOKEN)
