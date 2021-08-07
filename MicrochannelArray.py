# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Get the design of experiment for micro channe arrays, build the geometery in 
"nTopology Platform" and create buildfiles in Nanoscribe
"""
from env_var import *
from Class_buildSample import *

if __name__ == "__main__":
    path=os.getcwd()
    setCredentials(path,'credentials.txt')
    sample = buildSample(path)
    sample.createTree()
    sample.readDOE()
    
    sample.readCustomBlock()
    sample.nTopTemplate()
    sample.createuChannelInputJSON()
    sample.createuChannelSTL()
    
    sample.setCustomBlock("MeshMerge.ntop")
    sample.nTopTemplate()
    


    sample.summary()
    
     


