from tkinter import Tk, Frame, Label, Entry, Button, Scrollbar, VERTICAL, HORIZONTAL, N, S, E, W
from tkinter.ttk import Treeview, Style
import matplotlib.pyplot as plt
import requests

API_KEY = 'eb7366217370656d66a56a057b8511b0'  # Updated to FMP API Key

def get_current_ratio(ticker, ratio_type):
    url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if ratio_type == 'PE':
        return data[0].get('priceEarningsRatioTTM', 0)
    elif ratio_type == 'PB':
        return data[0].get('priceToBookRatioTTM', 0)
    return 0

def crea_finestra_principale():
    root = Tk()
    root.title("Stocks Manager")
    return root

def crea_layout_GUI(root, lotti, aggiungi_lotto, modifica_lotto, elimina_lotto, on_treeview_click, mostra_grafico):
    style = Style()
    style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
    
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

    tree = Treeview(root, columns=("Nome", "Prezzo Acquisto", "Prezzo", "Quantità", "PE TTM", "PB TTM"), show="headings")
    tree.heading("Nome", text="Nome", command=lambda: sort_column(tree, "Nome", False))
    tree.heading("Prezzo Acquisto", text="Prezzo Acquisto", command=lambda: sort_column(tree, "Prezzo Acquisto", False))
    tree.heading("Prezzo", text="Prezzo", command=lambda: sort_column(tree, "Prezzo", False))
    tree.heading("Quantità", text="Quantità", command=lambda: sort_column(tree, "Quantità", False))
    tree.heading("PE TTM", text="PE TTM", command=lambda: sort_column(tree, "PE TTM", False))
    tree.heading("PB TTM", text="PB TTM", command=lambda: sort_column(tree, "PB TTM", False))
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
        pe_ttm = get_current_ratio(lotto.nome, 'PE')
        pb_ttm = get_current_ratio(lotto.nome, 'PB')
        tree.insert("", "end", values=(lotto.nome, lotto.prezzo_acquisto, lotto.prezzo, lotto.quantita, pe_ttm, pb_ttm))

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

def mostra_grafico(ticker, years, ratios, ratio_type):
    plt.figure(figsize=(10, 6))
    plt.plot(years, ratios, marker='o', linestyle='-', color='purple')
    plt.xlabel("Anno")
    plt.ylabel(f"{ratio_type} Ratio")
    plt.title(f"{ratio_type} Ratio Storico per {ticker}")
    plt.grid()
    plt.show()

def sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: sort_column(tv, col, not reverse))
