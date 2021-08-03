import subprocess
# r= subprocess.run('git --no-pager blame --line-porcelain README.md',s stdout= subprocess.PIPE)
#currently uses system command line to read a specific document.

# tab = r.stdout.split(b'\t') 
# print(r.stdout)

test_data = b"author hallewhittaker\nauthor-mail <88335095+hallewhittaker@users.noreply.github.com>\nauthor-time 1627917128\nauthor-tz +0100\ncommitter GitHub\ncommitter-mail <noreply@github.com>\ncommitter-time 1627917128\ncommitter-tz +0100\nsummary Create README.md\nboundary\nfilename README.md\n\t--->\n'"
tab = test_data.split(b'\t') 

arrayofDictionaries = []
# current string = b'author': b'author hallewhittaker' .split(b" ")[0]
# new string = b'author': hallewhittaker'
#b'author hallewhittaker': b'author hallewhittaker' without .split

for lineinfoS in tab:
    #print(lineinfoS)
    #print("----")
    linearray= lineinfoS.split(b'\n')
    tempdictionary = {}

    for individL in linearray:
        #print(individL)
        splitline = individL.split(b" ")
        tempkeyN = splitline[0]
        #print(splitline) 
        splitline[0] = b" "
        
        joinline = b" ".join(splitline)
        #print(joinline)
        tempdictionary[tempkeyN] = joinline
    arrayofDictionaries.append(tempdictionary)
print(arrayofDictionaries)








#print(tempkeyN)

        #print("____")



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

#Using Dictionaries
# testdictionary1= {"email": "whittaker@gmail.com", "message": "hello welcom"}
# testdictionary2= {"email": "like@gmail.com", "message": "bye welcom"}

# #print(testdictionary1["email"])
# arrayofD= [testdictionary1,testdictionary2]

# #print(arrayofD)

# for currentDictionary in arrayofD:
#     print(currentDictionary["email"])