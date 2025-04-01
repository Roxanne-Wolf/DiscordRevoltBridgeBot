import discord
import pyvolt
from pyvolt.ext import commands
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
REVOLTBOTTOKEN = config.get('revoltbottoken')
REVOLTBOTPREFIX = config.get('revoltbotprefix')
BOTNAME = config.get('botname')
DISCORDCHANNELID = config.get('discordchannelid')
DISCORDWEBHOOKURL = config.get('discordwebhookurl')
REVOLTCHANNELID = config.get('revoltchannelid')
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

revoltclient = pyvolt.Client()
revoltclient = commands.Bot(token=REVOLTBOTTOKEN, command_prefix=REVOLTBOTPREFIX)

@revoltclient.on(pyvolt.MessageCreateEvent)
async def on_message(event: pyvolt.MessageCreateEvent):
    message = event.message
    if message.author_id == revoltclient.state.my_id:
        return
    if message.channel.id == REVOLTCHANNELID:
        webhook = SyncWebhook.from_url(DISCORDWEBHOOKURL)
        webhook.send(f"{message.content}", username=f"{message.author.id}", avatar_url=f"{message.author.internal_avatar.attach_state(message.author.state, 'avatars').url()}", allowed_mentions=discord.AllowedMentions(everyone=False))

@revoltclient.command()
async def help(ctx):
    embed = pyvolt.SendableEmbed(title=f"{BOTNAME}", description=f"{REVOLTBOTPREFIX}help - {translation['help-helpd']}\n{REVOLTBOTPREFIX}ping - {translation['help-pingd']}\n{REVOLTBOTPREFIX}botinfo - {translation['help-botinfod']}\n{REVOLTBOTPREFIX}debug - {translation['help-debugd']}")
    await ctx.channel.send(embeds=[embed])

@revoltclient.command()
async def ping(ctx):
    await ctx.channel.send(translation['help-pingd'])

@revoltclient.command()
async def botinfo(ctx):
    embed = pyvolt.SendableEmbed(title=f"{BOTNAME} {translation['informationtext']}", description=f"{translation['botinfo-madeby']}: RoxanneWolf#6117\n{translation['botinfo-gitlabsource']}: https://gitlab.com/roxannewolf/discordrevoltbridgebot\n{translation['botinfo-codebergsource']}: https://codeberg.org/roxannewolf/DiscordRevoltBridgeBot\n\n{translation['botinfo-info']}")
    await ctx.channel.send(embeds=[embed])

@revoltclient.command()
async def debug(ctx, debugoption=""):
    if debugoption == "config":
        try:
            embed = pyvolt.SendableEmbed(title=f"{BOTNAME} {translation['debug-title']}", description=f"{translation['debug-dchannel']}: {DISCORDCHANNELID}\n{translation['debug-rchannel']}: {REVOLTCHANNELID}\n{translation['debug-dbotprefix']}: {DISCORDBOTPREFIX}\n{translation['debug-rbotprefix']}: {REVOLTBOTPREFIX}")
            await ctx.channel.send(embeds=[embed])
        except:
            await ctx.channel.send(translation['errormessage'])
    if debugoption == "troubleshoot":
        embed = pyvolt.SendableEmbed(title=f"{BOTNAME} {translation['debug-title']}", description=f"{translation['debug-troubleshoot']}")
        await ctx.channel.send(embeds=[embed])
    else:
        return





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
            await revoltclient.http.send_message(REVOLTCHANNELID, f"{message.content}", masquerade=pyvolt.MessageMasquerade(name=f"{message.author.name}", avatar=f"{message.author.avatar}"))





async def main():
    pyvolt.utils.setup_logging(root=True)
    discordclient = DiscordBot()
    await asyncio.gather(
        discordclient.start(DISCORDBOTTOKEN),
        revoltclient.start(),
    )

asyncio.run(main())
