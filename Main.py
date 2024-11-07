import json  # Per la gestione dei file JSON
from tkinter import messagebox  # Per le finestre di messaggio
from Get_Price import recupera_prezzo_corrente  # Funzione per il prezzo corrente
from get_eps import mostra_eps  # Funzione per visualizzare il grafico degli EPS
from Get_Ratios import mostra_ratios  # Funzione per visualizzare i grafici PE e PB
from GUI import crea_finestra_principale, crea_layout_GUI, aggiorna_tabella, on_treeview_click  # Import GUI functions

# Classe per rappresentare un lotto di azioni
class LottoAzione:
    def __init__(self, nome, prezzo_acquisto, prezzo, quantita, pe_ratio=None, pb_ratio=None):
        self.nome = nome
        self.prezzo_acquisto = prezzo_acquisto
        self.prezzo = prezzo
        self.quantita = quantita
        self.pe_ratio = pe_ratio
        self.pb_ratio = pb_ratio

    def calcola_PL_percentuale(self):
        return ((self.prezzo - self.prezzo_acquisto) / self.prezzo_acquisto) * 100

    def modifica(self, prezzo_acquisto, prezzo, quantita):
        self.prezzo_acquisto = prezzo_acquisto
        self.prezzo = prezzo
        self.quantita = quantita

# Funzione per salvare i dati
def salva_dati(lotti, filename):
    with open(filename, 'w') as file:
        json.dump([lotto.__dict__ for lotto in lotti], file)

# Funzione per caricare i dati
def carica_dati(filename):
    try:
        with open(filename, 'r') as file:
            lotti_dati = json.load(file)
            return [LottoAzione(**dati) for dati in lotti_dati]
    except FileNotFoundError:
        return []

def aggiungi_lotto(entry_nome, entry_prezzo_acquisto, entry_quantita, lotti, tree):
    if not entry_nome.get() or not entry_prezzo_acquisto.get() or not entry_quantita.get():
        messagebox.showwarning("Input Mancante", "Compila tutti i campi.")
        return
    nome = entry_nome.get()
    prezzo_acquisto = float(entry_prezzo_acquisto.get())
    quantita = int(entry_quantita.get())
    prezzo = recupera_prezzo_corrente(nome)
    if prezzo is None:
        return
    if messagebox.askokcancel("Conferma", "Sei sicuro di aggiungere questo lotto?"):
        lotto = LottoAzione(nome, prezzo_acquisto, prezzo, quantita)
        lotti.append(lotto)
        salva_dati(lotti, 'StocksManager.json')
        aggiorna_tabella(tree, lotti)

def modifica_lotto(entry_nome, entry_prezzo_acquisto, entry_quantita, lotti, tree):
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]
        nome = tree.item(item, 'values')[0]
        for lotto in lotti:
            if lotto.nome == nome:
                if not entry_nome.get() or not entry_prezzo_acquisto.get() or not entry_quantita.get():
                    messagebox.showwarning("Input Mancante", "Compila tutti i campi.")
                    return
                prezzo = recupera_prezzo_corrente(nome)
                if prezzo is None:
                    return
                if messagebox.askokcancel("Conferma", "Sei sicuro di modificare questo lotto?"):
                    lotto.modifica(float(entry_prezzo_acquisto.get()), prezzo, int(entry_quantita.get()))
                    salva_dati(lotti, 'StocksManager.json')
                    aggiorna_tabella(tree, lotti)
                    return
    else:
        messagebox.showwarning("Selezione Mancante", "Seleziona un lotto da modificare.")

def elimina_lotto(lotti, tree):
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]
        nome = tree.item(item, 'values')[0]
        for lotto in lotti:
            if lotto.nome == nome:
                if messagebox.askokcancel("Conferma", "Sei sicuro di eliminare questo lotto?"):
                    lotti.remove(lotto)
                    salva_dati(lotti, 'StocksManager.json')
                    aggiorna_tabella(tree, lotti)
                    return
    else:
        messagebox.showwarning("Selezione Mancante", "Seleziona un lotto da eliminare.")

# Carica i dati
lotti = carica_dati('StocksManager.json')

# Crea la finestra principale e il layout GUI
root = crea_finestra_principale()
frame, entry_nome, entry_prezzo_acquisto, entry_quantita, tree = crea_layout_GUI(
    root, lotti,
    lambda: aggiungi_lotto(entry_nome, entry_prezzo_acquisto, entry_quantita, lotti, tree),
    lambda: modifica_lotto(entry_nome, entry_prezzo_acquisto, entry_quantita, lotti, tree),
    lambda: elimina_lotto(lotti, tree),
    on_treeview_click,
    lambda: mostra_eps(entry_nome.get())
)

# Aggiorna la tabella con i dati caricati
aggiorna_tabella(tree, lotti)

# Avvia il loop principale della GUI
root.mainloop()
