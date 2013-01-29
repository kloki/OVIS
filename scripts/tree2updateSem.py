#!/usr/bin/env python
#
# kloki
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Koen Klinkers k.klinkers@gmail.com


import random, sys


def main():
    post=False
    for i in xrange(1,len(sys.argv)):
        if sys.argv[i]== "-f":#file to evaluate
            inputfile=open(sys.argv[i+1]).readlines()
        elif sys.argv[i]== "-p":#postprocessing
            post=True
        elif sys.argv[i]== "-h":#print help screen
            helpprint()
            exit()
    for line in inputfile:
        transformed=transform(line[:-1],post)
        print transformed
        

def transform(tree,post):
    semanticUpdate=""
    tree=tree[5:-1]#remove top
    treeStructure=buildTreeStructure(tree)
    semanticUpdate=buildSem(treeStructure)
    if post:
        semanticUpdate=postProcess(semanticUpdate)
    return semanticUpdate


def buildTreeStructure(treestring): # tree structure is a recursivly nested list.
    splitted=treestring.split()
    [treeStructure,splitted]=parseTree(splitted)
    return treeStructure


def parseTree(splitted):
    node=splitted.pop(0)
    if "|" in node:
        semantic=node.split("|")[1]
    else:
        semantic="NOSEMAN"
    children=[]
    while True:#parse al children
        if splitted==[]:
            break
        elif splitted[0][-1]==")" and "|" not in splitted[0]: #next element closes current subtree and it not a semantic 
            if splitted[0][-2]==")":#count the brackets this way mutliple subtrees in a row are closed nicely
                splitted[0]=splitted[0][:-1]
            else:
                notuse=splitted.pop(0)
            break
        else:
            [child,splitted]=parseTree(splitted)
            children.append(child)
    
    if children==[]:
        treeStructure=[semantic]
    else:
        treeStructure=[semantic,children]
    return [treeStructure,splitted]



def buildSem(treeStructure):
    semanticUpdate=treeStructure[0]

    ds=["d1","d2","d3","d4","d5","d6"]
    for d in ds:
        if d in semanticUpdate:
            pieces=semanticUpdate.split(d)
            variable=buildSem(treeStructure[1][int(d[1])-1])#ha see what I did there
            semanticUpdate=pieces[0]+variable+pieces[1]
    return semanticUpdate

def postProcess (update):
    #sometimes there are extra parenthesis around the update, this cannot directly be infered from the tree
    if ";" in update:
        if unnesstedbracket(update):
            update="("+update+")"
    #sometimes origin appears twice in the tree so derivation also has origin two times, example:sentence 120
    update=update.replace(".origin.origin.",".origin.")
    update=update.replace(".origin.(origin.",".(origin.")
    update=update.replace(".origin.[#origin.",".[#origin.")
    #apperently we can also do some Arithmetic but only for christmas example:152
    update=update.replace("24+1","25")
    update=update.replace("24+2","26")
    # and this special case 468
    update=update.replace("3+20","23")
    #errors dont have parenthesis 487
    update=update.replace("(error.not_understood)","error.not_understood")
    #the plus sign is removed example:563
    update=update.replace("minute.+","minute.")
    #minus time is changed:229
    if "minute.-" in update:
        update=adjustMinus(update)


    #century is added example:5352
    if "year." in update and "year.19" not in update:
        update=update.replace("year.","year.19")
    
    #months by names not numbers example: 5694
    if "month." in update:
        if "month.12" in update:
            update=update.replace("month.12","month.december")
        elif "month.11" in update:
            update=update.replace("month.11","month.november")
        elif "month.10" in update:
            update=update.replace("month.10","month.october")
        elif "month.9" in update:
            update=update.replace("month.9","month.september")
        elif "month.8" in update:
            update=update.replace("month.8","month.august")
        elif "month.7" in update:
            update=update.replace("month.7","month.july")
        elif "month.6" in update:
            update=update.replace("month.6","month.june")
        elif "month.5" in update:
            update=update.replace("month.5","month.may") 
        elif "month.4" in update:
            update=update.replace("month.4","month.april")
        elif "month.3" in update:
            update=update.replace("month.3","month.march")
        elif "month.2" in update:
            update=update.replace("month.2","month.february")
        elif "month.1" in update:
            update=update.replace("month.1","month.january")
            
    return update

def adjustMinus(update):
    for i in xrange(8,len(update)+1):
        if update[i-8:i]=="minute.-":
            if update[i+1].isdigit():#will never give an error because of parenthesis
                left=update[:i]
                right=update[i+2:]
                x=str(60-int(update[i:i+2]))
                update=left+x+right
            else:
                left=update[:i]
                right=update[i+1:]
                x=str(60-int(update[i]))
                update=left+x+right
                
    for i in xrange(11,len(update)):
        if update[i-11:i]=="clock_hour.":
            if update[i+1].isdigit():
                left=update[:i]
                right=update[i+2:]
                x=str(int(update[i:i+2])-1)
                if x=="0":
                    x="12"
                update=left+x+right
            else:
                left=update[:i]
                right=update[i+1:]
                x=str(int(update[i])-1)
                if x=="0":
                    x="12"
                update=left+x+right

    #remove minus
    update=update.replace("minute.-","minute.")    
    return update


def unnesstedbracket(update):
    answer=False
    count=0
    for i in xrange(0,len(update)):
        if update[i]=="(" or update[i]=="[":
            count+=1
        elif update[i]=="]" or update[i]==")":
            count-=1
        elif update[i]==";" and count==0:
            answer=True
            break
    return answer

def helpprint():

    print "use: ./tree2updateSem.py -f Inputfile"
    print "-p: Do a post processing step to get 100 percent on the golden standard (incomplete)"
    print "-h: You just did this"
    


#-------------------------------
if __name__ == "__main__":
    main()
