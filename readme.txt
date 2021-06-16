
Creat a "data" folder

step 0: remove duplication to original data
run: python remove_duplicate_data.py
input "test.txt"; format:﻿ job_id, inchi_key, scan_term, dde_values
output: 'test_2.txt'; format: the same with before file

step 1: collect information and cut fragments
run python collect_core_frags.py   
input 'test_2.txt' 
output 'collect_inchi_smile.log'

step3: remove dupliicate core fragments and plot all core fragments, molecules, and themselves intra_fitting

load stx_workflow
load ffengine module
modify the "path" in "﻿plt_mole_frag_diha" function
run python remove_duplicate_frags.py

input ﻿"collect_inchi_smile.log"
output ﻿"non_repeat_core_frags.log", frags,molecule, dihedral picture.
