#!/usr/bin/python

temp={}
temp1=[]

with open("ary") as test_file:
 lines = test_file.readlines()
with open("list") as test_filea:
 linesa = test_filea.readlines()
for i in range(len(lines)):
 temp1=lines[i].split(',')
 temp[str(temp1[0])]=temp1[1]
 temp1=[]
for i in range(len(linesa)):
 print str(linesa[i].strip())+','+temp[linesa[i].strip()]
