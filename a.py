#!/usr/bin/python
import json
import math

def calc_value(test,base):
 i=str(test)
 j=str(base)
 a=0
 b=0
 pos=[]
 res=[]
 with open(i) as test_file:
     lines = test_file.readlines()
 with open(j+'.json') as base_file:
     data = json.load(base_file)
 for i in range(len(lines)):
     line=lines[i]
     if line[:11]=="REMARK VINA":
       b= b+1
       if b>1:
         res.append(min(pos))
         pos=[]
     if line[:6]=="HETATM":
       for p in data['data']:
         x=float(p['x'])
         y=float(p['y'])
         z=float(p['z'])
         tx=float(line[32:38])
         ty=float(line[40:46])
         tz=float(line[48:54])
         dist=math.pow((math.pow((x-tx),2)+math.pow((y-ty),2)+math.pow((z-tz),2)),(0.5))
         if a==0:
           temp =dist
           a=1 
         temp = min(temp,dist)
       pos.append(temp)
       a=0 
     else:
       continue
 if b==9:
   res.append(min(pos))
   pos=[]
 return res

for l in range(609):
 aa1=[]
 aa2=[]
 aa3=[]
 aa4=[]
 aa1=calc_value(l+1,1)
 aa2=calc_value(l+1,2)
 aa3=calc_value(l+1,3)
 aa4=calc_value(l+1,4)
 for k in range(len(aa1)):
  if max(aa1[k],aa2[k],aa3[k],aa4[k])<=3.4 :
   print str(l+1)+" "+str(k+1)
   break
