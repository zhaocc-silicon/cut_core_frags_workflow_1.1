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
#from collections import Counter
from rdkit.Chem.Draw import IPythonConsole, MolsToGridImage
#from fragment_cut import cut_fragment as cf
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image
from io import BytesIO

'''
plot dihedral picture
'''
#from get_intra_path import get_intra_path as gip
#from plot_dihedral import plot_dihedral as pdh

def remove_core_frag(path,new_path):
    info_dict = {}
    with open (path,"r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if len(lines[i].split())==0:
            continue
        if "#" in lines[i]:
            continue
        info_dict[i] = lines[i].split()
    
    unreap_dict = {}
    
    for key, value in info_dict.items():
       if len(unreap_dict.keys()) == 0:
           unreap_dict[key] = value
       else:
           smiles = value[2]
           dde = value[-1]
           mol = Chem.MolFromSmiles(smiles)
           fp0 = AllChem.GetMorganFingerprintAsBitVect(mol,2)
           
           ii = 0
           for key_1, value_1 in unreap_dict.items():
               ii +=1
               smiles_1 = value_1[2]
               dde_1 = value_1[-1]
               mol1 = Chem.MolFromSmiles(smiles_1)
               fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1,2)
               sm12 =DataStructs.FingerprintSimilarity(fp0,fp1,metric=DataStructs.DiceSimilarity)
               if sm12 > 0.98:
                   if abs(float(dde)) > abs(float(dde_1)):
                       print(dde_1,dde)
                       unreap_dict[key_1] = value
                   break
               if ii == len(unreap_dict.keys()):
                       unreap_dict[key] = value
                       break
                   
   
    #print(kmeans_library_2)
    
    with open(new_path,"w")as f:
         for key,value in unreap_dict.items():
             ss = value[0]
             for va in value[1:]:
                 ss += " ,"+ va 
             f.write(ss)
             f.write('\n')
                 
    return unreap_dict 

'''    
def plt_moles(smiles,plt_name):
    frag_moles = []
    for sm in smiles:
        mol = Chem.MolFromSmiles(sm)
        frag_moles.append(mol)
        
    img = Draw.MolsToGridImage(frag_moles, molsPerRow=5,subImgSize=(300, 300))
    img.save("_new_labels_"+str(plt_name)+".png")    
'''
def draw_mole_frag_stur_2(mol_smiles, frag_smiles, center_atoms, mol_name, frag_name):
    #my_mol = self.mol
    my_frag = Chem.MolFromSmiles(frag_smiles)  #[C]c1c(C(=O)[O-])oc([9*])c1[13*]
    my_mol = Chem.MolFromSmiles(mol_smiles)
    
    env_0 = Chem.FindAtomEnvironmentOfRadiusN(my_mol,1,center_atoms[0])
    amap={}
    submol01=Chem.PathToSubmol(my_mol,env_0,atomMap=amap)
    smi_01 =Chem.MolToSmiles(submol01).upper()
    
    
    
    env_1 = Chem.FindAtomEnvironmentOfRadiusN(my_mol,1,center_atoms[1])
    amap={}
    submol11=Chem.PathToSubmol(my_mol,env_1,atomMap=amap)
    smi_11 =Chem.MolToSmiles(submol11).upper()
    #fp1 = AllChem.GetMorganFingerprint(submol11,2)
    mol_smi = [smi_01,smi_11]
    print("mol smi",mol_smi)
    atoms = my_frag.GetAtoms()
    light_frag_atoms = []
    for i in range(len(atoms)):
        env = Chem.FindAtomEnvironmentOfRadiusN(my_frag,1,i)
        amap={}
        submol=Chem.PathToSubmol(my_frag,env,atomMap=amap)
        smi =Chem.MolToSmiles(submol).upper()
        #fp =AllChem.GetMorganFingerprint(submol,2)
        print("frag smi",i,smi)
        
        if smi in mol_smi:
            light_frag_atoms.append(i)
            #print("light frag atoms:",i)
    mol_highlightBonds = my_mol.GetBondBetweenAtoms(center_atoms[0],center_atoms[1]).GetIdx()   
    #print(mol_highlightBonds)
    d = rdMolDraw2D.MolDraw2DCairo(500, 500)
    rdMolDraw2D.PrepareAndDrawMolecule(d, my_mol, highlightAtoms=[], highlightBonds=[mol_highlightBonds])
    
    d.FinishDrawing()
    png = d.GetDrawingText()
    bio = BytesIO(png)
    img = Image.open(bio)   
    img.save(mol_name)
    #print(light_frag_atoms)
    frag_highlightBonds = my_frag.GetBondBetweenAtoms(light_frag_atoms[0],light_frag_atoms[1]).GetIdx() 
    #print("frag-bond",frag_highlightBonds)
    d = rdMolDraw2D.MolDraw2DCairo(500, 500)
    rdMolDraw2D.PrepareAndDrawMolecule(d, my_frag, highlightAtoms=[],
                               highlightBonds=[frag_highlightBonds])
    
     
    d.FinishDrawing()
    png = d.GetDrawingText()
    bio = BytesIO(png)
    img = Image.open(bio)   
    img.save(frag_name)  


def plt_mole_frag_diha(unreap_dict):
    for values in unreap_dict.values():
        inchi_key = values[0]
        mol_smile = values[1]
        frag_smile = values[2]
        job_id = values[3]       
        ca = values[4].split('-')
        center_atoms = [int(ca[1]),int(ca[2])]
        dde = values[-1]
        mol_name = 'data/pic/'+inchi_key+"_"+job_id+"_"+"mol.png"
        frag_name = 'data/pic/'+inchi_key+"_"+job_id+"_"+"frag.png"
        try:
            draw_mole_frag_stur_2(mol_smile, frag_smile, center_atoms, mol_name, frag_name)
        except:
            print(mol_smile,center_atoms," is error")
        
        '''
        path_tmp = gip(job_id)
        path = "/nfs3/ffde_data/"+path_tmp
        dihedral = values[4]
        pdh(path, job_id, inchi_key,dihedral)
        '''
if __name__ == "__main__":
    
    path = "data/collect_inchi_smile.log"
    new_path = "data/non_repeat_core_frags.log"
    
    unreap_dict = remove_core_frag(path,new_path)
    plt_mole_frag_diha(unreap_dict)
    

    
    