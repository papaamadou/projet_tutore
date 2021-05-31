
import json
import argparse
from copy import deepcopy
def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs="?", type=argparse.FileType('r'),help="path to input conllu file")
    parser.add_argument("context",nargs=1,choices=["interne","dependance","voisin","none"],help="choose the context you want")
    parser.add_argument("nil", nargs=1, choices=["nil", "not_nil"], help= "do you want to take nil into account")
    parser.add_argument("punct", nargs=1, choices=["punct", "not_punct"], help="do you want to take punctuation into account")
    parser.add_argument("word", nargs=1, choices=["wordform", "lemma"],help="wordform or lemma")

    arg=parser.parse_args()
    file_name=arg.infile.name
    context = arg.context[0]
    if arg.nil[0]=="nil":
        test_nil = True
    else:
        test_nil=False
    if arg.punct[0] == "punct":
        punct= True
    else:
        punct = False
    if arg.word[0] =="lemma":
        lemma = True
    else:
        lemma = False
    return file_name,context, test_nil,punct, lemma

def data_extraction(file_name):
    """
    input: file name of a .conllu file
    output: dictionary with key:id of the sentence, value: (position, word, lexeme,pos_tagging, governor, relation_name)
    """
    with open(file_name, "r", encoding="utf8") as file:
        lines = file.readlines()
        dico = {}
        for l in lines:
            if l[0] == "#":
                if l[2] == "s":
                    sent_id = l[12:].strip("\n")
                    dico[sent_id] = []
            if l[0].isdigit():
                line = l.split("\t")[0:8]
                if '-' not in line[0]:
                    del line[4:6]
                    dico[sent_id].append(line)
    return dico


def context(sentence, position_word1, position_word2, lemma):
    """
    output: internal context and neighbour context for 2 given words
    """
    i=1
    phrase = [elt[i].lower() for elt in sentence]
    if lemma:
        i=2
        phrase = [elt[i] for elt in sentence]

    interne = phrase[position_word1:position_word2 - 1]
    voisins = [0, phrase[position_word1], phrase[position_word2 - 2], 0]
    if position_word1 != 1:
        voisins[0] = phrase[position_word1 - 2]
    if position_word2 != len(sentence):
        voisins[3] = phrase[position_word2]
    if position_word1 + 1 == position_word2:
        voisins[1], voisins[2] = 0, 0
    if position_word1 + 2 == position_word2:
        voisins[2] = 0

    return interne, voisins


def couple(dico, cont, punct=True, lemma=False):
    """
    output: dictionary with all the pair of word which are related, key :(word1, word2)  value:(sent_id, position_word1, position_word2,relation_name, chosen context)
    """
    i =1
    if lemma :
        i = 2

    list_couple = {}
    for k, v in dico.items():
        for elt in v:
            if i==1:
                word1 = elt[i].lower()
                word2 = v[int(elt[4]) - 1][i].lower()
            else :
                word1 = elt[i]
                word2 = v[int(elt[4]) - 1][i]
            if elt[5] == "root":
                relation = [word1, "##empty##", k, int(elt[0]), 0, elt[5], [], [0, 0, 0, 0], "","##none##"]

            elif not punct and  (elt[3] == "PUNCT" or v[int(elt[4]) - 1][3]== "PUNCT") :
                continue
            else:
                rel = elt[5]
                position_word1 = int(elt[0])
                position_word2 = int(v[int(elt[4]) - 1][0])

                if position_word1 < position_word2:
                    rel = rel + " - R"
                    interne, voisins = context(v, position_word1, position_word2, lemma)

                    relation = [word1, word2, k, position_word1, position_word2, rel, interne, voisins,
                                v[int(elt[4]) - 1][5],"##none##"]

                else:
                    rel = rel + " - L"
                    interne, voisins = context(v, position_word2, position_word1, lemma)

                    relation = [word2, word1, k, position_word2, position_word1, rel, interne, voisins,
                                v[int(elt[4]) - 1][5], "##none##"]

                    # relation = [word1, word2, sent_id, position_1, position_2, relation_name, internal_context, neighbour_context, depandency_context]

            choose_context(relation, list_couple, cont)
    return list_couple


def nil(list_couple, dico, cont, lemma):
    """
    output: dictionary with all the relevant nil pair of word
    """
    p=1
    if lemma:
        p=2
    list_nil = {}
    for k, v in dico.items():
        for i, elt in enumerate(v):
            for j in range(i + 1, len(v)):
                if p == 1:
                    word1 = elt[p].lower()
                    word2 = v[j][p].lower()
                else:
                    word1 = elt[p]
                    word2 = v[j][p]
                if (word1, word2) in list_couple and elt[4] != v[j][0] and int(v[j][4]) != int(elt[0]):
                    position_word1 = int(elt[0])
                    position_word2 = int(v[j][0])
                    interne, voisins = context(v, position_word1, position_word2,lemma)
                    nil_relation = [word1, word2, k, position_word1, position_word2, "NIL", interne, voisins, "",
                                    "##none##"]
                    choose_context(nil_relation, list_nil, cont)
    return list_nil


def choose_context(relation, couple, cont="interne"):
    """
    choose the context that will be  take into account for the comparison (interne, voisins, dependance,without context)
    """
    i, v, d, n = 6, 7, 8,9
    indice = i
    if cont == "voisin":
        indice = v
    if cont == "dependance":
        indice = d
    if cont =="none":
        indice = n
    if (relation[0], relation[1]) not in couple:
        couple[(relation[0], relation[1])] = [(*relation[2:6], relation[indice])]
    else:
        couple[(relation[0], relation[1])].append((*relation[2:6], relation[indice]))


def compare(n_couple, list_couple=[], list_nil=[],result={}, nil=False):
    """
    for a given pair of word, compare the context and return the potential errors
    """
    if nil:
        l = list_couple + list_nil
    else:
        l = list_couple
    for i, elt in enumerate(l):
        for ind,j in enumerate (l[0:i]):
            if elt[4] == j[4] and elt[3] != j[3]:
                k=str((n_couple,elt[4]))
                if k not in result:
                    result[k]={}
                if str(elt[3]) not in result[k]:
                    result[k][str(elt[3])]=[elt[:3]]
                elif elt[:3] not in result[k][str(elt[3])]:
                    result[k][str(elt[3])].append(elt[:3])
                if str(j[3]) not in result[k]:
                    result[k][j[3]]=[j[:3]]
                elif j[:3] not in result[k][str(j[3])]:
                    result[k][str(j[3])].append(j[:3])

    return result

def filter(dico):
    """ remove the false positive couples"""
    sup_key = []
    dico = deepcopy(dico)
    for k, v in dico.items():
        if "NIL" in dico[k]:
            nil = []
            for elt in dico[k]["NIL"]:
                for k1, v1 in dico[k].items():
                    if k1 != "NIL":
                        for i in v1:
                            if i[0] == elt[0]:
                                if ("- R" in k1) and (int(i[1]) == int(elt[1])):
                                    nil.append(elt)
                                if ("- L" in k1) and (int(i[2]) == int(elt[2])):
                                    nil.append(elt)
            for elt in nil:
                if elt in dico[k]["NIL"]:
                    dico[k]["NIL"].remove(elt)
            if len(dico[k]["NIL"]) == 0:
                dico[k].pop("NIL")
            if len(dico[k]) == 1:
                sup_key.append(k)
    for elt in sup_key:
        dico.pop(elt)
    return dico

def recuperer_phrase(dico, sent_id):
    phrase =""
    for elt in dico[sent_id]:
        phrase += elt[1] +" "
    return phrase


def conllu_format(dico, couple):
    file = ""
    for k,v in couple.items():
        for elt in v:
            file += "# sent_id = "+elt[0]+"\n"
            file += "# text = "+ recuperer_phrase(dico, elt[0]) + "\n"
            for word in dico[elt[0]]:
                if (int(word[0])==elt[1] and int(word[4])== elt[2]) or (int(word[4])==elt[1] and int(word[0])== elt[2]):
                    file += word[0]+"\t"+word[1]+"\t"+word[2]+"\t"+word[3] +"\t_\t_\t"+word[4]+"\t"+word[5]+"\t_\t_\n"
                else:
                    file += word[0] + "\t" + word[1] + "\t" + word[2] +"\t"+word[3]+"\t_\t_\t_\t_\t_\t_\n"
        file+="\n"
    return file

def main():
    file_name, context, test_nil, punct,lemma = get_argument()
    dico = data_extraction(file_name)
    list_couple = couple(dico, context,punct,lemma)
    list_nil = nil(list_couple, dico, context,lemma)
    potential_errors = {}

    for k, v in list_couple.items():
        if len(v) > 1 or k in list_nil:
            if k in list_nil:
                compare(k,v, list_nil[k],result=potential_errors, nil=test_nil)
            else:
                compare(k,v,result=potential_errors, nil=test_nil)
                
    with open("result_"+context+".json","w")as file:
        json.dump(potential_errors,file)

    potential_errors_filt=filter(potential_errors)
    with open("result_filt"+context+".json","w")as file:
        json.dump(potential_errors_filt,file)

    for k,v in potential_errors.items():
        print(k,v)


main()



