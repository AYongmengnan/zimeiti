"""
ja3指纹验证
"""

import requests
from curl_cffi import requests as rq

def get_data(p):
    url = f'https://match.yuanrenxue.cn/api/match/19?page={p}'
    response = rq.get(url=url,headers=headers, impersonate="chrome110")
    num = 0
    data = response.json()['data']
    for da in data:
        num += da['value']
    return num

def get_tls():

    # 注意这个 impersonate 参数，指定了模拟哪个浏览器
    r = rq.get("https://tls.browserleaks.com/json", impersonate="chrome110")

    print(r.json())
    # output: {'ja3_hash': '53ff64ddf993ca882b70e1c82af5da49'
if __name__ == '__main__':
    headers = {
        'cookie': 'sessionid=gvfwlyegi5q6kf29iul4ite28ctg3ncc',
        'user-agent': 'yuanrenxue.project',
    }
    nums = 0
    for i in range(1,6):
        nums += get_data(i)
    print(nums)