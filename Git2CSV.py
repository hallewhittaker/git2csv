#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import os 
import sys
import csv
import datetime
import subprocess
import argparse
import copy

parser = argparse.ArgumentParser()
parser.add_argument('--format', type=str, help = "format used for file", action= "store") #just this -- for formatfuzzer
parser.add_argument('--filelist', type=str, help= "files to run (exclude binary files)", action="store")
parser.add_argument('--overwrite_existing', help= "overwrite the existing file",  action='store_true', default=False) 
parser.add_argument('filepath', type=str, help = "filepath of program", action= "store") #need all -- for my repo 
parser.add_argument('output_file', type=str, action= "store", help = "output filename") 
args = parser.parse_args()

filepath = args.filepath 
output_file = args.output_file
specified_format = args.format
list_of_files = args.filelist
overwrite_boolean = args.overwrite_existing

# TODO Remove Print Statement/ Adjust Logic
# TODO (#5): Instead of using print, let's use the logging module in python.
# https://docs.python.org/3/howto/logging.html
# Also add a new flag that allows use to set the debugging level
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer --format csv --debugging-level DEBUG TestCSV.csv

mydir = os.getcwd()
mydir_static_copy = copy.copy(mydir)

if overwrite_boolean == False:
    filename_ = output_file
    isExist= os.path.exists(mydir_static_copy + '\\{}'.format(filename_))
    if isExist == True:
        print("File Already Exists")
        raise Exception ("To Do")
    else:
        None

if filepath != None:
    mydir_tmp = filepath #"C:\Users\Whitt\hallewhittaker\FormatFuzzer"
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd() 
else:
    mydir_tmp = mydir_static_copy #"C:\\Users\\Whitt\\hallewhittaker" 
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd()

if list_of_files != None:
    finalArray = []
    filename_txt = list_of_files
    with open(mydir_static_copy + '\\{}'.format(filename_txt), "r", encoding='ISO-8859-1', newline='') as f:
        content_lines = f.readlines()
        for i in content_lines:
            splitvalues= i.split('\r\n')
            finalArray.append(splitvalues[0])    
else:
    z= subprocess.run('git ls-tree --full-tree --name-only -r HEAD', stdout= subprocess.PIPE)
    stan_out = z.stdout
    finalArray = []
    filearray = stan_out.split(b'\n')
    for i in filearray:
        x= i.decode("utf-8")
        finalArray.append(x)
    finalArray.remove("")

arrayofDictionaries = []
for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),stdout= subprocess.PIPE)
    standard_out = r.stdout
    linearray = standard_out.split(b'\n') 

    # Change this to be like logging.debugging instead of print
    # print("Current length of dictionary: " + str(len(arrayofDictionaries)))
    # print("We're currently analyzing the file: " + finalArray[i])

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
    #print("Final Array:" + str(arrayofDictionaries))
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

if filepath != None and overwrite_boolean ==True and specified_format =="csv": #dealing with overwrites
    filename_csv = "TestCSV.csv"
    isExist = os.path.exists(mydir_static_copy + '\\{}'.format(filename_csv))
    if isExist == True:
        with open(mydir_static_copy + '\\{}'.format(filename_csv), "w+", encoding='ISO-8859-1', newline='') as sys.stdout:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

if filepath != None and specified_format == None and filetype != "csv" and filetype != "json": #no format, no filetype csv=default
    filename_csv = output_file
    with open(mydir_static_copy + '\\{}'.format(filename_csv), "w", encoding='ISO-8859-1', newline='') as sys.stdout:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

if filepath != None and specified_format == "csv" and output_file == '-': #stdout
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

filename_csvE = output_file
isExist1 = os.path.exists(mydir_static_copy + '\\{}'.format(filename_csvE))
if filepath != None and specified_format == "csv" and isExist1 == False: # format is csv and output file doesnt exist
    with open(mydir_static_copy + '\\{}'.format(filename_csvE), "w", encoding='ISO-8859-1', newline='') as sys.stdout:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

elif filepath != None and specified_format == "csv": #format first priority
    filename_csv= "TestCSV.csv"
    isExist = os.path.exists(mydir_static_copy + '\\{}'.format(filename_csv))
    if isExist == True and overwrite_boolean ==False:
        print("You are attempting to overwrite a file that already exists, use --overwrite_existing to perform this action (csv elif 1)")
    else:
        with open(mydir_static_copy + '\\{}'.format(filename_csv), "w", encoding='ISO-8859-1', newline='') as sys.stdout:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

elif specified_format == "json": #if format json, nothing
    None

elif filepath != None and filetype == "csv": #filetype second priority 
    filename_csv = output_file
    isExist = os.path.exists(mydir_static_copy + '\\{}'.format(filename_csv))
    if isExist == True and overwrite_boolean ==False:
        print("You are attempting to overwrite a file that already exists, use --overwrite_existing to perform this action (csv elif 2)")
    else:
        with open(mydir_static_copy + '\\{}'.format(filename_csv), "w", encoding='ISO-8859-1', newline='') as sys.stdout:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

if filepath == None: #no arguments
    filename_csv = 'TestCSV.csv'
    with open(mydir_static_copy + '\\{}'.format(filename_csv), 'w', encoding='ISO-8859-1', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

#JSON
if filepath != None and overwrite_boolean ==True and specified_format== "json": #dealing with overwriting
    filename_json = "data.json"
    isExist = os.path.exists(mydir_static_copy + '\\{}'.format(filename_json))
    if isExist == True:
        with open(mydir_static_copy + '\\{}'.format(filename_json), "w+", encoding='ISO-8859-1', newline='')  as sys.stdout:
            sys.stdout.write(jsonstring)

if filepath != None and specified_format == "json" and output_file == '-': #stdout 
    sys.stdout.write(jsonstring)
    sys.stdout.close()

filename_jsonE = output_file
isExist2 = os.path.exists(mydir_static_copy + '\\{}'.format(filename_jsonE))
if filepath != None and specified_format == "json" and isExist2 == False: # format json and filename doesnt exist
    with open(mydir_static_copy + '\\{}'.format(filename_jsonE), "w", encoding='ISO-8859-1', newline='')  as sys.stdout:
            sys.stdout.write(jsonstring)

elif filepath != None and  specified_format == "json": #specifying format first
    filename_json= "data.json"
    isExist = os.path.exists(mydir_static_copy + '\\{}'.format(filename_json))
    if isExist == True and overwrite_boolean ==False:
        print("You are attempting to overwrite a file that already exists, use --overwrite_existing to perform this action (elif 1)")
    else:
        with open(mydir_static_copy + '\\{}'.format(filename_json), "w", encoding='ISO-8859-1', newline='')  as sys.stdout:
            sys.stdout.write(jsonstring) 

elif specified_format == "csv": #if csv do nothing.
    None

elif filepath != None and  filetype =="json": #specifying filetype second priority
    filename_json= output_file
    isExist = os.path.exists(mydir_static_copy + '\\{}'.format(filename_json))
    if isExist == True and overwrite_boolean ==False:
        print("You are attempting to overwrite a file that already exists, use --overwrite_existing to perform this action (elif 2)")
    else:
        with open(mydir_static_copy + '\\{}'.format(filename_json), "w", encoding='ISO-8859-1', newline='')  as sys.stdout:
            sys.stdout.write(jsonstring) 

if filepath == None: # no arguments entered
    filename_json= "data.json"
    with open(mydir_static_copy + '\\{}'.format(filename_json), "w", encoding='ISO-8859-1', newline='')  as jsonFile:   
        jsonFile.write(jsonstring)









#TensureFlow Fix (let's not do this yet)
#Fix commit lines to 1,1,1

#JSON
#py Git2CSV.py --format json C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.txt (working) PRINT JSON
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json (working)
#py Git2CSV.py --format json C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv (working) PRINT JSON

#CSV 
#py Git2CSV.py --format csv C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json (working) PRINT CSV
#py Git2CSV.py --format csv C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.txt (working) PRINT CSV in TXT file doesnt care for overwright
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv  (working)

#Stdout
#py Git2CSV.py --format json C:\Users\Whitt\hallewhittaker\FormatFuzzer - (working)
#py Git2CSV.py --format csv C:\Users\Whitt\hallewhittaker\FormatFuzzer - (working)
#py Git2CSV.py --format csv --filelist ListofFiles.txt C:\Users\Whitt\hallewhittaker\FormatFuzzer - > TestCSV.csv (working)
#py Git2CSV.py --format json --filelist ListofFiles.txt C:\Users\Whitt\hallewhittaker\FormatFuzzer - > data.json (working)

#JSON Overwriting
#py Git2CSV.py --format json --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json (works)
#py Git2CSV.py --format json --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv (works) 
#py Git2CSV.py --format json --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.txt (works)
#py Git2CSV.py --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json (works) 
#py Git2CSV.py --format json C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.txt (Works as expected, json in next output file)

#CSV Overwriting 
#py Git2CSV.py --format csv --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json (works)
#py Git2CSV.py --format csv --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv (works) 
#py Git2CSV.py --format csv --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.txt (works)
#py Git2CSV.py --overwrite_existing C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv (works) 
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer data.txt (Works as expected, csv in new output file )

