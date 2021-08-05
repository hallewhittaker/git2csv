import subprocess
r= subprocess.run('git --no-pager blame --line-porcelain README.md',stdout= subprocess.PIPE)

tab = r.stdout.split(b'\t') 
arrayofDictionaries = []


for lineinfoS in tab:
    linearray= lineinfoS.split(b'\n')
    tempdictionary = {}
    
    for individL in linearray:
        individL = individL.decode("utf-8")
        splitline = individL.split(" ")  # Could we maybe have a counter of some sort? Since "Hash" is always the "first" entry in individL

        if len(str(splitline[0])) == 40: # What if another line happens to be 40 chars? =P
            tempdictionary["Hash"] = splitline[0]
            Number2D = splitline[0]

        for key,value in dict(tempdictionary).items():
            if key == Number2D:

                x= value.split(" ")
                for i in range(0, len(x)):
                    x[i] = int(x[i])
                if len(x) == 3:
                    tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[1], 'groupLine' : x[2]}
                else:
                    tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[1], 'groupLine' : '' } 

                del tempdictionary[key]
                
            testkey = list(tempdictionary.keys())[0]  
            if testkey != "Hash":
                del tempdictionary[testkey]

        tempkeyN = splitline[0] # Maybe if the tempkeyN is equal to " " or "", don't add it =) 
        splitline[0] = " "
        joinline = " ".join(splitline).lstrip()
        tempdictionary[tempkeyN] = joinline
    arrayofDictionaries.append(tempdictionary)    
print(arrayofDictionaries)






















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

#Starting Conditions
# for key,value in dict(tempdictionary).items():
#             if key == Number2D:
#                 for singleN in value:
#                     x = singleN.split(" ")
#                     tempdictionary["CommitLinesN"] = {'originalLine': x[0], 'finalLine': x[0], 'groupLine' : x[0]}
#                 del tempdictionary[key]
                
#             testkey = list(tempdictionary.keys())[0]  
#             if testkey != "Hash":
#                 del tempdictionary[testkey]





#Count digits calculator
# str = "👋 Hi, I’m @hallewhittaker"
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