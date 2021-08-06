# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Get the design of experiment for micro channe arrays, build the geometery in 
nTopology Platform and create buildfiles in Nanoscribe
"""
from env_var import *
from Class_buildSample import *
from nTop_template import *
# import readDOE



if __name__ == "__main__":
    path=os.getcwd()
    setCredentials(path,'credentials.txt')
    sample = buildSample(path)
    sample.readDOE()
    sample.readCustomBlock()
    nTopTemplate(sample.customBlock)
    sample.summary()
     


