import requests
from tkinter import messagebox
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='get_price.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

API_KEY = 'eb7366217370656d66a56a057b8511b0'

def recupera_prezzo_corrente(ticker):
    """
    Recupera il prezzo corrente utilizzando Financial Modeling Prep API.

    Args:
    ticker (str): Il simbolo del ticker per cui recuperare il prezzo.

    Returns:
    float: Il prezzo corrente del ticker.
    """
    try:
        url = f'https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={API_KEY}'
        response = requests.get(url)
        logging.debug(f"API URL: {url}")
        logging.debug(f"API Response Status Code: {response.status_code}")
        logging.debug(f"API Response Text: {response.text}")
        
        data = response.json()
        if response.status_code == 200 and data:
            prezzo_corrente = data[0].get('price')
            if prezzo_corrente is not None:
                return prezzo_corrente
            else:
                raise ValueError(f"No price data found for the given ticker: {ticker}")
        else:
            raise ValueError(f"No valid data found for the given ticker: {ticker}. Full response: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Errore", f"Errore di rete: {e}")
        logging.error(f"Network error: {e}")
        return None
    except ValueError as e:
        messagebox.showerror("Errore", str(e))
        logging.error(f"Value error: {e}")
        return None
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile recuperare il prezzo per {ticker}. Errore: {e}")
        logging.error(f"General error: {e}")
        return None

# Test the function
if __name__ == "__main__":
    ticker = "ENEL.MI"  # Example ticker symbol for testing
    prezzo = recupera_prezzo_corrente(ticker)  # Retrieve the current price for the example ticker
    if prezzo:
        print(f"Il prezzo corrente di {ticker} è {prezzo}")
    else:
        print(f"Impossibile recuperare il prezzo corrente di {ticker}.")