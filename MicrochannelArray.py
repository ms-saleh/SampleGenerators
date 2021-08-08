# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Get the design of experiment for micro channe arrays, build the geometery in 
"nTopology Platform" and create buildfiles in Nanoscribe
"""
from env_var import *
from Class_buildSample import *

def runConventionalWorkflow():
    path=os.getcwd()
    setCredentials(path,'credentials.txt')
    
    sample.exePath = r"C:/Program Files/nTopology/nTopology/ntopCL.exe"
    
    sample = buildSample(path)
    sample.createTree()
    sample.readDOE()
    
    sample.readCustomBlock()
    sample.nTopTemplate()
    sample.createuChannelInputJSON()
    sample.createuChannelSTL()
    
    sample.setCustomBlock("MeshMerge.ntop")
    sample.nTopTemplate()
    sample.createMeshMergeInputJSON()
    sample.createMeshMergeSTL()
    
    sample.exePath = r"C:/Program Files/Nanoscribe/DeScribe/DeScribe.exe"
    sample.createBottomRecipe("Bottom_job.recipe")
    sample.createuChannelRecipe("uChannel_job.recipe")
    sample.sliceBottomSTL()
    sample.sliceuChannelSTL()
    
    sample.blockNumbers = 0
    sample.moveBottomOutput()
    sample.moveuChannelOutput()
    
    sample.createCombinedJob()
    sample.modifyBottomData()
    sample.modifyuChannelData()

    sample.summary()   

if __name__ == "__main__":
    runConventionalWorkflow()
    
     


