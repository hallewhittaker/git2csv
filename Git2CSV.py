#!/usr/bin/env python3
#-*- coding: utf-8 -*-
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

for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),stdout= subprocess.PIPE)
    standard_out = r.stdout
    arrayofDictionaries = []
    linearray = standard_out.split(b'\n') 

    #Fixing line dictionary issues
    # The phase after of the project , will be writing the data out to a csv file.

    count = 0
    tempdictionary = {}
    for individL in linearray:
        individL = individL.decode("utf-8")
        splitline = individL.split(" ") # might not always be needed for every line, but probably easier to do it anyway =) eg: tab iteration case won't need to split on the spaces, it'll split on the tab :) 

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

        elif count >= 1 and count <= 11:
            if count == 3:
                # int_time_author= int(first_word_removed)
                # date_author_time = datetime.datetime.fromtimestamp(int_time_author)  
                # new_format = date_author_time.strftime('%Y-%m-%d %H:%M:%S')
                tempdictionary["author-time"] = first_word_removed

            elif count == 4:
                # authortz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                # new_atz = datetime.timezone.tzname( authortz, None )
                tempdictionary["author-tz"] = first_word_removed
    
            elif count == 7:
                # int_time_commiter= int(first_word_removed)
                # date_commiter_time = datetime.datetime.fromtimestamp(int_time_commiter)  
                # new_format2 = date_commiter_time.strftime('%Y-%m-%d-%H:%M:%S') 
                tempdictionary["commiter-time"] = first_word_removed

            elif count == 8:
                # commitertz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                # new_ctz = datetime.timezone.tzname( commitertz, None )
                # tempdictionary["commiter-tz"] = new_ctz
                tempdictionary["commiter-tz"] = first_word_removed

            else:
                tempdictionary[temp_key_name] = first_word_removed

        elif count == 12:
            commit_content_text = individL
            if commit_content_text[0:2] == '\t-':
                slice_string = commit_content_text[3:]
                tempdictionary["commit_content"] = slice_string.lstrip()
            elif commit_content_text[0:1] == "\t":
                slice_string = commit_content_text[1:]
                tempdictionary["commit_content"] = slice_string.lstrip()
            else:
                tempdictionary["commit_content"] = commit_content_text.lstrip()

        count += 1 # generally easier to have at the end
        if count >= 13: #using >= attempts to limit issues (defensive programming)
            arrayofDictionaries.append(tempdictionary)
            tempdictionary = {} # not technically needed, but probably easier for debugging and learning
            count = 0
    print("Final arrayofDictionaries = " + str(arrayofDictionaries))














#authordate =  datetime.datetime.strptime(new_format, '%Y-%m-%d %H:%M:%S').date()
#authortime = datetime.datetime.strptime(new_format, '%Y-%m-%d %H:%M:%S').time()
#mydatetz = datetime.datetime.combine(authordate, authortime, authortz)

#Git LS
# x= subprocess.run('git ls-tree -r main --name-only',stdout= subprocess.PIPE)
# print(x.stdout)
# y= subprocess.run('git log --pretty=format: --name-only --diff-filter=A', stdout= subprocess.PIPE)
# print(y.stdout)


 # tempauthordate = mydatetz.replace(tzinfo= authortz)
# new_format5 = tempauthordate#.strftime('%z') 
    #new_tz = datetime.timezone.tzname( authortz, None )
    #tempdictionary["author-tz"] = new_tz

# tempauthordate = date_author_time 
# tempauthordate = tempauthordate.replace(tzinfo= authortz)
# new_format5 = tempauthordate.strftime('%Y-%m-%d %H:%M:%S %z')
# tempdictionary["author-tz"] = new_format5

# tempauthordate = tempdictionary["author-time"] 
# tempauthordate = tempauthordate.replace(tzinfo=datetime.timezone.utc)
# tempdictionary["author-tz"] = tempauthordate









# dt = datetime.datetime.now()
#             dt = dt.replace(tzinfo=datetime.timezone.utc)
#             tempdictionary["author-tz"] = (dt.isoformat())



 # new_format.add_time_zone_info(first_word_removed) # This is not a real function!

            # Goal: have the timezone added (not just as a string like it currently is)
            #new_format = new_format.replace(tzinfo=datetime.timezone.utc)# TODO: Actually parse the timezone instead of blindly using utc!, ADD timezone info to author time

            # Line below is optional, up to you if you keep it
            # tempdictionary["author-tz"] = convert_to_timezone(first_word_removed) # TODO: Make this a timezone object! 
            # new_format = new_format.replace(tzinfo=to_timezome(first_word_removed))





















#datetime.datetime(1900, 1, 1, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)))
#'+0100'
#'+01:00:00'

# new_format_that_is_aware_of_timezone = datetime_with_timezone(new_format, )

            # new_format = new_format_that_is_aware_of_timezone


            # tempdictionary[""]
            # x= datetime.timezone(datetime.timedelta(hours=24), first_word_removed)
            #int_tz_author= int(first_word_removed)
            # date_author_tz = datetime.timezone(datetime.timedelta(hours=24))
            #x= datetime.datetime(int_tz_author, tzinfo=datetime.timezone.utc)

            #x= datetime.datetime.strptime(first_word_removed, '%z')
            #datetime_object = datetime.datetime.strptime(first_word_removed, '%z')

            #date_author_time = tempdictionary["commit-time"]
    
            # tempdictionary[temp_key_name] = first_word_removed 
            # this is just to prevent the syntax highlighter from giving us an error at the moment
            # pass # remove this line as soon as you add any code above :) 


#'hash': 'd6b24e6dec9eca5db2acfcb393a62146f640759f', 
# 'CommitLinesN': {'originalLine': 1, 'finalLine': 1, 'groupLine': 1}, 
# 'author': 'hallewhittaker', 
# 'author-mail': '<88335095+hallewhittaker@users.noreply.github.com>', 
# 'author-time': '1627917128',  THIS
# 'author-tz': '+0100', THIS
# 'committer': 'GitHub',
# 'committer-mail': '<noreply@github.com>', 
# 'committer-time': '1627917128',  THIS
# 'committer-tz': '+0100', ' THIS
# summary': 'Create README.md',
#  'boundary': '', 
# 'filename': 'README.md',
#  'commit_content': '👋 Hi, I’m @hallewhittaker'}


# elif count == 1 or count == 2 or count == 3 or count == 4 or count == 5 or count == 6 or count == 7 or count == 8 or count == 9 or count == 10 or count == 11:
#elif count >= 1 and count <= 11:

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