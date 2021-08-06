# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Sets the credinitials for "nTopology Platform" as 
virtual environment variables
"""
import os

def writeENV(User,Pass):
    os.environ['nTop_user'] = User
    os.environ['nTop_pass'] = Pass
    
def setCredentials(path,filename):
    with open(path+"\\"+filename) as f:
        UserPass = f.readlines()
    writeENV(UserPass[0].split(' ')[2],UserPass[1].split(' ')[2])

    