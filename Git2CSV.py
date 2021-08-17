#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import os 
import sys
import csv
import datetime
import subprocess

n = len(sys.argv)
 
if len(sys.argv) > 1:
    mydir = os.getcwd() 
    mydir_tmp = sys.argv[1]
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd() 
else:
    mydir = os.getcwd() 
    mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" # TODO: Figure out why it's not working :p 
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd()


z= subprocess.run('git ls-tree --full-tree --name-only -r HEAD', stdout= subprocess.PIPE)
stan_out = z.stdout

finalArray = []
filearray = stan_out.split(b'\n')

for i in filearray:
    x= i.decode("utf-8")
    finalArray.append(x)
finalArray.remove("")

for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),stdout= subprocess.PIPE)
    standard_out = r.stdout
    arrayofDictionaries = []
    linearray = standard_out.split(b'\n') 

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
        #break
    print("Final Array:" + str(arrayofDictionaries))

def myconverter(k):
    if isinstance(k, datetime.datetime):
        return k.__repr__()
jsonstring= json.dumps(arrayofDictionaries, default = myconverter)

fieldnames = ['hash','CommitLinesN', 'author','author-mail','author-time','author-tz','committer','committer-mail', 'commiter-time','commiter-tz','summary', 'previous', 'boundary', 'filename','commit_content']
rows = arrayofDictionaries

try:
    filetype = sys.argv[2].split(".")
except:
    None

if len(sys.argv) > 2 and filetype == "csv":
    csv_output = filetype[1]

    filename_csv = csv_output #sys.argv[2]
    with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: # woot woot, this looks good!
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
else: 
    filename_csv = 'TestCSV.csv'
    with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

try:
    filetype1 = sys.argv[2].split(".") 
except:
    None
  
if len(sys.argv) > 2 and filetype1 == "json":
    json_output = filetype1[1]

    filename_json= json_output #sys.argv[2]
    jsonFile = open(filename_json, "w+")
    jsonFile.write(jsonstring)
    jsonFile.close()
else:
    filename_json= "data.json"
    jsonFile = open(filename_json, "w+")
    jsonFile.write(jsonstring)
    jsonFile.close()

#Task 4
#Why isnt it writing the same way as README.md?? (csv)

#Task 5
#Why isnt it writing the same way as README.md?? (json)


#Manual Directory Paths
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker\\FormatFuzzer" #runs formatfuzzer
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" #runs Git2CSV

#Commands to specify folder
# py Git2CSV.py C:\Users\Whitt\hallewhittaker 
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer 

#Commands to specify output
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer  2>&1 | tee data.json
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer > data.json 
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer  2>&1 | tee TestCSV.csv
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer > TestCSV.csv 

#Further Commands to Specify Output
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json 
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer > data.json (use me)

#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer > TestCSV.csv  (use me)
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv





#Previous Code:
# if len(sys.argv) > 2:
#     filename_json= json_output #sys.argv[2]
#     jsonFile = open(filename_json, "w+")
#     jsonFile.write(jsonstring)
# else:
#     filename_json= "data.json"
#     jsonFile = open(filename_json, "w+")
#     jsonFile.write(jsonstring)
# jsonFile.close()
  
# fieldnames = ['hash','CommitLinesN', 'author','author-mail','author-time','author-tz','committer','committer-mail', 'commiter-time','commiter-tz','summary', 'previous', 'boundary', 'filename','commit_content']
# rows = arrayofDictionaries

# if len(sys.argv) > 2:
#     filename_csv = csv_output #sys.argv[2]
#     with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: # woot woot, this looks good!
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)
# else:
#     filename_csv = 'TestCSV.csv'
#     with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: 
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)