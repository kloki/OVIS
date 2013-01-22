set -e

echo "setting up files"
pythonScript/setup.py

echo "building the grammar this may take a while"
java -jar PCFG_extractor.jar trainTrees combinedGrammar
pythonScript/splitGrammar.py combinedGrammar grammar lexicon
rm combinedGrammar
pythonScript/bitParSentence.py testSentencesDum testSentences
echo "done"

echo "running bitpar"
bitpar grammar lexicon testSentences bitParResults -p -s TOP -u unknown -v
pythonScript/sanitizeResults.py bitParResults results

echo "extracting semantics"
../scripts/tree2updateSem.py -f results -p > extractedSemantics

echo "evaluation"
../scripts/ovisEva.py -f extractedSemantics -g testSemantics