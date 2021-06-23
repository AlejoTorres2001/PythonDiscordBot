import random
from discord.ext import commands


class EightBall(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question=None):
        if question is None:
            msg = 'Haceme una pregunta'
            await ctx.channel.send(msg)
            return

        answerList = ['En mi opinión, sí',
                      'Es cierto',
                      ',Es decididamente así',
                      'Probablemente',
                      'Buen pronóstico',
                      'Todo apunta a que sí',
                      'Sin duda',
                      'Sí',
                      'Sí - definitivamente',
                      'Debes confiar en ello',
                      'Ahora no tengo ganas, vuelve a intentarlo',
                      'Pregunta en otro momento',
                      'Será mejor que no te lo diga ahora',
                      'No puedo predecirlo ahora',
                      'Concéntrate y vuelve a preguntar',
                      'No cuentes con ello',
                      'Mi respuesta es no',
                      'Mis fuentes me dicen que no',
                      'Las perspectivas no son buenas',
                      'Muy dudoso']
        rand_num = random.randint(0, len(answerList) - 1)
        msg = '{}'.format(answerList[rand_num])
        await ctx.channel.send(msg)


def setup(client):
    client.add_cog(EightBall(client))
