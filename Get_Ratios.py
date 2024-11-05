import requests
import matplotlib.pyplot as plt

API_KEY = 'eb7366217370656d66a56a057b8511b0'  # Updated to FMP API Key

def get_annual_ratio(ticker, ratio_type, year):
    """
    Ottiene il valore annuale del ratio (PE o PB) da FMP.

    Args:
    ticker (str): Il simbolo del ticker.
    ratio_type (str): Il tipo di ratio ('PE' o 'PB').
    year (int): L'anno per cui ottenere il ratio.

    Returns:
    float: Il valore annuale del ratio.
    """
    url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Debug: stampare i dati grezzi ricevuti
    print(f"Dati grezzi ricevuti dall'API per il {year}: ", data)
    
    for item in data:
        if str(year) in item['date']:
            if ratio_type == 'PE':
                return float(item.get('priceEarningsRatio', 0))
            elif ratio_type == 'PB':
                return float(item.get('priceToBookRatio', 0))
    return 0

def mostra_ratios(ticker, ratio_type):
    """
    Mostra una serie storica di PE o PB ratios per un dato ticker utilizzando valori annuali.

    Args:
    ticker (str): Il simbolo del ticker per cui mostrare i ratios.
    ratio_type (str): Il tipo di ratio da mostrare ('PE' o 'PB').

    Returns:
    None
    """
    years = list(range(2019, 2024))
    ratios = [get_annual_ratio(ticker, ratio_type, year) for year in years]

    # Debug: stampare i dati dei ratios
    print(f"Dati {ratio_type} ratios annuali per {ticker}:", ratios)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, ratios, marker='o', linestyle='-', color='purple')
    plt.xlabel("Anno")
    plt.ylabel(f"{ratio_type} Ratio")
    plt.title(f"{ratio_type} Ratio Storico per {ticker}")
    plt.grid()
    plt.show()