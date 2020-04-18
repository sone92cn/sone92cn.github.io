# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018
@author: Felix
"""

import os
import json
import markdown
from jinja2 import FileSystemLoader, Environment
from PathTool import createTreeAsPath, createDirAsTree


def getHeadLines(text, n):
    index = text[:n].rfind("\n")
    return text[:n] if index == -1 else text[:index+1]


def writeMenu(fname, bodys, auto_add=True):
    with open(fname, "w", encoding="utf-8") as handle:
        handle.write("<article>")
        if auto_add:
            handle.write("<p><a id=\"view_head\" href=\"javascript:viewHead('#content_1', 'template/menu.html');\">返回</a></p>")
        if len(bodys):
            for body in sorted(bodys.keys(), reverse=True):
                handle.write("<h2><a href=\"javascript:viewArticle('#content_1', '%s');\">%s %s</a></h2>" % (bodys[body], body[:10], body[11:]))
        else:
            handle.write("<h2>此类别下暂无文章，请继续关注！</h2>")
        handle.write("</article>")


def RenderTemplate(menu, recents):
    try:
        TemplateLoader = FileSystemLoader(searchpath="template", encoding='utf-8')
        TemplateEnv = Environment(loader=TemplateLoader)
        template = TemplateEnv.get_template("index.html")
    except BaseException:
        raise
    else:
        with open("index.html", "w", encoding="utf-8") as wfile:
            wfile.write(template.render(title="Felix's Page", menu=menu, recents=recents))


if __name__ == "__main__":
    debug = False
    html_d = None  # 文章目录字典
    mkdn_d = None  # markdown文件字典
    succ_h, fail_h = [], []  # 更新最近记录
    succ_d, fail_d = [], []  # 删除文章记录
    succ_c, fail_c, skip_c = [], [], []  # 更新全部记录

    # 设置资源文件夹
    path_head = "article_head"
    path_html = "article_html"
    path_mkdn = "article_markdown"


    # 获取当前脚本所在路径
    root = os.path.split(os.path.realpath(__file__))[0]

    # 设置脚本文件目录为工作目录
    os.chdir(root)
    print(f"开始更新({root})：")

    # 删除原最近文章
    for key in createTreeAsPath("article_head", scanSubFolder=False, treeMode=False, forFile=True):
        os.remove(key)

    # 按MD目录结构初始化正文目录
    temp = createTreeAsPath("article_html", scanSubFolder=False, treeMode=False, relativePath=True, forFile=False)
    if len(temp):
        html_d = {key[:2]: os.path.join("article_html", key) for key in temp}
    else:
        raise BaseException("No Sub Dirs.")

    # 检索markdown文件
    temp = createTreeAsPath("article_md", fileRegular=r'^\d{8}.+\.\d{2}\.md$', scanSubFolder=False, relativePath=True)
    mkdn_d = {f"{key[:4]}-{key[4:6]}-{key[6:8]}{key[8:-6]}": os.path.join("article_md", key) for key in temp}
    head_d = {key: mkdn_d[key] for key in list(sorted(mkdn_d.keys(), reverse=True))[:5]}

    # 生成最近文章
    for key in head_d:
        try:
            with open(head_d[key], mode="r", encoding="utf-8") as r:
                input_text = getHeadLines(r.read(), 300)  # 摘要最多输出300字
                with open(os.path.join("article_head", f"{key}.html"), "w", encoding="utf-8") as w:
                    w.write("<article>")
                    w.write(markdown.markdown(input_text))
                    url = os.path.join("/article_html", heads[key]).replace("\\", "/")
                    url = os.path.splitext(url)[0] + ".html"
                    output_file.write(f"\n<p><a href=\"javascript:viewArticle('#content_0', '{url}');\">...</a></p></article>")

        fname = os.path.split(heads[key])[1]
        fname = os.path.splitext(fname)[0]





        except BaseException:
            fail_h.append(hfile)
        else:
            succ_h.append(hfile)
    print(head_d)
