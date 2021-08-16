#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# The phase after of the project , will be writing the data out to a csv file.

import datetime
import subprocess

z= subprocess.run('git ls-tree --full-tree --name-only -r HEAD', stdout= subprocess.PIPE)
stan_out = z.stdout

finalArray = []
filearray = stan_out.split(b'\n')

for i in filearray:
    x= i.decode("utf-8")
    finalArray.append(x)
finalArray.remove("")

#finalArray = ["README.md"]
#finalArray = ["Git2CSV.py"]
finalArray = ["Hello.py"]

for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),stdout= subprocess.PIPE)
    standard_out = r.stdout
    arrayofDictionaries = []
    linearray = standard_out.split(b'\n') 

    count = 0
    tempdictionary = {}
    for individL in linearray:
        individL = individL.decode("utf-8")
        splitline = individL.split(" ") 

        temp_key_name = splitline[0]
        first_word_removed = splitline.copy()
        first_word_removed[0] = " "
        first_word_removed = " ".join(first_word_removed).lstrip()

        # print(individL)
        #print("Adding key=" + temp_key_name + " at count=" + str(count) + " with first_word_removed=" + first_word_removed)

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
        
            # commit_content_text = individL
        elif count >= 1 and count <= 12:
            if count == 3:
                # int_time_author= int(first_word_removed)
                # date_author_time = datetime.datetime.fromtimestamp(int_time_author)  
                
                # new_format = date_author_time.strftime('%Y-%m-%d %H:%M:%S')
                # tempdictionary["author-time"] = new_format
                
                # tempdictionary["author-time"] = date_author_time #native datetime
                
                tempdictionary["author-time"] = first_word_removed
            elif count == 4:
                # authortz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                # new_atz = datetime.timezone.tzname( authortz, None )
                # tempdictionary["author-tz"] = new_atz
                # tempdictionary["author-time"].replace(tzinfo=authortz)
                
                tempdictionary["author-tz"] = first_word_removed
            elif count == 7:
                # int_time_commiter= int(first_word_removed)
                # date_commiter_time = datetime.datetime.fromtimestamp(int_time_commiter)
                  
                #new_format2 = date_commiter_time.strftime('%Y-%m-%d-%H:%M:%S') 
                #tempdictionary["commiter-time"] = new_format2
                
                #tempdictionary["commiter-time"] = date_commiter_time
                tempdictionary["commiter-time"] = first_word_removed
            elif count == 8:
                # commitertz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                # new_ctz = datetime.timezone.tzname( commitertz, None )
                # tempdictionary["commiter-tz"] = new_ctz
                # tempdictionary["commiter-time"].replace(tzinfo=commitertz)
                tempdictionary["commiter-tz"] = first_word_removed
            
            elif individL[0:1] == '\t':
                slice_string = individL[1:]
                tempdictionary["commit_content"] = slice_string
                arrayofDictionaries.append(tempdictionary)
                tempdictionary = {} # not technically needed, but probably easier for debugging and learning
                count = -1 
            # elif ((count == 12) and ("boundary" in tempdictionary) or ("previous" in tempdictionary)):
            #     commit_content_text = individL
            #     slice_string = commit_content_text[1:]
            #     tempdictionary["commit_content"] = slice_string
            else:
                tempdictionary[temp_key_name] = first_word_removed
               
        count += 1
        # if count >= 13: 
            
    print("Final Array:" + str(arrayofDictionaries))