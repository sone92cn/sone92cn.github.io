import os
from jinja2 import FileSystemLoader, Environment

path = os.path.split(os.path.realpath(__file__))[0]
inputfile = os.path.join(path, "template\\index.html")
outputfile = os.path.join(path, "index.html")

print(inputfile)
print(outputfile)

"""
try:
	rfile = open(inputfile, "r", encoding="utf-8")
	wfile = open(outputfile, "w", encoding="utf-8")
except:
	print("Fail to open files.")
else:
	text = rfile.read()
	template = Template(text)
	html = template.render(title="Felix's Page")
	wfile.write(html)
	rfile.close()
	wfile.close()
	print("Succeed to update file.")
"""

menu = {
	"大类一":{"id":"content_menu_1","child":{"小类一":"article_html/2018-02-26-Git基本用法.html", "小类二":"article_html/2018-02-27-PyMySQL基本用法.html", "小类三":"html/about.html"}},
	"大类二":{"id":"content_menu_2","child":{"小类一":"article_html/2018-02-26-Git基本用法.html", "小类二":"article_html/2018-02-27-PyMySQL基本用法.html", "小类三":"html/about.html"}},
	"大类三":{"id":"content_menu_3","child":{"小类一":"article_html/2018-02-26-Git基本用法.html", "小类二":"article_html/2018-02-27-PyMySQL基本用法.html", "小类三":"html/about.html"}},
}

try:
    TemplateLoader = FileSystemLoader(searchpath=os.path.join(path, "template"), encoding='utf-8')
    TemplateEnv = Environment(loader=TemplateLoader)
    template = TemplateEnv.get_template("index.html")
except:
    print("Fail to open files.")
else:
    html = template.render(title="Felix's Page", menu=menu)
    wfile = open(outputfile, "w", encoding="utf-8")
    wfile.write(html)
    wfile.close()
    print("Succeed to update file.")

os.system("pause")
