#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:33:10 2021

@author: silicon
"""
#import pandas as pd                   
import matplotlib.pyplot as plt      
import matplotlib.pylab as pyl
import numpy as np                    


class plot_bar_pie_line():
    
    def __init__(self):
        pass

    def plt_bar(self, x,y,title,pic_name):                                                                               
                                                                                                  
        params = {'figure.figsize': '20, 12'}                                                     
        plt.rcParams.update(params)                                                               
                                                                                                  
        fig, ax = plt.subplots()                                                                  
        ax.bar(x, y, width=0.35, align='center', color='blue', alpha=0.8)                                            
        #plt.xlabel(x, size='small',rotation=30)                                                                                          
        plt.title(title, loc='center', fontsize='25',            
              fontweight='bold', color='black')  
        plt.xticks(fontsize='20')
        plt.yticks(fontsize='20')
        plt.xlabel("Number of Paraents' Molecules(lg)",fontsize='20')
        plt.ylabel("Number of fragments",fontsize='20')
        for a,b in zip(x,y):
            plt.text(a,b+0.01,'%.0f'%b, ha='center',va='bottom',fontsize=20)                                              
        plt.savefig(pic_name)                                                                  
        plt.show()                                                                                

    def plt_h_bar (self, x,y,title,picture_name):

        #y_11 = []
        #for i in range(len(y)):
        #    y_11.append(int(float(y[i])))
        
        params = {'figure.figsize': '20, 50'}                                          
        plt.rcParams.update(params)                                                                                                                       
        fig, ax = plt.subplots()   
        x1 = np.arange(len(x))
        #print(x1,y)                                            
        b1 = plt.barh(x1, y, color='red',height=0.3, label="")                            
                                                                                   
        #设置Y轴纵坐标上的刻度线标签。                                                           
        plt.yticks(range(len(x)),x,size=20)                                                                                                    
        plt.xticks(())     
    
        for rect in b1:                                                             
            w = rect.get_width()                                                   
            ax.text(w, rect.get_y()+rect.get_height()/2, '%d' %                    
                    int(w), ha='left', va='center',fontsize=8) 
                                                                    
        #plt.legend(["chembl","qm"],loc='upper right',fontsize=20)                                                        
        plt.title(title, loc='center', fontsize='25',
                  fontweight='bold', color='black')                                
        plt.savefig(picture_name)                                                         
        plt.show()  
    
    def plt_pie (self,labels,value,explode,title, picture_name):
        plt.figure(figsize=(6,6)) 
        plt.pie(value,explode=explode,labels=labels,
        autopct='%1.1f%%')
        plt.savefig(picture_name)                                                         
        plt.show() 
        
    def plt_line(self, data_list,file_name): #data[[[x,..],[y,]],[[],[]]]
        #xy_1 = np.array(data_list[0])
        xy_1 =data_list[0] 
        xy1 = zip(xy_1[0],xy_1[1])
        xy1_dic = dict(xy1)
        xy1_key = list(xy1_dic.keys())
        xy1_key.sort()
        xy1_value =[]
        for key in xy1_key:
            xy1_value.append(xy1_dic[key])
        
        xy_2 =data_list[1] 
        xy2 = zip(xy_2[0],xy_2[1])
        xy2_dic = dict(xy2)
        xy2_key = list(xy2_dic.keys())
        xy2_key.sort()
        xy2_value =[]
        for key in xy2_key:
            xy2_value.append(xy2_dic[key])
        
        plt.plot(xy1_key, xy1_value, 'r', marker='o',label='QM')
        plt.plot(xy2_key, xy2_value, 'b', marker='o',label='MM')
        plt.legend()
        plt.xlabel('Dihedral[o]')
        plt.ylabel('Energy [kcal/mol]')
        
        plt.savefig(file_name,dpi=900)
        plt.show()
        
if __name__ == "__main__":
    pp = plot_bar_pie_line()
    data = [[[-149.84, 150.166, 60.171, 90.169, -89.837, 30.168, -119.834, 0.164, 120.166, -59.839, -29.832, -179.835], [9.236, 9.227, 6.972, 10.637, 10.569, 2.291, 10.165, 0, 10.126, 6.87, 2.255, 9.098]],
            [[-149.84, 150.166, 60.171, 90.169, -89.837, 30.168, -119.834, 0.164, 120.166, -59.839, -29.832, -179.835], [8.924, 8.908, 6.894, 10.655, 10.548, 2.314, 10.68, 0, 10.685, 6.868, 2.293, 9.224]],
            [[[12, 2, 3, 8], [1, 2, 3, 4]], ['h_1n$n_3keh$c_3arn$n_2a', 'c_3o$n_3keh$c_3arn$c_3ah']]]
    pp.plt_line(data,"test_png")
         
        
        
            
        
        
        
        
        
        
        
        
        
        
        
        