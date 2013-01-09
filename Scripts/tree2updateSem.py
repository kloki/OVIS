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
import cPickle as pickle



def main():
    for i in xrange(1,len(sys.argv)):
        if sys.argv[i]== "-f":#file to evaluate
            inputfile=open(sys.argv[i+1]).readlines()
        elif sys.argv[i]== "-h":#print help screen
            helpprint()
            exit()
    
    for line in inputfile:
        transformed=transform(line[:-1])
        print transformed
        

def transform(tree):
    semanticUpdate=""
    tree=tree[5:-1]#remove top
    treeStructure=buildTreeStructure(tree)
    print treeStructure
    semanticUpdate=buildSem(treeStructure)
    return semanticUpdate


def buildTreeStructure(treestring): # tree structure is a recursivly nested list.
    splitted=treestring.split()
    [treeStructure,splitted]=parseTree(splitted)
    return treeStructure

#def errorChild():

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
        elif splitted[0][-1]==")": #next element closes current subtree
            if splitted[0][-2]==")":#count the brackets this way mutliple subtrees in a row are closed nicely
                splitted[0]=splitted[0][:-1]
            else:
                notuse=splitted.pop(0)
            break
        else:
            [child,splitted]=parseTree(splitted)
            children.append(child)
    
    if children==[]:
        treeStructure=semantic
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

def helpprint():

    print "use: ./tree2updateSem.py -f Inputfile"
    print "-h: You just did this"



#-------------------------------
if __name__ == "__main__":
    main()
