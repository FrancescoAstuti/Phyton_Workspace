import requests
import matplotlib.pyplot as plt

API_KEY = '11CAQCZUVYCUIZ3V'

def get_ttm_ratio(ticker, ratio_type):
    """
    Ottiene il valore TTM del ratio (PE o PB) da Alpha Vantage.

    Args:
    ticker (str): Il simbolo del ticker.
    ratio_type (str): Il tipo di ratio ('PE' o 'PB').

    Returns:
    float: Il valore TTM del ratio.
    """
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Debug: stampare i dati grezzi ricevuti
    print("Dati grezzi ricevuti dall'API:", data)
    
    if ratio_type == 'PE':
        return float(data.get('TrailingPE', 0))
    elif ratio_type == 'PB':
        return float(data.get('PriceToBookRatio', 0))
    else:
        raise ValueError("Tipo di ratio non valido")

def mostra_ratios(ticker, ratio_type):
    """
    Mostra una serie storica di PE o PB ratios per un dato ticker utilizzando il valore TTM.

    Args:
    ticker (str): Il simbolo del ticker per cui mostrare i ratios.
    ratio_type (str): Il tipo di ratio da mostrare ('PE' o 'PB').

    Returns:
    None
    """
    years = list(range(2000, 2024))
    ttm_ratio = get_ttm_ratio(ticker, ratio_type)
    ratios = [ttm_ratio] * len(years)

    # Debug: stampare i dati dei ratios
    print(f"Dati {ratio_type} ratios TTM per {ticker}:", ratios)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, ratios, marker='o', linestyle='-', color='purple')
    plt.xlabel("Anno")
    plt.ylabel(f"{ratio_type} Ratio")
    plt.title(f"{ratio_type} Ratio Storico per {ticker}")
    plt.grid()
    plt.show()
