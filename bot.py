# Start date November 17th, 2018
# Python v3.6

from discord.ext import commands


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as: ')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.command()
async def hello(ctx: "Context"):
    """
    If a user types !hello the bot will respond with 'Hello! (nameOfUser here)
    """
    await ctx.send(f"Hello! {ctx.message.author.mention}")

bot.run(TOKEN)
