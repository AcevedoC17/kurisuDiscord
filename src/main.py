# the os module helps us access environment variables
# i.e., our API keys
import os, platform
try:
    import nacl
except ImportError:
    try:
      if platform.system().lower().startswith('win'):
        os.system("pip install pynacl")
      else:
        os.system("pip3 install pynacl")
    except Exception as e:
      print("Error:", e)
      exit()

# these modules are for querying the Hugging Face model
import json
import requests

# the Discord Python API
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_search import YoutubeSearch
import asyncio
from yt_dlp import YoutubeDL
from threading import Thread


# this is my Hugging Face profile link
API_URL = 'https://api-inference.huggingface.co/models/BlightZz/'
loop = False

class MyClient(commands.Bot):



    





    def __init__(self, model_name, command_prefix):
        super().__init__(command_prefix = "$", intents=intents)
        self.queue = []
        self.queuedict = {}
        self.loopdict = {}
        self.dataFromClient = ""
        self.Carlos = None
        self.Diego = None
        
        with open("servers.json", "r") as json_file:
          self.queuedict = json.load(json_file)
        self.playlistdict = {}
        with open("playlists.json", "r") as json_file:
          self.playlistdict = json.load(json_file)
        self.api_endpoint = API_URL + model_name
        # retrieve the secret API token from the system environment
        huggingface_token = os.environ['HUGGINGFACE_TOKEN']
        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }


#---------------------------- BUTTONS / INTERFACE --------------------------------






#----------------------------- HELLO ---------------------------------------------
        @self.command(name="Hello")
        async def Hello(ctx):
          view = discord.ui.View() # Establish an instance of the discord.ui.View class
          style = discord.ButtonStyle.green  # The button will be gray in color
          item = discord.ui.Button(style=style, label="Read the docs!", custom_id="skip") 
          #item.callback(interaction=self.invoke(self.get_command("play"), url="blue lobster meme")) # Create an item to pass into the view class.
          view.add_item(item=item)  # Add that item into the view class
          await ctx.send("This message has buttons!", view=view)  # Send your message with a button.

          
          
        





#--------------------------------- JOIN ------------------------------------------
        @self.command(name="join")
        async def join(ctx):
          channel = ctx.message.author.voice.channel
          voice = get(self.voice_clients, guild=ctx.guild)
          if voice and voice.is_connected():
            await voice.move_to(channel)
          else:
            voice = await channel.connect()










#-------------------------------- PLAY --------------------------------------------
        @self.command(name="play")
        async def play(ctx,*, url):
              print(url)
              if 'porn' in url:
                await ctx.send("I'm not playing that.")
                return
              if 'hentai' in url:
                await ctx.send("I'm not playing that.")
                return
              print("play called")
              await ctx.invoke(self.get_command("join"))
              message = await ctx.send('Working on it...')
              FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'} #youtube_dl options
              YDL_OPTIONS = {'format': 'bestaudio/best', 'extractaudio': True, 'audioformat': 'mp3', 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
              'restrictfilenames': True, 'noplaylist': True, 'nocheckcertificate': True, 'ignoreerrors': False, 'logtostderr': False, 'quiet': True,
              'no_warnings': True, 'default_search': 'auto', 'source_address': '0.0.0.0'}
              voice = get(self.voice_clients, guild=ctx.guild)




              #Youtube stuff
              if not voice.is_playing():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                  if url.startswith("https"):
                    URL = url
                    results = YoutubeSearch(url, max_results=1).to_dict()
                    info = ydl.extract_info(URL, download=False)
                    URL = info['url']
                    url2 = info['id']
                  else:
                    results = YoutubeSearch(url, max_results=1).to_dict()
                    #print(str(results))
                    url2 = results[0]['id']
                    #print(url2)
                    info = ydl.extract_info(url2, download=False)
                    #print(info)
                    URL = info['url']
                    #print(URL)
                  voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS, ), after= lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx, url), self.loop).result())
            
                  view = discord.ui.View() # Establish an instance of the discord.ui.View class
                  styleSkip = discord.ButtonStyle.green  # The button will be gray in color
                  itemSkip = discord.ui.Button(style=styleSkip, label="Skip", custom_id="skip") 
                  stylePause = discord.ButtonStyle.red
                  itemPause = discord.ui.Button(style=stylePause, label="Pause", custom_id="Pause")
                  styleDisplay = discord.ButtonStyle.blurple
                  itemDisplay = discord.ui.Button(style=styleDisplay, label="Queue", custom_id="Display")
                  styleRepeat = discord.ButtonStyle.gray
                  itemRepeat = discord.ui.Button(style=styleRepeat, label="Loop", custom_id = "Repeat")
                  view.add_item(item=itemSkip) 
                  view.add_item(item=itemPause)
                  view.add_item(item=itemDisplay)
                  view.add_item(item=itemRepeat)
                   # Add that item into the view class
                          #Auxiliary Message Handling
                  voice.is_playing()
                if not url.startswith("https:"):
                  await message.edit(content = 'Enjoy your music! (Looping: **'+ str(self.loopdict[ctx.guild.id]) + '**)' + '\n ' + 'https://www.youtube.com/watch?v='+url2, view=view)
                else:
                  await message.edit(content = 'Enjoy your music! (Looping:** '+ str(self.loopdict[ctx.guild.id]) + '**)' + '\n'+ url,view=view)
                  emoji = discord.utils.get(ctx.guild.emojis, name = 'KurisuThumbsUp')
                  emoji2 = discord.utils.get(ctx.guild.emojis, name = 'KurisuHeart')
                  await message.add_reaction(emoji)
                  await message.add_reaction(emoji2)
              else:
                try:
                  self.queuedict[ctx.guild.id].append(url)
                except:
                  self.queuedict[ctx.guild.id] = [url]
                await ctx.message.delete()
                await ctx.send("I added your song to the queue.")



              while voice.is_playing():
                    print("Entered initial while check ") #Checks if voice is playing
                    await asyncio.sleep(1) #While it's playing it sleeps for 1 second
              else:
                    print("Entered else")
                    await asyncio.sleep(60) #If it's not playing it waits 60 seconds
                    while voice.is_playing(): #and checks once again if the bot is not playing
                        break #if it's playing it breaks
                    else:
                        await ctx.send("If you've got nothing to play, I'll leave.")
                        await ctx.message.guild.voice_client.disconnect()


                




















#--------------------------------- RESUME ---------------------------------------------
        @self.command(name="resume")
        async def resume(ctx):
                  voice = get(self.voice_clients, guild=ctx.guild)
                  if not voice.is_playing():
                    voice.resume()
                    await ctx.send('Resuming.')
            # check if the bot is already playing
                  else:
                    await ctx.send("Resume what? The music is already playing.")
                    return















#-------------------------------------- STOP -------------------------------------------
        @self.command(name="stop")
        async def stop(ctx):
              voice = get(self.voice_clients, guild=ctx.guild)
              self.queue.clear()
              if voice.is_playing():
                voice.stop()
                await ctx.send('Stopped.')
              else:
                await ctx.send("Stop what? Seriously, pay attention. There's nothing playing.")


















#-------------------------------- PAUSE ---------------------------------------------------
        @self.command(name="pause")
        async def pause(ctx):
              voice = get(self.voice_clients, guild=ctx.guild)
              if voice.is_playing():
                voice.pause()
                await ctx.send('Paused.')
              else:
                if not self.queuedict[ctx.guild.id]:
                  await ctx.invoke(self.get_command("resume"))
                  return
                await ctx.send("Pay attention, there's nothing playing.")










#----------------------------------- HENTAI -----------------------------------------------
        @self.command(name="hentai")
        async def hentai(ctx):
              await ctx.channel.send(file=discord.File('Horny.gif'))


#------------------------------- COMMANDLIST --------------------------------------------
        @self.command(name="commandlist")
        async def commandlist(ctx):
          await ctx.channel.send('Hey! These are the commands available right now:\n $join\n$play\n$resume\n$pause\n$stop\n$hentai\n\nYou can also @ me if you want to chat!')











#--------------------------------- SKIP -------------------------------------------------
        @self.command(name="skip")
        async def skip(ctx):
              if len(self.queuedict[ctx.guild.id]) >= 1:
                print("skip if success.")
                voice = get(self.voice_clients, guild=ctx.guild)
                if voice.is_playing():
                  voice.stop()
                  await ctx.send("Skipping.")
                else:
                  ctx.send("What do you want me to skip? There's nothing playing.")
              else:
                voice = get(self.voice_clients, guild=ctx.guild)
                voice.stop()
                await ctx.send("The queue is empty now.")












#---------------------------------- LEAVE -----------------------------------------------
        @self.command(name="leave")
        async def leave(ctx):
          self.queuedict[ctx.guild.id].clear()
          await ctx.message.guild.voice_client.disconnect()
          await ctx.send("See you later.")




















#------------------------------------ DISPLAY -----------------------------------------
        @self.command(name="display")
        async def display(ctx):
          count = 1
          temp = "```These are the songs currently in the queue:\n"
          for s in self.queuedict[ctx.guild.id]:
            temp = temp + str(count) + ". " + s + "\n"
            count = count + 1
          temp = temp + "```"
          await ctx.send(temp)













#-----------------------------------------REPEAT ---------------------------------------
        @self.command(name="repeat")
        async def repeat(ctx):
          self.loopdict[ctx.guild.id] = not self.loopdict[ctx.guild.id]
          if self.loopdict[ctx.guild.id]:
            await ctx.send("I'll loop the song.")
          else:
            await ctx.send("I'll stop looping the song")






















#------------------------------------------MAKEPLAYLIST ----------------------------------
        @self.command(name="makePlaylist")
        async def makePlaylist(ctx, *, content):
          self.playlistdict[content] = []
    














#-----------------------------------------ADDTOPLAYLIST--------------------------------------
        @self.command(name="addtoPlaylist")
        async def addtoPlaylist(ctx, *, content):
          targetPlaylist = content[0:content.find(',')]
          song = content[content.find(',')+2: len(content)]
          self.playlistdict[targetPlaylist].append(song)
          with open("playlists.json", "w") as outfile:
            json.dump(self.playlistdict, outfile)
          message = "Added " + "*" + song + "*" " to playlist " + "*" + targetPlaylist + "*"
          await ctx.send(message)















#-------------------------------------SHOW PLAYLISTS --------------------------------------
        @self.command(name="showPlaylists")
        async def showPlaylists(ctx):
          temp = "```These are the currently available playlists and their content.\n"
          count = 1
          for key, value in self.playlistdict.items():
            temp = temp + key + ":" + "\n"
            count = 1
            for s in value:
              temp = temp + str(count) + ". " + s + "\n"
              count = count + 1
          temp  = temp + "```"
          await ctx.send(temp)


























#--------------------------------- PLAYLIST --------------------------------------------
        @self.command(name="playlist")
        async def playlist(ctx, *, content):
            for s in self.playlistdict[content]:
              try:
                self.queuedict[ctx.guild.id].append(s)
              except:
                self.queuedict[ctx.guild.id] = [s]
            #await self.play(ctx, url = self.queuedict[ctx.guild.id].pop(0))
            await ctx.invoke(self.get_command("play"), url=self.queuedict[ctx.guild.id].pop(0))



























#---------------------------------- DEVDISPLAY -----------------------------------------
        @self.command(name="devDisplay")
        async def devDisplay(ctx):
            await ctx.send(self.playlistdict)





















#------------------------------ DELETE FROM PLAYLIST --------------------------------------
        @self.command(name="deleteFromPlaylist")
        async def deleteFromPlaylist(ctx, *, content):
          targetPlaylist = content[0:content.find(',')]
          song = content[content.find(',')+2: len(content)]
          self.playlistdict[targetPlaylist].remove(song)
          with open("playlists.json", "w") as outfile:
            json.dump(self.playlistdict, outfile)
          message = "Removed " + "*" + song + "*" " from playlist " + "*" + targetPlaylist + "*"
          await ctx.send(message)
#--------------------------------------- END OF COMMANDS ------------------------------------
        @self.event
        async def on_interaction(interaction):
              print("this works")
              print(interaction.data)
              await interaction.response.defer()
              ctx = await self.get_context(interaction.channel.last_message)
              if interaction.data['custom_id'] == "skip":
                await ctx.invoke(self.get_command("skip"))
              if interaction.data['custom_id'] == "Pause":
                await ctx.invoke(self.get_command("pause"))
              if interaction.data['custom_id'] == "Display":
                await ctx.invoke(self.get_command("display"))
              if interaction.data['custom_id'] == "Repeat":
                await ctx.invoke(self.get_command("repeat"))
              

#----------------------------------------------------------------------------------------------------


    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret
    















    
    
    
  


















    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print("Kurisu is in", len(self.guilds), "servers")
        await self.change_presence(activity=discord.Game(name="$play URL, or @ me to chat!"))
        self.sendDMs.start()
                              
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        self.query({'inputs': {'text': 'Hello!'}})
        self.NCASChannel = self.get_channel(958715860049076296)
        for guild in self.guilds:
          if(guild.id == 958714492269785108):
            self.NCASServer = guild
          self.queuedict[guild.id] = []
          self.loopdict[guild.id] = False
          print(guild.id)
          print("added to dict")
        with open("servers.json", "w") as outfile:
          json.dump(self.queuedict, outfile)
          print("Saved server list as json.")
        
        
    








 






























    



    async def on_message(self, message):
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
           return
         # ignore if not @
        if "fuck" in message.content:
          emoji = discord.utils.get(message.guild.emojis, name = 'KurisuPout') 
          await message.add_reaction(emoji)
        if "vamo" in message.content:
          emoji = discord.utils.get(message.guild.emojis, name = 'OKabe')
          await message.add_reaction(emoji)
        if "kurisu" in message.content:
          emoji = discord.utils.get(message.guild.emojis, name = 'KurisuCute')
          await message.add_reaction(emoji)
        if "sus" in message.content:
          emoji = discord.utils.get(message.guild.emojis, name = 'Amadeus')
          await message.add_reaction(emoji)
        if "ostia" in message.content:
          emoji = discord.utils.get(message.guild.emojis, name = 'ostia')
          await message.add_reaction(emoji)
        if not self.user.mentioned_in(message):
          await self.process_commands(message)
          return
        
        # form query payload with the content of the message
        payload = {'inputs': {'text': message.content}}

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)
        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'No use talking anymore.'

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)





 
            
            









              
      
       
         
          
    
      
    








      
    












#---------------------------Play function----------------------------------
    












    async def play_next(self, ctx, url):
      if self.loopdict[ctx.guild.id]:      
          #await self.play(ctx = ctx, url = url)
          await ctx.invoke(self.get_command("play"), url=url)
      print("play_next called")
      if len(self.queuedict[ctx.guild.id]) >= 1:
        print("play_next if success.")
        #await self.play(ctx = ctx, url = self.queuedict[ctx.guild.id].pop(0))
        await ctx.invoke(self.get_command("play"), url=self.queuedict[ctx.guild.id].pop(0))
      else:
        print("play_next else fulfilled")
        return




        
    


########################################  SERVER  ##################################
    @tasks.loop(seconds=10)
    async def sendDMs(self):
          print("Got loop")
              
            
            
      


      
         












  
    
  

  

if __name__ == '__main__':
    #DialoGPT-medium-Kurisu is my model name
  intents = discord.Intents.all()
  intents.all()
  intents.members = True
  client = MyClient('DialoGPT-medium-Kurisu', commands.Bot(command_prefix="$",     intents=intents))
  print("running client")
  client.run(os.environ['DISCORD_TOKEN'])
  my_secret = os.environ['DISCORD_TOKEN']
