import json  # Per la gestione dei file JSON
from tkinter import *  # Per l'interfaccia grafica
from tkinter import messagebox  # Per le finestre di messaggio
from tkinter import ttk  # Per i widget tematici come Treeview
from Get_Price import recupera_prezzo_corrente  # Funzione per il prezzo corrente
from get_eps import mostra_eps  # Funzione per visualizzare il grafico degli EPS
from Get_Ratios import mostra_ratios  # Funzione per visualizzare i grafici PE e PB

# Classe per rappresentare un lotto di azioni
class LottoAzione:
    def __init__(self, nome, prezzo_acquisto, prezzo, quantita):
        self.nome = nome
        self.prezzo_acquisto = prezzo_acquisto
        self.prezzo = prezzo
        self.quantita = quantita

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

# Funzioni per aggiungere, modificare ed eliminare un lotto
def aggiungi_lotto():
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
        aggiorna_tabella()

def modifica_lotto():
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
                    aggiorna_tabella()
                    return
    else:
        messagebox.showwarning("Selezione Mancante", "Seleziona un lotto da modificare.")

def elimina_lotto():
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]
        nome = tree.item(item, 'values')[0]
        for lotto in lotti:
            if lotto.nome == nome:
                if messagebox.askokcancel("Conferma", "Sei sicuro di eliminare questo lotto?"):
                    lotti.remove(lotto)
                    salva_dati(lotti, 'StocksManager.json')
                    aggiorna_tabella()
                    return
    else:
        messagebox.showwarning("Selezione Mancante", "Seleziona un lotto da eliminare.")

def aggiorna_tabella():
    for i in tree.get_children():
        tree.delete(i)
    for lotto in lotti:
        tree.insert("", "end", values=(lotto.nome, lotto.prezzo_acquisto, lotto.prezzo, lotto.quantita, f"{lotto.calcola_PL_percentuale():.2f}"))

def on_treeview_click(event):
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]
        values = tree.item(item, 'values')
        entry_nome.delete(0, END)
        entry_nome.insert(0, values[0])
        entry_prezzo_acquisto.delete(0, END)
        entry_prezzo_acquisto.insert(0, values[1])
        entry_quantita.delete(0, END)
        entry_quantita.insert(0, values[3])

# Carica i dati e configura la finestra principale
lotti = carica_dati('StocksManager.json')

root = Tk()
root.title("Gestione Portfolio Azioni")

# Configura stile
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
style.configure("TEntry", padding=5)
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
style.configure("Treeview", rowheight=25)

# Layout GUI
frame = Frame(root, bg="#f0f0f0")
frame.pack(pady=10, padx=10, fill=X)

lbl_nome = Label(frame, text="Nome Azione", bg="#f0f0f0")
lbl_nome.grid(row=0, column=0, sticky=W)
entry_nome = Entry(frame)
entry_nome.grid(row=0, column=1)

lbl_prezzo_acquisto = Label(frame, text="Prezzo Acquisto", bg="#f0f0f0")
lbl_prezzo_acquisto.grid(row=1, column=0, sticky=W)
entry_prezzo_acquisto = Entry(frame)
entry_prezzo_acquisto.grid(row=1, column=1)

lbl_quantita = Label(frame, text="Quantità", bg="#f0f0f0")
lbl_quantita.grid(row=2, column=0, sticky=W)
entry_quantita = Entry(frame)
entry_quantita.grid(row=2, column=1)

btn_aggiungi = Button(frame, text="Aggiungi Lotto", command=aggiungi_lotto)
btn_aggiungi.grid(row=3, column=0, pady=10)

btn_modifica = Button(frame, text="Modifica Lotto", command=modifica_lotto)
btn_modifica.grid(row=3, column=1, pady=10)

btn_elimina = Button(frame, text="Elimina Lotto", command=elimina_lotto)
btn_elimina.grid(row=3, column=2, pady=10)

# Tabella
tree = ttk.Treeview(root, columns=("Nome", "Prezzo Acquisto", "Prezzo", "Quantità", "P/L %"), show='headings', height=10)
tree.heading("Nome", text="Nome")
tree.heading("Prezzo Acquisto", text="Prezzo Acquisto")
tree.heading("Prezzo", text="Prezzo Corrente")
tree.heading("Quantità", text="Quantità")
tree.heading("P/L %", text="P/L %")
tree.bind("<ButtonRelease-1>", on_treeview_click)
tree.pack(pady=10)

# Pulsanti per grafici EPS, PE e PB
btn_eps = Button(root, text="EPS", command=lambda: mostra_eps(entry_nome.get()))
btn_eps.pack(side=LEFT, padx=5, pady=5)

btn_pe = Button(root, text="PE Ratio", command=lambda: mostra_ratios(entry_nome.get(), 'PE'))
btn_pe.pack(side=LEFT, padx=5, pady=5)

btn_pb = Button(root, text="PB Ratio", command=lambda: mostra_ratios(entry_nome.get(), 'PB'))
btn_pb.pack(side=LEFT, padx=5, pady=5)

aggiorna_tabella()

root.mainloop()
