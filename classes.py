import numpy as np

class mot:
    def __init__(self,position,mot,lemme,pos):
        self.position = position
        self.mot = mot
        self.lemme = lemme
        self.pos = pos

    def __str__(self):
        return self.mot

    def __repr__(self):
        return self.mot

    def __eq__(self,other):
        return self.mot == other.mot

class relation:
    def __init__(self,mot1,mot2,lien,gouverneur,mots,contexte_int=[],contexte_ext=[]):
        self.mot1 = mot1
        self.mot2 = mot2
        self.lien = lien
        self.gouverneur = gouverneur
        self.mots = mots
        self.contexte_int = contexte_int
        self.contexte_ext = contexte_ext
        self.sens = ''
        self.set_cont_int()
        self.set_cont_ext()
        self.contexte_dep = []
        self.contexte_int = self.cont_int_strings()
        self.contexte_ext = self.cont_ext_strings()

    #On calcule le contexte interieur ici
    def set_cont_int(self):
        pos1 = int(self.mot1.position)
        pos2 = int(self.mot2.position)
        if pos1 > pos2:
            self.sens = 'droite'
            self.contexte_int = np.linspace(pos2+1,pos1-1,pos1-pos2-1)
        if pos1 < pos2:
            self.sens = 'gauche'
            self.contexte_int = np.linspace(pos1+1,pos2-1,pos2-pos1-1)
    #On calcule le contexte voisin
    def set_cont_ext(self):
        pos1 = int(self.mot1.position)
        pos2 = int(self.mot2.position)
        l = []
        #Je recupere le contexte gauche du premier mot
        if pos1 < pos2 and pos1 >1:
            l.append(pos1-1)
        elif pos2 < pos1 and pos2 > 1:
            l.append(pos2-1)
        #Je recupere le contexte droite du premier mot
        if pos1 < pos2 and pos1 + 1 != pos2:
            l.append(pos1+1)
        elif pos2 < pos1 and pos2 + 1 != pos1:
            l.append(pos2+1)
        #Je recupere le constexte gauche du deuxieme mot
        if pos2 > pos1 and pos2 - 1 != pos1:
            l.append(pos2 - 1)
        elif pos1 > pos2 and pos1 - 1 != pos2:
            l.append(pos1 - 1)
        #Je recupere le contexte droite du dernier mot
        if pos2 > pos1 and pos2 < len(self.mots):
            l.append(pos2+1)
        elif pos1 > pos2 and pos1 < len(self.mots):
            l.append(pos1+1)
        self.contexte_ext = list(set(l))

    def set_cont_dep(self):
        pass

    def __str__(self):
        return '(' + self.mot1.mot+' <- ' + self.mot2.mot + ' relation :' + self.lien +' cont_int : ' + " ".join(self.contexte_int) +' cont_voisin : ' + " ".join(self.contexte_ext) +' )'
    
    def __repr__(self):
        return '(' + self.mot1.mot+' <- ' + self.mot2.mot + ' relation :' + self.lien +' cont_int : ' + " ".join(self.contexte_int) +' cont_voisin : ' + " ".join(self.contexte_ext) +' )'

    def __eq__(self, other):
        return self.mot1 == other.mot1 and self.mot2 == other.mot2

    def cont_int_strings(self):
        s = []
        for i in self.contexte_int:
            s.append(self.mots[int(i-1)].mot)
        return s

    def cont_ext_strings(self):
        s = []
        for i in self.contexte_ext:
            s.append(self.mots[int(i-1)].mot)
        return s
        


class phrase:
    def __init__(self,sent_id,mots,liens):
        self.sent_id = sent_id
        self.mots = mots
        self.lien = liens
        self.set_cont_dep()

    def __str__(self):
        l = []
        for mot in self.mots:
            l.append(mot.mot)
        return " ".join(l)

    def set_cont_dep(self):
        for index, relation in enumerate(self.lien):
            if int(relation.gouverneur) == 0:
                self.lien[index].contexte_dep = 'root'
            elif int(relation.gouverneur != 0):
                actuel_gouv = relation.gouverneur
                for r in self.lien:
                    if r.mot1.position == actuel_gouv:
                        self.lien[index].contexte_dep = r.lien


