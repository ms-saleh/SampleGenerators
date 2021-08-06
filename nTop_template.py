# -*- coding: utf-8 -*-
"""
Created on Fr Mar 13 15:03:20 2021

@author: Sadeq Saleh @ Cornell.edu

generate a template for the nTop file
"""
import subprocess
class nTopTemplate():
    
    exePath = r"C:/Program Files/nTopology/nTopology/ntopCL.exe"
    
    def __init__(self,nTopFilePath):
        # Generate template for MicroChannel nTop
        Arguments = [self.exePath]               #nTopCL path
        Arguments.append("-t")              #json template argument
        Arguments.append(nTopFilePath)      #.ntop notebook file path
        #nTopCL call with arguments
        print(" ".join(Arguments))
        output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
                   stderr= subprocess.PIPE).communicate()
        #Print the return messages
        print(output.decode("utf-8"))