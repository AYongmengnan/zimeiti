# coding:utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import sys
import importlib
importlib.reload(sys)
# reload(sys)
# sys.setdefaultencoding('utf-8')

wp = Client('http://qqhappyfarm.cn/xmlrpc.php', 'adminroot', 'Qwer1234!@#$')

post = WordPressPost()
post.title = '悉语'
post.content = '悉语'
post.post_status = 'publish'  # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
post.definition = '1111111111111111111111111'

# post.terms_names = {
#     # 'post_tag': ['tag1', 'tag2'],  # 文章所属标签，没有则自动创建
#     'category': ['Ai模型']  # 文章所属分类，没有则自动创建
# }
#
# post.custom_fields = []  # 自定义字段列表
# # post.custom_fields.append({  # 添加一个自定义字段
# #     'key': '_sites_link',
# #     'value': 'https://chuangyi.taobao.com/pages/aiCopy'
# # })
# post.custom_fields.append({  # 添加第二个自定义字段
#     'key': '_sites_type',
#     'value': 'sites'
# })
# post.custom_fields.append({  # 添加第二个自定义字段
#     'key': 'post_type',
#     'value': 'sites'
# })
# post.custom_fields.append({  # 添加第二个自定义字段
#     'key': '_sites_sescribe',
#     'value': '阿里旗下智能文案工具，一键生成电商营销文案'
# })
# post.custom_fields.append({  # 添加第二个自定义字段
#     'key': 'sidebar_layout',
#     'value': 'default'
# })
post.id = wp.call(posts.NewPost(post))
print(post.id)