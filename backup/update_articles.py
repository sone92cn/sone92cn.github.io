# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018
@author: Felix
"""

import os
import json
import pickle
import markdown
from PathTool import createTreeAsPath, createDirAsTree


def getHeadLines(text, n):
    count = 0
    index = -1
    while True:
        index = text.find("\n", index + 1)
        if index == -1:
            break
        else:
            count += 1
        if count >= n:
            break
    if index == -1:
        return text
    else:
        return text[:index+1]


def writeMenu(fname, bodys, auto_add=True):
    with open(fname, "w", encoding="utf-8") as handle:
        handle.write("<article>")
        if auto_add:
            handle.write("<p><a id=\"view_head\" href=\"javascript:viewHead('#content_1', 'template/menu.html');\">返回</a></p>")
        if len(bodys) > 0:
            keys = sorted(bodys.keys(), reverse=True)
            for body in keys:
                handle.write("<h2><a href=\"javascript:viewArticle('#content_1', '%s');\">%s %s</a></h2>" % (bodys[body], body[:10], body[11:]))
        else:
            handle.write("<h2>此类别下暂无文章，请继续关注！</h2>")
        handle.write("</article>")


if __name__ == "__main__":
    succ_h, fail_h = 0, 0
    succ_c, fail_c, succ_d, fail_d = 0, 0, 0, 0
    root = os.path.split(os.path.realpath(__file__))[0]

    os.chdir(root)
    path = os.path.join(root, "article_head")
    tree = createTreeAsPath(path, scanSubFolder=False, treeMode=False, forFile=True)
    for file in tree:
        os.remove(file)

    path = os.path.join(root, "article_md")
    print("MD FILE Path :", path)
    tree = createTreeAsPath(path, scanSubFolder=True, treeMode=True, relativePath=True, forFile=False)
    if len(tree):
        if createDirAsTree(os.path.join(root, "article_html"), tree):
            print("Succeed to copy Dirs.")
        else:
            print("Fail to copy Dirs.")
    else:
        print("No Sub Dirs.")

    files = createTreeAsPath(path, fileRegular=r'^.+\.md$', scanSubFolder=True, relativePath=True)
    heads = {os.path.splitext(os.path.split(file)[1])[0]: file for file in files}
    keys = reversed(sorted((heads.keys())))
    keys = [key for key in keys][:5]
    heads = {key: heads[key] for key in keys}

    for key in heads:
        fname = os.path.split(heads[key])[1]
        fname = os.path.splitext(fname)[0]
        mfile = os.path.join("article_md", heads[key])
        hfile = os.path.join(os.path.join(root, "article_head"), fname + ".html")

        with open(mfile, mode="r", encoding="utf-8") as input_file:
            input_text = getHeadLines(input_file.read(), 8)

        try:
            output_file = open(hfile, "w", encoding="utf-8")
        except BaseException:
            fail_h += 1
            print("Fail to create %s." % hfile)
        else:
            output_file.write("<article>")
            output_file.write(markdown.markdown(input_text))
            url = os.path.join("/article_html", heads[key]).replace("\\", "/")
            url = os.path.splitext(url)[0] + ".html"
            output_file.write(f"\n<p><a href=\"javascript:viewArticle('#content_0', '{url}');\">...</a></p></article>")
            output_file.close()
            succ_h += 1
            print("Succeed to create %s." % hfile)

    for mfile in files:
        fname = os.path.splitext(mfile)[0]
        mfile = os.path.join("article_md", mfile)
        tfile = os.path.join(os.path.join(root, "article_html"), fname + ".html")

        if os.path.isfile(tfile):
            if os.path.getmtime(tfile) > os.path.getmtime(mfile):
                print("skip:", mfile)
                continue

        with open(mfile, mode="r", encoding="utf-8") as input_file:
            input_text = input_file.read()

        try:
            output_file = open(tfile, "w", encoding="utf-8")
        except BaseException:
            fail_c += 1
            print("Fail to create %s." % tfile)
        else:
            output_file.write("<article>")
            output_file.write("<p style=\"text-indent:0em;\"><a id=\"view_head\" href=\"javascript:viewHead('#content_1');\">返回</a></p>")
            output_file.write(markdown.markdown(input_text))
            output_file.write("</article>")
            output_file.close()
            succ_c += 1
            print("Succeed to create %s." % tfile)

    path = os.path.join(root, "article_html")
    files = createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=True, relativePath=True)
    for tfile in files:
        fname = os.path.splitext(tfile)[0]
        mfile = os.path.join("article_md", fname+".md")
        if not os.path.isfile(mfile):
            tfile = os.path.join("article_html", tfile)
            try:
                os.remove(tfile)
            except BaseException:
                fail_d += 1
            else:
                succ_d += 1
                print("Succeed to delete %s." % tfile)

    files = createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=True, relativePath=True)
    bodys = {os.path.splitext(os.path.split(file)[1])[0]: file for file in files}
    keys = reversed(sorted(bodys.keys()))
    bodys = {key: os.path.join("article_html", bodys[key]) for key in keys}

    bodys = {key: bodys[key].replace("\\", "/") for key in bodys}
    with open('articles.pkl', 'wb') as handle:
        pickle.dump(bodys, handle, protocol=pickle.HIGHEST_PROTOCOL)

    writeMenu("template/menu.html", bodys, auto_add=False)
    folders = createTreeAsPath(path, scanSubFolder=True, relativePath=True, forFile=False)
    for folder in folders:
        fpath = os.path.join("article_html", folder)
        files = createTreeAsPath(fpath, fileRegular=r'^.+\.html$', scanSubFolder=False, relativePath=True, forFile=True)
        files = {os.path.splitext(file)[0]: os.path.join(fpath, file).replace("\\", "/") for file in files}
        writeMenu(os.path.join(fpath, "menu.htm"), files)

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
    css_show = "var var_show=" + json.dumps(show_dt) + ";"
    css_load = "var var_load=" + json.dumps(load_dt) + ";"
    css_append = "var var_append=" + json.dumps(append_dt) + ";"

    with open("js/setting.js", "w", encoding="utf-8") as file:
        file.write(css_show)
        file.write(css_load)
        file.write(css_append)

    print("\n")
    print("Setting: updated!")

    print("Head: %s files succeed, %s files fail." % (succ_h, fail_h))
    print("Create: %s files succeed, %s files fail." % (succ_c, fail_c))
    print("Delete: %s files succeed, %s files fail." % (succ_d, fail_d))

os.system("pause")
