# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018

@author: Felix
"""

import os, markdown
from PathTool import createTreeAsPath

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
        

succ, fail = 0, 0
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
    
    index = findSubStr("\n", text, 18)
    if index == -1:
        head = text
    else:
        head = text[:index] + "\n..."

    try:
        output_hfile = open(hfile, "w", encoding="utf-8")
        output_tfile = open(tfile, "w", encoding="utf-8")
    except:
        fail += 1
        print("error to translate %s." % file)
    else:
        output_hfile.write("<article>")
        output_tfile.write("<article>")
        
        output_hfile.write(markdown.markdown(head))
        output_tfile.write(markdown.markdown(text))

        output_hfile.write("</article>")
        output_tfile.write("</article>")

        output_hfile.close()
        output_tfile.close()
        succ +=1
        print("finish to transate %s." % file)
        
print("Succeed:%s missions, Fail:%s missions" % (succ, fail))
os.system("pause")
    
