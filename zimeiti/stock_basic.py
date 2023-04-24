import baostock as bs
import tushare as ts
import schedule
from sqlalchemy import create_engine
def get_data():
    pro = ts.pro_api('24002e0f53fb88b3fe9685faab5bc90f71a2e3f8a5867823c646a6ff')
        #### 登陆系统 ####
    lg = bs.login()
        # 显示登陆返回信息
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,market,area,industry,list_date,fullname,enname,cnspell,exchange,curr_type,list_status,delist_date,is_hs')
    print(data)
    return data

def save_data():
    df = get_data()
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/cc_11?charset=utf8')
    df.to_sql(name='stock', con=engine, if_exists='replace')


if __name__ == '__main__':
    # save_data()
    schedule.every().day.at('10:00').do(save_data)  # 每天10点运行
    while True:
        schedule.run_pending()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(ds, 'interval', minutes=2)
    # scheduler.start()
