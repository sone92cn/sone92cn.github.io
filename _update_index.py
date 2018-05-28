import os, pickle
from PathTool import createTreeAsPath
from jinja2 import FileSystemLoader, Environment

path = os.path.split(os.path.realpath(__file__))[0]

def RenderTemplate(menu, recents):
    try:
        TemplateLoader = FileSystemLoader(searchpath=os.path.join(path, "template"), encoding='utf-8')
        TemplateEnv = Environment(loader=TemplateLoader)
        template = TemplateEnv.get_template("index.html")
    except:
        return False
    else:
        html = template.render(title="Felix's Page", menu=menu, recents=recents)
        wfile = open(outputfile, "w", encoding="utf-8")
        wfile.write(html)
        wfile.close()
        return True
    
if __name__ == "__main__":
    
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

    if RenderTemplate(menu=menu, recents=recents):
        print("Succeed to update index page.")
    else:
        print("Fail to update index page.")

os.system("pause")
