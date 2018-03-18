# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:43 2018

@author: Felix
"""

import os
from git import Repo
from PathTool import createTreeAsPath

succ, fail = 0, 0
root = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
hpath = os.path.join(root, "source_html")
mpath = os.path.join(root, "source_md")
print("Root Path :", root)
files = createTreeAsPath(hpath, fileRegular=r'^.+\.html$', scanSubFolder=False)

try:
    repo = Repo(root)
    index = repo.index
except:
    print("Fail to create Repo.")
else:
    n = 0
    for hfile in files:
        path, file = os.path.split(hfile)
        fstr, fext = os.path.splitext(file)
        mfile = os.path.join(mpath, fstr+".md")
        if not os.path.isfile(mfile):
            try:
                os.remove(hfile)
                index.remove([hfile, mfile])
            except:
                print("Fail to remove:%s." % file)
            else:
                n +=1
    if n >0:
        try:
            index.commit('del')
        except:
            print("Fail to remove %d files." % n)
        else:
            print("Succeed to remove %d files." % n)
    else:
        print("No file deleted.")
os.system("pause")
    
