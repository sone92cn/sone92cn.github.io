import os, pickle
from PathTool import createTreeAsPath
from jinja2 import FileSystemLoader, Environment

path = os.path.split(os.path.realpath(__file__))[0]
inputfile = os.path.join(path, "template\\index.html")
outputfile = os.path.join(path, "index.html")

print("Input:", inputfile)
print("Output", outputfile)

with open("articles.pkl", "rb") as handle:
    articles = pickle.load(handle)

keys = list(articles.keys())[:6]
recents = {key:articles[key] for key in keys}

i = 0
menu = {}
heads = createTreeAsPath("article_html", scanSubFolder=False, relativePath=True, forFile=False)
for head in heads:
    i += 1
    title = head[3:]
    titles = createTreeAsPath(os.path.join("article_html", head), scanSubFolder=False, relativePath=True, forFile=False)
    menu[title] = {"id":"content_menu_"+str(i), "child":{}}
    child = menu[title]["child"]
    for title in titles:
        child[title[3:]] = os.path.join(os.path.join(os.path.join("article_html", head), title), "menu.htm").replace("\\", "/")

"""
menu = {
	"财税审计":{"id":"content_menu_1","child":{"小类一":"article_html/2018-02-26-Git基本用法.html", "小类二":"article_html/2018-02-27-PyMySQL基本用法.html", "小类三":"html/about.html"}},
	"数据分析":{"id":"content_menu_2","child":{"小类一":"article_html/2018-02-26-Git基本用法.html", "小类二":"article_html/2018-02-27-PyMySQL基本用法.html", "小类三":"html/about.html"}},
	"信息技术":{"id":"content_menu_3","child":{"小类一":"article_html/2018-02-26-Git基本用法.html", "小类二":"article_html/2018-02-27-PyMySQL基本用法.html", "小类三":"html/about.html"}},
}"""

try:
    TemplateLoader = FileSystemLoader(searchpath=os.path.join(path, "template"), encoding='utf-8')
    TemplateEnv = Environment(loader=TemplateLoader)
    template = TemplateEnv.get_template("index.html")
except:
    print("Fail to open files.")
else:
    html = template.render(title="Felix's Page", menu=menu, recents=recents)
    wfile = open(outputfile, "w", encoding="utf-8")
    wfile.write(html)
    wfile.close()
    print("Succeed to update index page.")


os.system("pause")
