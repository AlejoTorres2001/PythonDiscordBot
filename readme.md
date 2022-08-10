## Bots de Discord

**Codigo y explicacion paso a paso para crear tu bot de Discord**

En primer lugar debemos crear nuestro entorno virtual
  
  ```bash
  pipenv shell 
  ```
yo utilice la version de python 3.10.4 especificandola en el comando mediante la flag 

```bash
--python 3.10.4
```

vamos a crear la carpeta src dentro de nuestra carpeta del proyecto
aqui es donde crearemos todos los archivos de codigo fuente
  
  ```bash
  mkdir src
  ```

Necesitamos establecer nuestra app de discord desde el aaprtadod e desarrolladores de la pagina para obtener las calves de acceso a su API web

(https://discordapp.com/developers)


1- Vamos a crear una nueva aplicacion

2- Crear un bot dentro de esa aplicacion

3- Luego darle los permisos que nosotros consideremos necesarios a ese bot

4- Generamos una url para invitar a nuestro bot al servidor

5- copiamos el token secreto de nuestro bot

**Volvamos a VSCode**

Instalemos el paquete de discord.py
  ```bash
 pipenv install discord.py
   ```

Creamos el archivo main.py dentro de src

y dentro de main.py escribimos lo siguiente

```python
from discord.ext.commands import Bot


bot = Bot(command_prefix='!')
bot.run()
```

Esta es la manera mas simple de crear un bot e indicarle el prefijo para sus comandos, en este caso !
Tratemos de correr el programa

**Ups!** Tenemos un error, Que esta pasando?


Necesitamos el Token para poder acceder a la API de discord

Para ello vamos a crear un archivo **.env** el cual alamcenara el TOKEN y demas variables de entorno

**las variables de entorno son secretas en muchos casos por lo que es recomendable agregar el archivo .env a la lista de archivos ignorados de git**

  Vamos a instalar una dependencia que nos ayude con eso

  ```bash
    pipenv install python-dotenv
  ```

Realizamos las siguientes modifcaciones en **main.py**
  
  ```python 
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())
bot = Bot(command_prefix='!')
bot.run(os.getenv('DISCORD_API_TOKEN'))
  ```

Ahora vamos a interactuar con el bot mediante el comando *!help* Desde Discord


## Primeras funcionalidades

vamos a relalizar los sigueintes cambios en nuestro archivo main
  
  ```python
  from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())
bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    
bot.run(os.getenv('DISCORD_API_TOKEN'))
  ```
**Y que es todo esto!?**

lo que acabamos de hacer puede explicarse de la siguiente manera:

vamos a indicar que nuestro bot debe escuchar los comandos que definamos a continuacion
 **La logica de nuestros comandos se define en funciones indicadas con el decorador bot.command()**

 Pero estas funciones tiene algo distinto la palabra reservada *async*

 El asincronismo es una funcionalidad que nos permite escribir codigo **NO-BLOQUEANTE** 

nuestros comandos deben ser escritos en una funcion que se llame como el comando que se quiere ejecutar, luego veremos que tambien pueden tener alias asociados

Es importante pasar como primer argumento a nuestro comando el **contexto** de la invocacion del comando

*ctx*  Es un objeto de contexto que se pasa al comando, contiene datos como desde que canal se ejecuto, en que mensaje y quien lo ejecuto

## Emojis
  Discord interpreta emojis mediante la sintaxis :emoji:, donde emoji se reemplaza con una palabra que lo describa

  **Ejemplo:**
  
  ```python
  from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())
bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! :grin:')
    
bot.run(os.getenv('DISCORD_API_TOKEN'))
  ``` 

## El objeto contexto

  El objeto contexto contiene informacion como el canal donde se ejecuto el comando, el mensaje que se ejecuto, quien lo ejecuto, etc

  **Ejemplo:**
  
  ```python
  from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())
bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
  user=ctx.message.author.name
  await ctx.send(f'Hello {user}! :grin:')
    
bot.run(os.getenv('DISCORD_API_TOKEN'))
  ```

  Ahora nuestro bot puede enviar mensajes personalizados a cada usuario que lo invoca


## Embed

los embed son mensajes de Discord que tiene la capacidad de procesar recursos de forma mas compleja como imagenes, videos, etc

  **Ejemplo:**
  
  ```python
  from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv

import discord

load_dotenv(find_dotenv())
bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
  user=ctx.message.author.name
  embed=discord.Embed(title="Hello",description=f"Hello {user}",color=0x00ff00)
  await ctx.send(embed=embed)
    
bot.run(os.getenv('DISCORD_API_TOKEN'))
  ```
## Cogs
 La API de discord nos permite utilizar una forma de modularizacion llamada cogs, de no hacerlo nuestro codigo puede convertirse en *codigo spaghetti* rapidamente
 Vamos a refactorizar nuestro codigo para que sea mas legible y no tenga muchas lineas de codigo en el archivo principal


  Dentro de **src** creamos la carpeta **cogs**

  Dentro de cogs creamos un archivo **Hellp.py**
  **Ejemplo:**
  
  ```python
  import discord
from discord.ext import commands

class Hello(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def hello(self,ctx):
      user=ctx.message.author.name
      embed=discord.Embed(title="Hello",description=f"Hello {user}",color=0x00ff00)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Hello(bot))
  ```

Lo que hicimos fue modularizar ese comando

Creamos una subclase de la clase Cogs donde definimos la logica de nuestro comando, es importante pedir como argumento en la creacion de al isntancia  nuestro bot para que nuestro comando pueda interactuar con el.
por ultimo el metodo setup es el encargado de instanciar el cog y agregarlo al bot

En el archivo **main.py** realizamos la siguiente modificacion
  
```python
from discord.ext import commands
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
bot = commands.Bot(command_prefix='!')

bot.load_extension('cogs.Hello')
    
bot.run(os.getenv('DISCORD_API_TOKEN'))
```

## Cog Info

Cargar los cogs uno a uno tampoco es una muy buena forma de hacerlo, por lo que:

```python
def load_all_cogs(bot):
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
```

Ahora si definamos nuestro nuevo cog Info

Cremoas un archivo **info.py**

```python
import discord
from discord.ext import commands

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def getchannel(self,ctx):
    channels_names = [c.name for c in ctx.guild.channels if type(c) is discord.TextChannel]
    print(channels_names)


def setup(bot):
  bot.add_cog(Info(bot))
``` 

Vamos a listar los canales del servidor que sean de texto

## Mensajes Privados

Podemos enviar mensajes privados al usuario invocador del comando utilizando el objeto contexto


vamos a crear un nuevo comando dentro del cog **Hello**
```python
  @commands.command()
    async def dmme(self,ctx):
      user = ctx.message.author.name
      await ctx.author.send(f"Hello {user}")
```
Esto generara un mensaje privado al usuario que lo invoco

## Manejo de Eventos

Un manejador de eventos es una funcion que se ejecuta solo cuando un evento en particular ocurre, por ejemplo cuando un usuario entra en un canal

Agregamos el siguiente envento en el archivo **main.py**

```python
@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')
``` 

el decorador **@bot.event** no lo instanciamos, de esta forma nos permite sobreescribir la logica por defecto de ese evento en la API

Tambien podemos hacer esto en Cogs

En el cog **Hello**
  
  ```python 
  import discord
from discord.ext import commands

class Hello(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
    
    @commands.command()
    async def hello(self,ctx):
      user=ctx.message.author.name
      embed=discord.Embed(title="Hello",description=f"Hello {user}",color=0x00ff00)
      await ctx.send(embed=embed)
      
    @commands.command()
    async def dmme(self,ctx):
      user = ctx.message.author.name
      await ctx.author.send(f"Hello {user}")
      
def setup(bot):
    bot.add_cog(Hello(bot))
  ```
lo unico que cambio es el decorador que usamos, esta vez si lo instanciamos

## Practica React-Role

Vamos a implementar una funcion que nos permita agregar roles a un usuario basado en la reaccion de un mensaje

Primero debemos darle al bot autorizacion de manejar los roles del servidor

Luego debemos crear un rol el cual va a ser el que se agregara al usuario


Creamos un nuevo Cog **Role**
```python
import discord
from discord.ext import commands

class Role(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload):
    pass
    
def setup(bot):
  bot.add_cog(Role(bot))
``` 

Un payload es parecido al contexto pero no tiene tanta informacion end etalle, a veces es mas facil utilizar el payload y mas util.

Creamos desde el cliente un nuevo chat donde los nuevos usuarios van a entrar y se les va a agregar el rol

  
  ```python
   @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload):
    guild = self.bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name="Hacker")
    await payload.member.add_roles(role, reason="you are a Hacker", atomic=True)
  ```


## Music.py

Vamos a implementar una funcion que nos permita reproducir canciones en un canal de voz, traidas directamente de youtube

Primero debemos instalar 2 librerias
  
  ```bash
  pip install youtube_dl
  pip install PyNaCl
  ```
yotube_dl es la libreria que nos permite descargar canciones de youtube de manera programatica

PyNaCl es una libreria que nos permite encriptar y desencriptar informacion, es utilizada al momento de reproducir las canciones en el canal de voz del cliente de discord ya que el stream de audio requiere un formato especifico para poder ser enviado a travez de la API de discord

Vamos a crear un nuevo cog **Music**

```python
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
```
Vamos a inicializar unos atributos que nos permitiran manejar mejor las funcionalidades de este cog

```python
   class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.vc = ""
```

Primero vamos a necesitar algunas funciones auxiliares para organizar mejor el codigo

```python
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f'ytsearch:{item}', download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
```
la siguiente funcion
```python
 def play_next(self,ctx):
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

```
y por ultimo

```python
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
```
Ahora si vamos con los comandos

  ```python
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
  ```

Comando para mostrar la cola de reproduccion

```python
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
```

Comando para saltear la cancion
  
  ```python
   @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc.is_connected():
            self.vc.stop()
            self.is_playing = False
            await self.play_music(ctx=ctx)
  ```

Comando para apagar la musica y sacar al bot del canal

```python
@commands.command(name='stop', help='frena la musica y se retira el bot')
    async def stop(self,ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()
        self.is_playing = False
```

Comando para pausar la reproduccion de musica
  
  ```python 

  @commands.command(name='pause', help='pausa la musica')
    async def pause(self,ctx):
        voice = ctx.message.guild.voice_client
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Ya esta pausado")
  ```

  Comando para reproducir la musica
  
  ```python
   @commands.command(name='resume', help='reanuda la musica')
    async def resume(self,ctx):
        voice = ctx.message.guild.voice_client
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Ya esta sonando!")
  ```

  ## Cog de Sys

  Es muy comun encontrar un cog quea grupe funcionalidades de administrador de servidores, como por ejemplo borrar mensajes, cambiar el nombre de un canal, banear a un usuario, etc.

  ```python
  import discord
from discord.ext import commands

class Sys(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    def is_admin(self,ctx):
        return ctx.author.id == 470679833844776972
    @commands.command()
    async def clear(self,ctx,amount:int,):
        if(self.is_admin(ctx)):
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.send("No tienes permiso de hacer eso")
            

"""Setup"""
def setup(bot):
    bot.add_cog(Sys(bot))
  ```

## AVISO

**necesitan tener los binarios de FFMPEG en la carpet Scripts de su entorno de python**

In case you get this error message : discord.errors.ClientException: ffmpeg was not found go to FFMPEG official site and download the biniaries according to your OS,then put them in ..\Python\PythonX\Scripts 

feel free to suggest any changes or new features