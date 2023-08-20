# -*- coding: utf-8 -*-
"""
    @Author: skong
    @File  : __init__.py
    @GitHub: https://github.com/Fromsko
    @notes : 配置文件
"""
import discord
from discord.ext import commands
from loguru import logger as log

import json
from pathlib import Path
from typing import Union
from datetime import datetime

_conf_data = {
    "proxy": "",
    "token": "",
}


format_ = "{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}"
log.add(f"logs/{datetime.now().strftime('%Y-%m-%d')}.log",
        format=format_, retention="7 days")


class Config:
    conf: Path = Path(__file__).parent / "config.json"

    def __init__(self, file: Union[Path, None] = None, data: dict = _conf_data) -> None:
        self.file_path: Path = file or self.conf
        self.conf_data: dict = data

    def load_file(self) -> Union[None, dict]:
        """ 导入配置文件 """
        assert self._check_conf, exit(0)
        try:
            with open(str(self.file_path), "r", encoding="utf-8") as f:
                conf = json.loads(f.read())
        except Exception as _:
            return
        return conf

    def gen_conf(self, data: dict, file: Union[Path, None] = None):
        """ 生成配置 """
        new_pt = file or str(self.file_path)
        try:
            with open(new_pt, mode="w", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False))
        except Exception as err:
            raise err

    @property
    def _check_conf(self):
        """ 检测配置 """
        if not self.file_path.exists():
            self.gen_conf(self.conf_data)
            return False
        return True


cfg = Config()
if (config := cfg.load_file()) is not None:
    TOKEN = config.get("token")
    PROXY = config.get("proxy", None)


intents = discord.Intents.default()
intents.message_content = True

MetaClient = commands.Bot(
    command_prefix="!",
    intents=intents,
    **{"proxy": PROXY},
)

__all__ = ("MetaClient", "TOKEN", "PROXY", "Config")
