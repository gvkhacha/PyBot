# Start date November 17th, 2018
# Python v3.6

import discord
from discord.ext import commands

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as: ')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!hello"):
            await client.send_message(message.channel, content=(f"Hello! {message.author.mention}"))


if __name__ == '__main__':
    try:
        with open("token.txt", 'r') as file:
            TOKEN = file.read()
            client = MyClient()
            client.run(TOKEN)

    except FileNotFoundError:
        pass