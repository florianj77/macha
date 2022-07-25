#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:03:58 2022

@author: Johannes Karwanoupoulos and Åsmund Kaupang
"""

import sys
import os
import glob

################################################################################
### VARIABLES/SETTINGS
################################################################################
ligands_dir = "ligands"
input_ext = "pdb"

################################################################################
### FUNCTIONS
################################################################################
# HET BLOCK GENERATION
################################################################################
def genPROblock(protein_id, segment_id="PROA"):
    
    block = f"!-------------------------------------------------------------------------------\n"\
            f"! PROTEIN:\n"\
            f"open read card unit 10 name {protein_id.lower()}_{segment_id.lower()}.crd\n"\
            f"read sequence coor card unit 10 resid\n"\
            f"generate {segment_id.upper()} setup warn first NTER last CTER\n"\
            f"\n"\
            f"open read unit 10 card name {protein_id.lower()}_{segment_id.lower()}.crd\n"\
            f"read coor unit 10 card resid\n"\
            f"!-------------------------------------------------------------------------------\n"

    return block

def genHETblock(ligand_id, segment_id="HETA"):
    
    block = f"!-------------------------------------------------------------------------------\n"\
            f"open read card unit 10 name {ligand_id.lower()}.crd\n"\
            f"read sequence coor card unit 10 resid\n"\
            f"generate {segment_id.upper()} setup warn first none last none\n"\
            f"\n"\
            f"open read unit 10 card name {ligand_id.lower()}.crd\n"\
            f"read coor unit 10 card resid\n"\
            f"!-------------------------------------------------------------------------------\n"

    return block

def genWATblock(protein_id, segment_id="WATA"):
    
    block = f"!-------------------------------------------------------------------------------\n"\
            f"open read card unit 10 name {protein_id.lower()}_{segment_id.lower()}.crd\n"\
            f"read sequence coor card unit 10 resid\n"\
            f"generate {segment_id.upper()} setup warn noangle nodihedral\n"\
            f"\n"\
            f"open read unit 10 card name {protein_id.lower()}_{segment_id.lower()}.crd\n"\
            f"read coor unit 10 card resid\n"
            f"!-------------------------------------------------------------------------------\n"

    return block

################################################################################
# HBUILD CONTROL
################################################################################
def hbuild_preserve_explicit_H(segids):

    segid_head = f"hbuild sele hydr .and. .not. ("
    segid_vars = ""
    for idx, segid in enumerate(segids):
        if idx == len(segids) - 1:
            segid_add = f"segid {segid}"
        else:
            segid_add = f"segid {segid} .or. "
        segid_vars = segid_vars + segid_add
    segid_tail = f") end"

    block = f"!-------------------------------------------------------------------------------\n"\
            f"! MOD: HBUILD control - preserve explicit H-coordinates\n"\
            f"prnlev 5\n"\
            f"echo START_HBUILD\n"\
            f"{segid_head + segid_vars + segid_tail}\n"\
            f"echo END_HBUILD\n"\
            f"!-------------------------------------------------------------------------------\n"
    return block

################################################################################
# PRINT USED PARAMETERS
################################################################################
def insert_parameter_print():
    block = f"!-------------------------------------------------------------------------------\n"\
            f"! MOD: Print used parameters\n"\
            f"echo START_PAR\n"\
            f"print para used\n"\
            f"echo END_PAR\n"\
            f"!-------------------------------------------------------------------------------\n"
    return block

################################################################################
# OTHER FUNCTIONS
################################################################################

def streamWriter(work_dir, stream_name, blocks_as_lst):
    with open(f"{work_dir}/{stream_name}.str", 'w') as ostr:
        for block in blocks_as_lst:
            ostr.write(block)

def inputFileInserter(inpfile, cases, blocks, inversions):
    assert len(cases) == len(blocks)

    # Check for the presence of a backup, and start from this
    # or make a backup if none exists
    if os.path.exists(f"{inpfile}.premod"):
        shutil.copy(f"{inpfile}.premod", f"{inpfile}")
    else:
        shutil.copy(f"{inpfile}", f"{inpfile}.premod")

    inp_backup = f"{inpfile}.premod"
    outfile = inpfile

    with open(outfile, 'w') as out:
        with open(inp_backup, 'r') as inf:
            for line in inf:
                for case, block, inversion in zip(cases, blocks, inversions):
                    if case in line:
                        if inversion == True:
                            line = f"{block}\n"\
                                   f"\n"\
                                   f"{case}\n"
                        elif inversion == None:
                            line = f"{block}\n"
                        else:
                            line = f"{case}\n"\
                                   f"\n"\
                                   f"{block}\n"
                out.write(line)


################################################################################
# MAIN (WORK)
################################################################################
# GET LIGAND ID(S) AND PUT THESE IN A LIST
# DOC: If called with an argument, a single ligand id will be processed.
# DOC: If no argument is given, the folder ligands_dir is searched for files
# DOC: with the extenstion input_ext and the names of these files will be
# DOC: used.

# Check for ligand as argument, and if found, run in single ligand mode
try:
    ligand_id = sys.argv[1]
    # Check for existence of ligands/"ligandid"  
    if os.path.exists(f"{ligands_dir}/{ligand_id}.{input_ext}"):
        pass
    else:
        sys.exit(f"Input file: {ligands_dir}/{ligand_id}.{input_ext} not found!")
        
# If no argument is given, run in multiple ligand mode
except IndexError():
    ligand_id = None #None in particular

# Create the master list of the ligand/system names and fill it based on
# the findings above
ligand_ids = []
if ligand_id == None:
    for ifile in glob.glob(f"{ligands_dir}/*.{input_ext}"):
        ligand_ids.append(#
                          os.path.splitext(os.path.basename(ifile))[0]
                          )
elif ligand_id != '':
    ligand_ids.append(ligand_id)
else:
    sys.exit(f"Unknown ligand (file) name error with name: {ligand_id}")
    
###############################################################################
    


