# This example requires the 'message_content' privileged intent to function.

import discord
import random

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        if message.content.startswith('!1d'):
            msg_array =  message.content.split('d')
            # on recupere l'id du channel dans lequel le message à été envoyé puis le channel lui même
                # channel_id = message.channel.id
                # channel = self.get_channel(channel_id)
            if message.content.find(' ') != -1:
                chiffre = msg_array[1][0:message.content.find(' ')]
            else:
                chiffre = msg_array[1]
            print(chiffre)
            print(chiffre.isdigit())
            if chiffre.isdigit():
                await message.reply(random.randrange(1,int(chiffre),1), mention_author=True)
            else:
                await message.reply("Something went wrong...", mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTAxMjI5MjI0NzYzNjY4NDgyMA.GeE3F_.KRa9UdareJVjM1QOhY38Bl0UF9hW5-wCE2BHJs')