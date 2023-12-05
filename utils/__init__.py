# -*- coding: utf-8 -*-
"""
@Author: skong
@File  : __init__.py
@GitHub: https://github.com/Fromsko
@notes : 配置文件
"""
import discord
from discord.ext import commands

import json
from pathlib import Path
from typing import Union

from .log import Logger

WORKPATH = Path.cwd()
_conf_data = {
    "proxy": "",
    "token": "",
    "openai": {
        "api_key": "",
        "api_base": "",
    },
    "img": {
        "font_size": 30,
        "width": 700,
        "font_path": str(WORKPATH.joinpath(
            'res', 'font',
            'sarasa-mono-sc-regular.ttf'
        )),
        "offset_x": 50,
        "offset_y": 50
    },
}


class Config:
    RESPATH = WORKPATH.joinpath('res')
    CONFPATH: Path = WORKPATH.joinpath("config.json")

    def __init__(self, file: Union[Path, None] = None, data: dict = _conf_data) -> None:
        self.file_path: Path = file or self.CONFPATH
        self.conf_data: dict = data
        self.conf = self.load_file()

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

    def get_key(self, key: str = "proxy", proxy=True):
        # if key == "openai":
        #     self.conf['openai'].update({'proxy': self.conf['proxy']})

        if key not in list(self.conf.keys()):
            return
        else:
            if key == "openai" and not proxy:
                self.conf['openai']['proxy'] = self.conf['proxy']

        return self.conf[key]


CONFIG = Config()
intents = discord.Intents.default()
intents.message_content = True

MetaClient = commands.Bot(
    command_prefix="!",
    intents=intents,
    **{"proxy": CONFIG.get_key('proxy')},
)

__all__ = ("MetaClient", "TOKEN", "PROXY", "Config", "Logger")
