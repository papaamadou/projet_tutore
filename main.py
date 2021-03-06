from classes import mot
from classes import relation
from classes import phrase
import pandas as pd

def to_dict(file):
    with open(file,'r') as file:
        lignes = file.readlines()
        #On initialise une liste qui va contenir les sent_id
        sent_id = []
        #On initialise une liste qui va contenir les indices de debut et de fin de chaque phrases
        indices = [0]
        for indice,ligne in enumerate(lignes):
            #On teste et recupere les sent_id : les lignes contenant les sent_id commencent par # suivi du caractere s 
            if ligne[0]=='#'and ligne[2]=='s':
                sent_id.append(ligne) 
            #On teste et recupere les indices de debut et de fin : les lignes contenant les sent_id commencent par # suivi du caractere s 
            elif ligne == '\n':
                indices.append(indice)
            #Maintenant qu'on connait l'indice de debut et de fin on peut recuperer les phrases de chaque sent_id
    #On initialise une une liste qui va contenir une liste de phrase
    text=[]
    for i in range(len(indices)-1):
        #Chaque phrase correspond a une liste
        l=list(lignes[indices[i]+3:indices[i+1]])
        #Text devient alors une liste de liste
        text.append(l)
    #Les phrases que nous avons recuperé ne sont pas nettoyés  notre objectif ici est de les nettoyer 
    text_utile = []
    for t in text: 
        #temp est une liste temporaire qui permet de recuperer tous les mots d'une phrase
        temp = []
        for i in t:
            #Tous les element dans chaque ligne sont séparés par des /t donc on peut exploiter ce caracteristique pour savoir
            # Ce qu'on a exactement a chaque endroit de la ligne 
            l = i.split('\t')
            #Ici on fait un traiement sur la liste pour ne garder que ce qui nous interesse
            l=l[:8]
            del l[4:6]
            temp.append(l)
        #A ce niveau text_utile sera une liste de liste ou chaque sous-liste est liste des mots de la phrase
        text_utile.append(temp)
    #Les differentes etapes faites plus hauts nous on mené a nous retrouver avec 2 listes une qui contient les sent_id et une autre qui 
    #qui contient les les infos de chaque phrase. On peut donc construire un dictionnaire dont la clé est le sent_id et la valeur est une liste
    #de liste qui contient respectivement la position du mot dans le phrase,le mot en question, son lemme, son pos tagging, son gouverneur et 
    #et la relation qui le lie a son gouverneur
    dico={}
    for key,value in zip(sent_id,text_utile):
        dico[key]=value
    return dico
#Ici Nous creons une fonction qui prend comme entree le dictionnaire cité plus haut et qui va mapper les données dans nos nos classes
#mot,relation et phrase qui gere respectivement chaque mot de la phrase, chaque relation entre les mots de la phrase et la phrase elle meme
def to_phrase(dico):
    #on cree un liste qui va contenir toutes les phrases
    phrases = []
    for key,value in dico.items():
        #ici on recupere le sent_id
        sent_id = key
        #on cree un liste qui va contenir tous les mots d'une phrase
        mots = []
        #on cree un liste qui va contenir toutes les relations d'une phrase
        liens = []
        for m in value:
            if '-' not in m[0]:
                position = m[0]
                word = m[1]
                lemme = m[2]
                pos = m[3]
                #On recupere les attributs relatif a la classe mot et on instancie un objet 
                m = mot(position,word,lemme,pos)
                #On ajouter l'objet crée dans la liste des mots
                mots.append(m)
        for m in value:
            if '-' not in m[0]:
                if m[4] == '0':
                    lien = 'root'
                    gouverneur = '0'
                    pos_mot1 = int(m[0])
                    mot1 = mots[pos_mot1 - 1]
                    mot2 = mot(0,'root','root','root')
                    l = relation(mot1,mot2,lien,gouverneur,mots)
                    liens.append(l)
                if m[4]!='0':
                    lien = m[5]
                    gouverneur = m[4]
                    pos_mot1 = int(m[0])
                    pos_mot2 = int(gouverneur)
                    mot1 = mots[pos_mot1 - 1]
                    mot2 = mots[pos_mot2 - 1]
                    #On recupere les attributs relatif a la classe relation et on instancie un objet 
                    l = relation(mot1,mot2,lien,gouverneur,mots)
                    #On ajouter l'objet crée dans la liste des relations
                    liens.append(l)
        #On instancie un objet phrases qui va le sent_id de la phrase, une liste de tous les mots de la phrase et une liste de toutes les
        #relations de la phrase
        p = phrase(sent_id,mots,liens)
        #Puis on ajoute cet objet dans la liste des phrases de notre treebank
        phrases.append(p)

    return phrases

def to_csv(phrases):
    l_sent_id = []
    l_mots = []
    l_relations = []
    for phrase in phrases:
        l_sent_id.append(phrase.sent_id)
        l_mots.append(phrase.mots)
        l_relations.append(phrase.lien)
    df = pd.DataFrame({'sent_id': l_sent_id,'phrase' : phrases,'mots': l_mots, 'relations': l_relations})
    df.to_csv('fr_gsd-ud-dev_new2.csv',index=False)
# Je compare les relations de deux phrases s'il existe deux relations avec les meme mots mais avec des annotations differentes
def check_relation(phrase1,phrase2):
    l = []
    for r1 in phrase1.lien:
        for r2 in phrase2.lien:
            if r1 == r2 and r1.lien != r2.lien:
                l.append((phrase1.sent_id,phrase2.sent_id,r1.lien,r2.lien))

    return l

#Je verifie s'il ya deux relations qui ont exactement les meme mots et qui ne sont pas annotées de la meme facon
def basic_comparaison(phrases):
    results = []
    for phrase1 in phrases:
        for phrase2 in phrases:
            results.append(check_relation(phrase1,phrase2))
    return results

#Calcul des NIL
def nil_construction(phrase):
    all_duo = []
    #Je commence par former l'ensemble des des duos
    for mot1 in phrase.mots:
        for mot2 in phrase.mots:
            all_duo.append((mot1,mot2))
    #J'elimine les duo qui existent deja dans mes relations
    



if __name__ == "__main__":
    path = 'UD_French-GSD/fr_gsd-ud-dev.conllu'
    dico = to_dict(path)
    print(len(dico))
    phrases = to_phrase(dico)
    print(len(phrases))
    #to_csv(phrases)
    basic = basic_comparaison(phrases)
    df = pd.DataFrame({'id 1, id 2, relation id 1, relation id 2 ': basic})
    df.to_csv('errors.csv',index=False)


