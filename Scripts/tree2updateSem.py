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
    splitted=tree.split()
    [semanticUpdate,splitted]=buildSem(splitted)
    return semanticUpdate


def buildSem(splitted):
    semantics=splitted.pop(0)
    if "|" in semantics:#there are semantics in the node
        semantics=semantics.split("|")[1]
        ds=["d1","d2","d3","d4","d5","d6"]
        for d in ds:
            if d in semantics:
                pieces=semantics.split(d)
                [variable,splitted]=buildSem(splitted)
                semantics=pieces[0]+variable+pieces[1]
        #dontuse=splitted.pop(0) #next node is terminal has no semantical value
        stringer=semantics
    else:#try next node
        [stringer,splitted]=buildSem(splitted)
    return [stringer,splitted]

def helpprint():

    print "use: ./tree2updateSem.py -f Inputfile"
    print "-h: You just did this"



#-------------------------------
if __name__ == "__main__":
    main()
