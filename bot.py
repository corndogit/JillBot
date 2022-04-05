import os
import libs.weather

from libs.doc.weathercodes import weathercodes, decode_uv_index
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print("{0.user} is now online!".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.reply('Hello there!')

    if message.content.startswith('!about'):
        about_me = discord.Embed(
            title="About",
            url="https://github.com/corndogit",
            description="JillBot is an open-source Discord bot written in Python by corndog#2974"
        )
        about_me.set_thumbnail(url="https://avatars.githubusercontent.com/u/101812777?v=4")
        about_me.add_field(name="Prefix", value="!")
        about_me.add_field(name="Commands", value="`hello`, `about`", inline=False)
        await message.channel.send(embed=about_me)

    if message.content.startswith('!weather'):
        location = str(message).split().pop(0).join(' ')
        weather_data = libs.weather.get_weather(location)

        if weather_data == "API_Error":
            await message.channel.send("API error - your request produced no suggestions.")

        else:
            embed = discord.Embed(title="Showing results for {location}", url="https://github.com/corndogit/weather-cli/")
            embed.add_field(name="Type", value=weathercodes[str(weather_data['SignificantWeatherCode'])], inline=False)
            embed.add_field(name="Max Temperature", value=f"{round(weather_data['MaxTemperature'])} degrees Celsius", inline=True)
            embed.add_field(name="Min Temperature", value=f"{round(weather_data['MinTemperature'])} degrees Celsius", inline=True)
            embed.add_field(name="Chance of Precipitation", value=f"{weather_data['ChanceOfPrecipitation']}%", inline=True)
            embed.add_field(name="Wind Speed", value=f"{round(float(weather_data['WindSpeed'] / 0.44704), 1)} mph", inline=True)
            embed.add_field(name="Max UV Index Rating", value=f"{weather_data['MaxUvIndex']} ({decode_uv_index(weather_data['MaxUvIndex'])})", inline=True)
            embed.set_footer(text="Data collected from Met Office Weather DataHub")
            await message.channel.send(embed=embed)


client.run(TOKEN)
