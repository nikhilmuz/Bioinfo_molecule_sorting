#!/usr/bin/python
import json
import math
import os
import subprocess
import sys
import shutil
from shutil import rmtree
from subprocess import call


def screen(envpath,pn,rn,resd,cutoffenergy):    #path,protein name , residue number,residues,cutoffenergy

    total_moles_count =0
    selected_moles_count=0
    ####################################################### Asking for protein Name and no of import residue in it's active site
    Protein_Name = pn

    with open(envpath+str(Protein_Name)) as test_file:
         lines = test_file.readlines()
    num_residue = int(rn)

    ####################################################### Loop to ask Residue number
    res=[]
    for i in range (num_residue):
        x=resd[i]
        res.insert(i,x)
        i+=1

    ####################################################### Asking for Energy cutoff
    cutoff_Energy = cutoffenergy
    ####################################################### function to generate json files of coordinates of important residues

    j=0
    list =[]
    for i in range(len(lines)):
      if (lines[i][0:4]=='ATOM')and(lines[i][77:78]!='H'):
          if int(lines[i][23:26])>int(res[j]):
                jfile =open(envpath+str(j+1)+".json",'w')
                jfile.write("{"+'"data"'+":"+json.dumps(list)+"}")
                jfile.close()
                list=[]
                j=j+1
                if j==len(res):
                    break
          if int(lines[i][23:26])==int(res[j]):
                my_dict = dict()
                my_dict ={"x":float(lines[i][31:38]),"y":float(lines[i][39:46]), "z":float(lines[i][47:54])}
                list.append(my_dict)








    ####################################################### Program control function

    path = envpath
    files = os.listdir(path)


    for file in files:
         if '.pdbqt' in file:
           if 'ZINC' in file:
                total_moles_count+=1
                selected_moles_count=calc_value(cutoff_Energy,envpath,num_residue,file,selected_moles_count)

    #######################################################Print Result of the program
    result = open(path + 'result.txt', 'a')
    result.write("total_moles_count" + str(total_moles_count)+"\n")  ## Result file
    result.write("selected_moles_count"+str(selected_moles_count)+"\n")
    result.close()
    ####################################################### Generating folder to copy selected ligand

    os.mkdir(envpath+"/Best_molecules")

    ####################################################### copying file to Best_molecules folder

    src = envpath+"/result.txt"
    des = envpath+"/Best_molecules"
    shutil.move(src, des)
    with open(envpath+'bash.sh', 'rb') as file:
        script = file.readlines()
        for line in script:
            subprocess.call(line,shell = True)

    ####################################################### Main function to select the correct molecules

def calc_value(cutoff_Energy,path,num_residue,file,selected_moles_count):
    a=0
    temp =0
    pos ={}

    for p in range(1,num_residue+1):
        pos[str(p)] =[]

    with open(path+file) as test_file:
        lines = test_file.readlines()

    #################################### Loop selecting lingand's line one by one
    for i in range(len(lines)):
        line=lines[i]



        if (line[:5]=="MODEL"):
            pose = line[6:7]
        if line[:11]=="REMARK VINA":                                            ## selectinf value of Model and Energyf model
            energy =float(line[25:29])


        if (line[:6]=="HETATM"):
            for m in range(1,num_residue+1):
                m = str(m)
                with open(path+m+'.json') as base_file:                              ## Checking each line with each residue one by one
                    data = json.load(base_file)

                for p in data['data']:
                    x=float(p['x'])
                    y=float(p['y'])                                             ## Coordinates of atom of residue
                    z=float(p['z'])

                    tx=float(line[32:38])
                    ty=float(line[40:46])                                       ## coordinates of ligand's line
                    tz=float(line[48:54])

                    dist=math.pow((math.pow((x-tx),2)+math.pow((y-ty),2)+math.pow((z-tz),2)),(0.5))  #Distance formula

                    if a==0:
                        temp =dist
                        a=1
                    temp = min(temp,dist)
                pos[m].append(temp)
                a=0

        if line[:6] =="ENDMDL":                                                ## Print selecting file
            r=1
            for p in range (1,num_residue+1):
                if (min(pos[str(p)])>3.449):
                    r=0

            if r==0:
                for p in range(1,num_residue+1):                               ## Empty Dictionary
                    pos[str(p)] =[]

            else:
                for p in range(1,num_residue+1):                               ##Empty Dictionary
                    pos[str(p)] =[]

                    if (float(energy)<float(cutoff_Energy)):                               ## Energy_cutoff checking
                        selected_moles_count = selected_moles_count+1

                        result = open(path+'result.txt', 'a')
                        result.write(file+"\t"+pose+ "\t"+str(energy)+"\n")    ## Result file
                    result.close()

                    sh = open(path+'bash.sh', 'a')
                    sh.write("cp "+path+file+" "+path+"Best_molecules"+"\n")                ##bash file
                    sh.close()
                    break
        else:
            continue
    return selected_moles_count
