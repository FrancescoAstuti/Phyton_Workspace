import requests  # Import requests for making HTTP requests
from tkinter import messagebox  # Import the messagebox from tkinter for displaying error messages

API_KEY = 'eb7366217370656d66a56a057b8511b0'  # Updated to FMP API Key

def recupera_prezzo_corrente(nome):
    """
    Recupera il prezzo corrente utilizzando Financial Modeling Prep API.

    Args:
    nome (str): Il simbolo del ticker per cui recuperare il prezzo.

    Returns:
    float: Il prezzo corrente del ticker.
    """
    try:
        url = f'https://financialmodelingprep.com/api/v3/quote/{nome}?apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if data:
            prezzo_corrente = data[0]['price']  # Extract the current price from the response
            return prezzo_corrente  # Return the current price
        else:
            raise ValueError(f"No data found for the given ticker: {nome}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Errore", f"Errore di rete: {e}")
        return None
    except ValueError as e:
        messagebox.showerror("Errore", str(e))
        return None
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile recuperare il prezzo per {nome}. Errore: {e}")
        return None

# Test the function
if __name__ == "__main__":
    nome_ticker = "ENEL.MI"  # Example ticker symbol for testing
    prezzo = recupera_prezzo_corrente(nome_ticker)  # Retrieve the current price for the example ticker
    if prezzo:  # Check if the price is successfully retrieved
        print(f"Il prezzo corrente di {nome_ticker} è {prezzo}")  # Print the current price
    else:
        print(f"Impossibile recuperare il prezzo corrente di {nome_ticker}.")  # Print error message if unable to retrieve the price
