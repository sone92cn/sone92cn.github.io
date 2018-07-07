import os, pickle
from FelixFunc import saveJSON
from PathTool import createTreeAsPath
from jinja2 import FileSystemLoader, Environment

def RenderTemplate(menu, recents, path):
    try:
        TemplateLoader = FileSystemLoader(searchpath=os.path.join(path, "template"), encoding='utf-8')
        TemplateEnv = Environment(loader=TemplateLoader)
        template = TemplateEnv.get_template("index.html")
    except:
        return False
    else:
        html = template.render(title="Felix's Page", menu=menu, recents=recents)
        with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as wfile:
            wfile.write(html)
        return True
  
if __name__ == "__main__":
    
    try:
        path = os.path.split(os.path.realpath(__file__))[0]
    except:
        path = r'E:\Projects\Git\GitWeb'
        print('Use static path')
    
    
    with open(os.path.join(path, "articles.pkl"), "rb") as handle:
        articles = pickle.load(handle)
        
    saveJSON(os.path.join(path, "js/articles.json"), articles)
    
    keys = list(articles.keys())[:6]
    recents = {key:articles[key] for key in keys}

    i = 0
    menu = {}
    heads = createTreeAsPath(os.path.join(path, "article_html"), scanSubFolder=False, relativePath=True, forFile=False)
    for head in heads:
        i += 1
        title = head[3:]
        titles = createTreeAsPath(os.path.join(os.path.join(path, "article_html"), head), scanSubFolder=False, relativePath=True, forFile=False)
        menu[title] = {"id":"content_menu_"+str(i), "child":{}}
        child = menu[title]["child"]
        for title in titles:
            child[title[3:]] = os.path.join(os.path.join(os.path.join("article_html", head), title), "menu.htm").replace("\\", "/")

    if RenderTemplate(menu=menu, recents=recents, path=path):
        print("Succeed to update index page.")
    else:
        print("Fail to update index page.")
    
os.system("pause")
