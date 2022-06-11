import math
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
import json
import calculation

with open("config.json", "r") as config:
    config = json.load(config)
    token = config["token"]
    prefix = config["prefix"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))

lengthErrorMsg = "\nMessage exceeded 2000 characters."

@bot.command(aliases = ["pos", "p"])
async def possibilities(ctx: Context, *, text: str = ""):
    if text == "": return await ctx.reply("At least 1 argument is required.")
    acceptedKeys = ["speed", "strafe45", "mindistance", "prevslip", "currentslip", "results", "airtime"]
    values = {
        "results": 25,
        "speed": 0,
        "strafe45": "false",
        "mindistance": 0.01,
        "prevslip": 0.6,
        "currentslip": 0.6,
        "airtime": 2
    }

    for arg in text.split(' '):
        keyValue: list = arg.split("=")

        if keyValue[0].lower() in acceptedKeys:
            values[keyValue[0]] = keyValue[1]

    airtime = math.floor(float(values["airtime"]))
    if airtime < 0 or airtime > 255: return await ctx.reply("`airtime` has to be a value between `0` and `255`.")

    results = calculation.possibilities(
        vz=float(values["speed"]),
        strafe45=values["strafe45"].lower() == "true",
        minDistance=float(values["mindistance"]),
        prevSlip=float(values["prevslip"]),
        currSlip=float(values["currentslip"]),
        startAirtime=airtime
    )

    if (len(results) <= 0): return await ctx.reply("No results found.")

    resultMessage = "```\n"

    for index, result in enumerate(results):
        if index >= float(values["results"]): break

        newLine = f"[Poss by: {result['possBy']} {result['closestPixels']}px ({result['closestDistance']} blocks) "
        newLine += f"Tier {12 - result['airtime']} (Airtime {result['airtime']}) Distance made: {result['distance']}]\n"

        if (len(resultMessage + newLine) >= 2000 - len(lengthErrorMsg)):
            resultMessage += lengthErrorMsg
            break
        else: resultMessage += newLine

    await ctx.send(resultMessage + "\n```")

@bot.command(aliases = ["h"])
async def help(ctx: Context):
    embed = discord.Embed()
    embed.title = "How to use this bot!"
    embed.description = "This bot has a single command, `possibilities`, it simulates a single sprintjump with the given initial speed"
    embed.description += " and gives results of jumps that are possible with the given arguments."
    embed.description += "\nThe command can also be used with the following aliases, [`pos`, `p`]"
    embed.description += "\nArguments are as follow (values in parenthesis are the default values):"
    embed.add_field(name="strafe45 (False)", value="Whether the bot will be doing a sprintjump45 or just a sprintjump.", inline=True)
    embed.add_field(name="mindistance (0.01)", value="The amount a jump should be possible by to be included in results.", inline=True)
    embed.add_field(name="airtime (2)", value="Starting airtime for the simulation. Accepts values between 0 and 255.", inline=True)
    embed.add_field(name="speed (0)", value="The initial speed.", inline=True)  
    embed.add_field(name="currentslip (0.6)", value="Slip of the sprintjump tick.", inline=True)
    embed.add_field(name="prevslip (0.6)", value="Slip of the previous tick.", inline=True)
    embed.add_field(name="results (25)", value="The amount of results to display. By default, this exceeds message character limit.", inline=True)

    embed.add_field(name="Example use", value="`-pos speed=0 results=8 strafe45=true`", inline=False)

    await ctx.reply(embed=embed)

bot.run(token)