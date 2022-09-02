import sys
import os
if __name__ =="__main__":
    totfiles = 0
# sys.argv[1]=path of final folder
# sys.argv[2]=path of merged index
# sys.argv[3]=path of secondary index file
    lines = []
    filecount = 0
    threshold = 15000
    file = open(sys.argv[2], 'r')
    sec = open(sys.argv[3], 'w')
    line = file.readline().strip('\n')
    try:
        os.mkdir(sys.argv[1])
    except:
        pass
    while line:
            
        w=line.split(":")
        w=w[0]
        lines.append(line)

        if(len(lines)%threshold==0 and lines!=[]):
            firstWordOfSec=lines[0]
            firstWordOfSec=firstWordOfSec.split(":")
            firstWordOfSec=firstWordOfSec[0]+"\n"
            sec.write(firstWordOfSec)
            fileName=sys.argv[1]+"/fin"+str(filecount)+ ".txt"
            indexFile=open(fileName,"w")
            for l in lines:
                indexFile.write(l+"\n")
            
            filecount+=1
            lines=[]
        line = file.readline().strip('\n')

    if(lines!=[]):
            firstWordOfSec=lines[0]
            firstWordOfSec=firstWordOfSec.split(":")
            firstWordOfSec=firstWordOfSec[0]+"\n"
            fileName=sys.argv[1]+"/fin"+str(filecount)+ ".txt"

            indexFile=open(fileName,'w')
            for l in lines:
                indexFile.write(l+"\n")
            filecount+=1
            lines=[]
        
    file.close()
    sec.close()
