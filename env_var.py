# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Sets the credinitials for "nTopology Platform" as 
virtual environment variables
"""
import os
from getpass import getpass

def writeENV(User,Pass):
    os.environ['nTop_user'] = User
    os.environ['nTop_pass'] = Pass
    
def setCredentials(path,filename):
    try:
        with open(path+"\\"+filename) as f:
            UserPass = f.readlines()
        writeENV(UserPass[0].strip().split(' ')[2],UserPass[1].strip().split(' ')[2])
    except:
        username = input('nTop login username:')
        password = getpass('nTop login password:')
        writeENV(username,password)

    