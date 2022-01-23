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

    listComplete = False
    offset = 0
    floorPrice = 0
    while listComplete == False:
        result = api.assets(owner=wallet, offset=offset)
        collectionList = {}

        for i in result['assets']:
            if i['collection']['slug'] in collectionList:
                floorPrice += collectionList[i['collection']['slug']]
            else:
                time.sleep(.5)     
                collection = api.collection(collection_slug=i['collection']['slug'])['collection']
                try:
                    floorPrice += collection['stats']['floor_price']
                    collectionList[i['collection']['slug']] = collection['stats']['floor_price']
                except:
                    floorPrice += 0
                    collectionList[i['collection']['slug']] = 0

        if len(result['assets']) < 50:
            listComplete = True
        else:
            offset += 50

    embed = discord.Embed(
    title="Combined Floor Price of {}'s NFTs".format(ctx.author.display_name),
    url="https://opensea.io/{}".format(wallet),
    description="Combined Floor Price: {} ETH".format(round(floorPrice, 4)),
    color=discord.Color.blue())

    await ctx.send(embed=embed)

client.run(config.keys['DISCORD_BOT_KEY'])