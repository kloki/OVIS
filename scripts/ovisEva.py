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
        elif sys.argv[i]== "-i":#debug mode
            incorrect=True
        elif sys.argv[i]== "-h":#print help screen
            helpprint()
            exit()
    if len(evalfile)!=len(golden):
        print "input file and golden file must contain the same amount of lines"
        exit()


    evalItem=itemize(evalfile,debug)
    goldenItem=itemize(golden,debug)

    evaluate(evalItem,goldenItem,verbose,incorrect)



# returns a list of all semantically sensible items per line.
def itemize(inputlist,debug):
    itemized=[]
    counter=1
    for line in inputlist:
        linelist=[]
        
        try:
            linelist=breakup(line[:-1],linelist,"","")#remove end of line symbol
        except:
            lineslist=["error"]
        if debug:
            print counter
            counter=counter+1
            print linelist
            
        itemized.append(linelist)
    return itemized

#breakup a line in items
def breakup(stringer,lister,prefix,suffix):
    if nested(stringer):
        stringer=stringer[1:-1]
    stringer=stringer+";"
    while (len(stringer)>1):
        [chunk,stringer]=getchunk(stringer)
        if "(" in chunk or "[" in chunk :#still nested elements
            if ifSuffix(chunk):#they only occur 5 times or something!!!!!!
                [chunker,suffix2]=getsuf(chunk)
                lister=breakup(chunker,lister,prefix,suffix2+suffix)#add a dot because it looks nice
            else:#prefix of just nested, handeled the same (nested uses an empty prefix)
                    [chunker,prefix2]=getpred(chunk)
                    lister=breakup(chunker,lister,prefix+prefix2+".",suffix)#add a dot because it looks nice
        else:
            lister.append(prefix+chunk+suffix) #single elements

    return lister


def nested(stringer):
    answer=False
    brackets=0
    if "(" in stringer or "[" in stringer or "{" in stringer:
        for i in xrange(len(stringer)):
            if stringer[i]=="(" or stringer[i]=="[" or stringer[i]=="{":
                brackets=brackets+1
            elif stringer[i]==")" or stringer[i]=="]"or stringer[i]=="{":
                brackets=brackets-1
            if brackets==0:
                if i==len(stringer)-1:
                    answer=True
                break
    return answer

def ifSuffix(chunk):
    answer=False
    if chunk[0]=="(" or chunk[0]=="[" or chunk[i]=="{":
        for i in xrange(len(chunk)-1,0,-1):
            if chunk[i]==")" or chunk[i]=="]" or chunk[i]=="}":
                break
            elif chunk[i]==".":
                answer=True
                break
 
    return answer

def getchunk(stringer):
    brackets=0
    for i in xrange(0,len(stringer)):
        if stringer[i]=="(" or stringer[i]=="{" :
            brackets=brackets+1
        if stringer[i]==")" or stringer[i]=="}" :
            brackets=brackets-1    
        if brackets==0 and stringer[i]==";":#only unnestedsemicolons
            chunk=stringer[:i]
            stringer=stringer[i+1:]
            break
    return [chunk,stringer]

def getpred(stringer):
    prefix=""
    for i in xrange(0,len(stringer)-1):
        if stringer[i]=="(" or stringer[i]=="{" or stringer[i]=="[":
            prefix=stringer[:i-1]
            stringer=stringer[i:]
            break
    return [stringer,prefix]

def getsuf(stringer):
    suffix=""
    for i in xrange(len(stringer)-1,0,-1):
        if stringer[i]=="]" or stringer[i]==")" or stringer[i]=="}" :
            suffix=stringer[i+1:]
            stringer=stringer[:i+1]
            break
    return [stringer,suffix]

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
