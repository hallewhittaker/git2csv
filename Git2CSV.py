import subprocess
testdictionary1= {"email": "whittaker@gmail.com", "message": "hello welcom"}
testdictionary2= {"email": "like@gmail.com", "message": "bye welcom"}

#print(testdictionary1["email"])
arrayofD= [testdictionary1,testdictionary2]

#print(arrayofD)

for currentDictionary in arrayofD:
    print(currentDictionary["email"])



# r= subprocess.run('git --no-pager blame --line-porcelain README.md', stdout= subprocess.PIPE)
#currently uses system command line to read a specific document.

# tab = r.stdout.split(b'\t') 
# for lineinfoS in tab:
#     #print(lineinfoS)
#     print("----")
#     linearray= lineinfoS.split(b'\n')
#     for individL in linearray:
#         print(individL)
#         print("____")
#currently splits tabs and new lines and prints this edited format.

# cheader =[]
# cdata = []

# import re
# a="b'filename README.md'" #work
# b="b'boundary'" #work
# c="b'author-mail <88335095+hallewhittaker@users.noreply.github.com>'" #work

# pattern = r"\s+|[']|'(?=\s)"
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