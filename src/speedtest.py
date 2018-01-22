__author__="Harshit.Kashiv"

import os
from subprocess import *
import re
from matplotlib.cbook import Null
#call(["dmesg", "|", "grep", "hda"])

str1 = "ab -n 10 -c 1 -p 1.post http://localhost:4050/ArticleSimilarity"
#output=check_output("dmesg | grep hda", shell=True)
a=[]
b = [1,5,10,20,40,50,60]
c = [10,100,1000,5000]

for item in str1.split(" "):
    a.append(item)

for i in c:
    a[2] = str(i)
    for j in b:
        if(j <= i):
            a[4] = str(j)
            print a
            output = Popen(a, stdout=PIPE).communicate()[0]
#            file = open("abc.txt","w+")
 #           file.write(output)
  #          file.close()
            match = re.search("Connect",output)
        if match == None:
            print "match not found"
            break
        else:
            file = open("abc.txt","a+")
            file.write((str(a)+"\n"))
            file.write(output)
            file.close()

'''    
match_png = re.search('png',"article_url")
if match_png == None:
    print "abc"
    
print match_png

#apr_socket_recv
#print a
#call(a)
#call(a)
#output = Popen(a, stdout=PIPE).communicate()[0]

#print "output"

#print output
#file = open("abc.txt","a")

#file.write(output)
'''
            