import execjs
import requests


def get_parmas():
    ctx = execjs.compile(open('./static/js/16.js','r',encoding='utf-8').read())#读取编译js
    r = ctx.call('get_parmas')
    return r

def get_data(p):
    r = get_parmas()
    print(r)
    # url = f'https://match.yuanrenxue.cn/api/match/16'
    url = f'https://match.yuanrenxue.cn/api/match/16?page={p}&m={r["m"]}&t={r["t"]}'
    print(url)
    response = requests.get(url,headers=headers).json()
    print(response)
    data = response['data']
    values = []
    for da in data:
        values.append(da['value'])
    print(values)
    return sum(values)


if __name__ == '__main__':
    num = 0
    headers = {
        'cookie': 'sessionid=z4hes7n6twvjs1rufhcief25e8s6sdl3',
        'user-agent': 'yuanrenxue.project',
    }
    for p in range(1,6):
        v = get_data(p)
        num += v
        # break
    print(num)