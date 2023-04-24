import requests
import time
import random
import undetected_chromedriver as uc
driver = uc.Chrome(version_main=110, use_subprocess=True)
driver.maximize_window()
# driver.get('https://baidu.com')
# time.sleep(3)
driver.get('https://so.toutiao.com/search?wid_ct=1681724633314&dvpf=pc&source=search_subtab_switch&keyword=重庆旅游&pd=information&action_type=search_subtab_switch&page_num=0&search_id=&from=news&cur_tab_title=news')

time.sleep(3)
print(driver.page_source)

time.sleep(random.random())
driver.close()
