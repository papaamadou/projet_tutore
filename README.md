# corpus_correction
corpuscorrection.py allows you to detect errors in corpus annotated with dependency annotations.
When running it, on the interface you will have to choose your conllu file with the corpus you want to analyze.
But also different characteristics such as the context (internal, neighbour, dependency or without context), the kind of  element (wordform or lemma), and finally if you want to take into account the NIL relations and the punctuation.

In the file test.conllu, there is 4 sentences with some errors. If you want to try it and verify the errors, here are the results you should obtain with this file when you take into account punctuation and NIL relation.
For the neighboring context, only one erroneous couple:
the couple ('le','chat') with the context ['voit', 0, 0, 0]. The potential errors are in sentence 2 (word 4, word 5) with conj-R annotation and sentence 1 (word 4, word 5) with det-R annotation.


For the internal context, only one erroneous couple:
the couple ('le','chat') with the context []. The potential errors are in phrase 2 (word 4, word 5) with conj-R annotation and phrase 1 (word 4, word 5), phrase 1 (word 1, word 2), phrase 2 (word 1, word 2) with det-R annotation.

For the dependency context, two erroneous couples:
the couple ('le','chat') with the context 'obj'. The potential errors are in phrase 2 (word 4, word 5) with conj-R annotation and phrase 1 (word 4, word 5) with det-R annotation.
the couple ('est','maison') with the context 'root'. The potential errors are in phrase 4 (word 2, word 5) with obl-L annotation and phrase 3 (word 2, word 4) with obj-R annotation.






