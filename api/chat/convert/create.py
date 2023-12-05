"""
    @Author: skong
    @File  : create
    @GitHub: https://github.com/Fromsko
    @notes : 生成
"""

import time
from base64 import b64encode
from .text_to_image import text_to_img, CONFIG


def create_img(message: str):
    """
    生成图片
        - `message`: 信息
    """
    # 唯一id

    filename = CONFIG.RESPATH.joinpath('imgs', f'{int(time.time())}.png')

    base_text = "[小安] Say:\n"
    img = text_to_img(
        base_text + "\t" + message
    )

    img.save(filename)

    return filename


def image_to_base64(pathload):
    """ 图片转字节码 """
    with open(pathload, mode="rb+") as img_obj:
        content: bytes = img_obj.read()
    return b64encode(content)
