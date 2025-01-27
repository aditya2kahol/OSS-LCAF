## Extract the declared licenses

import os
import glob
from typing import List, Dict

# Search for license files in the repository
def find_license_files(repo_path:str)->List[str]:
    license_files = []
    # license filename patterns
    patterns = ['license*','copying*','LICENSE*','COPYING*','License*','Copying*']
    for root, _, files in os.walk(repo_path):
        for pattern in patterns:
            search_pattern = os.path.join(root, pattern)
            matching_files = glob.glob(search_pattern)
            for file_path in matching_files:
                license_files.append(file_path)
    return license_files

# Function to filter out incorrect license texts.
def contains_garbage_keyword(input_text):
    """Returns True if garbage keyword exists in the input_text."""
    garbage_keywords = ["<?php","<!DOCTYPE","/*!","<?xml","cocos2d-x authors & contributors","li#","<p ","{-#","#copyright{","#!/bin/true","<!--","@import","<div","# Authors","<a ",".copy","&lt;","use std","#set","/*","#ifndef","&gt;","#include "]
    for keyword in garbage_keywords:
        if keyword in input_text:
            print("keyword - ", keyword)
            return True
    return False

# Extract the declared licenses.
def extract_license_text_from_license_file(license_file:str):
    try:
        #, errors='ignore'
        with open(license_file, 'r', encoding="utf8") as f:
            license_text = f.read()
            flag = contains_garbage_keyword(license_text)
        if flag:
            print("flag - ", flag)
            return None
        return license_text
    except Exception as e:
        print(f"Error reading file {license_file}: {e}") # This usually happens if the folder name has the word license in it.
        return None

# Extract and return license texts
def extract_declared_licenses(repo_paths:List)->Dict:
    # repo_paths: ["<path_to_your_directory>/<repo_name>",...]
    license_dict = {"Repository name":[],
                    "Repository path":[],
                    "License text":[],
                    "License type":[]
                    }
    for repo_path in repo_paths:
        license_files = find_license_files(repo_path)
        for file in license_files:
            print(f"Checking the path: {file}...")
            license_text = extract_license_text_from_license_file(file)
            if license_text:
                license_dict['Repository name'].append(repo_path.split('/')[-1])
                license_dict['Repository path'].append(file)
                license_dict['License text'].append(str(license_text))
                license_dict['License type'].append("Declared")
    return license_dict
