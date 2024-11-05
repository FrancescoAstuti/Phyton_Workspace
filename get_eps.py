import requests
import matplotlib.pyplot as plt
from tkinter import messagebox

API_KEY = '11CAQCZUVYCUIZ3V'  # Inserisci la tua chiave API di Alpha Vantage

def mostra_eps(nome_azione):
    if not nome_azione:
        messagebox.showwarning("Input Mancante", "Inserisci un nome per l'azione.")
        return

    # URL dell'API per ottenere gli EPS annuali e le stime dell'azione specificata
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={nome_azione}&apikey={API_KEY}'

    try:
        response = requests.get(url)
        data = response.json()
    except requests.RequestException as e:
        messagebox.showerror("Errore di Rete", f"Errore durante la connessione: {e}")
        return

    # Debug: stampare i dati grezzi ricevuti
    print("Dati grezzi ricevuti dall'API:", data)

    # Controllo dati EPS storici
    if 'annualEarnings' not in data or not data['annualEarnings']:
        messagebox.showerror("Dati Mancanti", f"Nessun dato EPS disponibile per {nome_azione}.")
        return

    # Estrazione dei dati storici EPS
    earnings_data = [
        (item['fiscalDateEnding'][:4], float(item['reportedEPS']))
        for item in data['annualEarnings']
    ]
    earnings_data.sort(key=lambda x: int(x[0]))  # Ordina per anno

    # Debug: stampa i dati EPS ordinati
    print("Dati EPS storici:", earnings_data)

    # Estrazione delle stime EPS (se disponibili)
    estimates_data = []
    if 'annualEstimates' in data:
        estimates_data = [
            (item['fiscalDateEnding'][:4], float(item['estimatedEPS']))
            for item in data['annualEstimates'] if 'estimatedEPS' in item
        ]
        estimates_data.sort(key=lambda x: int(x[0]))  # Ordina per anno

        # Debug: stampa i dati delle stime EPS ordinati
        print("Dati stime EPS:", estimates_data)

    # Separazione degli anni e degli EPS per il grafico
    anni_storici = [item[0] for item in earnings_data]
    eps_storici = [item[1] for item in earnings_data]

    anni_stimati = [item[0] for item in estimates_data]
    eps_stimati = [item[1] for item in estimates_data]

    # Creazione del grafico con EPS storici e stime
    plt.figure(figsize=(10, 6))
    plt.bar(anni_storici, eps_storici, color='blue', label="EPS Storici")
    plt.plot(anni_stimati, eps_stimati, color='red', marker='o', linestyle='--', label="Stime EPS")
    
    plt.title(f'EPS Annuali e Stime per {nome_azione}')
    plt.xlabel('Anno')
    plt.ylabel('EPS (Earnings Per Share)')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()
