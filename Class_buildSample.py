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
    blockNumbers = 0
    
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
    
    def setRecipe(self,recipe):
        self.recipe=self.path+'\\'+recipe
        
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
        self.json=[]
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
        self.json.append(self.path+"\\input.json")
            
            
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

    def createMeshMergeSTL(self):
        for JSON in self.json:
            self.nTopRun(JSON, self.customBlock)
            if self.cleanUp and os.path.isfile(JSON):
                os.remove(JSON)
    
    def createBottomRecipe(self,recipe):
        self.setRecipe(recipe)
        with open(self.recipe,mode='r') as f:
            Lines=f.readlines()
        f = open("./BuildFiles/Bottom_job.recipe",mode='w')
        f.truncate(0)
        f.close()
        f = open(self.buildPath+"\\Bottom_job.recipe",mode='a')
        for line in Lines:
            if line[:14]=="Model.FilePath":
                f.write(('Model.FilePath = '+self.STLPath +"\\"+ self.sampleName + "Bottom.stl\n"))
            else:
                f.write(line)
        f.close()
    
    def createuChannelRecipe(self,recipe):
        self.setRecipe(recipe)
        with open(self.recipe,mode='r') as f:
            Lines=f.readlines()
        f = open("./BuildFiles/uChannel_job.recipe",mode='w')
        f.truncate(0)
        f.close()
        f = open(self.buildPath+"\\uChannel_job.recipe",mode='a')
        for line in Lines:
            if line[:14]=="Model.FilePath":
                f.write(('Model.FilePath = '+self.STLPath +"\\"+ self.sampleName + "uChannel.stl\n"))
            else:
                f.write(line)
        f.close()
    
    def sliceBottomSTL(self):
        Arguments = [self.exePath]
        Arguments.append("-p")
        Arguments.append(self.buildPath+"\\Bottom_job.recipe")
        print(" ".join(Arguments))
        subprocess.call(Arguments)
    
    def sliceuChannelSTL(self):
        Arguments = [self.exePath]
        Arguments.append("-p")
        Arguments.append(self.buildPath+"\\uChannel_job.recipe")
        print(" ".join(Arguments))
        subprocess.call(Arguments)
        
    def moveuChannelOutput(self):
        uChannel_BuildPath = self.buildPath + "\\uChannel_job_output"
        if os.path.isdir(uChannel_BuildPath):
            files = os.listdir(uChannel_BuildPath)
            for file in files:
                src = os.path.join(uChannel_BuildPath,file)
                dst = os.path.join(self.buildPath,file)
                if os.path.isfile(src):
                    shutil.copy(src,dst)
                elif os.path.isdir(src):
                    if os.path.exists(dst) and os.path.isdir(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src,dst)
            shutil.rmtree(uChannel_BuildPath)
            shutil.copy(os.path.join(self.buildPath,self.sampleName+'uChannel_data.gwl')
                      ,os.path.join(self.buildPath,self.sampleName+'uChannel_data.orig'))
        self.blockNumbers =self.blockNumbers + len(os.listdir(self.buildPath+"\\"+self.sampleName+"uChannel_files"))
        
        
    def moveBottomOutput(self):
        Bottom_BuildPath = self.buildPath + "\\Bottom_job_output"
        if os.path.isdir(Bottom_BuildPath):
            files = os.listdir(Bottom_BuildPath)
            for file in files:
                src = os.path.join(Bottom_BuildPath,file)
                dst = os.path.join(self.buildPath,file)
                if os.path.isfile(src):
                    shutil.copy(src,dst)
                elif os.path.isdir(src):
                    if os.path.exists(dst) and os.path.isdir(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src,dst)
            shutil.rmtree(Bottom_BuildPath)
            shutil.copy(os.path.join(self.buildPath,self.sampleName+'Bottom_data.gwl')
                      ,os.path.join(self.buildPath,self.sampleName+'Bottom_data.orig'))
        self.blockNumbers =self.blockNumbers + len(os.listdir(self.buildPath+"\\"+self.sampleName+"Bottom_files"))  
                
        
    def createCombinedJob(self):
        jobFilePath = self.path+"\\_job.gwl"
        with open(jobFilePath,mode='r') as jobFile:
            Lines = jobFile.readlines()
        
        open(self.buildPath+"\\"+self.sampleName+"_job.gwl", mode='w').close()
        
        with open(self.buildPath+"\\"+self.sampleName+"_job.gwl", mode='a') as job:
            for line in Lines:
                words = line.strip().split(" ")
                if line == "%%% Last Line in Parameter Settings\n":
                    job.write(line)
                    job.write("\nvar $BlockNumbers = %s\n" %self.blockNumbers)
                    job.write("var $count = 0\n\n")
                elif len(words)>1:
                    if words[0] == "include" and words[1][-9:] == "_data.gwl":
                        job.write(" ".join([words[0],self.sampleName+words[1][8:]])+"\n")
                    else:
                        job.write(line)
                else:
                    job.write(line)
        
    def modifyBottomData(self):
        dataFilePath = self.buildPath+"\\"+self.sampleName+"Bottom_data.orig"
        with open(dataFilePath,mode='r') as dataFile:
            Lines = dataFile.readlines()
        
        f = open(self.buildPath+"\\"+self.sampleName+"Bottom_data.gwl", mode='w')
        f.truncate(0)
        f.close()
        
        with open(self.buildPath+"\\"+self.sampleName+"Bottom_data.gwl", mode='a') as data:
            for line in Lines:
                words = line.strip().split(" ")
                if line == "FindInterfaceAt $interfacePos\n":
                    pass# do nothing
                elif len(words)>1:
                    if words[0] == '%' and words[1] == 'BLOCK':
                        data.write(line)
                        data.write("set $count = $count +1\n")
                        data.write(r'MessageOut "Print Progress = %.1f." #($count/$BlockNumbers*100)'+"\n")
                    else:
                        data.write(line)
                else:
                    data.write(line)
            
    def modifyuChannelData(self):
        dataFilePath = self.buildPath+"\\"+self.sampleName+"uChannel_data.orig"
        with open(dataFilePath,mode='r') as dataFile:
            Lines = dataFile.readlines()
        
        f = open(self.buildPath+"\\"+self.sampleName+"uChannel_data.gwl", mode='w')
        f.truncate(0)
        f.close()
        
        with open(self.buildPath+"\\"+self.sampleName+"uChannel_data.gwl", mode='a') as data:
            for line in Lines:
                words = line.strip().split(" ")
                if line == "FindInterfaceAt $interfacePos\n":
                    pass# do nothing
                elif len(words)>1:
                    if words[0] == '%' and words[1] == 'BLOCK':
                        data.write(line)
                        data.write("set $count = $count +1\n")
                        data.write(r'MessageOut "Print Progress = %.1f." #($count/$BlockNumbers*100)'+"\n")
                    else:
                        data.write(line)
                else:
                    data.write(line)
        
        
        

