# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018

@author: Felix
"""

import os, markdown
from PathTool import createTreeAsPath, createDirAsTree

root = os.path.split(os.path.realpath(__file__))[0]
path = os.path.join(root, "article_md")

tree = createTreeAsPath(path, scanSubFolder=True, treeMode=True, relativePath=True, forFile=False)

if len(tree):
	if createDirAsTree(os.path.join(root, "article_head"), tree) and createDirAsTree(os.path.join(root, "article_html"), tree):
		print("Succeed to copy Dirs.")
	else:
		print("Fail to copy Dirs.")
else:
	print("No Dirs.")

"""
def findSubStr(substr, totalstr, i):
    count = 0
    index = -1
    while True:
        index = totalstr.find(substr, index+1)
        if index == -1:
            break;
        else:
            count += 1
            if count >= i:
                break
    return index
        

succ_c, fail_c, succ_d, fail_d = 0, 0, 0, 0
root = os.path.split(os.path.realpath(__file__))[0]
path = os.path.join(root, "article_md")
print("MD Path :", path)
files = createTreeAsPath(path, fileRegular=r'^.+\.md$', scanSubFolder=False)

for mfile in files:
    path, file = os.path.split(mfile)
    fstr, fext = os.path.splitext(file)

    hfile = os.path.join(os.path.join(root, "article_head"), fstr+".html")
    tfile = os.path.join(os.path.join(root, "article_html"), fstr+".html")
    
    if os.path.isfile(hfile):
        if os.path.getmtime(hfile) > os.path.getmtime(mfile):
            continue
        
    inout_file = open(mfile, mode="r", encoding="utf-8")
    text = inout_file.read()
    inout_file.close()
    
    index = findSubStr("\n", text, 10)
    if index == -1:
        head = text
    else:
        head = text[:index] + "\n..."

    try:
        output_hfile = open(hfile, "w", encoding="utf-8")
        output_tfile = open(tfile, "w", encoding="utf-8")
    except:
        fail_c += 1
        print("Fail to translate %s." % file)
    else:
        output_hfile.write("<article>")
        output_tfile.write("<article>")
        
        output_hfile.write(markdown.markdown(head))
        output_tfile.write(markdown.markdown(text))

        output_hfile.write("</article>")
        output_tfile.write("</article>")

        output_hfile.close()
        output_tfile.close()
        succ_c +=1
        print("Succeed to transate %s." % file)


path = os.path.join(root, "article_head")
files = createTreeAsPath(path, fileRegular=r'^.+\.html$', scanSubFolder=False)
for hfile in files:
        path, file = os.path.split(hfile)
        fstr, fext = os.path.splitext(file)
        tfile = os.path.join(os.path.join(root, "article_html"), fstr+".html")
        mfile = os.path.join(os.path.join(root, "article_md"), fstr+".md")
        if not os.path.isfile(mfile):
            try:
                os.remove(hfile)
                os.remove(tfile)
            except:
                fail_d += 1
                print("Fail to remove:%s." % tfile)
            else:
                succ_d += 1
                print("Succeed to remove:%s." % tfile)
        
print("<Update> succeed: %s files, Fail: %s files" % (succ_c, fail_c))
print("<Delete> succeed: %s files, Fail: %s files" % (succ_d, fail_d))
"""

os.system("pause")
    
