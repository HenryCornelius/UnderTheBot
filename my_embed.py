import discord

def create_help_embed():
    embed = discord.Embed(title='**COMMANDS**',
                        description='', colour=discord.Colour.green())
    embed.add_field(name='`!1d<chiffre>`',
                    value='Lance un dé. Exemple: `!1d6`',
                    inline=False)
    embed.add_field(name='`!2d<chiffre> [<chiffre>]`',
                    value='Lance deux dés. Exemples: `!2d6` - `!2d6 8`',
                    inline=False)
    embed.add_field(name='`!randomChamp`',
                    value='Selectionne un champion de manière aléatoire sur son rôle principal.',
                    inline=False)
    embed.add_field(name='`!checkRank <summoner name> [<type ranked>]`',
                    value='Vérifie le rang du pseudo entré. Exemples: `!checkRank Tobia` - `!checkRank Tobia TFT`',
                    inline=False)
    return embed

    
def create_mates_embed1(matesArray, live_title, desc):
    embed1 = discord.Embed(title=live_title,
                        description=desc, colour=discord.Colour.blue())
    for i in range(5):
        embed1.add_field(name=matesArray[i].titleleft,
                    value=matesArray[i].descleft,
                    inline=True)
        embed1.add_field(name=matesArray[i].titlemid,
                    value=matesArray[i].descmid,
                    inline=True)
        embed1.add_field(name=matesArray[i].titleright,
	    		    value=matesArray[i].descright,
	    		    inline= True)
    return embed1
def create_mates_embed2(matesArray, live_title, desc):
    embed2 = discord.Embed(title=live_title,
                        description=desc, colour=discord.Colour.red())
    
    for i in range(5):
        embed2.add_field(name=matesArray[i+5].titleleft,
                    value=matesArray[i+5].descleft,
                    inline=True)
        embed2.add_field(name=matesArray[i+5].titlemid,
                    value=matesArray[i+5].descmid,
                    inline=True)
        embed2.add_field(name=matesArray[i+5].titleright,
	    		    value=matesArray[i+5].descright,
	    		    inline= True)
    return embed2