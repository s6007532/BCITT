import os
k = os.listdir("saves")
k = list(set([i[:-6] for i in k]))
f = open(input("map file name : "),"w")
for i in k:
    f.write(i)
    f.write("\n")
f.close()