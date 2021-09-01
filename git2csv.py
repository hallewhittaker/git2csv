#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import os
from posixpath import join 
import sys
import csv
import datetime
import subprocess
import argparse
import copy
import logging

parser = argparse.ArgumentParser()
parser.add_argument('--format', type=str, help = "format used for file", action= "store") 
parser.add_argument('--filelist', type=str, help= "specific files to run (exclude binary files)", action="store")
parser.add_argument('--overwrite_existing', help= "overwrites the existing file",  action='store_true', default=False) 
parser.add_argument('--debugging_level', type=str, help= "prints debug statements seen in program", action="store")
parser.add_argument('filepath', type=str, help = "filepath of program", action= "store") 
parser.add_argument('output_file', type=str,help = "output filename", action= "store") 
args = parser.parse_args()

filepath = args.filepath 
output_file = args.output_file
specified_format = args.format
list_of_files = args.filelist
overwrite_boolean = args.overwrite_existing
debugging_level = args.debugging_level

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

mydir = os.getcwd()
mydir_static_copy = copy.copy(mydir)

if overwrite_boolean == False:
    filename_ = output_file
    open1 = os.path.join(mydir_static_copy , filename_)
    isExist= os.path.exists(open1)
    if isExist == True:
        logging.error("File Already Exists")
        raise Exception ("Use --overwrite_existing to rewrite this file or use a file that doesn't exist")
    else:
        None

if filepath != None:
    mydir_tmp = filepath
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd() 
else:
    mydir_tmp = mydir_static_copy 
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd()

if list_of_files != None:
    finalArray = []
    filename_txt = list_of_files
    fileopen= os.path.join(mydir_static_copy , filename_txt)
    with open(fileopen, "r", encoding='ISO-8859-1', newline='') as f:
        content_lines = f.readlines()
        for i in content_lines:
            splitvalues= i.split('\r\n')
            finalArray.append(splitvalues[0])    
else:
    z= subprocess.run('git ls-tree --full-tree --name-only -r HEAD',shell=True, stdout= subprocess.PIPE)
    stan_out = z.stdout
    finalArray = []
    filearray = stan_out.split(b'\n')
    for i in filearray:
        x= i.decode("utf-8")
        finalArray.append(x)
    finalArray.remove("")

arrayofDictionaries = []
for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),shell=True, stdout= subprocess.PIPE)
    standard_out = r.stdout
    linearray = standard_out.split(b'\n') 

    if debugging_level != None:
        logging.debug("Current length of dictionary: " + str(len(arrayofDictionaries)))
        logging.debug("We're currently analyzing the file: " + finalArray[i])

    count = 0
    tempdictionary = {}
    for individL in linearray:
        individL = individL.decode("ISO-8859-1")
        splitline = individL.split(" ") 

        temp_key_name = splitline[0]
        first_word_removed = splitline.copy()
        first_word_removed[0] = " "
        first_word_removed = " ".join(first_word_removed).lstrip()

        if count == 0:
            tempdictionary["hash"] = temp_key_name
            commitNumbers = first_word_removed.split(" ") 

            for i in range(0, len(commitNumbers)):
                try:
                    commitNumbers[i] = int(commitNumbers[i])
                except:
                    None

            if len(commitNumbers) == 3:
                tempdictionary["CommitLinesN"] = {'originalLine': commitNumbers[0], 'finalLine': commitNumbers[1], 'groupLine' : commitNumbers[2]}
            elif len(commitNumbers) == 2:
                tempdictionary["CommitLinesN"] = {'originalLine': commitNumbers[0], 'finalLine': commitNumbers[1] } 
        
        elif count >= 1 and count <= 12:
            if count == 3:
                int_time_author= int(first_word_removed)
                date_author_time = datetime.datetime.fromtimestamp(int_time_author)   
                tempdictionary["author-time"] = date_author_time 
                
            elif count == 4:
                authortz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                new_atz = datetime.timezone.tzname( authortz, None )
                tempdictionary["author-tz"] = new_atz
                tempdictionary["author-time"].replace(tzinfo=authortz)
        
            elif count == 7:
                int_time_commiter= int(first_word_removed)
                date_commiter_time = datetime.datetime.fromtimestamp(int_time_commiter)
                tempdictionary["commiter-time"] = date_commiter_time
    
            elif count == 8:
                commitertz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                new_ctz = datetime.timezone.tzname( commitertz, None )
                tempdictionary["commiter-tz"] = new_ctz
                tempdictionary["commiter-time"].replace(tzinfo=commitertz)
            
            elif individL[0:1] == '\t':
                slice_string = individL[1:]
                tempdictionary["commit_content"] = slice_string.lstrip()

            else:
                tempdictionary[temp_key_name] = first_word_removed

        count += 1 
        for key,value in dict(tempdictionary).items():
            if key == "commit_content":
                arrayofDictionaries.append(tempdictionary)
                tempdictionary = {} 
                count = 0

# if debugging_level != None:
#     logging.debug("Final Array:" + str(arrayofDictionaries))

def myconverter(k):
    if isinstance(k, datetime.datetime):
        return k.__repr__()
jsonstring= json.dumps(arrayofDictionaries, default = myconverter)

fieldnames = ['hash','CommitLinesN', 'author','author-mail','author-time','author-tz','committer','committer-mail', 'commiter-time','commiter-tz','summary', 'previous', 'boundary', 'filename','commit_content']
rows = arrayofDictionaries

try:
    split_outputfile = output_file.split(".")   
    filetype= split_outputfile[-1]
except:
    None

write_mode = "w"
force_overwrite = False

if force_overwrite == True:
    write_mode = "w+"

output_type = sys.stdout
change_output = False

if change_output == True:
    output_type = f

def open_csv(filename_csv):
    file0open = os.path.join(mydir_static_copy , filename_csv)
    with open(file0open, write_mode, encoding='ISO-8859-1', newline='') as output_type:
        writer = csv.DictWriter(output_type, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

file1open= os.path.join(mydir_static_copy , output_file)
isExist1= os.path.exists(file1open)
if filepath != None and overwrite_boolean ==True and specified_format =="csv" and isExist1 ==True: 
    filename_csv = "TestCSV.csv"
    force_overwrite == True
    open_csv(filename_csv)

if filepath != None and specified_format == None and filetype != "csv" and filetype != "json": 
    filename_csv = output_file
    open_csv(filename_csv)
    
if filepath != None and specified_format == "csv" and output_file == '-':  
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

if filepath != None and specified_format == "csv" and isExist1 == False and output_file != '-':  
    filename_csv = output_file
    open_csv(filename_csv)

elif filepath != None and specified_format == "csv" and list_of_files == None:  
    filename_csv= "TestCSV.csv"
    open_csv(filename_csv)
    
elif specified_format == "json": 
    None

elif filepath != None and filetype == "csv": 
    filename_csv = output_file
    open_csv(filename_csv)

if filepath == None: 
    filename_csv = 'TestCSV.csv'
    change_output == True
    open_csv(filename_csv)

def open_json(filename_json):
    file2open = os.path.join(mydir_static_copy , filename_json)
    with open (file2open, write_mode, encoding='ISO-8859-1', newline='')  as output_type:
        output_type.write(jsonstring) 

file3open= os.path.join(mydir_static_copy , output_file)
isExist2= os.path.exists(file3open)
if filepath != None and overwrite_boolean ==True and specified_format =="json" and  isExist2==True: 
    filename_json = "data.json"
    force_overwrite == True
    open_json(filename_json)

if filepath != None and specified_format == "json" and output_file == '-': 
    sys.stdout.write(jsonstring)
    sys.stdout.close()

if filepath != None and specified_format == "json" and isExist2 == False and output_file != '-': 
    filename_json = output_file
    open_json(filename_json)

elif filepath != None and specified_format == "json" and list_of_files == None: 
    filename_json= "data.json"
    open_json(filename_json) 

elif specified_format == "csv": 
    None

elif filepath != None and filetype =="json":  
    filename_json= output_file
    open_json(filename_json) 

if filepath == None: 
    filename_json= "data.json"
    change_output == True
    open_json(filename_json)
