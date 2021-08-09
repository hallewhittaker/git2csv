#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import subprocess
r= subprocess.run('git --no-pager blame --line-porcelain README.md',stdout= subprocess.PIPE)

standard_out = r.stdout
# tab = standard_out.split(b'\t')

arrayofDictionaries = []

# for lineinfoS in tab:

# {'Hash': 'd6b24e6dec9eca5db2acfcb393a62146f640759f', 'CommitLinesN': {'originalLine': 10, 'finalLine': 25}, 'author': 'hallewhittaker', 'author-mail': '<88335095+hallewhittaker@users.noreply.github.com>', 'author-time': '1627917128', 'author-tz': '+0100', 'committer': 'GitHub', 'committer-mail': '<noreply@github.com>', 'committer-time': '1627917128', 'committer-tz': '+0100', 'summary': 'Create README.md', 'boundary': '', 'filename': 'README.md', '\t-': 'Halle says Hi!', 'previous': '0755943ff1734715bfe150143982bc9ce02562d8 README.md', '\t': '', '\tIf': 'I add these lines of code, I have to manually commit it to github?!', '\tAnswer:': 'Yes.', '\t<!---': '', '\thallewhittaker/hallewhittaker': 'is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.', '\tYou': 'can click the Preview link to take a look at your changes.', '\t--->': ''}]

# 6b24e6dec9eca5db2acfcb393a62146f640759f
# author        
# author-mail   
# author-time   
# author-tz     
# committer     
# committer-mail
# committer-time
# committer-tz  
# summary       
# boundary      
# filename      
# \t



linearray = standard_out.split(b'\n') 

count = 0
tempdictionary = {}
for individL in linearray:
    individL = individL.decode("utf-8")
    splitline = individL.split(" ") # might not always be needed for every line, but probably easier to do it anyway =) eg: tab iteration case won't need to split on the spaces, it'll split on the tab :) 

    temp_key_name = splitline[0]

    print("Count is currently " + str(count))
    print(individL)

    first_word_removed = splitline.copy()
    first_word_removed[0] = " "
    first_word_removed = " ".join(first_word_removed).lstrip()

    if count == 0:
        tempdictionary["Hash"] = temp_key_name
    elif count == 1 or count == 2 or count == 3:
        tempdictionary[temp_key_name] = first_word_removed
    # elif count == 2:
    #     tempdictionary[splitline[0]] = first_word_removed
    # elif count == 3:
    #     tempdictionary[splitline[0]] = first_word_removed
    
    
    

    


    count += 1 # generally easier to have at the end
    if count >= 13: #using >= attempts to limit issues (defensive programming)
        arrayofDictionaries.append(tempdictionary)
        tempdictionary = {} # not technically needed, but probably easier for debugging and learning
        count = 0

print("Final arrayofDictionaries = " + str(arrayofDictionaries))

# tempdictionary = {}

# count = 0
# for individL in linearray:
#     count += 1
#     individL = individL.decode("utf-8") # Could we maybe have a counter of some sort? Hash always 1st entry on Individl
#     splitline = individL.split(" ") 

#     #if count == 1:
#     #   print(individL)
    
#     #print(count)
#     # for some reason it goes 1 to 13 (correct) then 1 to 14??  
        

#     # if count == 2:
#     #     print(individL)

    
#     # if count == 1:
#     #     print(individL)
#     #Here the 1 shows all of the text seen in the document + the intial hash value
#     #Here the 2 shows all of the hash values in the document except the first one + Commit lines
        
#     if len(str(splitline[0])) == 40: # What if another line happens to be 40 chars? =P
#         tempdictionary["Hash"] = splitline[0]
#         Number2D = splitline[0]
        
#     for key,value in dict(tempdictionary).items():
#         if key == Number2D:
#             x= value.split(" ")
#             for i in range(0, len(x)):
#                 x[i] = int(x[i])
#             if len(x) == 3:
#                 tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[1], 'groupLine' : x[2]}
#             else:
#                 tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[1] } 
#             del tempdictionary[key] 

#         testkey = list(tempdictionary.keys())[0]  
#         if testkey != "Hash":
#             tempdictionary["Changed"] = tempdictionary[testkey]
#             del tempdictionary[testkey]

#     tempkeyN = splitline[0]
#     # print(tempkeyN)
#     if tempkeyN == '\t-': 
#         tempdictionary["Message"] = splitline[1]
#         #del tempkeyN
#     else:
#         splitline[0] = " "
#         joinline = " ".join(splitline).lstrip()
#         tempdictionary[tempkeyN] = joinline
# arrayofDictionaries.append(tempdictionary)
# #break
# print(arrayofDictionaries)




 

# print(test1)

# count = 0
# for i in test1:
#     if i == ('\n'):
#         count += 1

# while count == 13:
#     print (str(test1[12]) + "\t")
        
# print(count)

# # x= test1.split('\n')
# # print(x)

# # nlines = test1.count('\n')
# # print(nlines)





#1 =13
#b'd6b24e6dec9eca5db2acfcb393a62146f640759f 1 1 1
# \nauthor hallewhittaker
# \nauthor-mail <88335095+hallewhittaker@users.noreply.github.com>
# \nauthor-time 1627917128
# \nauthor-tz +0100
# \ncommitter GitHub
# \ncommitter-mail <noreply@github.com>
# \ncommitter-time 1627917128
# \ncommitter-tz +0100
# \nsummary Create README.md
# \nboundary
# \nfilename README.md
# \n\t- \xf0\x9f\x91\x8b Hi, I\xe2\x80\x99m @hallewhittaker
# \n

#2=13
#0755943ff1734715bfe150143982bc9ce02562d8 2 2 4
# \nauthor hallewhittaker
# \nauthor-mail <88335095+hallewhittaker@users.noreply.github.com>
# \nauthor-time 1627919610
# \nauthor-tz +0100
# \ncommitter GitHub
# \ncommitter-mail <noreply@github.com>
# \ncommitter-time 1627919610
# \ncommitter-tz +0100
# \nsummary Halle added additional information.
# \nprevious d5e223cc949db03d3a8ad3b42d9451413a7181d4 README.md
# \nfilename README.md
# \n\t- \xf0\x9f\x91\x80 I\xe2\x80\x99m interested in everything IT!
# \n

#3= 13
#0755943ff1734715bfe150143982bc9ce02562d8 3 3
# \nauthor hallewhittaker
# \nauthor-mail <88335095+hallewhittaker@users.noreply.github.com>
# \nauthor-time 1627919610
# \nauthor-tz +0100
# \ncommitter GitHub
# \ncommitter-mail <noreply@github.com>
# \ncommitter-time 1627919610
# \ncommitter-tz +0100
# \nsummary Halle added additional information.
# \nprevious d5e223cc949db03d3a8ad3b42d9451413a7181d4 README.md
# \nfilename README.md
# \n\t- \xf0\x9f\x8c\xb1 I\xe2\x80\x99m currently learning how to spot security vulnerabilities in source code.
# \n




# test_list = ['1', '4', '3', '6', '7']
  
# for i in range(0, len(test_list)):
#     test_list[i] = int(test_list[i])
      
# print(test_list)

# count = 0
# for i in x:
# count += 1
# if count == 3:
# tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[1], 'groupLine' : x[2]}
# if count == 2:
#     tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[1], 'groupLine' : " " } 


#Count digits calculator
# str = "If I add these lines of code, does it automatically update on github?!"
# digit=letter=0
# for ch in str:
#    if ch.isdigit():
#       digit=digit+1
#    elif ch.isalpha():
#       letter=letter+1
#    else:
#       pass
# print("Letters:", letter)
# print("Digits:", digit)

#Code in progress for CommitLines
        # for x in joinline:
        #     if x in joinline == ('1 1 1'):
        #         tempdictionary["CommitLinesN"] = joinline
        # for x in joinline:
#Manual Splitline
# if i in splitline[0] ==('d6b24e6dec9eca5db2acfcb393a62146f640759f'): 
#     tempdictionary["Hash"] = splitline[0]

#Manual Deltion of Hash
# for key,value in dict(tempdictionary).items():
#     if key == ('d6b24e6dec9eca5db2acfcb393a62146f640759f'):
#             del tempdictionary[key]

#Automated Checking of Hash
#for i in splitline[0]:
#    if len(str(splitline[0])) == 40:
#               tempdictionary["Hash"] = splitline[0]
#Automated Deletion of stuff
# for key,value in dict(tempdictionary).items():
#               if key == Number2D:
#                    del tempdictionary[key]

#Using Dictionaries
# testdictionary1= {"email": "whittaker@gmail.com", "message": "hello welcom"}
# testdictionary2= {"email": "like@gmail.com", "message": "bye welcom"}

# #print(testdictionary1["email"])
# arrayofD= [testdictionary1,testdictionary2]

# #print(arrayofD)

# for currentDictionary in arrayofD:
# print(currentDictionary["email"])


#if str(arrayofDictionaries) == "[{b'author': b'hallewhittaker', b'author-mail': b'<88335095+hallewhittaker@users.noreply.github.com>', b'author-time': b'1627917128', b'author-tz': b'+0100', b'committer': b'GitHub', b'committer-mail': b'<noreply@github.com>', b'committer-time': b'1627917128', b'committer-tz': b'+0100', b'summary': b'Create README.md', b'boundary': b'', b'filename': b'README.md', b'': b''}, {b'--->': b'', b\"'\": b''}]":
#    print("passed!")
# else:
#    print("FAILED!!!!")

# test_data = b"author hallewhittaker\nauthor-mail <88335095+hallewhittaker@users.noreply.github.com>\nauthor-time 1627917128\nauthor-tz +0100\ncommitter GitHub\ncommitter-mail <noreply@github.com>\ncommitter-time 1627917128\ncommitter-tz +0100\nsummary Create README.md\nboundary\nfilename README.md\n\t--->\n'"
# tab = test_data.split(b'\t') 

#Using re.split
# cheader =[]
# cdata = []

# import re
# a="b'filename README.md'" #work
# b="b'boundary'" #work
# c="b'author-mail <88335095+hallewhittaker@users.noreply.github.com>'" #work

# #pattern = r"\s+|[']|'(?=\s)"
# result = [s for s in re.split(pattern, c) if s]
# print(result)

# cheader.append(result[1])
# print(cheader)

# if len(result) >2:
#     cdata.append(result[2])       
# else:
#     cdata.append('N/A')
# print(cdata) 
#currently uses a string, splits said string into column header + data