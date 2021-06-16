#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 14:39:33 2021

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


import pymysql

    # give a inchi_key, get the  number of conformation
def get_info(inchi_key):   
        con=pymysql.connect(
        host='10.86.1.149',   # 连接你要取出数据库的ip，如果是本机可以不用写   
        user='stx',     # 你的数据库用户名
        passwd='linux123',# 你的数据库密码
        db ='compound',
        charset='utf8')
        cursor=con.cursor()
        #execute执行一句查询语句
        sql ="SELECT smiles from compound_table WHERE (inchi_key = '%s') " %inchi_key
        #print(sql)
        cursor.execute(sql)
        num=cursor.fetchone()[0]
        return num

def read_inchi_key_smiles(path,new_file):
    info = []
    with open(path,"r") as f:
        lines = f.readlines()
    for line in lines:
       if "#" in line:
           continue
       job_id = line.split()[0] 
       inchi_key = line.split()[1]
       center_atom = (line.split()[2]).split("-")[1:3]      
       diherdial = line.split()[2]
       dde = line.split()[-1]
       cas = []
       for ca in center_atom:
           cas.append(int(ca))
       smiles = get_info(inchi_key)
       
       mol = Chem.MolFromSmiles(smiles)
       #print("mol_smiles",smiles,center_atom )
       try:
           cff = cf(cas, mol)     
           cff. main_cut()  
           info.append([inchi_key,smiles,cff.true_smile,job_id,diherdial,dde])
           print("frag_smiles", cff.true_smile) 
       except:
           print(inchi_key,smiles," is error")
       
    with open (new_file,'w') as f:
        for ff in info:
            ss = "{}  {}  {}  {} {}  {}".format(ff[0],ff[1],ff[2],ff[3],ff[4],ff[5])
            f.write(ss)
            f.write('\n')
            
    return info
       
       
if __name__ == "__main__":
    
    '''
    inital file
    format: job_id, inchi_key, scan_term, dde_values
    '''     
    original_path = "data/test_2.txt"
    
    '''
    contained new fragment file
    format: inchi_key, smiles, core_smiles, job_id, scan_term, dde_values
    '''
    new_file = 'data/collect_inchi_smile.log'
    frag_smiles = read_inchi_key_smiles(original_path,new_file)
    






