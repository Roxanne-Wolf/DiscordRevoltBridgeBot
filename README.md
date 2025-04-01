# Discord+Revolt Bridge Bot

Made by: roxanne.wolf. (On Discord) / RoxanneWolf#6117 (On Revolt.chat)

## About:

This Discord+Revolt Bridge Bot source code allows you to connect your Discord and Revolt community together. This will allow your Discord and Revolt members to communicate with each other. This code is meant to be a simple and memory-efficient way to bridge your Discord and Revolt community.

This project will only work for 1 Discord and 1 Revolt server.

## Requirements:

- Python 3.10 or newer.
- Some basic knowledge of Python
- A Discord AND revolt.chat bot
- At least 256mb ram free and 512mb disk free.

## Setup:

Here is the steps needed to get started with using this source code.

1. Download/Fork this source code and upload it to your server
2. Create a Discord and Revolt bot.
- For Discord: Go to https://discord.com/developers/applications and create a new application. Under the bot section, enable the Message content intent so the bot can check the messages and send them to the Revolt channel set.
- For Revolt: Go to https://app.revolt.chat/settings/bots and create a new bot. Make sure to copy the token.
3. Open config.json and fill in everything it asks for:
- "discordbottoken": "" => Put in your Discord bot token here
- "discordbotprefix": "!" => Put in the prefix for the Discord bot (not used)
- "revoltbottoken": "" => Put in your Revolt.chat bot token.
- "revoltbotprefix": "!" => Put in the prefix for the Revolt.chat bot.
- "botname": "" => Enter the name you want to call your bot here (this name will show up on the embeds within the commands).
- "discordchannelid": DISCORD_CHANNEL_ID_HERE => Replace DISCORD_CHANNEL_ID_HERE with your Discord channel ID
- "discordwebhookurl": "" => Put in your Discord webhook url here.
- "revoltchannelid": "" => Put in the Revolt channel ID here (Make sure the Revolt.chat bot has the "Use Masquerade" permission.
- "lang": "" => Set the language code of the language. Defaults to English. (Refer to the supported languages section below)
4. Invite your Discord and Revolt bot to your server
- For the Discord bot, make sure it has the Read Messages permission on the channel you are trying to bridge to Revolt.
- For the Revolt bot, make sure the bot has the "View Channel", "Send Messages", "Send Embeds", and "Use Masquerade" permissions (check channel overrides as well)
5. Install everything from the requirements.txt file.
6. Run the main.py file. Assuming you did all steps correctly, your Discord+Revolt bridge bot should work.

## ToDo

- Make it where the webhooks show the member's username instead of ID.
- Get Translators to get better accurate translations
- Command support for the Discord bot

Please open an issue or pull request if you have a solution to any of these issues.

## Supported Languages:

- en = English (Default/Main)
- es = Spanish
- de = German
- tr = Turkish

| Language     | Verified translation? | Translation by (Revolt usernames)                  |
|--------------|-----------------------|----------------------------------------------------|
| English (en) | :white_check_mark:    | [RoxanneWolf#6117](https://gitlab.com/roxannewolf) |
| Spanish (es) | :x:                   | Google Translate                                   |
| German (de)  | :x:                   | Google Translate                                   |
| Turkish (tr) | :x:                   | Google Translate                                   |