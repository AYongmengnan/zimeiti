# -*- encoding:utf-8 -*-
import requests

from zimeiti.public import get_conn, execute


def change_title(url,data,headers):
    if data:
        form_data = {"prompt": f"帮我创新的改写标题只要一条最优结果不要其他的废话，以下是需要改写的标题：{data[1]}", "history": []}
        response = requests.post(url=url,json=form_data,headers=headers)
        result = ''.join(response.json()['response'].strip().replace('\\','').replace('"','').split())
        # print(data[1],result)
        sql = f"""insert into test1(title,new_title) VALUES ('{data[1]}','{result}')"""
        # print(sql)
        execute(sql)
        return update_gather(data[0])
    return None

def change_text(data):
    form_data = {"prompt": f"创新包含html标签文章，保留原有的html标签：{data}", "history": [],'top_p':0.5}
    response = requests.post(url=url, json=form_data, headers=headers)
    # result = ''.join(response.json()['response'].strip().replace('\\', '').replace('"', '').split())
    result = response.json()['response']
    print(result)

def get_detail_url():
    sql = """
    select id,title from cc_gushidaquan where is_gather=0 limit 1
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    # print(results)
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    conn.commit()
    cur.close()
    conn.close()
    print(results)
    return results[0]

def update_gather(id):
    sql = f"""
        update cc_gushidaquan set is_gather=1 where id={id}
        """
    conn = get_conn()
    cur = conn.cursor()
    results = cur.execute(sql)
    # print(results)
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    conn.commit()
    cur.close()
    conn.close()
    print(results)
    return results


def test_api(data):
    form_data = {"prompt": f"{data}", "history": [],'top_p':1,'temperature':1,'max_length':4096}
    response = requests.post(url=url, json=form_data, headers=headers)
    # result = ''.join(response.json()['response'].strip().replace('\\', '').replace('"', '').split())
    result = response.json()['response']
    print(result)


if __name__ == '__main__':
    url = 'http://192.168.0.200:8000'
    headers = {'Content-Type': 'application/json'}
    # # data ={"prompt": "帮我创新的改写标题只给出一条最优结果不要其他的废话，以下是需要改写的标题：比亚迪海豚纯电动2022款最低报价 入门款补贴后仅售10万", "history": []}
    # while True:
    #     data = get_detail_url()
    #     change_title(url, data, headers)
    # change_text(url, [1,'运输安全承诺书5篇范文'], headers)

    data = """<h2>
                                    小羊过桥的<a href="https://www.gushidaquan.com.cn" title="故事大全网" target="_blank">故事</a>
                                </h2>
                                <p>草原上有一条小河，河上架着一座独木桥。</p>
                                <p>小黑羊和小白羊分别住在独木桥两边。</p>
                                <p>
                                    <img src='https://www.gushidaquan.com.cn/wp-content/uploads/2023/03/img_6414172e1f01b.png' alt="小羊过桥的故事"/>
                                </p>
                                <p>这天一大早，小黑羊要到桥西去看奶奶，小白羊要到桥东去看爷爷。两只小羊都要从桥上过。可真巧，它们在桥中间相遇了。</p>
                                <p>小黑羊挺起胸脯，对小白羊说：“我先上的桥，你赶紧退回去。”</p>
                                <p>小白羊不服气，说：“这桥又不是你们家的，凭什么让我退回去？”它一步也不让。</p>
                                <p>两只小羊站在桥中间，谁也不让谁。可一直耗着也不是办法啊！两只小羊都急着过桥办事情呢！</p>
                                <p>这时它们都想先过去。发起来倔脾气，动起手来。两只小羊使劲蹬着腿。角顶着角，在桥中间拼命顶了起来。</p>
                                <p>咚咚咚，咚咚咚，结果两只小羊都扑通掉进了水里，成了两只落水羊。</p>
                                <h2>小羊过桥的故事告诉我们什么道理</h2>
                                <p>两只羊都互不相让，所以最后两只羊都过不了桥，还掉进水里，成了落水羊。生活中，我们遇到事情一定要做到互相礼让，最后受益的是我们自己。</p>"""
    # change_text(data)
    # data1 = f'改写以下包含HTML标签的文章：{data}'
    data1 = """将下面的每个HTML标签中内容适当修改并替换：<p>小花猫有一顶漂亮的帽子。</p>
    <p>一天，它出去玩，一阵风把它的帽子刮到树上去了。小花猫伤心地哭了。</p>
    <p><img src="ef50bc12a3_02.jpg" alt="小花猫的帽子"></p>
    <p>一只小猴子听到哭声，跑过来问：“小花猫，你怎么了？”小花猫一边哭一边说“我的帽子被风吹到树上去了。”“别哭了，我帮你拿吧。”小猴子说。</p>
    <p>“你怎么帮我拿呀，你没有长长的鼻子，也没有长长的钩子。”小花猫看着小猴子，不相信它。</p>
    <p>小猴子说：“可是我会爬树呀。”说着，就爬上了树，帮小花猫把帽子取了下来。</p>
    <p>小花猫高兴极了，一个劲儿地跟小猴子说“谢谢”。</p>
    <p>---------------------------------------------------</p>
    <p>这是一个小朋友编的故事，按照正常思维就是小花猫也是会爬树的，可能是小朋友太小了还不知道猫是会爬树的，也可能是故事里的这只猫太小了，还不会爬树；也许是只懒猫，还没学会爬树，大家自己去想象吧。。。</p>
    """
    test_api(data1)