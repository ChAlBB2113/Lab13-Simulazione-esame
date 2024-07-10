import copy

import networkx

from database.DAO import DAO


class Model:
    def __init__(self):
        #per loading pagina
        self._listaAnni=[]
        self._listaForme=[]
        #per creazione grafo
        self._listaNodi=[]
        self._listaArchi=[]
        self._grafo= networkx.Graph()
        self._dizionarioNodi={}
        self._dizArchiPesi={}
        self._dizionarioPesoAdicenti={}

    #per loading pagina:sti metodi li chiamero nel fillDD nel controller
    def aggiornaListaAnni(self):
        self._listaAnni=DAO.getAnni()

    def GetListaAnni(self):
        self._listaAnni.clear()
        self.aggiornaListaAnni()
        return self._listaAnni

    def aggiornaListaForme(self):
        self._listaForme=DAO.getForme()

    def getListaForme(self):
        self._listaForme.clear()
        self.aggiornaListaForme()
        return self._listaForme


    #per creazione grafo: nel contorller chiamero solo creagrafo che dovra chiamare tutti altri metodi qui sotto
    def getNodi(self):
        self._listaNodi=DAO.getStati()

    def getArchi(self, dizionarioStati):
        self._listaArchi=DAO.getArchi(dizionarioStati)

    def getPesoPerArco(self, anno, forma, dizionarioArchiPesiInizializzati):
        self._dizArchiPesi=DAO.aggiornaDizArchiPesi(anno, forma, dizionarioArchiPesiInizializzati)



    def creaGrafo(self, anno, forma): #deve prendere parametri che servono a metodi che chiama,
                                      #oppure crearli nel suo corpo

        #pulisco tutto per nuova chiamata se non è la prima
        self._listaNodi.clear()
        self._listaArchi.clear()
        self._grafo.clear()
        self._dizionarioNodi.clear()
        self._dizArchiPesi.clear()
        self._dizionarioPesoAdicenti.clear()

        #creo tutto (o ricreo se non è prima chiamata) con metodi definiti qui sopra e altri di libreria
        self.getNodi()
        print(self._listaNodi)

        self._grafo.add_nodes_from(self._listaNodi)


        for nodo in self._listaNodi:
            self._dizionarioNodi[nodo.id]=nodo

        self.getArchi(self._dizionarioNodi)
        #self._grafo.add_edges_from(self._listaArchi)

        for arco in self._listaArchi:
            self._dizArchiPesi[arco[0].id, arco[1].id ]=0

        self.getPesoPerArco(anno, forma, self._dizArchiPesi) #a questo punto diz archi pesi è gia inizializzato
        #che assegna al self._dizArchiPeso un nuovo dizionario uguale a quello di prima ma con i pesi aggiornati

        for chiave,valore in self._dizArchiPesi.items():
            print(chiave,valore)
            #occhio che chiave non è tupla con due stati ma tupla id di due stati
            self._grafo.add_edge(self._dizionarioNodi[chiave[0]], self._dizionarioNodi[chiave[1]], weight=valore)

        for nodo in self._listaNodi:
            sum=0
            for vicino in self._grafo.neighbors(nodo):
                sum+=self._grafo[nodo][vicino]['weight']
            self._dizionarioPesoAdicenti[nodo]=sum

    def getNumeroNodi(self):
        return len(self._grafo.nodes())
    def getNumeroArchi(self):
        return len(self._grafo.edges())