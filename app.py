# discord bot for updating stock information of eorange
from discord.ext import commands
# from discord.ext.commands import command
import asyncio
import os
import dotenv
from datetime import datetime


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.print_log('entered commands.Cog class - commands.Cog class')
        self.bot = bot

    @commands.command(name='p')
    async def cmd_ping(self, ctx):
        self.print_log('send - "ping successful"')
        await ctx.send('ping successful')

    @commands.Cog.listener()
    async def on_ready(self):
        print("MyCog is ready - Cog.on_ready()")

    def process_url(self, msg):
        print(msg)

    @commands.Cog.listener()
    async def on_message(self, msg):
        self.print_log('responding to message - commands.Cog.on_message()')
        self.process_url(msg.content)
        # the function below is not necessary in the Cog class. but it is needed in the Bot class.
        # Cog class automatically invokes the command, where Bot class doesn't
        # await self.bot.process_commands(msg)

        
    def send_log_async(self, msg, channel):
        asyncio.run_coroutine_threadsafe(self.send_log(msg, channel), asyncio.get_event_loop())
        # self.send_log(msg, channel)

    def send_log_async2(self, msg, channel, evt_loop): # for threads
        asyncio.run_coroutine_threadsafe(self.send_log(msg, channel), evt_loop)

    async def send_log(self, msg, channel):
        print(msg, datetime.now().isoformat(), '\n\n')
        await channel.send(msg)

    def print_log(self, msg):
        print(msg)

    def bot_log(self, msg, channel):
        # await channel.send('Test') # We can't do this because of the above comment
        self.send_log(msg, channel)
        # asyncio.run_coroutine_threadsafe(self.send_log(msg, channel), self.evt_loop)


class DiscordBot(commands.Bot):
    def __init__(self):
        self.print_log('entered bot class - commands.Bot.__init__()')
        command_prefix = '..'
        super().__init__(command_prefix=command_prefix)

        self.dict_channels = {}

        # necessary IDs
        self.CH_ID_web_clipper = int(os.environ['CHANNEL_ID_WEB_CLIPPER']) # 92931949111083418601 test
        self.GUILD_ID = int(os.environ['GUILD_ID']) # 82820083936971981901 test
     
    def run(self):
        DISCORD_TOKEN = os.environ['DISCORD_TOKEN'] # OTI5MzE3MzkyODg1MDk2NDc4.YdlkRA.OqmQYp9bSBN7N5skYeF5PzxwIHw01

        self.print_log('running bot - commands.Bot.run()')
        super().run(DISCORD_TOKEN, reconnect=True)

    async def on_connect(self):
        self.print_log('bot connected - commands.Bot.on_connect()')

    async def on_disconnect(self):
        self.print_log('bot disconnected - commands.Bot.on_disconnect()')

    # @self.event
    async def on_ready(self):
        self.dict_channels = dict(
            web_clipper = self.get_channel(self.CH_ID_web_clipper),
            )

        self.kwargs = dict(
            guild=self.get_guild(self.GUILD_ID)
            )
        self.print_log('bot is ready - commands.Bot.on_ready()')
        self.print_log(f'Guild Name: {self.kwargs["guild"]}')
        self.print_log(f'Channel Name: {self.dict_channels["web_clipper"]}')

    def print_log(self, msg):
        print(msg)

def main():
    dotenv.load_dotenv()
    dbot = DiscordBot()
    dbot.add_cog(MyCog(dbot))
    dbot.run()
    

if __name__ == "__main__":
    main()


### useful links
# concept of sending discord message from background task >> https://stackoverflow.com/a/64370097
# concept of using await object out of async funtion >> https://stackoverflow.com/a/53726266
# concept of killing threads gracefully >> https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread
# concept of sorting dictionary >> https://towardsdatascience.com/sorting-a-dictionary-in-python-4280451e1637
# concept of using threadpool executor >> https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3