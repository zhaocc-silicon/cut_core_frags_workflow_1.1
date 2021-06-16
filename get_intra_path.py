#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 17:31:05 2021

@author: silicon
"""


from ffengine import configuration as conf
from ffengine.utils.database.service.fitting import FittingService
from ffengine.utils.database.service.parameter import ParameterService

def get_intra_path(job_id):
    fitting_service = FittingService()
    para_service = ParameterService()
    data_persistence_path = conf.get("core", "data_persistence")
    '''
    with open("", "r") as f:
        job_id_list = []
        for line in f.readlines():
            job_id_list.append(int(line.strip().split()[0]))
    for job_id in job_id_list:
    '''    
    record = fitting_service.filter_first(id=job_id)
    if record:
        result_file_id = record.result_file
        file_path = para_service.get_file_path(data_persistence_path, file_id=result_file_id)
        #print("job_id: {0} file_path: {1}".format(job_id, file_path))
        return file_path
    else:
        return None

