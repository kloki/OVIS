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

from __future__ import division
import random, sys
import cPickle as pickle


def main():
    verbose=False
    ignoreUserWant=False
    debug=False
    incorrect=False
    #read input parameters
    for i in xrange(1,len(sys.argv)):
        if sys.argv[i]== "-f":#file to evaluate
            evalfile=open(sys.argv[i+1]).readlines()
        elif sys.argv[i]== "-g":#file with golden results
            golden=open(sys.argv[i+1]).readlines()
        elif sys.argv[i]== "-v":#print results per line
            verbose=True
        elif sys.argv[i]== "-d":#debug mode
            debug=True
        elif sys.argv[i]== "-i":#list al incorrect lines
            incorrect=True
        elif sys.argv[i]== "-h":#print help screen
            helpprint()
            exit()
    if len(evalfile)!=len(golden):
        print "input file and golden file must contain the same amount of lines"
        exit()

    print "itemizing eval file.."
    evalItem=itemize(evalfile,debug)
    print "itemizing golden file..."
    goldenItem=itemize(golden,debug)
    print "comparing"
    evaluate(evalItem,goldenItem,verbose,incorrect)



# returns a list of all semantically sensible items per line.
def itemize(inputlist,debug):
    itemized=[]
    counter=1
    for line in inputlist:
        linelist=[]

        try:
            linelist=breakup(line[:-1])#remove end of line symbol
        except:
            lineslist=["error"]
        if debug:
            print counter
            counter=counter+1
            print linelist
            
        itemized.append(linelist)
    return itemized

#breakup a line in items

def breakup(stringer):
    itemlist=[]
    
    while True:
        [chunk,stringer]=getchunk(stringer)
        if "(" in chunk:
            [prefix,middle,suffix]=getfix(chunk)
            newlist=breakup(middle)
            for item in newlist:
                itemlist.append(prefix+item+suffix)
        else:
            itemlist.append(chunk)
        if stringer=="":
            break
    return itemlist


def getchunk(stringer):
    brackets=0
    chunk="XOXO"
    for i in xrange(0,len(stringer)):
        if stringer[i]=="(":
            brackets=brackets+1
        if stringer[i]==")":
            brackets=brackets-1    
        if brackets==0 and stringer[i]==";":#only unnestedsemicolons
            chunk=stringer[:i]
            stringer=stringer[i+1:]
            break
    if chunk=="XOXO":
        chunk=stringer
        stringer=""
    return [chunk,stringer]


def getfix(chunk):
    index1=0
    index2=0
    for i in xrange(len(chunk)):
        if chunk[i]=="(":
            index1=i
            break
    for i in xrange(len(chunk)-1,-1,-1):
        if chunk[i]==")":
            index2=i
            break
    return [chunk[:index1],chunk[index1+1:index2],chunk[index2+1:]]

    

def evaluate(Input,Golden,verbose,incorrect):
    Correct=0
    Precision=0
    Retrieval=0
    if incorrect:
        incorrectfile=open('incorrect','w')
    for i in xrange(0,len(Input)):
        currentPrecision=0
        currentRetrieval=0
        #check Precisions
        for element in Input[i]:
            if element in Golden[i]:
                currentPrecision=currentPrecision+1
        #check Retrieval
        for element in Golden[i]:
            if element in Input[i]:
                currentRetrieval=currentRetrieval+1
        if len(Input[i])==0: #This should never happen but this is for error catching
            currentPrecision=0
        else:
            currentPrecision=currentPrecision/len(Input[i])
        if len(Golden[i])==0: #This should never happen but this is for error catching
            currentRetrieval=0
        else:
            currentRetrieval=currentRetrieval/len(Golden[i])
        
        if verbose:
            print "line: ",i
            print "  Precision: ",currentPrecision
            print "  Retrieval: ",currentRetrieval
        Precision=Precision+currentPrecision
        Retrieval=Retrieval+currentRetrieval
        if currentPrecision==1 and currentRetrieval==1:
            Correct=Correct+1
        elif incorrect:
            incorrectfile.write(str(i+1)+"\n")
    Precision=Precision/len(Input)
    Retrieval=Retrieval/len(Input)
    if incorrect:
        incorrectfile.close()


    print "-----Totalscore----"
    print "Correct: ",Correct," of ", len(Input)
    print "Precision: ",Precision
    print "Retrieval: ",Retrieval
            

def helpprint():

    print "use: ./OvisEva -f Inputfile -g Goldenfile"
    print "-v: verbose, print results per line"
    print "-d: print the created items from the semantical annotation"
    print "-i: Creates a file containing als line numbers of updates that were incorrect"
    print "-h: You just did this"






#-------------------------------
if __name__ == "__main__":
    main()
