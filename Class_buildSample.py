# -*- coding: utf-8 -*-
"""
Created on Fr Mar 12 13:36:25 2021

@author: Sadeq Saleh @ Cornell.edu

Get the design of experiment for micro channe arrays, build the geometery in 
nTopology Platform and create buildfiles in Nanoscribe
"""
import os
import subprocess
import time
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

class buildSample(object):
    exePath = r"C:/Program Files/nTopology/nTopology/ntopCL.exe"
    cleanUp = True
    
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
        
    def setMeshMergeBlock(self):
        self.customBlock=self.path+'\\'+"MeshMerge.ntop"
        
    def nTopTemplate(self):
        # Generate template for MicroChannel nTop
        Arguments = [self.exePath]               #nTopCL path
        Arguments.append("-t")              #json template argument
        Arguments.append(self.customBlock)      #.ntop notebook file path
        #nTopCL call with arguments
        print(" ".join(Arguments))
        output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
                   stderr= subprocess.PIPE).communicate()
        #Print the return messages
        print(output.decode("utf-8"))
    
    def nTopRun(self,jsonFile,nTopFile):
        # Generate template for MicroChannel nTop
        Arguments = [self.exePath]                              #nTopCL path
        Arguments.append("-j")                                  #json input argument
        Arguments.append(jsonFile)                              #input json file
        Arguments.append("-o")                                  #output argument
        Arguments.append(self.path+"\\"+"out.json")             #output json path
        Arguments.append(nTopFile)                              #.ntop notebook file path
        #nTopCL call with arguments
        print("\n".join(Arguments))
        output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
                   stderr= subprocess.PIPE).communicate()
        #Print the return messages
        print(output.decode("utf-8"))
    
    def createuChannelInputJSON(self):
        try:
            with open(self.path+"\\input_template.json") as f:
                Inputs_JSON = json.load(f)
        except:
            self.nTopTemplate()
            with open(self.path+"\\input_template.json") as f:
                Inputs_JSON = json.load(f)
        self.json=[]
        for index1, Line in enumerate(self.DOE):
            Dim = Line.strip().split(",")
            Inputs_JSON['inputs'][0]['value']=self.STLPath+'\\'+'uChannel_'+str(index1)+'.stl'
            self.json.append(self.path+"\\"+"input_"+str(index1)+".json")
            for index2, item in enumerate(Inputs_JSON['inputs'][1:]):
                item['value']=float(Dim[index2])
            with open(self.json[index1], 'w') as outfile:
                json.dump(Inputs_JSON, outfile, indent=4)
     
    def createMeshMergeInputJSON(self):
        try:
            with open(self.path+"\\input_template.json") as f:
                Inputs_JSON = json.load(f)
        except:
            self.nTopTemplate()
            with open(self.path+"\\input_template.json") as f:
                Inputs_JSON = json.load(f)
        for index, item in enumerate(sorted(os.listdir(self.STLPath))):
            Inputs_JSON['inputs'][4]['value'][index]=self.STLPath +"\\"+item
        fnt = ImageFont.truetype(r'/Library/Fonts/arial.ttf', 900)
        img = Image.new('RGB', (1000 , 1000), color = "black")
        d = ImageDraw.Draw(img)
        d.text((10,10), self.sampleName[-2:] , font=fnt, fill="blue")
        img.save(self.path+"\\"+self.sampleName[-2:]+".png")
        Inputs_JSON['inputs'][0]['value'] = self.STLPath +"\\"+ self.sampleName + "Bottom.stl"
        Inputs_JSON['inputs'][1]['value'] = self.STLPath +"\\"+ self.sampleName + "uChannel.stl"
        Inputs_JSON['inputs'][2]['value'] = self.STLPath +"\\"+ self.sampleName + "Top.stl"
        Inputs_JSON['inputs'][3]['value'] = self.path +"\\"+ self.sampleName[-2:] + ".png"
        
        with open(self.path+"\\input.json", 'w') as outfile:
            json.dump(Inputs_JSON, outfile, indent=4)
            
            
    def createTree(self):
        if os.path.isdir(self.STLPath):
            shutil.rmtree(self.STLPath)
        os.mkdir(self.STLPath)
        if os.path.isdir(self.buildPath):
            shutil.rmtree(self.buildPath)
        os.mkdir(self.buildPath)
        
    def createuChannelSTL(self):
        for JSON in self.json:
            self.nTopRun(JSON, self.customBlock)
            if self.cleanUp and os.path.isfile(JSON):
                os.remove(JSON)
            
            
        
        
        
        

