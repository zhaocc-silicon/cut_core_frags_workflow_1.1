#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 17:19:01 2021

@author: silicon
"""


import rdkit 
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit import DataStructs
from collections import Counter
from rdkit.Chem.Draw import IPythonConsole, MolsToGridImage
from fragment_cut import cut_fragment as cf
import numpy as np
from sklearn.cluster import KMeans
import csv

path = "kmeans_10_fragments.log"
kmeans_library_1 = {i: [] for i in range(2)}  # num cluster
kmeans_library_2 = {i: [] for i in range(2)}
with open (path,"r") as f:
    lines = f.readlines()
for line in lines:
    if len(line.split())>0:
        num,smile = int(line.split()[0]), line.split()[1]
    kmeans_library_1[num].append(smile)
#print(kmeans_library_1)
for key, value in kmeans_library_1.items():
   # print(key,value)
    value_tem = [value[0]]
    #print(value_tem)
    
    for va in value[1:]:
        flag = True
        mol_va = Chem.MolFromSmiles(va)
        for va_t in value_tem:
            mol_va_t = Chem.MolFromSmiles(va_t)
           # print(key,value_tem)
            fp0 = AllChem.GetMorganFingerprintAsBitVect(mol_va,2)
            fp1 = AllChem.GetMorganFingerprintAsBitVect(mol_va_t,2)
            sm12 =DataStructs.FingerprintSimilarity(fp0,fp1,metric=DataStructs.DiceSimilarity)
            #print(key,sm12)
            if sm12 > 0.99:
                flag = False
                break
        if flag:
             value_tem.append(va)              
               # print(value_tem)
               # exit
    kmeans_library_2[key] = value_tem

print(kmeans_library_2)
with open("non_repeat_cluster_smiles.log","w")as f:
     for key,value in kmeans_library_2.items():
         ss = str(key)
         for va in value:
             ss += ",  " +va 
         f.write(ss)
         f.write('\n')
         
    
def plt_moles(smiles,plt_name):
    frag_moles = []
    for sm in smiles:
        mol = Chem.MolFromSmiles(sm)
        frag_moles.append(mol)
        
    img = Draw.MolsToGridImage(frag_moles, molsPerRow=5,subImgSize=(300, 300))
    img.save("_new_labels_"+str(plt_name)+".png")    
    
for key, value in kmeans_library_2.items(): 
    plt_moles(value,key)
    
    