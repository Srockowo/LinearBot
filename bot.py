import discord
from discord.ext import commands
from discord.ext.commands.context import Context
import json
import calculation
import parser
import args

with open("config.json", "r") as config:
    config = json.load(config)
    token = config["token"]
    prefix = config["prefix"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

messageCache = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.id not in messageCache: return

    botMsg: discord.Message = messageCache[before.id]

    displayMessage = await handleInput(after, after.content)

    if displayMessage is None: return

    botMsg: discord.Message = await botMsg.edit(content=displayMessage)
    
@bot.command(aliases = ["pos", "p"])
async def possibilities(ctx: Context, *, text: str = ""):
    displayMessage = await handleInput(ctx, text)

    if displayMessage is None: return

    botMsg: discord.Message = await ctx.send(displayMessage)

    messageCache[ctx.message.id] = botMsg

@bot.command(aliases = ["h"])
async def help(ctx: Context):
    embed = discord.Embed()
    embed.title = "How to use this bot!"
    embed.description = "This bot has a single command, `possibilities`, it simulates a single sprintjump with the given initial speed"
    embed.description += " and gives results of jumps that are possible with the given arguments."
    embed.description += "\nThe command can also be used with the following aliases: [`pos`, `p`]"
    embed.description += "\nArguments are as follow (values in parenthesis are the default values):"
    
    defaultArgs = args.default()

    for key, value in defaultArgs.items():
        embed.add_field(name=f"{key} ({value['value']})", value=value["description"], inline=True)

    embed.add_field(name="Example use", value="`-pos speed=0 results=8 strafe45=true`", inline=False)

    await ctx.reply(embed=embed)

async def handleInput(replyTo: Context | discord.Message, input: str):
    if input == "":
        await errorMsg(replyTo, "At least 1 argument is required.")
        return
    
    try: inputArgs = parser.parseInput(input)
    except:
        await errorMsg(replyTo, f"Invalid arguments. Use `{prefix}help` for more information")
        return

    airtime = inputArgs["airtime"]
    if airtime < 0 or airtime > 255:
        await errorMsg(replyTo, "`airtime` has to be a value between `0` and `255`.")
        return

    results = calculation.possibilities(inputArgs)

    if (len(results) < 1):
        await errorMsg(replyTo, "No results found.")
        return

    return calculation.toString(results, inputArgs)

async def errorMsg(to: Context | discord.Message, msg: str):
    await to.reply(content=msg, delete_after=5)

bot.run(token)