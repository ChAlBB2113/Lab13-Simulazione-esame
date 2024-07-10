import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        listaAnni=self._model.GetListaAnni()
        for anno in listaAnni:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))

        listaForme=self._model.getListaForme()
        for forma in listaForme:
            self._view.ddshape.options.append(ft.dropdown.Option(forma))

        self._view.update_page()
    #questo metodo non è chiamato da alcun input utente es pressione bottone o scelta da dropdown
    #ma è una attività che fa parte della inizializzazione della pagina; quindi
    #deve essere chiamato dalla funzione load interface della view che sarà a sua volta chiamata
    #dal main quando si fa il run


    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.txt_result.controls.append(ft.Text(f"scegliere un anno"))
            self._view.update_page()
            return
        if self._view.ddshape.value is None:
            self._view.txt_result.controls.append(ft.Text(f"scegliere una forma"))
            self._view.update_page()
            return

        anno=self._view.ddyear.value
        forma=self._view.ddshape.value

        print (anno, forma)
        self._model.creaGrafo(anno, forma)
        print(f"..................{self._model._grafo.nodes()}")
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.getNumeroNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {self._model.getNumeroArchi()}"))
        for nodo in self._model._dizionarioPesoAdicenti:
            self._view.txt_result.controls.append(ft.Text(f"Nodo:{nodo.id}, somma pesi su archi= {self._model._dizionarioPesoAdicenti[nodo]}"))
        self._view.update_page()


    def handle_path(self, e):
            pass