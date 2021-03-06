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


import random, sys, numpy


def main():
    trees=open("../corpora/conformedTreesCurly").readlines()
    sentences=open("../corpora/sentences").readlines()
    semantics=open("../corpora/updateSemantics").readlines()
    assert len(trees)==len(sentences)
    print str(len(trees))+" sentences" 

    #remove empty sentences, these are misrecordings
    for i in xrange(len(sentences)-1,0,-1):
        if sentences[i]=="\n":
            trees.pop(i)
            sentences.pop(i)
            semantics.pop(i)
    print "removed misrecordings"
    print str(len(trees))+" sentences left" 

    #shuffle
    p = numpy.random.permutation(len(trees))
    shuffTrees=[]
    shuffSentences=[]
    shuffSemantics=[]
    for i in p:
        shuffTrees.append(trees[i])
        shuffSentences.append(sentences[i])
        shuffSemantics.append(semantics[i])

    #create test set
    trainTrees=open("trainTrees","w+")
    testTrees=open("testTrees","w+")
    trainSentences=open("trainSentences","w+")
    testSentences=open("testSentencesDum","w+")
    trainSemantics=open("trainSemantics","w+")
    testSemantics=open("testSemantics","w+")
                
    
    for i in xrange(len(trees)):
        if i <(len(trees)-500):
            trainTrees.write(shuffTrees[i])
            trainSentences.write(shuffSentences[i])
            trainSemantics.write(shuffSemantics[i])
        else:
            testTrees.write(shuffTrees[i])
            testSentences.write(shuffSentences[i])
            testSemantics.write(shuffSemantics[i])
                              
    trainTrees.close()
    testTrees.close()
    trainSentences.close()
    testSentences.close()
    trainSemantics.close()
    testSemantics.close()



#-------------------------------
if __name__ == "__main__":
    main()
