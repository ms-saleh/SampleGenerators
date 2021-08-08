#Imports
import os
import subprocess 
import json
import shutil
import time
from PIL import Image, ImageDraw, ImageFont

#Assuming this script, ntop file, and json files will be in the same folder
Current_Directory = os.path.dirname(os.path.realpath('__file__'))
print(Current_Directory)
exePath = r"C:/Program Files/nTopology/nTopology/ntopCL.exe"  #nTopCL path
cleanUp = True
nTopFilePath2 = r"MeshMerge.ntop"   #nTop notebook file name

for fname in os.listdir(Current_Directory):
    if fname[-5:]==".ntop" and fname[:3]=="CB_":
        nTopFilePath = fname
        print(fname)
        
for fname in os.listdir(Current_Directory):
    if fname[-4:]==".csv" and fname[:6]=="Sample":
        SampleName = fname[:-4]
        print(SampleName)

dataFilePath = SampleName + r".csv" #list of dimensions for each uChannel
if os.path.isdir('./STL/'):
    shutil.rmtree('./STL/')
os.mkdir('./STL/')

if os.path.isdir('./BuildFiles/'):
    shutil.rmtree('./BuildFiles/')
os.mkdir('./BuildFiles/')

# Generate template for MicroChannel nTop
Arguments = [exePath]               #nTopCL path
Arguments.append("-t")              #json template argument
Arguments.append(nTopFilePath)      #.ntop notebook file path
#nTopCL call with arguments
print(" ".join(Arguments))
output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
           stderr= subprocess.PIPE).communicate()
#Print the return messages
print(output.decode("utf-8"))

# Generate template for MicroChannel nTop
Arguments = [exePath]               #nTopCL path
Arguments.append("-t")              #json template argument
Arguments.append("MeshMerge.ntop")      #.ntop notebook file path
#nTopCL call with arguments
print(" ".join(Arguments))
output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
           stderr= subprocess.PIPE).communicate()
#Print the return messages
print(output.decode("utf-8"))

with open("input_template.json") as f:
    Inputs_JSON2 = json.load(f)

if cleanUp and os.path.isfile("input_template.json"):
    os.remove("input_template.json")

if cleanUp and os.path.isfile("output_template.json"):
    os.remove("output_template.json")

# Prepare the output.csv
Header = ['Number']
Header = Header+[o['name'] for o in Inputs_JSON['inputs']][1:]
Header.append('Text2Pore')
print(Header)
output_file = open('output.csv', mode='w')
output_file.write(",".join(Header)+'\n')
output_file.close()

# read the dimensional data from .csv
Input_File_Name = "input.json"      #JSON input file name to be saved as
Output_File_Name = "out.json"       #JSON output file name to be saved as

data = open(dataFilePath,mode='r')
Lines = data.readlines()
data.close()
count = 0

# Creating the microchannels
start_time = time.time()

for Line in Lines:
    Dim = Line.strip().split(",")
    Inputs_JSON['inputs'][0]['value']='./STL/'+'uChannel_'+str(count)+'.stl'
    Inputs_JSON2['inputs'][4]['value'][count]='./STL/'+'uChannel_'+str(count)+'.stl'
    
    loopindex = 0
    for item in Inputs_JSON['inputs'][1:]:
        item['value']=float(Dim[loopindex])
        loopindex+=1
    
    #json paths
    input_path =  Input_File_Name
    output_path = Output_File_Name
    
    #nTopCL arguments in a list
    Arguments = [exePath]               #nTopCL path
    Arguments.append("-j")              #json input argument
    Arguments.append(input_path)        #json path
    Arguments.append("-o")              #output argument
    Arguments.append(output_path)       #output json path
    Arguments.append(nTopFilePath)      #.ntop notebook file path
    
    #Creating in.json file
    with open(input_path, 'w') as outfile:
        json.dump(Inputs_JSON, outfile, indent=4)
    
    #nTopCL call with arguments
    print(" ".join(Arguments))
    output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
               stderr= subprocess.PIPE).communicate()
    
    #Print the return messages
    print(output.decode("utf-8"))
    
    #csv output table
    with open(output_path, 'r') as f:
        dataLoad = json.load(f)
        T2Pratio = dataLoad[0]['value']['val']
    summary = [count]
    [summary.append(i) for i in Dim]
    summary.append(T2Pratio)
    output_file = open('output.csv', mode='a')
    output_file.write(",".join([str(i) for i in summary])+'\n')
    output_file.close()
    
    print(summary)
    count +=1
    
print ("--- %.1f seconds ---" % (time.time() - start_time))       

if cleanUp and os.path.isfile("input.json"):
    os.remove("input.json")

if cleanUp and os.path.isfile("out.json"):
    os.remove("out.json")
#%% ===== Merging the STL files and emobsing the number


Input_File_Name2 = "input2.json"      #JSON input file name to be saved as
Output_File_Name2 = "out2.json"       #JSON output file name to be saved as

input_path =  Input_File_Name2
output_path = Output_File_Name2

# generate the number PNG
 
img = Image.new('RGB', (1000 , 1000), color = "black")
fnt = ImageFont.truetype(r'/Library/Fonts/arial.ttf', 900)

d = ImageDraw.Draw(img)
d.text((10,10), SampleName[-2:] , font=fnt, fill="blue")
 
img.save(SampleName[-2:]+".png")

Inputs_JSON2['inputs'][0]['value'] = "./STL/" + SampleName + "Bottom.stl"
Inputs_JSON2['inputs'][1]['value'] = "./STL/" + SampleName + "uChannel.stl"
Inputs_JSON2['inputs'][2]['value'] = "./STL/" + SampleName + "Top.stl"
Inputs_JSON2['inputs'][3]['value'] = "./" + SampleName[-2:] + ".png"

with open(input_path, 'w') as outfile:
    json.dump(Inputs_JSON2, outfile, indent=4)

Arguments = [exePath]               #nTopCL path
Arguments.append("-j")              #json input argument
Arguments.append(input_path)        #json path
Arguments.append("-o")              #output argument
Arguments.append(output_path)       #output json path
Arguments.append(nTopFilePath2)      #.ntop notebook file path

print(" ".join(Arguments))
output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
           stderr= subprocess.PIPE).communicate()

#Print the return messages
print(output.decode("utf-8"))

if cleanUp and os.path.isfile("input2.json"):
    os.remove("input2.json")

if cleanUp and os.path.isfile("out2.json"):
    os.remove("out2.json")

if cleanUp and os.path.isfile(SampleName[-2:]+".png"):
    os.remove(SampleName[-2:]+".png")

print ("--- %.1f seconds ---" % (time.time() - start_time))
#%% Slice the Bottom part

print("Start Describe slicing: Bottom Part")

exePath = r"C:/Program Files/Nanoscribe/DeScribe/DeScribe.exe"  #DeScribe path

start_time = time.time()

recipeFilePath = "./Bottom_job.recipe"
recipe = open(recipeFilePath,mode='r')
Lines = recipe.readlines()
recipe.close()


f = open("./BuildFiles/Bottom_job.recipe",mode='w')
f.write("")
f.close()

f = open("./BuildFiles/Bottom_job.recipe",mode='a')
for line in Lines:
    if line[:14]=="Model.FilePath":
        f.write(('Model.FilePath = '+Current_Directory + u'\\STL\\'
                 +SampleName + 'Bottom.stl\n').replace(r'/',"\\"))
    else:
        f.write(line)
f.close()        


Arguments = [exePath]
Arguments.append("-p")
Arguments.append((("%s\\BuildFiles\\Bottom_job.recipe") %Current_Directory)
                 .replace("\\",r"/"))

print(" ".join(Arguments))

subprocess.call(Arguments)
print ("--- %.1f seconds ---" % (time.time() - start_time))

#%% Slice the uChannel container

print("Start Describe slicing: uChannel Part")

exePath = r"C:/Program Files/Nanoscribe/DeScribe/DeScribe.exe"  #DeScribe path

start_time = time.time()

recipeFilePath = "./uChannel_job.recipe"
recipe = open(recipeFilePath,mode='r')
Lines = recipe.readlines()
recipe.close()


f = open("./BuildFiles/uChannel_job.recipe",mode='w')
f.write("")
f.close()

f = open("./BuildFiles/uChannel_job.recipe",mode='a')
for line in Lines:
    if line[:14]=="Model.FilePath":
        f.write(('Model.FilePath = '+Current_Directory + u'\\STL\\'
                 +SampleName + 'uChannel.stl\n').replace(r'/',"\\"))
    else:
        f.write(line)
f.close()        


Arguments = [exePath]
Arguments.append("-p")
Arguments.append((("%s\\BuildFiles\\uChannel_job.recipe") %Current_Directory)
                 .replace("\\",r"/"))

print(" ".join(Arguments))
subprocess.call(Arguments)
print ("--- %.1f seconds ---" % (time.time() - start_time))


#%% Copy the files and create the combined Job file and edit the data files

uChannel_BuildPath = "%s\\BuildFiles\\uChannel_job_output" %Current_Directory
Bottom_BuildPath = "%s\\BuildFiles\\Bottom_job_output" %Current_Directory

if os.path.isdir(uChannel_BuildPath):
    files = os.listdir(uChannel_BuildPath)
    for file in files:
        src = os.path.join(uChannel_BuildPath,file)
        dst = os.path.join("%s\\BuildFiles" %Current_Directory,file)
        
        if os.path.isfile(src):
            shutil.copy(src,dst)
        elif os.path.isdir(src):
            if os.path.exists(dst) and os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(src,dst)
    
    shutil.rmtree(uChannel_BuildPath)
    shutil.copy(os.path.join("%s\\BuildFiles\\" %Current_Directory,SampleName+'uChannel_data.gwl')
              ,os.path.join("%s\\BuildFiles\\" %Current_Directory,SampleName+'uChannel_data.orig'))
    
if os.path.isdir(Bottom_BuildPath):
    files = os.listdir(Bottom_BuildPath)
    for file in files:
        src = os.path.join(Bottom_BuildPath,file)
        dst = os.path.join("%s\\BuildFiles" %Current_Directory,file)
        
        if os.path.isfile(src):
            shutil.copy(src,dst)
        elif os.path.isdir(src):
            if os.path.exists(dst) and os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(src,dst)
    
    shutil.rmtree(Bottom_BuildPath)
    shutil.copy(os.path.join("%s\\BuildFiles\\" %Current_Directory,SampleName+'Bottom_data.gwl')
              ,os.path.join("%s\\BuildFiles\\" %Current_Directory,SampleName+'Bottom_data.orig'))
    
    
BlockNumbers = len(os.listdir("%s\\BuildFiles\\" %Current_Directory+SampleName+"Bottom_files"))+len(os.listdir("%s\\BuildFiles\\" %Current_Directory+SampleName+"uChannel_files"))



#% ===== Prepare the combined job file

jobFilePath = "./_job.gwl"
jobFile = open(jobFilePath,mode='r')
Lines = jobFile.readlines()
jobFile.close()

open("./BuildFiles/"+SampleName+"_job.gwl", mode='w').close()

with open("./BuildFiles/"+SampleName+"_job.gwl", mode='a') as job:
    for line in Lines:
        words = line.strip().split(" ")
        if line == "%%% Last Line in Parameter Settings\n":
            job.write(line)
            job.write("\nvar $BlockNumbers = %s\n" %BlockNumbers)
            job.write("var $count = 0\n\n")
        elif len(words)>1:
            if words[0] == "include" and words[1][-9:] == "_data.gwl":
                job.write(" ".join([words[0],SampleName+words[1][8:]])+"\n")
            else:
                job.write(line)
        else:
            job.write(line)

#%  ===== Edit Bottom_data
dataFilePath = "./BuildFiles/"+SampleName+"Bottom_data.orig"
dataFile = open(dataFilePath,mode='r')
Lines = dataFile.readlines()
dataFile.close()

f = open("./BuildFiles/"+SampleName+"Bottom_data.gwl", mode='w')
f.truncate(0)
f.close()

with open("./BuildFiles/"+SampleName+"Bottom_data.gwl", mode='a') as data:
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
            
#% ===== Edit uChannel_data
dataFilePath = "./BuildFiles/"+SampleName+"uChannel_data.orig"
dataFile = open(dataFilePath,mode='r')
Lines = dataFile.readlines()
dataFile.close()

f = open("./BuildFiles/"+SampleName+"uChannel_data.gwl", mode='w')
f.truncate(0)
f.close()

with open("./BuildFiles/"+SampleName+"uChannel_data.gwl", mode='a') as data:
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

