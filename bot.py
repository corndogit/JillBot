import os
import libs.weather

from libs.doc.weathercodes import weathercodes, decode_uv_index
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
jillbot = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned,
    sync_commands_debug=True
)


@jillbot.event
async def on_ready():
    print(f"{jillbot.user} is now online!")


@jillbot.slash_command(description="Responds with 'Hello there!'")
async def hello(inter):
    await inter.response.send_message("Hello there!")


@jillbot.slash_command(description="Displays an embed with bot information")
async def about(inter):
    about_me = disnake.Embed(
        title="About",
        url="https://github.com/corndogit",
        description="JillBot is an open-source Discord bot written in Python by corndog#2974"
    )
    about_me.set_thumbnail(url="https://avatars.githubusercontent.com/u/101812777?v=4")
    about_me.add_field(name="Prefix", value="!")
    about_me.add_field(name="Commands", value="`hello`, `about`, `weather <location>`, `4panel`", inline=False)
    await inter.response.send_message(embed=about_me)


@jillbot.slash_command(
    description="Does a trick with images uploaded to cdn.discordapp.com that makes them display 4 times")
async def funny(inter, link: str):
    if not link.startswith("https://"):
        await inter.response.send_message("Invalid image link - must start with https://")
    else:
        link_content = link.split('https://')[1]
        await inter.response.send_message(f"https://{link_content}\n" +
                                          f"https://\\{link_content}\n" +
                                          f"https://\\\\{link_content}\n" +
                                          f"https://\\\\\\{link_content}\n")


@jillbot.slash_command(description="Displays a small weather report for the city provided.")
async def weather(inter, city: str):
    # await inter.response.send_message(f"Getting weather for {city}...")

    weather_data = libs.weather.get_weather(city)

    if weather_data == "API_Error":
        await inter.response.send_message("API error - your request produced no suggestions.")

    else:
        embed = disnake.Embed(title=f"Showing results for {weather_data['City']}, {weather_data['Country']}",
                              url="https://github.com/corndogit/weather-cli/")
        embed.add_field(name="Type",
                        value=weathercodes[str(weather_data['SignificantWeatherCode'])],
                        inline=False)
        embed.set_thumbnail(url="https://corndog.s-ul.eu/OZbm1tH1.jpg")
        embed.add_field(name="Max Temperature",
                        value=f"{round(weather_data['MaxTemperature'])}\u00B0C",
                        inline=True)
        embed.add_field(name="Min Temperature",
                        value=f"{round(weather_data['MinTemperature'])}\u00B0C",
                        inline=True)
        embed.add_field(name="Chance of Precipitation",
                        value=f"{weather_data['ChanceOfPrecipitation']}%",
                        inline=True)
        embed.add_field(name="Wind Speed",
                        value=f"{round(float(weather_data['WindSpeed'] / 0.44704), 1)} mph",
                        inline=True)
        embed.add_field(name="Max UV Index Rating",
                        value=f"{weather_data['MaxUvIndex']} ({decode_uv_index(weather_data['MaxUvIndex'])})",
                        inline=True)
        embed.set_footer(text="Data collected from Met Office Weather DataHub")
        await inter.response.send_message(embed=embed)


jillbot.run(TOKEN)
