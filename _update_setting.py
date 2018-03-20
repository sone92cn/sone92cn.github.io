import os, json
from PathTool import createTreeAsPath

root = os.path.split(os.path.realpath(__file__))[0]
path = os.path.join(root, "article_head")
list0 = ["article_head" + "/" + item for item in createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True)[:6]]

path = os.path.join(root, "article_html")
list1 = ["article_html" + "/" + item for item in createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True)]

append_dt = {
    "content_0":{
        ".content_0 .wrap-col-main":list0},
    "content_1":{
	".content_1 .wrap-col-main":list1},
    "content_2":{},
    "content_3":{}
    }

css_append = "var var_append=" + json.dumps(append_dt) + ";"

file = open("js/setting.js", "w", encoding="utf-8")
file.write(css_append)
file.close()

print("Succeed to update js/setting.js.")
os.system("pause")

