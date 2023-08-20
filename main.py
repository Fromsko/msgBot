# -*- coding: utf-8 -*-
"""
    @Author: skong
    @File  : main.py
    @GitHub: https://github.com/kongxiaoaaa
    @notes : Discord Bot
"""
from config import TOKEN
from handlers.oneSay_handler import MetaClient

if __name__ == "__main__":
    MetaClient.run(TOKEN)
