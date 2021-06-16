#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:25:54 2021

@author: silicon
"""

#path = '/Users/silicon/python_script/statistic_num_qm_db/jacs_info/job-11818-result.json'
import json
from plt_pic import plot_bar_pie_line 
from Read_DB import read_db 

core_frag = '[1*]c1c(C(=O)[O-])sc([9*])c1[12*]'

def plot_dihedral(path, job_id, inchi_key,dihedral):  #("11818",'NRFZSVJUQKNSNB-UHFFFAOYSA-N','12-2-3-8')
    pp = plot_bar_pie_line()
    rd = read_db()    
    #path = rd.get_json_file_path(job_id)
    #path = '/nfs3/ffde_data/'+path    # 149 database
    f = open(path,'r')
    content = f.read()
    a = json.loads(content)
    data = a['results']['pes'][inchi_key][dihedral]
    pic_name = 'data/'+job_id+"_"+inchi_key+'_'+dihedral+'.png'
    pp.plt_line(data,pic_name)


def read_non_repead_frag(path):
    info = []
    with open(path,'r') as f:
        lines =f.readlines()
    for line in lines:
        if len(line.split())>0:
            info.append([line.split(',')])

    return info

def read_collect_inchi_smiles(path):
    info = []
    with open(path,'r') as f:
        lines =f.readlines()
    for line in lines:
        if len(line.split())>0:
            info.append([line.split()])

    return info

if __name__ == "__main__":
            
    core_frag = read_non_repead_frag('non_repeat_cluster_smiles.log')
    collect_info = read_collect_inchi_smiles('collect_inchi_smile.log')

    for frag in core_frag:
        cluster = frag[0]
        core_smiles = frag[1]
        for info in collect_info:
            if core_smiles in info:
                cluster,job_id,inchi_key,dihedral = cluster, info[3], info[0],info[-1]
                plot_dihedral(job_id,inchi_key,dihedral)
                break


    


