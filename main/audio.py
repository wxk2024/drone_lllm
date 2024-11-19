# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import time
import asyncio
import aiohttp
import urllib.parse



class RequestApi:
    lfasr_host = 'https://raasr.xfyun.cn/v2/api'
    api_upload = '/upload'
    api_get_result = '/getResult'
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa

    async def upload(self, session):
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {
            'appId': self.appid,
            'signa': self.signa,
            'ts': self.ts,
            "fileSize": file_len,
            "fileName": file_name,
            "duration": "200"
        }
        data = open(upload_file_path, 'rb').read(file_len)

        url = RequestApi.lfasr_host + RequestApi.api_upload + "?" + urllib.parse.urlencode(param_dict)
        headers = {"Content-type": "application/json"}
        async with session.post(url, headers=headers, data=data) as response:
            result = json.loads(await response.text())
            return result

    async def get_result(self, session):
        uploadresp = await self.upload(session)
        orderId = uploadresp['content']['orderId']
        param_dict = {
            'appId': self.appid,
            'signa': self.signa,
            'ts': self.ts,
            'orderId': orderId,
            'resultType': "transfer,predict"
        }
        status = 3
        while status == 3:
            url = RequestApi.lfasr_host + RequestApi.api_get_result + "?" + urllib.parse.urlencode(param_dict)
            headers = {"Content-type": "application/json", "charset": "UTF-8"}
            async with session.post(url, headers=headers) as response:
                response.encoding = 'utf-8'
                result = json.loads(await response.text())
                status = result['content']['orderInfo']['status']
                if status == 4:
                    break
            await asyncio.sleep(5)
        return result


async def main():
    api = RequestApi(appid="your appid",
                     secret_key="your secret_key",
                     upload_file_path=r"")
    async with aiohttp.ClientSession() as session:
        result = await api.get_result(session)
        res = json.loads(result["content"]["orderResult"])
        ss = []
        for i in res["lattice2"]:
            ss_ = []
            for j in i["json_1best"]["st"]["rt"][0]["ws"]:
                ss_.append(j["cw"][0]["w"])
            ss.append("".join(ss_))
        with open("a.txt", encoding="utf-8", mode="w") as f:
            f.write("\n".join(ss))


if __name__ == '__main__':
    asyncio.run(main())