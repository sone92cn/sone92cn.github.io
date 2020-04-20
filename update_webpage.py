# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018
@author: Felix
"""

import os
import json
import markdown
from jinja2 import FileSystemLoader, Environment
from PathTool import createTreeAsPath


def getHeadLines(text, n):
    index = text[:n].rfind("\n")
    return text[:n] if index == -1 else text[:index+1]


def renderPage(model, title, recents, preview):
    try:
        TemplateLoader = FileSystemLoader(searchpath="template", encoding='utf-8')
        TemplateEnv = Environment(loader=TemplateLoader)
        template = TemplateEnv.get_template(model)
    except BaseException:
        raise
    else:
        with open(model, "w", encoding="utf-8") as wfile:
            wfile.write(template.render(title=title, recents=recents, preview=preview))


if __name__ == "__main__":
    debug = False
    view_d = {}  # 所有文章信息
    head_d = None  # 最近文章信息
    html_d = None  # 文章目录字典
    mkdn_d = None  # markdown文件字典
    succ_d, fail_d = [], []  # 删除文章记录
    succ_c, fail_c, skip_c = [], [], []  # 更新全部记录

    # 设置资源文件夹
    path_json = "json"
    path_html = "html"
    path_mkdn = r"E:\Projects\Markdown"

    # 获取当前脚本所在路径
    root = os.path.split(os.path.realpath(__file__))[0]

    # 设置脚本文件目录为工作目录
    os.chdir(root)
    print(f"工作目录：{root}：\n")

    # 任务开始
    print("----------------------START----------------------")

    # -- 初始化 html_d
    temp = createTreeAsPath(path_html, scanSubFolder=False, treeMode=False, relativePath=True, forFile=False)
    if len(temp):
        html_d = {key[:2]: f"{path_html}/{key}" for key in temp}
    else:
        raise BaseException("No Sub Dirs.")

    # 检索markdown文件 -- 初始化 mkdn_d
    temp = sorted(createTreeAsPath(path_mkdn, fileRegular=r'^\d{8}.+\.\d{2}\.md$', scanSubFolder=False, relativePath=True), reverse=True)
    mkdn_d = {f"{key[:4]}-{key[4:6]}-{key[6:8]}{key[8:-6]}": f"{path_mkdn}/{key}" for key in temp}

    # 生成全部文章
    for key in mkdn_d:
        temp = mkdn_d[key][-5:-3]
        if temp in html_d:
            hfile = f"{html_d[temp]}/{key}.html"
            if os.path.isfile(hfile):
                if os.path.getmtime(hfile) > os.path.getmtime(mkdn_d[key]):
                    view_d[key] = hfile
                    skip_c.append(hfile)
                    continue  # 跳过更新时间在markdown文件后的html文件
            try:
                with open(mkdn_d[key], mode="r", encoding="utf-8") as r:
                    input_text = r.read()
                    with open(hfile, "w", encoding="utf-8") as w:
                        w.write("<div class=\"article\">\n")
                        w.write("<p style=\"text-indent:0em;\"><a id=\"view_head\" href=\"#\" onclick=\"javascript:viewHead($(this));\">返回</a></p>\n")
                        w.write(markdown.markdown(input_text))
                        w.write("\n</div>")
            except BaseException:
                fail_c.append(hfile)
            else:
                view_d[key] = hfile
                succ_c.append(hfile)
        else:
            fail_c.append(mkdn_d[key])

    # 删除MD目录已删除的文章
    temp = createTreeAsPath(path_html, fileRegular=r'^.+\.html$', scanSubFolder=True, relativePath=True)
    for key in temp:
        k1, k2 = os.path.split(key)
        k2, k3 = os.path.splitext(k2)
        if not os.path.isfile(f"{path_mkdn}/{k2[:4]}{k2[5:7]}{k2[8:]}.{k1[:2]}.md"):
            try:
                os.remove(f"{path_html}/{key}")
            except BaseException:
                fail_d.append(f"{path_html}/{key}")
            else:
                succ_d.append(f"{path_html}/{key}")

    # 输出所有文章到json
    with open(f"{path_json}/articles.json", "w", encoding="utf-8") as w:
        json.dump({"cate": createTreeAsPath(path_html, scanSubFolder=False, relativePath=True, forFile=False), "full": view_d}, w)

    # 生成最近文章
    view_s = []
    head_d = {key: mkdn_d[key] for key in list(sorted(mkdn_d.keys(), reverse=True))[:5]}
    for key in head_d:
        temp = head_d[key][-5:-3]
        if temp in html_d:
            try:
                with open(head_d[key], mode="r", encoding="utf-8") as r:
                    input_text = getHeadLines(r.read(), 300)
                    view_s.append("<div class=\"article\">")
                    view_s.append(markdown.markdown(input_text))
                    view_s.append(f"<p><a href=\"javascript:viewArticle($('#content_0'), '/{html_d[temp]}/{key}.html');\">...</a></p>\n</div>")
            except BaseException:
                raise
            else:
                head_d[key] = view_d[key]
        else:
            raise Exception(f"{head_d[key]}无法归入现有类别！")

    # 更新Index页面
    try:
        renderPage(model="index.html", title="Felix's Git Page", recents=head_d, preview="\n".join(view_s))
    except BaseException:
        raise Exception("Fail to update index page.")
    else:
        print(f"网站首页：更新成功.\n")

    # 打印更新结果
    print(f"更新文章: {len(succ_c)} succeed, {len(fail_c)} fail, {len(skip_c)} skip.")
    print(f"删除文章: {len(succ_d)} succeed, {len(fail_d)} fail.")
    if len(succ_c):
        print("成功更新的文章：")
        for file in succ_c:
            print(file)
    if len(fail_c):
        print("更新失败的文章：")
        for file in fail_c:
            print(file)
    if len(succ_d):
        print("删除成功的文章：")
        for file in succ_d:
            print(file)
    if len(fail_d):
        print("删除失败的文章：")
        for file in fail_d:
            print(file)

    # 任务结束
    print("\n----------------------FINISH----------------------")
