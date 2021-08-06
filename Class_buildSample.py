# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Get the design of experiment for micro channe arrays, build the geometery in 
nTopology Platform and create buildfiles in Nanoscribe
"""
import os

class buildSample(object):
    
    def __init__(self,path):
        self.path = path
        self.setOutputPath(path)
        self.setSTLPath(self.outputPath+"\\STL")
        self.setBuildPath(self.outputPath+"\\BuildFiles")
    
    def setOutputPath(self, outputPath):
        self.outputPath=outputPath
    
    def setSTLPath(self, STLPath):
        self.STLPath=STLPath
    
    def setBuildPath(self, buildPath):
        self.buildPath=buildPath
    
    def setSampleName(self,sampleName):
        self.sampleName=sampleName
    
    def summary(self):
        print('{:>20} {}'.format('Sample Name:',self.sampleName))
        print('{:>20} {}'.format('Costum nTop Block:',self.customBlock))
        print('{:>20} {}'.format('Output Path:',self.outputPath))
        print('{:>20} {}'.format('STL Path:',self.STLPath))
        print('{:>20} {}'.format('Build Files Path:',self.buildPath))
        
    def readDOE(self):
        #look for DOE file
        for fname in os.listdir(self.path):
            if fname.endswith(".csv") and fname[:6]=="Sample":
                self.setSampleName(fname[:-4])
        #import the DOE dimensions from the Sample##.CSV
        with open(self.sampleName+'.csv',mode='r') as f:
            self.setDOE(f.readlines())
    
    def setDOE(self,DOE):
        self.DOE=DOE
    
    def readCustomBlock(self):
        for fname in os.listdir(self.path):
            if fname.endswith(".ntop") and fname[:3]=="CB_":
                self.setCustomBlock(fname)
    
    def setCustomBlock(self,nTop):
        self.customBlock=self.path+'\\'+nTop
        
        
        

