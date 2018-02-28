# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:35:11 2018

@author: Felix
"""

import os, sys
from git import Repo

path = os.path.split(os.path.realpath(__file__))[0]

print("Current Path :", path)
try:
    repo = Repo(path)
except:
    print("Fail to create Repo.")
else:
    remote = repo.remote()
    try:
        remote.pull()
    except:
        print("Fail to pull Repo.")
    else:
        print("Succeed to pull Repo.")
os.system("pause")
