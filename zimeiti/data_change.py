import configparser
import json
import os
from public import redis_con, get_conn, execute
import requests
from urllib.parse import urlencode
# import urllib.parse
# urllib.parse.quote(font)
rcon = redis_con()
# 读取配置文件
def get_setting():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    cf = configparser.ConfigParser()
    cf.read("settingfile/setting.ini")
    # cf = configparser.RawConfigParser()
    # cf.read(os.path.join(parent_dir, 'settingfile/setting.ini'))
    tablename = cf.get('sql','name')
    return tablename

# 获取原数据
def get_data():
    if rcon.exists('data_all') == 1:
        info = json.loads(rcon.lpop('data_all'))
        title = post_api(info[1])
        content = post_api(info[2])
        if title and content:
            return up_data(info[0],title,content)

    return None

# 请求接口替换内容
def post_api(info):
    url = 'http://apis.5118.com/wyc/rewrite'
    data = {
        'txt':urlencode(info),
        'retype':0,
        'keephtml':True,
        'sim':0,
        'strict':0
    }
    response = requests.post(url=url,json=data).json()
    # {
    #     "errcode": "0",
    #     "errmsg": "",
    #     "like": "0.5521350546176762",
    #     "data": "在线智能工具是网络编辑、员工和站长非常必要的工具。"
    # }
    if response['errcode'] == '0':
        return response['data']
    return None

# 更新数据库
def up_data(id,title,content):
    sql = f"""update {get_setting()} set title='{title}',Ncontent='{content}',is_change=1 where id={id}"""
    result = execute(sql)
    if result is True:
        print(f'更新成功，{get_setting()},id={id}')
    else:
        print('更新失败')
    return