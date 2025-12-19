import discord
import stoat
from stoat.ext import commands
import json
import asyncio
from discord import SyncWebhook
import os
import time
import requests
import random

with open('config.json') as f:
    config = json.load(f)

DISCORDBOTTOKEN = config.get('discordbottoken')
DISCORDBOTPREFIX = config.get('discordbotprefix')
REVOLTBOTTOKEN = config.get('stoatbottoken')
REVOLTBOTPREFIX = config.get('stoatbotprefix')
DISCORDCHANNELID = config.get('discordchannelid')
DISCORDWEBHOOKURL = config.get('discordwebhookurl')
REVOLTCHANNELID = config.get('stoatchannelid')
LANGSETTING = config.get('lang')

def load_translations(lang=LANGSETTING):
    translation_file = f'./lang/{lang}.json'
    if os.path.exists(translation_file):
        with open(translation_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"Translation file for {lang} not found, defaulting to English.")
        return load_translations('en')

lang = LANGSETTING
translation = load_translations(lang)
stoatclient = commands.Bot(token=REVOLTBOTTOKEN, command_prefix=REVOLTBOTPREFIX)

@stoatclient.on(stoat.MessageCreateEvent)
async def on_message(event: stoat.MessageCreateEvent):
    message = event.message
    if message.author_id == stoatclient.state.my_id:
        return
    if message.channel.id == REVOLTCHANNELID:
        webhook = SyncWebhook.from_url(DISCORDWEBHOOKURL)
        webhook.send(f"{message.content}", username=f"{message.author.id}", avatar_url=f"{message.author.internal_avatar.attach_state(message.author.state, 'avatars').url()}", allowed_mentions=discord.AllowedMentions(everyone=False))

@stoatclient.command()
async def help(ctx):
    embed = stoat.SendableEmbed(title=f"{stoatclient.user.name}", description=f"{REVOLTBOTPREFIX}help - {translation['help-helpd']}\n{REVOLTBOTPREFIX}ping - {translation['help-pingd']}\n{REVOLTBOTPREFIX}botinfo - {translation['help-botinfod']}\n{REVOLTBOTPREFIX}debug - {translation['help-debugd']}\n{REVOLTBOTPREFIX}say\n{REVOLTBOTPREFIX}presence\n{REVOLTBOTPREFIX}status\n{REVOLTBOTPREFIX}statusreset")
    await ctx.channel.send(embeds=[embed])

@stoatclient.command()
async def ping(ctx):
    await ctx.channel.send(translation['help-pingd'])

@stoatclient.command()
async def botinfo(ctx):
    embed = stoat.SendableEmbed(title=f"{stoatclient.user.name} {translation['informationtext']}", description=f"{translation['botinfo-madeby']}: RoxanneWolf#6117\n{translation['botinfo-gitlabsource']}: https://gitlab.com/roxannewolf/discordrevoltbridgebot\n{translation['botinfo-codebergsource']}: https://codeberg.org/roxannewolf/DiscordRevoltBridgeBot\n\n{translation['botinfo-info']}")
    await ctx.channel.send(embeds=[embed])

@stoatclient.command()
async def debug(ctx, debugoption=""):
    if debugoption == "config":
        try:
            embed = stoat.SendableEmbed(title=f"{stoatclient.user.name} {translation['debug-title']}", description=f"{translation['debug-dchannel']}: {DISCORDCHANNELID}\n{translation['debug-rchannel']}: {REVOLTCHANNELID}\n{translation['debug-dbotprefix']}: {DISCORDBOTPREFIX}\n{translation['debug-rbotprefix']}: {REVOLTBOTPREFIX}")
            await ctx.channel.send(embeds=[embed])
        except:
            await ctx.channel.send(translation['errormessage'])
    if debugoption == "troubleshoot":
        embed = stoat.SendableEmbed(title=f"{stoatclient.user.name} {translation['debug-title']}", description=f"{translation['debug-troubleshoot']}")
        await ctx.channel.send(embeds=[embed])
    if debugoption == "bot":
        embed = stoat.SendableEmbed(title=f"{stoatclient.user.name} {translation['debug-title']}", description=f"Bot ID: {stoatclient.state.my_id}\nUsers: {len(stoatclient.users)}")
        await ctx.channel.send(embeds=[embed])
    if debugoption == "server":
        embed = stoat.SendableEmbed(title=f"{stoatclient.user.name} {translation['debug-title']}", description=f"Server Name: {ctx.server.name}\nServer ID: {ctx.server.id}\nOwner ID: {ctx.server.owner_id}\nServer Discoverable?: {ctx.server.discoverable}")
        await ctx.channel.send(embeds=[embed])
    else:
        return

@stoatclient.command()
@commands.is_owner()
async def say(ctx, *, message:str):
    if any(word in message for word in blockedwords):
        await ctx.send("Sorry but I will not say anything that is racist or promotes/encourages illegal activities")
        return
    await ctx.channel.send(message)

@stoatclient.command()
@commands.is_owner()
async def presense(ctx, presencetype=""):
    if presencetype == "online":
        await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(presence=pyvolt.Presence.online))
        await ctx.channel.send("Bot status has been changed")
    if presencetype == "idle":
        await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.idle))
        await ctx.channel.send("Bot status has been changed")
    if presencetype == "focus":
        await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.focus))
        await ctx.channel.send("Bot status has been changed")
    if presencetype == "dnd":
        await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.busy))
        await ctx.channel.send("Bot status has been changed")
    if presencetype == "invisible":
        await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.invisible))
        await ctx.channel.send("Bot status has been changed")

@stoatclient.command()
@commands.is_owner()
async def status(ctx, *, statustext):
    await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(text=f"{statustext}"))
    await ctx.channel.send("Bot status has been changed")

@stoatclient.command()
@commands.is_owner()
async def statusreset(ctx):
    await stoatclient.http.edit_my_user(status=stoat.UserStatusEdit(text=None))
    await ctx.channel.send("Bot status has been reset")





class DiscordBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=DISCORDBOTPREFIX, intents=intents)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.webhook_id:
            return
        if message.channel.id == DISCORDCHANNELID:
            await stoatclient.http.send_message(REVOLTCHANNELID, f"{message.content}", masquerade=stoat.MessageMasquerade(name=f"{message.author.name}", avatar=f"{message.author.avatar}"))





if "__main__" == __name__:
    with open("blockedwords.txt", "r") as f:
        blockedwords = f.read().splitlines()

async def main():
    discordclient = DiscordBot()
    await asyncio.gather(
        discordclient.start(DISCORDBOTTOKEN),
        stoatclient.start(),
    )

asyncio.run(main())
