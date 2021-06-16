#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:21:16 2021

@author: silicon
"""
import rdkit 
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
from collections import Counter
from rdkit.Chem.Draw import IPythonConsole, MolsToGridImage
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image
from io import BytesIO


class cut_fragment():
      
    def __init__(self,center_atoms,mol):
        self.center_atoms = center_atoms
        self.mol = mol
        self.break_bond = []
        self.connect_atom = self.center_atoms
        self.ssr = Chem.GetSymmSSSR(self.mol)
        self.true_smile = ''
        
    def connect_bonds(self):                                               
        len_mole = len(self.mol.GetAtoms())                                                 
        for aa in range(len_mole):                                                     
            atom_n = []                                                                
            if aa not in self.connect_atom:                                                 
                atom = self.mol.GetAtomWithIdx(aa)                                          
                atom_neighs = atom.GetNeighbors()                                      
                for atom_neigh in atom_neighs:                                         
                    atom_neigh_idx = atom_neigh.GetIdx()                               
                    if atom_neigh_idx in self.connect_atom:                                 
                        bond = self.mol.GetBondBetweenAtoms(atom_neigh_idx,aa)              
                        self.break_bond.append(bond.GetIdx())                               
                        #print(aa,atom_neigh_idx,bond.GetIdx())      
    
    def cut_mole(self):                                                                                                                           
        true_smile = ''                                                        
        new_mol = Chem.FragmentOnBonds(self.mol, self.break_bond)                        
        new_mol_smile = Chem.MolToSmiles(new_mol, isomericSmiles=True)         
        smiles = str(new_mol_smile).split('.')     
        #print(smiles)                            
        for smile in smiles:                                                   
           if  smile.count("*") == len(self.break_bond): 
               atoms = ''
               try:
                   mol1 =Chem.MolFromSmiles(smile)    
                   atoms = mol1.GetAtoms()
               except:
                   pass
               if  smile.count("*") +  len( self.connect_atom) ==  len(atoms): 
                   #print(len( self.connect_atom),len(atoms))
                   
                   true_smile = smile                                      
        return true_smile                                                      
                                                                                                                                       
    def main_cut(self):
        #print(int(self.center_atoms[0]))
        atom_1 = self.mol.GetAtomWithIdx(int(self.center_atoms[0]))                          
        atom_2 = self.mol.GetAtomWithIdx(int(self.center_atoms[1]))                           
        atoms1_n = atom_1.GetNeighbors()                          
        atoms2_n = atom_2.GetNeighbors()                          
        atoms_n = atoms1_n + atoms2_n                             
        for at_n in atoms_n:                                      
            self.connect_atom.append(at_n.GetIdx())  
            #print("nei",at_n.GetIdx())                  
            if at_n.IsInRing():                                   
                for ring in self.ssr:                                  
                                                                  
                    if at_n.GetIdx()in list(ring):                
                        for a in ring:                            
                            self.connect_atom.append(a)                
            else:                                                 
                pass                                              
        self.connect_atom = list(set(self.connect_atom))                    
        #print("connect_atom",self.connect_atom)                        
        self.connect_bonds()
        try:
            self.true_smile = self.cut_mole()
        except:   # center fragment is mol itself
            self.true_smile = Chem.MolToSmiles(self.mol)


    def draw_mole_frag_stur(self):
        #my_mol = self.mol
        my_frag = Chem.MolFromSmiles(self.true_smile)  #[C]c1c(C(=O)[O-])oc([9*])c1[13*]
        
        #my_frag = Chem.MolFromSmiles("c1c(C(=O)[O-])occ1") 
        self.center_atoms
     
        env_0 = Chem.FindAtomEnvironmentOfRadiusN(self.mol,1,self.center_atoms[0])
        amap={}
        submol01=Chem.PathToSubmol(self.mol,env_0,atomMap=amap)
        smi_01 =Chem.MolToSmiles(submol01).upper()
        
      
        
        env_1 = Chem.FindAtomEnvironmentOfRadiusN(self.mol,1,self.center_atoms[1])
        amap={}
        submol11=Chem.PathToSubmol(self.mol,env_1,atomMap=amap)
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
        mol_highlightBonds = self.mol.GetBondBetweenAtoms(self.center_atoms[0],self.center_atoms[1]).GetIdx()   
        #print(mol_highlightBonds)
        d = rdMolDraw2D.MolDraw2DCairo(500, 500)
        rdMolDraw2D.PrepareAndDrawMolecule(d, self.mol, highlightAtoms=[], highlightBonds=[mol_highlightBonds])

        d.FinishDrawing()
        png = d.GetDrawingText()
        bio = BytesIO(png)
        img = Image.open(bio)   
        img.save("my_mol.png")
        
        frag_highlightBonds = my_frag.GetBondBetweenAtoms(light_frag_atoms[0],light_frag_atoms[1]).GetIdx() 
        #print("frag-bond",frag_highlightBonds)
        d = rdMolDraw2D.MolDraw2DCairo(500, 500)
        rdMolDraw2D.PrepareAndDrawMolecule(d, my_frag, highlightAtoms=[],
                                   highlightBonds=[frag_highlightBonds])
        
         
        d.FinishDrawing()
        png = d.GetDrawingText()
        bio = BytesIO(png)
        img = Image.open(bio)   
        img.save("my_frag.png")
        
        
if __name__ == "__main__":
    mol = Chem.MolFromSmiles("CN1C(=O)C(c2ccccc2)(c2ncccn2)[NH+]=C1N")
    
    center_atoms = ["4","5"]
    cas = []
    for ca in center_atoms:
        cas.append(int(ca))
    cf = cut_fragment(cas,mol)     
    cf. main_cut()  
    print(cf.true_smile)  
    #cf.draw_mole_frag_stur()
    
    
                    

    

