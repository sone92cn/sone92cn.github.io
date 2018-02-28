# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:35:11 2018

@author: Felix
"""

import os
from git import Repo

path = os.path.split(os.path.realpath(__file__))[0]
print("Current Path :", path)
try:
    repo = Repo(path)
except:
    print("Fail to create Repo.")
else:
    index = repo.index
    try:
        index.add(['source_html', 'source_md'])
        index.commit('refresh pages')
    except:
        print("Fail to refresh Repo.")
    else:
        remote = repo.remote()
        try:
            remote.push()
        except:
            print("Fail to push Repo.")
        else:
            print("Succeed to refresh and push Repo.")
os.system("pause")