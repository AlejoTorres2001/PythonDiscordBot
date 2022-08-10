import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f'ytsearch:{item}', download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def  play_next(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            # primera url
            m_url = self.music_queue[0][0]['source']

            # sacar el elemento que estoy por reproducir
            music=self.music_queue.pop(0)
            embed=discord.Embed(title="Reproduciendo", description=music[0]['title'], color=0x00ff00)
            asyncio.run_coroutine_threadsafe(ctx.send(embed=embed),self.bot.loop)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx=ctx))
            #funcion anonima a after,cuando se acaba la musica vuelve a reproducir
        else:
            self.is_playing = False

    async def play_music(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # intento de conexion al voice channel
            if self.vc == "" or not self.vc.is_connected() or self.vc is None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            # elimina el primer elemento de la cola
            music=self.music_queue.pop(0)
            embed = discord.Embed(title="Reproduciendo", description=music[0]['title'], color=0x00ff00)
            await ctx.send(embed=embed)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx=ctx))
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)  # convertir args en string
        voice_channel = ctx.message.author.voice.channel if ctx.message.author.voice else None
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):  # Para el return False
                await ctx.send(
                    "Could not download the song. Incorrect format try another keyword. This could be due to playlist "
                    "or a livestream format.")
            else:
                embed =discord.Embed(
                  title= "Siguiente cancion en cola 🎵",
                  description = song['title']
                  )
                if(self.is_playing):
                  await ctx.send(embed=embed)
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
                    await self.play_music(ctx=ctx)
    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f'{i+1}. '+ self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            embed = discord.Embed(
            title= "Cola de canciones 🎵",
            description = retval)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
            title= "No hay canciones en la Cola🎵",
            description = retval)
            await ctx.send(embed=embed)
            
    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc.is_connected():
            self.vc.stop()
            self.is_playing = False
            await self.play_music(ctx=ctx)

    @commands.command(name='stop', help='frena la musica y se retira el bot')
    async def stop(self,ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @commands.command(name='pause', help='pausa la musica')
    async def pause(self,ctx):
        voice = ctx.message.guild.voice_client
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Ya esta pausado")

    @commands.command(name='resume', help='reanuda la musica')
    async def resume(self,ctx):
        voice = ctx.message.guild.voice_client
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Ya esta sonando!")


def setup(bot):
    bot.add_cog(Music(bot))