import os, json
from PathTool import createTreeAsPath

root = os.path.split(os.path.realpath(__file__))[0]

path = os.path.join(root, "article_html")
article = "article_html" + "/" + createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True)[0]

path = os.path.join(root, "article_head")
recent = ["article_head" + "/" + item for item in createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True)[:6]]

show_dt = {
    "content_0":"#content_0 #wrap-col-head",
    "content_1":"#content_1 #wrap-col-head",
    "content_2":"#content_2 #wrap-col-body",
    "content_3":"#content_3 #wrap-col-body",
    "content_4":"#content_4 #wrap-col-body"
}

load_dt = {
    "content_0":{},
    "content_1":{
		"#content_1 #wrap-col-head":article},
    "content_2":{},
    "content_3":{}
}

append_dt = {
    "content_0":{
        "#content_0 #wrap-col-head":recent},
    "content_1":{},
    "content_2":{},
    "content_3":{}
    }
css_show = "var var_show=" + json.dumps(show_dt) + ";"
css_load = "var var_load=" + json.dumps(load_dt) + ";"
css_append = "var var_append=" + json.dumps(append_dt) + ";"

file = open("js/setting.js", "w", encoding="utf-8")
file.write(css_show)
file.write(css_load)
file.write(css_append)
file.close()

print("Succeed to update js/setting.js.")
os.system("pause")

