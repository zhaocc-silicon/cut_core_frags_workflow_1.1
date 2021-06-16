#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:56:02 2021

@author: silicon
"""
import os

def re_write_intial_file(path,new_file):
    info_dict = {}
    #new_file = ''
    with open(path,"r") as f:
        lines = f.readlines()
    
    for line in lines:
        all_keys = info_dict.keys()
        if "#" in line.split()[0]:
            continue
        key = line.split()[1:3]
        key = '_'.join(key)
        value = [line.split()[0],line.split()[-1]]
        #print(key)
        #print(value)
        if key not in all_keys:
           info_dict[key] = value
        else:
            old_value = info_dict[key][-1]
            if value[-1] > old_value:
                info_dict[key] = value
    
    with open(new_file,"w") as f:
        for key, value in info_dict.items():
            key = key.split('_')
            s = "{}  {}  {}  {}".format(value[0],key[0],key[1],value[1]) 
            f.write(s)
            f.write('\n')

if __name__ == "__main__":
    '''
    inital file
    format: job_id, inchi_key, scan_term, dde_values
    '''
    current_path = os.getcwd()
    data_path = os.path.join(current_path,'data/pic')
    if os.path.exists(data_path):
        pass
    else:
        os.makedirs(data_path)
        
    path = "data/test.txt"
    
    '''
    the data in the "new_file" have been removed duplication
    format: job_id, inchi_key, scan_term, dde_values
    '''
    new_file = path.split('.')[0]+"_2"+"."+path.split('.')[1]
    re_write_intial_file(path,new_file)