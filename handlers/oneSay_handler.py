# -*- coding: utf-8 -*-
"""
    @Author: skong
    @File  : oneSay_handler.py
    @GitHub: https://github.com/Fromsko
    @notes : 一言接口编写入口
"""
from .chat_handler import MetaClient, Context, log
from api.one_say import one_api


_msg = """\
[ Commit  ] {0}
[ Creator ] {1}
[ Message ] {2}
"""


@MetaClient.hybrid_command()
async def onesay(ctx: Context):
    """ Random word """
    resp = one_api()
    text = resp[1]

    log.info(
        "类型:> {one_type} 调用者:> {caller}",
        one_type=resp[0], caller=ctx.author
    )

    await ctx.send(_msg.format(
        text['from'],
        text['creator'],
        text['hitokoto'],
    ))


@MetaClient.hybrid_command()
async def add(ctx: Context, a: int, b: int):
    """ Addition function """
    await ctx.send(a+b)
