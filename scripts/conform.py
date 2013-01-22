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
    semantical=True
    brackets=False
    for i in xrange(1,len(sys.argv)):
        if sys.argv[i]== "-f":#file to evaluate
            inputfile=open(sys.argv[i+1]).readlines()
        elif sys.argv[i]== "-s":
            semantical=False
        elif sys.argv[i]== "-b":
            brackets=True
        elif sys.argv[i]== "-h":#print help screen
            helpprint()
            exit()
    for tree in inputfile:
        conformed=conform(tree[:-1],semantical)#remove end of line symbol
        if brackets:
            conformed=curlyBrackets(conformed)
        print conformed


def curlyBrackets(conformed):
    bracketed=""
    conformed=conformed.split()
    for element in conformed:
        if "|" in element:
            pieces=element.split("|")
            bracketed=bracketed+" "+pieces[0]+"|"+pieces[1].replace(")","}").replace("(","{")
        else:
            bracketed=bracketed+" "+element
    return bracketed[1:]



def conform(tree,semantical):
    #is going to be a bit of a hack but they messed up tree annotation not me
    returntree="(TOP "
    if tree=="( empty_tree|error.nothing_recorded)":    
        returntree=returntree+tree[2:]
    elif tree[2]!="(": #we now have a single word
        xx=tree.split("/")
        returntree=returntree+"("
        if semantical:
            returntree=returntree+xx[0][2:]
        else:
            returntree=returntree+xx[0].split("|")[0][2:]
        returntree=returntree+" "+ xx[1]
        returntree=returntree+")"
    else:
        splitted=tree[2:].split()
        for element in splitted:
            if "/" in element: #end of tree needs to be adjusted
                if semantical:
                    xx=element.split("/")
                    returntree=returntree+"("+xx[0]+" "+xx[1]+") "
                else:
                    xx=element.split("/")
                    returntree=returntree+"("+xx[0].split("|")[0]+" "+xx[1]+") "
            else:
                if semantical:
                    returntree=returntree+element+" "
                else:
                    returntree=returntree+element.split("|")[0]+" "
                
        returntree=returntree[:-1]#remove lasts space

    return returntree

def helpprint():
    print "This function conforms the tree annotation to a more conventional one"
    print "use: ./conform -f Inputfile"
    print "-s: Ignore semantical annotations"
    print "-h: You just did this"
    print "-b: Use curly braces in semantical annotation to not confuse most parsers" 

#-------------------------------
if __name__ == "__main__":
    main()
