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
            input = msg_array[1]
            # on recupere l'id du channel dans lequel le message à été envoyé puis le channel lui même
                # channel_id = message.channel.id
                # channel = self.get_channel(channel_id)
            if input.find(' ') != -1:
                chiffre = input[0:input.find(' ')]
            else:
                chiffre = input
            if chiffre.isdigit():
                await message.reply(":8ball:" + " : " + str(random.randrange(1,int(chiffre),1)), mention_author=True)
            else:
                await message.reply("Something went wrong...", mention_author=True)
        
        if message.content.startswith('!2d'):
            # on recupere l'id du channel dans lequel le message à été envoyé puis le channel lui même
                # channel_id = message.channel.id
                # channel = self.get_channel(channel_id)
            if message.content.count(' ') > 0:
                chiffres = message.content.split(' ')
            else:
                if message.content[3:].isdigit():
                    chiffre = message.content[3:]
            if chiffre is None:
                for i in range(2):
                    if chiffres[i].isdigit() != True:
                        await message.reply("L'argument n°"+(i+1)" n'est pas un chiffre", mention_author=True)
                await message.reply("1er dé: "+random.randrange(1,int(chiffres[0]),1)+", 2eme dé: "+random.randrange(1,int(chiffres[1]),1), mention_author=True)
            else:
                await message.reply("1er dé: "+random.randrange(1,int(chiffre),1)+", 2eme dé: "+random.randrange(1,int(chiffre),1), mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTAxMjI5MjI0NzYzNjY4NDgyMA.GeE3F_.KRa9UdareJVjM1QOhY38Bl0UF9hW5-wCE2BHJs')