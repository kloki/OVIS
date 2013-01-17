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


import random, sys,numpy,os
import cPickle as pickle


def main():
    trees=open(sys.argv[1]).readlines()
    sentences=open(sys.argv[2]).readlines()
    assert len(trees)==len(sentences)
    print str(len(trees))+" sentences" 

    #remove empty sentences, these are misrecordings
    for i in xrange(len(sentences)-1,0,-1):
        if sentences[i]=="\n":
            trees.pop(i)
            sentences.pop(i)
    print "remove misrecording"
    print str(len(trees))+" sentences left" 

    #shuffle
    p = numpy.random.permutation(len(trees))
    shuffTrees=[]
    shuffSentences=[]
    for i in p:
        shuffTrees.append(trees[i])
        shuffSentences.append(sentences[i])
    

    #create test set
    trainTrees=open("trainTrees","w+")
    testTrees=open("testTrees","w+")
    trainSentences=open("trainSentences","w+")
    testSentences=open("testSentences","w+")
    
    for i in xrange(len(trees)):
        if i <=9500:
            trainTrees.write(shuffTrees[i])
            trainSentences.write(shuffSentences[i])
        else:
            testTrees.write(shuffTrees[i])
            testSentences.write(shuffSentences[i])
            
    print "building Grammar, This can take a while..."  
    os.system("java -jar PCFG_extractor.jar trainTrees combinedGrammar")
    os.system("./splitGrammar.py combinedGrammar grammar lexicon")
    os.system("rm combinedGrammar")
    print "done"
            
#-------------------------------
if __name__ == "__main__":
    main()
