#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import os 
import sys
import csv
import datetime
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str, help = "filepath of program", action= "store")
parser.add_argument('--format', type=str, help = "format used for file", action= "store")
parser.add_argument('output_file', type=str, action= "store", help = "output filename")
args = parser.parse_args()

filepath = args.filepath 
output_file = args.output_file
specified_format = args.format

if filepath != None:
    mydir = os.getcwd() 
    mydir_tmp = filepath
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd() 
else:
    mydir = os.getcwd() 
    mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" 
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd()

# TODO (#3): If the user specifies --stdout AND the format, then write the output to stdout and NOT a file
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer --format json --stdout
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer --format csv --stdout

# Examples of equivalent commands (if you have questions or are confused at all, please ask!):
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer --format csv --stdout > TestCSV.csv # everything from the ">" and beyond is handled already by the operating system
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer --format csv TestCSV.csv

# Made-up example of where it would be useful (this won't actually work, don't worry about it much yet):
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer --format json --stdout | tensorflow_script.py # pipe our output right to a tensorflow script, and avoid writing to disk


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

if specified_format == "csv":
    filename_csv = "TestCSV.csv"
    with open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_csv), "w+", encoding='ISO-8859-1', newline='') as sys.stdout:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
elif specified_format == "json":
    None
elif filetype == "csv":
    filename_csv = output_file
    with open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_csv), "w+", encoding='ISO-8859-1', newline='') as sys.stdout:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
else: 
    filename_csv = 'TestCSV.csv'
    with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if specified_format == "json":
    filename_json= "data.json"
    sys.stdout = open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_json), "w+", encoding='ISO-8859-1', newline='') 
    sys.stdout.write(jsonstring) 
elif specified_format == "csv":
    None
elif filetype =="json":
    filename_json= output_file
    sys.stdout = open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_json), "w+", encoding='ISO-8859-1', newline='') 
    sys.stdout.write(jsonstring) 
    sys.stdout.close() 
else:
    filename_json= "data.json"
    jsonFile = open(filename_json, "w+")
    jsonFile.write(jsonstring)
    jsonFile.close()













#arrayofDictionaries.append(tempdictionary.copy()) #Temp dictionary copy was not needed, i ran it regularly versus using copy. Regularly worked perfectly (compared output to be sure)

#TensureFlow Fix (let's not do this yet)
#Fix commit lines to 1,1,1

#Manual Directory Paths
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker\\FormatFuzzer" #runs formatfuzzer
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" #runs Git2CSV

#Commands to specify folder
# py Git2CSV.py C:\Users\Whitt\hallewhittaker 
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer 

#Further Commands to Specify Output
#py Git2CSV.py --filepath C:\Users\Whitt\hallewhittaker\FormatFuzzer --output_file data.json (use me)
#py Git2CSV.py --filepath C:\Users\Whitt\hallewhittaker\FormatFuzzer --output_file TestCSV.csv (use me)
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json   (works)
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv (works)

#Previous Code:
# if output_file != None and (specified_format == "csv" or filetype =="csv"):
#     filename_csv= output_file
#     with open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_csv), "w+", encoding='ISO-8859-1', newline='') as sys.stdout:
#         writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)  
# else: 
#     filename_csv = 'TestCSV.csv'
#     with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: 
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)

# if output_file != None (specified_format == "json" or filetype =="json"):
#     filename_json= output_file
#     sys.stdout = open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_json), "w+", encoding='ISO-8859-1', newline='') 
#     sys.stdout.write(jsonstring) 
#     sys.stdout.close() 
# else:
#     filename_json= "data.json"
#     jsonFile = open(filename_json, "w+")
#     jsonFile.write(jsonstring)
#     jsonFile.close()