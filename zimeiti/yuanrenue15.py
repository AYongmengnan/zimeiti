import requests

import math
import random
import time
import pywasm

def main():
    t = int(time.time())
    t1 = int(t / 2)
    t2 = int(t / 2 - math.floor(random.random() * 50 + 1))
    vm = pywasm.load("./main.wasm")
    result = vm.exec("encode", [t1, t2])
    # print(result)
    result = str(result) + '|' + str(t1) + '|' + str(t2)
    return result

def get_data(m,p):
    url = f'https://match.yuanrenxue.cn/api/match/15?m={m}&page={p}'
    # url = 'https://match.yuanrenxue.cn/api/match/15?m=12127340%7C841023768%7C841023767&page=1'
    print(url)
    response = requests.get(url,headers=headers).json()
    # print(response.text)
    # print(response.json())
    data = response['data']
    values = []
    for da in data:
        values.append(da['value'])
    print(values)
    return values
if __name__ == '__main__':
    headers = {
        # 'authority': 'match.yuanrenxue.cn',
        # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'cache-control': 'max-age=0',
        'cookie': 'sessionid=v1mne3zctp7j4mkaq5b54rpuw7a2n8z1',
        # 'referer': 'https://match.yuanrenxue.cn/list',
        # 'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'document',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-site': 'same-origin',
        # 'sec-fetch-user': '?1',
        # 'upgrade-insecure-requests': '1',
        'user-agent': 'yuanrenxue.project',
    }

    num_list = []
    for i in range(1,6):
        num_list += get_data(main(),i)

    result = sum(num_list)
    print(result)
    # get_data(main(),1)

