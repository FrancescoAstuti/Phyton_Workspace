import json  # For handling JSON files
from tkinter import *  # For the graphical user interface
from tkinter import messagebox  # For message boxes
from tkinter import ttk  # For themed widgets like Treeview
from Get_Price import recupera_prezzo_corrente  # Function to get the current price
from get_eps import mostra_eps  # Function to display the EPS chart
from Get_Ratios import mostra_ratios  # Function to display PE and PB charts

# Class to represent a batch of stocks
class LottoAzione:
    def __init__(self, nome, prezzo_acquisto, prezzo, quantita):
        self.nome = nome  # Stock name
        self.prezzo_acquisto = prezzo_acquisto  # Purchase price
        self.prezzo = prezzo  # Current price
        self.quantita = quantita  # Quantity

    def calcola_PL_percentuale(self):
        # Calculate the profit/loss percentage
        return ((self.prezzo - self.prezzo_acquisto) / self.prezzo_acquisto) * 100

    def modifica(self, prezzo_acquisto, prezzo, quantita):
        # Modify the batch details
        self.prezzo_acquisto = prezzo_acquisto
        self.prezzo = prezzo
        self.quantita = quantita

# Function to save data
def salva_dati(lotti, filename):
    with open(filename, 'w') as file:
        # Save the list of batches to a JSON file
        json.dump([lotto.__dict__ for lotto in lotti], file)

# Function to load data
def carica_dati(filename):
    try:
        with open(filename, 'r') as file:
            # Load the JSON data from the file
            lotti_dati = json.load(file)
            # Create a list of LottoAzione objects from the JSON data
            return [LottoAzione(dati['nome'], dati['prezzo_acquisto'], dati['prezzo'], dati['quantita']) for dati in lotti_dati]
    except FileNotFoundError:
        # Return an empty list if the file does not exist
        return []

# Functions to add, modify, and delete a batch
def aggiungi_lotto():
    if not entry_nome.get() or not entry_prezzo_acquisto.get() or not entry_quantita.get():
        messagebox.showwarning("Input Mancante", "Compila tutti i campi.")  # Show warning if fields are empty
        return
    nome = entry_nome.get()  # Get stock name from entry
    prezzo_acquisto = float(entry_prezzo_acquisto.get())  # Get purchase price from entry
    quantita = int(entry_quantita.get())  # Get quantity from entry
    prezzo = recupera_prezzo_corrente(nome)  # Get current price using the function
    if prezzo is None:
        return
    if messagebox.askokcancel("Conferma", "Sei sicuro di aggiungere questo lotto?"):  # Confirm addition
        lotto = LottoAzione(nome, prezzo_acquisto, prezzo, quantita)  # Create a new batch object
        lotti.append(lotto)  # Add the batch to the list
        salva_dati(lotti, 'StocksManager.json')  # Save the updated list to the file
        aggiorna_tabella()  # Update the table

def modifica_lotto():
    selected_item = tree.selection()  # Get the selected item from the table
    if selected_item:
        item = selected_item[0]  # Get the first selected item
        nome = tree.item(item, 'values')[0]  # Get the stock name from the item
        for lotto in lotti:
            if lotto.nome == nome:  # Find the batch with the matching name
                if not entry_nome.get() or not entry_prezzo_acquisto.get() or not entry_quantita.get():
                    messagebox.showwarning("Input Mancante", "Compila tutti i campi.")  # Show warning if fields are empty
                    return
                prezzo = recupera_prezzo_corrente(nome)  # Get current price using the function
                if prezzo is None:
                    return
                if messagebox.askokcancel("Conferma", "Sei sicuro di modificare questo lotto?"):  # Confirm modification
                    lotto.modifica(float(entry_prezzo_acquisto.get()), prezzo, int(entry_quantita.get()))  # Modify the batch details
                    salva_dati(lotti, 'StocksManager.json')  # Save the updated list to the file
                    aggiorna_tabella()  # Update the table
                    return
    else:
        messagebox.showwarning("Selezione Mancante", "Seleziona un lotto da modificare.")  # Show warning if no item is selected

def elimina_lotto():
    selected_item = tree.selection()  # Get the selected item from the table
    if selected_item:
        item = selected_item[0]  # Get the first selected item
        nome = tree.item(item, 'values')[0]  # Get the stock name from the item
        for lotto in lotti:
            if lotto.nome == nome:  # Find the batch with the matching name
                if messagebox.askokcancel("Conferma", "Sei sicuro di eliminare questo lotto?"):  # Confirm deletion
                    lotti.remove(lotto)  # Remove the batch from the list
                    salva_dati(lotti, 'StocksManager.json')  # Save the updated list to the file
                    aggiorna_tabella()  # Update the table
                    return
    else:
        messagebox.showwarning("Selezione Mancante", "Seleziona un lotto da eliminare.")  # Show warning if no item is selected

def aggiorna_tabella():
    for i in tree.get_children():
        tree.delete(i)  # Clear the table
    for lotto in lotti:
        tree.insert("", "end", values=(lotto.nome, lotto.prezzo_acquisto, lotto.prezzo, lotto.quantita, f"{lotto.calcola_PL_percentuale():.2f}"))  # Insert updated data

def on_treeview_click(event):
    selected_item = tree.selection()  # Get the selected item from the table
    if selected_item:
        item = selected_item[0]  # Get the first selected item
        values = tree.item(item, 'values')  # Get the values from the item
        entry_nome.delete(0, END)  # Clear the entry for stock name
        entry_nome.insert(0, values[0])  # Insert the stock name into the entry
        entry_prezzo_acquisto.delete(0, END)  # Clear the entry for purchase price
        entry_prezzo_acquisto.insert(0, values[1])  # Insert the purchase price into the entry
        entry_quantita.delete(0, END)  # Clear the entry for quantity
        entry_quantita.insert(0, values[3])  # Insert the quantity into the entry

# Load data and configure the main window
lotti = carica_dati('StocksManager.json')  # Load the data from the file

root = Tk()
root.title("Gestione Portfolio Azioni")  # Set the window title

# Configure style
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")  # Configure button style
style.configure("TEntry", padding=5)  # Configure entry style
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))  # Configure label style
style.configure("Treeview", rowheight=25)  # Configure Treeview style

# GUI layout
frame = Frame(root, bg="#f0f0f0")
frame.pack(pady=10, padx=10, fill=X)  # Pack the frame with padding

lbl_nome = Label(frame, text="Nome Azione", bg="#f0f0f0")
lbl_nome.grid(row=0, column=0, sticky=W)  # Label for stock name
entry_nome = Entry(frame)
entry_nome.grid(row=0, column=1)  # Entry for stock name

lbl_prezzo_acquisto = Label(frame, text="Prezzo Acquisto", bg="#f0f0f0")
lbl_prezzo_acquisto.grid(row=1, column=0, sticky=W)  # Label for purchase price
entry_prezzo_acquisto = Entry(frame)
entry_prezzo_acquisto.grid(row=1, column=1)  # Entry for purchase price

lbl_quantita = Label(frame, text="Quantità", bg="#f0f0f0")
lbl_quantita.grid(row=2, column=0, sticky=W)  # Label for quantity
entry_quantita = Entry(frame)
entry_quantita.grid(row=2, column=1)  # Entry for quantity

btn_aggiungi = Button(frame, text="Aggiungi Lotto", command=aggiungi_lotto)
btn_aggiungi.grid(row=3, column=0, pady=10)  # Button to add batch

btn_modifica = Button(frame, text="Modifica Lotto", command=modifica_lotto)
btn_modifica.grid(row=3, column=1, pady=10)  # Button to modify batch

btn_elimina = Button(frame, text="Elimina Lotto", command=elimina_lotto)
btn_elimina.grid(row=3, column=2, pady=10)  # Button to delete batch

# Table
tree = ttk.Treeview(root, columns=("Nome", "Prezzo Acquisto", "Prezzo", "Quantità", "P/L %"), show='headings', height=10)
tree.heading("Nome", text="Nome")  # Column heading for stock name
tree.heading("Prezzo Acquisto", text="Prezzo Acquisto")  # Column heading for purchase price
tree.heading("Prezzo", text="Prezzo Corrente")  # Column heading for current price
tree.heading("Quantità", text="Quantità")  # Column heading for quantity
tree.heading("P/L %", text="P/L %")  # Column heading for profit/loss percentage
tree.bind("<ButtonRelease-1>", on_treeview_click)  # Bind click event to Treeview
tree.pack(pady=10)  # Pack the Treeview with padding

# Buttons for EPS, PE, and PB charts
btn_eps = Button(root, text="EPS", command=lambda: mostra_eps(entry_nome.get()))
btn_eps.pack(side=LEFT, padx=5, pady=5)  # Button to display EPS chart

btn_pe = Button(root, text="PE Ratio", command=lambda: mostra_ratios(entry_nome.get(), 'PE'))
btn_pe.pack(side=LEFT, padx=5, pady=5)  # Button to display PE ratio chart

btn_pb = Button(root, text="PB Ratio", command=lambda: mostra_ratios(entry_nome.get(), 'PB'))
btn_pb.pack(side=LEFT, padx=5, pady=5)  # Button to display PB ratio chart

aggiorna_tabella()  # Update the table with data

root.mainloop()  # Run the Tkinter main loop
