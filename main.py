import opensea
import discord
import config
import time
from discord.ext import commands

client = commands.Bot(command_prefix = '?')
api = opensea.OpenseaAPI(apikey=config.keys['OPENSEA_API_KEY'])

@client.event
async def on_ready():
    print("Online")

@client.command()
async def nfts(ctx, wallet):
    result = api.assets(owner=wallet, export_file_name="asset.json")
    embed = discord.Embed(
        title="{}'s NFTs".format(ctx.author.display_name),
        url="https://opensea.io/{}".format(wallet),
        description="Here is a list of your NFTs!",
        color=discord.Color.blue())
    
    for i in result['assets']:
        try:
            collection = api.collection(collection_slug=i['collection']['slug'])['collection']
            embed.add_field(name=i['name'], value="Collection Floor Price: {} ETH".format(collection['stats']['floor_price']))
        except:
            embed.add_field(name='No Name Found', value="Collection Floor Price: {} ETH".format(collection['stats']['floor_price']))

    await ctx.send(embed=embed)
 
@client.command()
async def combinedfloor(ctx, wallet):
    result = api.assets(owner=wallet)
    
    fp = 0
    for i in result['assets']:
        time.sleep(.5)
        collection = api.collection(collection_slug=i['collection']['slug'])['collection']
        try:
            fp += collection['stats']['floor_price']
        except:
            fp += 0

    embed = discord.Embed(
    title="Combined Floor Price of {}'s NFTs".format(ctx.author.display_name),
    url="https://opensea.io/{}".format(wallet),
    description="Combined Floor Price: {} ETH".format(round(fp, 4)),
    color=discord.Color.blue())

    await ctx.send(embed=embed)

client.run(config.keys['DISCORD_BOT_KEY'])