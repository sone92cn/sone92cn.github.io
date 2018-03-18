import os, json
from PathTool import createTreeAsPath

load_dt = {
    "content_0":{
        ".content_0 #recent":"html/recent.html",
        ".content_0 #profile":"html/about.html"},
    "content_1":{
	".content_1 #recent":"html/recent.html"},
    "content_2":{
	".content_2 #recent":"html/recent.html"},
    "content_3":{
	".content_3 #recent":"html/recent.html"}
    }

root = os.path.split(os.path.realpath(__file__))[0]
path = os.path.join(root, "article_head")
list0 = ["article_head" + "/" + item for item in createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True)[:6]]

path = os.path.join(root, "article_html")
list1 = ["article_html" + "/" + item for item in createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True)]

print(list0)
print(list1)

"""
list0 = ["article_html/2018-02-26-Git-Help.html",
         "article_head/2018-02-26-Git-Help-Head.html",
         "article_head/2018-02-26-Git-Help-Head.html"]

list1 = ["article_html/2018-02-26-Git-Help.html"]
"""

append_dt = {
    "content_0":{
        ".content_0 .wrap-col-main":list0},
    "content_1":{
	".content_1 .wrap-col-main":list1},
    "content_2":{},
    "content_3":{}
    }

css_load = "var var_load=" + json.dumps(load_dt) + ";"
css_append = "var var_append=" + json.dumps(append_dt) + ";"

file = open("js/setting.js", "w", encoding="utf-8")
file.write(css_load + css_append)
file.close()

