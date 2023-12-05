"""
    @Author: skong
    @File  : chat_handler.py
    @GitHub: https://github.com/Fromsko
    @notes : ChatGPT Handler
"""
import discord

from api.chat import ChatClient as Client
from .base_handler import MetaClient, Context, log
from utils import CONFIG


Chat = Client(CONFIG.get_key('openai'))


@MetaClient.hybrid_command()
async def chat(ctx: Context, msg: str):
    """ ChatGPT Chat assistant """
    log.info(f"{ctx.author} 调用 GPT 命令")
    try:
        reply, spend_token = await Chat.send(msg, msg_type='img')
    except Exception as err:
        log.error(err)
        await ctx.send("GPT服务异常")
    else:
        log.info(spend_token)
        await ctx.send(
            file=discord.File(reply)
        )
