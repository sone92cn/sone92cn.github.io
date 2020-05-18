# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018
@author: Felix
"""

import re
import os
import json
import pickle
import markdown
from shutil import copyfile
from datetime import datetime
from PathTool import createTreeAsPath
from jinja2 import FileSystemLoader, Environment

# 清理已删除文章
del_mode = False

# 设置资源文件夹
path_json = "json"
path_html = "html"
path_mkdn = r"E:\Projects\Markdown"


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


def copyAsset(m):
    file = f"img/{m.group(2)}"
    if os.path.isfile(file):
        return f"{m.group(1)}/{file}{m.group(3)}"
    else:
        try:
            copyfile(f"{path_mkdn}/{m.group(2)}", file)
        except BaseException:
            raise Exception(f"复制{file}失败！")
        else:
            return f"{m.group(1)}/{file}{m.group(3)}"


if __name__ == "__main__":
    rest_n = 5  # 最近文章数量
    view_d = {}  # 所有文章信息
    head_d = None  # 最近文章信息
    html_d = None  # 文章目录字典
    mkdn_d = None  # markdown文件字典
    succ_d, fail_d = [], []  # 删除文章记录
    succ_c, fail_c, skip_c = [], [], []  # 更新全部记录
    succ_i, fail_i, skip_i = [], [], []  # 更新截图

    # 获取当前脚本所在路径
    root = os.path.split(os.path.realpath(__file__))[0]

    # 截图资源正则表达式
    re_copy = re.compile(r'(src\=\")(assets\/.+?\.png)(\")', re.IGNORECASE)

    # 设置脚本文件目录为工作目录
    os.chdir(root)
    print(f"工作目录：{root}：\n")

    # 任务开始
    print("----------------------START----------------------\n")

    # 初始化 html_d
    temp = createTreeAsPath(path_html, scanSubFolder=False, treeMode=False, relativePath=True, forFile=False)
    if len(temp):
        html_d = {key[:2]: f"{path_html}/{key}" for key in temp}
    else:
        raise BaseException("No Sub Dirs.")

    # 初始化 mkdn_d
    temp = sorted(createTreeAsPath(path_mkdn, fileRegular=r'^\d{8}.+\.\d{2}\.md$', scanSubFolder=False, relativePath=True), reverse=True)
    mkdn_d = {f"{key[:4]}-{key[4:6]}-{key[6:8]}{key[8:-6]}": f"{path_mkdn}/{key}" for key in temp}

    # 更新文章
    for key in mkdn_d:
        temp = mkdn_d[key][-5:-3]
        if temp in html_d:
            hfile = f"{html_d[temp]}/{key}.html"
            if os.path.isfile(hfile):
                if os.path.getmtime(hfile) > os.path.getmtime(mkdn_d[key]):
                    skip_c.append(hfile)
                    continue  # 跳过更新时间在markdown文件后的html文件
            try:
                with open(mkdn_d[key], mode="r", encoding="utf-8") as r:
                    with open(hfile, "w", encoding="utf-8") as w:
                        w.write("<div class=\"article\">\n")
                        w.write("<p style=\"text-indent:0em;\"><a id=\"view_head\" href=\"#\" onclick=\"javascript:viewHead($(this));\">返回</a></p>\n")
                        w.write(re_copy.sub(copyAsset, markdown.markdown(r.read(), extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code'])))
                        w.write(f"\n<p class=\"text-right\">最后更新时间：{datetime.fromtimestamp(os.path.getmtime(mkdn_d[key])).strftime('%Y-%m-%d %H:%M:%S')}</p></div>")
            except BaseException:
                fail_c.append(hfile)
            else:
                succ_c.append(hfile)
        else:
            fail_c.append(mkdn_d[key])

    # 检索全部文章
    view_d = {os.path.splitext(os.path.split(key)[1])[0]: f"{path_html}/{key}".replace('\\', '/') for key in createTreeAsPath(path_html, fileRegular=r'^.+\.html$', scanSubFolder=True, relativePath=True)}
    view_k = list(sorted(view_d.keys(), reverse=True))

    # 删除MD目录已删除的文章
    if del_mode:
        for temp in view_d:
            key = view_d[temp]
            k1, k2 = os.path.split(key)
            k2, k3 = os.path.splitext(k2)
            # print(f"{path_mkdn}/{k2[:4]}{k2[5:7]}{k2[8:]}.{key[len(path_html)+1:len(path_html)+3]}.md")
            if not os.path.isfile(f"{path_mkdn}/{k2[:4]}{k2[5:7]}{k2[8:]}.{key[len(path_html)+1:len(path_html)+3]}.md"):
                try:
                    pass  # os.remove(f"{path_html}/{key}")
                except BaseException:
                    fail_d.append(f"{path_html}/{key}")
                else:
                    view_k.remove(temp)
                    succ_d.append(f"{path_html}/{key}")

    # 储存所有文章到JSON
    with open(f"{path_json}/articles.json", "w", encoding="utf-8") as w:
        json.dump({"cate": createTreeAsPath(path_html, scanSubFolder=False, relativePath=True, forFile=False), "full": {key: view_d[key] for key in view_k}}, w)

    # 读取缓存的最近更新
    with open("preview.pkl", "rb") as r:
        rest_d = pickle.load(r)

    # 生成最近更新
    view_s = {}
    view_k = view_k[:rest_n]
    for key in view_k:
        if key in rest_d:
            view_s[key] = rest_d[key]
        elif key in mkdn_d:
            try:
                temp = []
                with open(mkdn_d[key], mode="r", encoding="utf-8") as r:
                    temp.append("<div class=\"article\">")
                    temp.append(re_copy.sub(copyAsset, markdown.markdown(getHeadLines(r.read(), 300), extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code'])))
                    # print(f"<p><a href=\"javascript:viewArticle($('#content_0'), '/{view_d[key]}/{key}.html');\">...</a></p>\n</div>")
                    temp.append(f"<p><a href=\"javascript:viewArticle($('#content_0'), '/{view_d[key]}/{key}.html');\">...</a></p>\n</div>")
            except BaseException:
                raise
            else:
                view_s[key] = "\n".join(temp)
        else:
            raise Exception(f"文章<{key}>不存在！")

    # 储存最近更新
    with open("preview.pkl", "wb") as w:
        pickle.dump(view_s, w)

    # 更新Index页面
    try:
        renderPage(model="index.html", title="My Local Page", recents={key: view_d[key] for key in view_k}, preview="\n".join(view_s.values()))
    except BaseException:
        raise Exception("Fail to update index page.")
    else:
        print(f"网站首页：更新成功.\n")

    # 打印结果
    print(f"更新文章: {len(succ_c)} succeed, {len(fail_c)} fail, {len(skip_c)} skip.")
    print(f"更新截图: {len(succ_i)} succeed, {len(fail_i)} fail, {len(skip_i)} skip.")
    print(f"删除文章: {len(succ_d)} succeed, {len(fail_d)} fail.\n")
    if len(succ_c):
        print("成功更新的文章：")
        for file in succ_c:
            print(file)
    if len(fail_c):
        print("更新失败的文章：")
        for file in fail_c:
            print(file)
    if len(succ_i):
        print("成功更新的截图：")
        for file in succ_i:
            print(file)
    if len(fail_i):
        print("更新失败的截图：")
        for file in fail_i:
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
