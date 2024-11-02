from tkinter import Tk, Frame, Label, Entry, Button, Scrollbar, VERTICAL, HORIZONTAL, N, S, E, W
from tkinter.ttk import Treeview  # Importa Treeview da tkinter.ttk

def crea_finestra_principale():
    root = Tk()
    root.title("Stocks Manager")
    return root

def crea_layout_GUI(root, lotti, aggiungi_lotto, modifica_lotto, elimina_lotto, on_treeview_click):
    frame = Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10)

    Label(frame, text="Nome Azione").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = Entry(frame)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    Label(frame, text="Prezzo Acquisto").grid(row=1, column=0, padx=5, pady=5)
    entry_prezzo_acquisto = Entry(frame)
    entry_prezzo_acquisto.grid(row=1, column=1, padx=5, pady=5)

    Label(frame, text="Quantità").grid(row=2, column=0, padx=5, pady=5)
    entry_quantita = Entry(frame)
    entry_quantita.grid(row=2, column=1, padx=5, pady=5)

    Button(frame, text="Aggiungi Lotto", command=aggiungi_lotto).grid(row=3, column=0, padx=5, pady=5)
    Button(frame, text="Modifica Lotto", command=modifica_lotto).grid(row=3, column=1, padx=5, pady=5)
    Button(frame, text="Elimina Lotto", command=elimina_lotto).grid(row=3, column=2, padx=5, pady=5)

    tree = Treeview(root, columns=("Nome", "Prezzo Acquisto", "Prezzo", "Quantità"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Prezzo Acquisto", text="Prezzo Acquisto")
    tree.heading("Prezzo", text="Prezzo")
    tree.heading("Quantità", text="Quantità")
    tree.grid(row=1, column=0, padx=10, pady=10, sticky=(N, S, E, W))

    scrollbar_verticale = Scrollbar(root, orient=VERTICAL, command=tree.yview)
    scrollbar_verticale.grid(row=1, column=1, sticky=(N, S))
    tree.configure(yscrollcommand=scrollbar_verticale.set)

    scrollbar_orizzontale = Scrollbar(root, orient=HORIZONTAL, command=tree.xview)
    scrollbar_orizzontale.grid(row=2, column=0, sticky=(E, W))
    tree.configure(xscrollcommand=scrollbar_orizzontale.set)

    tree.bind('<<TreeviewSelect>>', lambda event: on_treeview_click(event, entry_nome, entry_prezzo_acquisto, entry_quantita))

    return frame, entry_nome, entry_prezzo_acquisto, entry_quantita, tree

def aggiorna_tabella(tree, lotti):
    for item in tree.get_children():
        tree.delete(item)
    for lotto in lotti:
        tree.insert("", "end", values=(lotto.nome, lotto.prezzo_acquisto, lotto.prezzo, lotto.quantita))

def on_treeview_click(event, entry_nome, entry_prezzo_acquisto, entry_quantita):
    selected_item = event.widget.selection()
    if selected_item:
        item = selected_item[0]
        values = event.widget.item(item, "values")
        entry_nome.delete(0, 'end')
        entry_nome.insert(0, values[0])
        entry_prezzo_acquisto.delete(0, 'end')
        entry_prezzo_acquisto.insert(0, values[1])
        entry_quantita.delete(0, 'end')
        entry_quantita.insert(0, values[3])
