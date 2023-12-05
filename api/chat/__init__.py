"""
    @Author: skong
    @File  : __init__.py
    @GitHub: https://github.com/Fromsko
    @notes : GPT Client
"""
import json
import os
import aiohttp
from .convert import create_img


class ChatClient:

    def __init__(self, option: dict):
        self.api_key = option.get("api_key", None)
        self.api_base = option.get("api_base", None)
        self.proxy = option.get("proxy", 'http://localhost:7890')

        # if (proxy := option.get("proxy", None)) is not None:
        #     self.proxy = {
        #         "http_proxy": proxy,
        #         "https_proxy": proxy,
        #     }
        #     os.environ['http_proxy'] = proxy
        #     os.environ['https_proxy'] = proxy

    async def async_openai_request(self, messages):
        #    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            url = f"{self.api_base}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            payload = json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": self.set_prompt(messages),
                "temperature": 0.8,
                "presence_penalty": 0,
                "top_p": 1,
            })

            async with session.post(url, headers=headers, data=payload, proxy=self.proxy) as response:
                # print(response.status)
                # print("信息", await response.text())

                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(
                        f"OpenAI request failed with status code {response.status}")
                    print(await response.text())
                    return None

    @staticmethod
    def create(text: str):
        return create_img(text)

    @staticmethod
    def set_prompt(msg: str):
        return [
            {
                "role": "user",
                "content": msg,
            }
        ]

    async def send(self, messages: str, msg_type='img') -> tuple:
        resp = await self.async_openai_request(messages)
        content = resp['choices'][0]['message']['content']
        speed = f"实际消耗 Tokens: {resp['usage']['total_tokens']}"

        if msg_type == 'img':
            return self.create(content), speed
        return content, speed
