# -*- coding: utf-8 -*-
"""
    @Author: skong
    @File  : base_handler.py
    @GitHub: https://github.com/Fromsko
    @notes : 基础响应
"""
from discord.ext.commands import Context
from discord.ext import commands
from utils import MetaClient, Logger

log = Logger("logs/discord.log")()


@MetaClient.event
async def on_ready():
    log.info("msgBot 运行成功...")


@MetaClient.hybrid_command()
async def ping(ctx: Context):
    """ 基础响应 """
    log.info(f"{ctx.author} 执行 ping 命令")
    await ctx.send("pong")


@MetaClient.command()
@commands.has_permissions()
async def synccommands(ctx: Context):
    """ 同步信息 """
    log.info(f"{ctx.author} 执行同步命令")
    await MetaClient.tree.sync()
    await ctx.send("同步完成")
