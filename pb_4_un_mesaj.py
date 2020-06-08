"""
    grupa: 242
    nume: Nacu Florin Ionut
"""

import time


class Nod:
    def __init__(self, info, h):
        """
        :param info: tuplu, reprezentand pozitia biletului la un moment dat in matrice
        :param h: euristica
        """
        self.info = info
        self.h = h


class Problema:
    def __init__(self, start=None, scop=None, matrice_clasa=None, lista_suparati=None):
        """
        :param start: informatia nodului start
        :param scop: informatia nodului scop
        :param matrice_clasa: matrice de nume, reprezentand asezarea elevilor in clasa
        :param lista_suparati: lista de tupluri, reprezentand elevii care sunt suparati reciproc
        """
        if start is None:
            start = (0, 0)
        if scop is None:
            scop = (3, 5)
        if matrice_clasa is None:
            matrice_clasa = [["ionel", "alina", "teo", "eliza", "carmen", "monica"],
                             ["george", "diana", "bob", "liber", "nadia", "mihai"],
                             ["liber", "costin", "anda", "bogdan", "dora", "marin"],
                             ["luiza", "simona", "dana", "cristian", "tamara", "dragos"],
                             ["mihnea", "razvan", "radu", "patricia", "gigel", "elena"],
                             ["liber", "andrei", "oana", "victor", "liber", "dorel"],
                             ["viorel", "alex", "ela", "nicoleta", "maria", "gabi"]]
        if lista_suparati is None:
            lista_suparati = [("george", "ionel"),
                              ("ela", "nicoleta"),
                              ("victor", "oana"),
                              ("teo", "eliza"),
                              ("teo", "luiza"),
                              ("elena", "dragos"),
                              ("alina", "dragos")]

        self.nod_start = Nod(start, float("inf"))
        self.nod_scop = Nod(scop, 0)
        self.matrice_clasa = matrice_clasa
        self.lista_suparati = lista_suparati


class NodParcurgere:
    problema = None
    fct_h = None

    def __init__(self, nod_graf, parinte=None, g=0, directie=None):
        """
        :param nod_graf: obiect de tip Nod
        :param parinte: obiect de tip NodParcurgere
        :param g: costul muchiei tata-fiu
        :param directie: un string din lista [">", "<", "v", "^", "<<", ">>"] reprezentand directia pe care o alege biletul cand trece de la nodul parinte la nodul curent (self)
        """
        self.nod_graf = nod_graf
        self.parinte = parinte
        self.g = g
        self.directie = directie
        self.f = self.g + self.nod_graf.h

    def drum_arbore(self):
        """
        :return: lista formata din nodurile (obiecte de tip NodParcurgere) ce se afla in drumul de la nodul curent (self) pana la radacina
        """
        nod_curent = self
        drum = [nod_curent]
        while nod_curent.parinte is not None:
            drum = [nod_curent.parinte] + drum
            nod_curent = nod_curent.parinte
        return drum

    def contine_in_drum(self, nod):
        """
        :param nod: obiect de tip Nod
        :return: True daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self), False altfel
        """
        nod_curent = self
        while nod_curent is not None:
            if nod_curent.nod_graf.info == nod.info:
                return True
            nod_curent = nod_curent.parinte
        return False

    def expandeaza(self):
        """
        Succesorii sunt determinati prin crestearea/scaderea cu 1 a liniei/coloanei pe care se afla biletul la un moment dat.
        Deci pot fi maxim 4 succesori, insa daca pe pozitia pe care ar urma sa se duca biletul nu se afla vreun elev, sau
        daca elevul ce are biletul si cu elevul caruia urmeaza sa-i fie dat biletul sunt certati, atunci nu este luat in calcul
        ca fiind un seccesor valid.
        :return: lista de tupluri (nod_fiu, cost_muchie_tata_fiu, directie) formata din succesorii nodului curent (self),
                 nod_fiu este un obiect de tip Nod, cost_muchie_tata_fiu este de tip int, directie este un string
        """
        succesori = []
        nod_graf_curent = self.nod_graf.info
        matrice = NodParcurgere.problema.matrice_clasa

        for (i, j) in [(nod_graf_curent[0], nod_graf_curent[1] - 1),
                       (nod_graf_curent[0], nod_graf_curent[1] + 1),
                       (nod_graf_curent[0] - 1, nod_graf_curent[1]),
                       (nod_graf_curent[0] + 1, nod_graf_curent[1])]:  # parcurge lista celor 4 posibili succesori ai nodului curent (self)
            if 0 <= i < len(matrice) and 0 <= j < len(matrice[0]):
                if matrice[i][j] != "liber":  # verifica daca pozitia succesorului este ocupata de vreun elev
                    if ((matrice[i][j], matrice[nod_graf_curent[0]][nod_graf_curent[1]]) not in NodParcurgere.problema.lista_suparati) and ((matrice[nod_graf_curent[0]][nod_graf_curent[1]], matrice[i][j]) not in NodParcurgere.problema.lista_suparati):  # verifica daca elevul reprezentand nodul curent si cu elevul ce reprezinta posibilul succesor nu sunt certati
                        if i in [len(matrice) - 1, len(matrice) - 2]:  # verfica daca succesorul se afla pe ultimele doua linii
                            nod_info = (i, j)
                            if i == nod_graf_curent[0] + 1:
                                directie = "v"
                            elif i == nod_graf_curent[0] - 1:
                                directie = "^"
                            elif j == nod_graf_curent[1] + 1:
                                if j % 2 == 1:
                                    directie = ">"
                                else:
                                    directie = ">>"
                            else:
                                if j % 2 == 0:
                                    directie = "<"
                                else:
                                    directie = "<<"
                            succesori.append((Nod(nod_info, self.fct_h(nod_info)), 1, directie))

                        elif not ((j == nod_graf_curent[1] + 1 and j % 2 == 0) or (j == nod_graf_curent[1] - 1 and j % 2 == 1)):  # in acest caz succesorul nu se afla pe ultimele doua linii
                            if i == nod_graf_curent[0] + 1:
                                directie = "v"
                            elif i == nod_graf_curent[0] - 1:
                                directie = "^"
                            elif j == nod_graf_curent[1] + 1:
                                directie = ">"
                            else:
                                directie = "<"
                            nod_info = (i, j)
                            succesori.append((Nod(nod_info, self.fct_h(nod_info)), 1, directie))

        return succesori

    def fct_h1(self, nod_info):
        """
        Euristica este egala cu lungimea drumului pe care l-ar parcurge biletul insa luand in considerare si bancile libere si elevii suparati
        (biletul poate ajunge la un moment dat pe o banca libera sau poate fi trimis de elevul1 la elevul2 chiar daca elevul1 si elevul2 sunt suparati).
        Aceasta euristica va avea valoarea mai mica decat costul real, deoarcere la valoarea costului real se vor adauga ocolirea bancilor libere si evitarea
        transmiterii biletului intre elevii suparati.
        :param nod_info: acelasi ca si atributul info din clasa Nod
        :return: un intreg reprezentand euristica nodului ce are info = nod_info
        """
        i_curent = nod_info[0]
        j_curent = nod_info[1]
        i_final = NodParcurgere.problema.nod_scop.info[0]
        j_final = NodParcurgere.problema.nod_scop.info[1]
        matrice = NodParcurgere.problema.matrice_clasa

        if i_curent == len(matrice) - 1 or i_curent == len(matrice) - 2:
            return abs(i_curent - i_final) + abs(j_curent - j_final)

        if j_curent == j_final or (j_curent == j_final + 1 and j_curent % 2 == 1) or (
                j_curent == j_final - 1 and j_curent % 2 == 0):
            return abs(i_curent - i_final) + abs(j_curent - j_final)

        return (len(matrice) - 2 - i_curent) + abs(j_curent - j_final) + abs(len(matrice) - 2 - i_final)

    def fct_h2(self, nod_info):
        """
        Euristica este egala cu lungimea drumului pe care l-ar parcurge biletul mai intai coborand/urcand pana la linia nodului scop, si apoi mergand
        stanga/dreapta pana la pozitia nodului scop (biletul poate ajunga si in bancile libere, poate fi trimis si intre elevii suparati, si poate trece
        de la o coloana la alta fara restrictii).
        Este clar ca aceasta euristica este mai mica decat euristica de mai sus deoarece elemina si conditia de deplasare intre coloane, deci implicit
        este mai mica si decat costul real al drumului.
        :param nod_info: acelasi ca si atributul info din clasa Nod
        :return: un intreg reprezentand euristica nodului ce are info = nod_info
        """
        i_curent = nod_info[0]
        j_curent = nod_info[1]
        i_final = NodParcurgere.problema.nod_scop.info[0]
        j_final = NodParcurgere.problema.nod_scop.info[1]

        return abs(i_curent - i_final) + abs(j_curent - j_final)

    def fct_h3(self, nod_info):
        """
        --------Euristica gresita--------
        Contraexemplu: daca nodul curent se afla exect sub nodul scop, distanta reala este de 1, insa euristica rezultata pentru nodul curent este
        produsul dintre linia si coloana pe care se afla, ceea ce pate fi mai mare decat 1 => nu este o euristica admisibila
        :param nod_info: acelasi ca si atributul info din clasa Nod
        :return: un intreg reprezentand euristica nodului ce are info = nod_info
        """
        return nod_info[0] * nod_info[1]

    def test_scop(self):
        """
        :return: True daca nodul curent (self) este nodul scop, False altfel
        """
        return self.nod_graf.info == self.problema.nod_scop.info

    def __str__(self):
        if self.directie is None:
            return NodParcurgere.problema.matrice_clasa[self.nod_graf.info[0]][self.nod_graf.info[1]]
        else:
            return " " + self.directie + " " + NodParcurgere.problema.matrice_clasa[self.nod_graf.info[0]][self.nod_graf.info[1]]


def str_info_noduri(lista):
    """
    :param lista: lista ce contine obiecte de tip NodParcurgere
    :return: string ce reprezinta lista
    """
    sir = "\n"
    for nod in lista:
        sir += str(nod)
    sir += "\n"
    return sir


def in_lista(lista, nod):
    """
    :param lista: lista ce contine obiecte de tip NodParcurgere
    :param nod: obiect de tip Nod
    :return: elementul din lista care are nod_graf.info = nod.info, None daca nu se afla in lista
    """
    for i in range(len(lista)):
        if lista[i].nod_graf.info == nod.info:
            return lista[i]
    return None


def a_star(h, nume_fisier=None, modul_fisierului=None):
    """
    Functia care implementeaza algoritmul A-star
    Afisarea va fi realizata in consola daca nu se dau ultimii doi parametri, sau in fisierul "nume_fisier"
    :param h: euristica folosita
    :param nume_fisier: numele fisierului in care se va scrie rezultatul
    :param modul_fisierului: "w" sau "a" in functie de modul in care va fi deschis fisierul
    """
    radacina = NodParcurgere(NodParcurgere.problema.nod_start)
    lista_open = [radacina]  # open va contine elemente de tip NodParcurgere
    lista_closed = []  # open va contine elemente de tip NodParcurgere
    gasit = False

    if h == 1:
        NodParcurgere.fct_h = NodParcurgere.fct_h1
    elif h == 2:
        NodParcurgere.fct_h = NodParcurgere.fct_h2
    elif h == 3:
        NodParcurgere.fct_h = NodParcurgere.fct_h3

    time_start = time.time()
    nod_curent = None

    while len(lista_open):
        nod_curent = lista_open.pop(0)
        lista_closed.append(nod_curent)
        if nod_curent.test_scop() is True:
            gasit = True
            break
        succesori = nod_curent.expandeaza()
        for s in succesori:
            nod_nou = None
            nod_s = s[0]
            if nod_curent.contine_in_drum(nod_s) is False:
                nod_vechi_open = in_lista(lista_open, nod_s)
                nod_vechi_closed = in_lista(lista_closed, nod_s)
                if nod_vechi_open is not None:
                    if nod_vechi_open.f > nod_s.h + nod_curent.g + s[1]:
                        lista_open.remove(nod_vechi_open)
                        nod_nou = NodParcurgere(nod_s, nod_curent, nod_curent.g + s[1], s[2])
                elif nod_vechi_closed is not None:
                    if nod_vechi_closed.f > nod_s.h + nod_curent.g + s[1]:
                        lista_closed.remove(nod_vechi_closed)
                        nod_nou = NodParcurgere(nod_s, nod_curent, nod_curent.g + s[1], s[2])
                else:
                    nod_nou = NodParcurgere(nod_s, nod_curent, nod_curent.g + s[1], s[2])

                if nod_nou is not None:
                    i = 0
                    while i < len(lista_open):
                        if lista_open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(lista_open) and lista_open[i].f == nod_nou.f and lista_open[i].g > nod_nou.g:
                                i += 1
                            break
                    lista_open.insert(i, nod_nou)

    time_stop = time.time()

    if nume_fisier is not None:
        with open(nume_fisier, modul_fisierului) as g:
            g.write(f"\n------------- Concluzie pentru folosirea euristicii {h} -------------\n")
            if len(lista_open) == 0 and not gasit:
                g.write(f"Nu exista drum de la {NodParcurgere.problema.matrice_clasa[NodParcurgere.problema.nod_start.info[0]][NodParcurgere.problema.nod_start.info[1]]} la {NodParcurgere.problema.matrice_clasa[NodParcurgere.problema.nod_scop.info[0]][NodParcurgere.problema.nod_scop.info[1]]}\n")
            else:
                drum = nod_curent.drum_arbore()
                g.write(f"Drumul biletului este: {str_info_noduri(drum)}\n")
                g.write(f"Numarul de elevi pe la care trece biletul: {len(drum)}\n")
            g.write(f"Timpul de executare: {time_stop - time_start}\n")

    else:
        print(f"------------- Concluzie pentru folosirea euristicii {h} -------------\n")
        if len(lista_open) == 0 and not gasit:
            print(f"Nu exista drum de la {NodParcurgere.problema.matrice_clasa[NodParcurgere.problema.nod_start.info[0]][NodParcurgere.problema.nod_start.info[1]]} la {NodParcurgere.problema.matrice_clasa[NodParcurgere.problema.nod_scop.info[0]][NodParcurgere.problema.nod_scop.info[1]]}")
        else:
            drum = nod_curent.drum_arbore()
            print(f"Drumul biletului este: {str_info_noduri(drum)}")
            print(f"Numarul de elevi pe la care trece biletul: {len(drum)}")
        print(f"Timpul de executare: {time_stop - time_start}\n")


def cautare_pozitie_nume(matrice, nume):
    """
    :param matrice: matrice de nume
    :param nume: string reprezentand un nume
    :return: tuplu reprezentand pozitia pe care o ocupe numele in matrice, None altfel (insa se stie sigur ca se va gasi)
    """
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j] == nume:
                return i, j
    return None


def citire_problema(nume_fisier):
    """
    Realizeaza citirea datelor din fisier si crearea problemei
    :param nume_fisier: numele fisierului din care se citesc datele problemei
    :return: obiect de tip Problema
    """
    matrice_clasa = []
    lista_suparati = []

    with open(nume_fisier, "r") as f:
        line = f.readline().replace("\n", "")
        while line != "suparati":
            nume = line.split(" ")
            matrice_clasa.append(nume)
            line = f.readline().replace("\n", "")

        line = f.readline().replace("\n", "")
        while line.split(" ")[0] != "mesaj:":
            nume = line.split(" ")
            lista_suparati.append((nume[0], nume[1]))
            line = f.readline().replace("\n", "")

        nume_start = line.split(" ")[1]
        nume_scop = line.split(" ")[3]
        start = cautare_pozitie_nume(matrice_clasa, nume_start)
        scop = cautare_pozitie_nume(matrice_clasa, nume_scop)

    return Problema(start, scop, matrice_clasa, lista_suparati)


if __name__ == "__main__":
    fisiere_input = ["input_1.txt", "input_2.txt", "input_3.txt", "input_4.txt"]
    for index in range(len(fisiere_input)):
        NodParcurgere.problema = citire_problema(fisiere_input[index])
        nume_fisier_output = f"output_{index + 1}.txt"
        a_star(1, nume_fisier_output, "w")
        a_star(2, nume_fisier_output, "a")
        a_star(3, nume_fisier_output, "a")

    NodParcurgere.problema = Problema()
    a_star(1)
    a_star(2)
    a_star(3)
