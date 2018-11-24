# Start date November 17th, 2018
# Python v3.6

import re
import projectslist
from discord.ext import commands
from projectslist import ProjectInfo


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

@bot.command()
async def test(ctx: "Context"):
    channel = bot.get_channel()
    print(channel)


async def extract_project_info():
    links = []
    project_list_channel = bot.get_channel(515799506231492610)
    async for log in project_list_channel.history():
        try:
            text = str(log.content)
            title = re.findall(r"\*\*([^:]+)\*\*\n", text)[0]
            channel_id = re.findall(r"<#(\d+)>", text)[0]
            url = re.findall(r"\*\* (\S+github\S+)\n", text)[0]
            links.append(ProjectInfo(title, int(channel_id), url))
        except AttributeError:
            pass
    print(links)
    return links


@bot.command()
async def github(ctx: "Context"):
    """
    If a user types !github, the bot will find github links depending on the
    channel the message was sent and indexes #project-list
    If a user types !github <projectname> it will index #project-list and find
    matching names
    """
    all_links = await extract_project_info()	#TODO
    fields = ctx.message.content.split()
    if len(fields) > 1:
        if (fields[-1].lower() == "help"):
            await ctx.send('Usage:\n\t"!github" in a channel where a project exists.\n\t"!github [project_name]" otherwise')
            return
        # user has asked for a specific project, try to search it
        links = projectslist.get_by_name(fields[-1], all_links)
    else:
        # get the project that is assigned with users channel
        links = projectslist.get_by_channel(ctx.message.channel.id, all_links)
    if len(links) < 1:
        await ctx.message.add_reaction('😡')
        return
    msg = "\n".join(["{0}: {1}".format(project, url) for project, _, url in links])
    await ctx.send(msg)


bot.run(TOKEN)