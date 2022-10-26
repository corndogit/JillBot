import os
import libs.weather

from libs.doc.weathercodes import weathercodes, decode_uv_index
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("{0.user} is now online!".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Hello World
    if message.content.startswith('!hello'):
        await message.reply('Hello there!')

    # About
    if message.content.startswith('!about'):
        about_me = discord.Embed(
            title="About",
            url="https://github.com/corndogit",
            description="JillBot is an open-source Discord bot written in Python by corndog#2974"
        )
        about_me.set_thumbnail(url="https://avatars.githubusercontent.com/u/101812777?v=4")
        about_me.add_field(name="Prefix", value="!")
        about_me.add_field(name="Commands", value="`hello`, `about`, `weather <location>`, `4panel`", inline=False)
        await message.channel.send(embed=about_me)

    # Video link fixer
    if message.content.startswith('https://media.discordapp.net') and message.content.endswith('.mp4'):
        new_link = message.content.replace("https://media.discordapp.net", "https://cdn.discordapp.com")
        await message.reply(f"Fixed your media link: {new_link}")

    # Uses Discord exploit to make a 4 panel thing from Discord image links
    if message.content.startswith('!4panel'):
        link = message.content.split('!4panel ')[1]
        if not link.startswith('https://'):
            await message.channel.send('Invalid image link - must start with https://')
        else:
            link_content = link.split('https://')[1]
            await message.channel.send(f'https://{link_content}\n' +
                                       f'https://\\{link_content}\n' +
                                       f'https://\\\\{link_content}\n' +
                                       f'https://\\\\\\{link_content}\n')

    # weather-cli implementation
    if message.content.startswith('!weather'):
        command = message.content.split(' ')
        command.remove('!weather')
        location = ' '.join(command)
        await message.channel.send(f"Getting weather for {location}...")

        weather_data = libs.weather.get_weather(location)

        if weather_data == "API_Error":
            await message.channel.send("API error - your request produced no suggestions.")

        else:
            embed = discord.Embed(title=f"Showing results for {weather_data['City']}, {weather_data['Country']}", url="https://github.com/corndogit/weather-cli/")
            embed.add_field(name="Type", value=weathercodes[str(weather_data['SignificantWeatherCode'])], inline=False)
            embed.set_thumbnail(url="https://corndog.s-ul.eu/OZbm1tH1.jpg")
            embed.add_field(name="Max Temperature", value=f"{round(weather_data['MaxTemperature'])}\u00B0C", inline=True)
            embed.add_field(name="Min Temperature", value=f"{round(weather_data['MinTemperature'])}\u00B0C", inline=True)
            embed.add_field(name="Chance of Precipitation", value=f"{weather_data['ChanceOfPrecipitation']}%", inline=True)
            embed.add_field(name="Wind Speed", value=f"{round(float(weather_data['WindSpeed'] / 0.44704), 1)} mph", inline=True)
            embed.add_field(name="Max UV Index Rating", value=f"{weather_data['MaxUvIndex']} ({decode_uv_index(weather_data['MaxUvIndex'])})", inline=True)
            embed.set_footer(text="Data collected from Met Office Weather DataHub")
            await message.channel.send(embed=embed)


client.run(TOKEN)
