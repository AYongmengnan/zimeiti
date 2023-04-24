import json
import os
import sys
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from public import redis_con,get_conn
from data_change import get_setting

# 将数据查询到redis中
def get_data():
    con = get_conn()
    cur = con.cursor()
    sql = f"SELECT id,title,Ncontent from {get_setting()} where is_change=0 LIMIT 50000"
    num = cur.execute(sql)
    results = cur.fetchall()
    if num != 0:
        for res in results:
            res = json.dumps(list(res))
            redis_con().lpush('data_all',res)
        return True
    return False

def chat():
    if redis_con().exists('data_all') == 1:
        if redis_con().llen('data_all') < 5000:
            result = get_data()
            if result is True:
                print('更新数据成功')
                print(f"总数据{redis_con().llen('data_all')}")
                return True
        print(f"总数据{redis_con().llen('data_all')}")
    result = get_data()
    if result is True:
        print('更新数据成功')
        print(f"总数据{redis_con().llen('data_all')}")
        return True
    return False


if __name__ == '__main__':
    # scheduler = BlockingScheduler()
    # scheduler.add_job(chat, 'cron', minute =1,timezone='Asia/Shanghai')
    # scheduler.start()
    # # chat()
    while True:
        res = chat()
        if res is False:
            sys.exit(0) # 终止运行
        time.sleep(3600)

