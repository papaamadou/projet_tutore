# projet_tutore
Corpus correction applied on UD
Pendant l'execution les arguments se suivent comme suit:
le premier correspond au fichier input, 
Le deuxieme au contexte
troisieme nil ou not_nil (pour designer si on veut les nil ou pas)
quatrieme punct ou not_punct (pour prendre en compte les ponctuations ou pas)


Pour le fichier test.conllu,voici les erreurs que nous devons trouver:

couples d'erreur pour le contexte voisin:

(('le', 'chat'),['voit', 0, 0, 0]) {'conj - R': [('phrase 2', 4, 5)], 'det - R': [('phrase 1', 4, 5)]}

couples d'erreur pour le contexte interne:

(('le', 'chat')[]) {'conj - R': [('phrase 2', 4, 5)], 'det - R': [('phrase 1', 1, 2), ('phrase 1', 4, 5), ('phrase 2', 1, 2)]}

couples d'erreurs pour le contexte de dependance:

(('le', 'chat'),obj) {'conj - R': [('phrase 2', 4, 5)], 'det - R': [('phrase 1', 4, 5)]}

(('est', 'maison'),root) {'obl - L': [(' phrase 4', 2, 5)], 'obj - L': [('phrase 3', 2, 4)]}
