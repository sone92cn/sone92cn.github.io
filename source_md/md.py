# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018

@author: Felix
"""

import os, sys
import markdown
from PathTool import createTreeAsPath

succ, fail = 0, 0
print("Current Path :", sys.path[0])
files = createTreeAsPath(sys.path[0], fileRegular=r'^.+\.md$', scanSubFolder=False)

for mfile in files:
    path, file = os.path.split(mfile)
    fstr, fext = os.path.splitext(file)
    hfile = os.path.join(os.path.join(os.path.split(path)[0], "html"), fstr+".html")
    if os.path.isfile(hfile):
        if os.path.getmtime(hfile) > os.path.getmtime(mfile):
            continue
    inout_file = open(mfile, mode="r", encoding="utf-8")
    text = inout_file.read()
    inout_file.close()
    try:
        output_file = open(hfile, "w", encoding="utf-8")
    except:
        fail += 1
        print("error to translate %s." % file)
    else:
        output_file.write(markdown.markdown(text))
        output_file.close()
        succ +=1
        print("finish to transate %s." % file)
print("Succeed:%s missions, Fail:%s missions" % (succ, fail))
os.system("pause")
    
