import os
from PathTool import createTreeAsPath

# 获取当前脚本所在路径
root = os.path.split(os.path.realpath(__file__))[0]

# 设置脚本文件目录为工作目录
os.chdir(root)
print(f"开始更新：（ {root}）")

files = createTreeAsPath("article_md", fileRegular=r'^\d{6}.+\.\d{2}\.md$', scanSubFolder=False, relativePath=True)

for file in files:
    # ofile = os.path.join(root, file)
    # nfile = os.path.join(root, file.replace("-", "", 2).replace("-", " ", 1))
    # os.rename(ofile, nfile)
    print(file)

"""------------------------------------------------------------------------"""
# 检索MD文件并筛选最近更新文章
files = createTreeAsPath("article_md", fileRegular=r'^.+\.md$', scanSubFolder=True, relativePath=True)
heads = {os.path.splitext(os.path.split(file)[1])[0]: file for file in files}
keys = reversed(sorted((heads.keys())))
keys = [key for key in keys][:5]
heads = {key: heads[key] for key in keys}

# 生成最近文章
for key in heads:
    fname = os.path.split(heads[key])[1]
    fname = os.path.splitext(fname)[0]
    mfile = os.path.join("article_md", heads[key])
    hfile = os.path.join("article_head", fname + ".html")

    with open(mfile, mode="r", encoding="utf-8") as input_file:
        input_text = getHeadLines(input_file.read(), 300)  # 摘要最多输出300字

    try:
        with open(hfile, "w", encoding="utf-8") as output_file:
            output_file.write("<article>")
            output_file.write(markdown.markdown(input_text))
            url = os.path.join("/article_html", heads[key]).replace("\\", "/")
            url = os.path.splitext(url)[0] + ".html"
            output_file.write(f"\n<p><a href=\"javascript:viewArticle('#content_0', '{url}');\">...</a></p></article>")
    except BaseException:
        fail_h.append(hfile)
    else:
        succ_h.append(hfile)

# 生成全部文章
for mfile in files:
    fname = os.path.splitext(mfile)[0]
    mfile = os.path.join("article_md", mfile)
    tfile = os.path.join("article_html", fname + ".html")

    if os.path.isfile(tfile):
        if os.path.getmtime(tfile) > os.path.getmtime(mfile):
            skip_c.append(tfile)
            continue

    with open(mfile, mode="r", encoding="utf-8") as input_file:
        input_text = input_file.read()

    try:
        with open(tfile, "w", encoding="utf-8") as output_file:
            output_file.write("<article>")
            output_file.write("<p style=\"text-indent:0em;\"><a id=\"view_head\" href=\"javascript:viewHead('#content_1');\">返回</a></p>")
            output_file.write(markdown.markdown(input_text))
            output_file.write("</article>")
    except BaseException:
        fail_c.append(tfile)
    else:
        succ_c.append(tfile)

# 删除MD目录已删除的文章
files = createTreeAsPath("article_html", fileRegular=r'^.+\.html$', scanSubFolder=True, relativePath=True)
for tfile in files:
    fname = os.path.splitext(tfile)[0]
    mfile = os.path.join("article_md", fname+".md")
    if not os.path.isfile(mfile):
        try:
            os.remove(tfile)
        except BaseException:
            fail_d.append(tfile)
        else:
            succ_d.append(tfile)

# 收集更新后的全部文章
files = createTreeAsPath("article_html", fileRegular=r'^.+\.html$', scanSubFolder=True, relativePath=True)
bodys = {os.path.splitext(os.path.split(file)[1])[0]: file for file in files}
keys = sorted(bodys.keys(), reverse=True)
bodys = {key: os.path.join("article_html", bodys[key]).replace("\\", "/") for key in keys}

# 生成全部文章列表
writeMenu("template/menu.html", bodys, auto_add=False)

# 为每个具体类别生成文章列表
folders = createTreeAsPath("article_html", scanSubFolder=True, relativePath=True, forFile=False)
for folder in folders:
    fpath = os.path.join("article_html", folder)
    files = createTreeAsPath(fpath, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True, forFile=True)
    files = {os.path.splitext(file)[0]: os.path.join(fpath, file).replace("\\", "/") for file in files}
    writeMenu(os.path.join(fpath, "menu.htm"), files, auto_add=True)

# 更新setting.js
path = os.path.join(root, "article_head")
recent = ["article_head" + "/" + file for file in reversed(createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True))]
show_dt = {
    "content_0": "#content_0 #wrap-col-head",
    "content_1": "#content_1 #wrap-col-head",
    "content_2": "#content_2 #wrap-col-body",
    "content_3": "#content_3 #wrap-col-body",
    "content_4": "#content_4 #wrap-col-body"
}
load_dt = {
    "content_0": {},
    "content_1": {},
    "content_2": {},
    "content_3": {},
    "content_4": {}
}
append_dt = {
    "content_0": {
        "#content_0 #wrap-col-head": recent},
    "content_1": {},
    "content_2": {},
    "content_3": {},
    "content_4": {}
}
css_show = "var var_show=" + json.dumps(show_dt) + ";\n"
css_load = "var var_load=" + json.dumps(load_dt) + ";\n"
css_append = "var var_append=" + json.dumps(append_dt) + ";\n"
with open("js/setting.js", "w", encoding="utf-8") as file:
    file.write(css_show)
    file.write(css_load)
    file.write(css_append)

# 储存全部文章到json
with open("js/articles.json", 'w', encoding="utf-8") as output_file:
    json.dump(bodys, output_file)

# 生成首页菜单
i = 0
menu = {}
recents = {key: bodys[key] for key in heads}
heads = createTreeAsPath("article_html", scanSubFolder=False, relativePath=True, forFile=False)
for head in heads:
    i += 1
    title = head[3:]
    titles = createTreeAsPath(os.path.join("article_html", head), scanSubFolder=False, relativePath=True, forFile=False)
    menu[title] = {"id": "content_menu_"+str(i), "child": {}}
    child = menu[title]["child"]
    for title in titles:
        child[title[3:]] = os.path.join(os.path.join(os.path.join("article_html", head), title), "menu.htm").replace("\\", "/")

# 更新网站首页
try:
    RenderTemplate(menu=menu, recents=recents)
except BaseException:
    print("Fail to update index page.")
else:
    print(f"网站首页：Succeed to update.")

# 打印更新结果
print(f"最近文章: {len(succ_h)} succeed, {len(fail_h)} fail.")
print(f"更新文章: {len(succ_c)} succeed, {len(fail_c)} fail, {len(skip_c)} skip.")
print(f"删除文章: {len(succ_d)} succeed, {len(fail_d)} fail.")
if len(succ_c):
    print("成功更新的文章：")
    for file in succ_c:
        print(succ_c[file])
if len(fail_c):
    print("更新失败的文章：")
    for file in fail_c:
        print(fail_c[file])
if len(succ_d):
    print("删除成功的文章：")
    for file in succ_d:
        print(succ_d[file])
if len(fail_d):
    print("删除失败的文章：")
    for file in fail_d:
        print(fail_d[file])
