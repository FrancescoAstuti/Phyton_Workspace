from googlefinance import getQuotes  # Import the getQuotes function from googlefinance
from tkinter import messagebox  # Import the messagebox from tkinter for displaying error messages

def recupera_prezzo_corrente(nome):
    """
    Recupera il prezzo corrente utilizzando Google Finance.

    Args:
    nome (str): Il simbolo del ticker per cui recuperare il prezzo.

    Returns:
    float: Il prezzo corrente del ticker.
    """
    try:
        quote = getQuotes(nome)[0]  # Get the quote for the ticker
        prezzo_corrente = float(quote['LastTradePrice'])  # Extract the current price from the quote
        return prezzo_corrente  # Return the current price
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile recuperare il prezzo per {nome}. Errore: {e}")  # Display error message if there's an error
        return None  # Return None if there's an error

# Test the function
if __name__ == "__main__":
    nome_ticker = "AAPL"  # Example ticker symbol for testing
    prezzo = recupera_prezzo_corrente(nome_ticker)  # Retrieve the current price for the example ticker
    if prezzo:  # Check if the price is successfully retrieved
        print(f"Il prezzo corrente di {nome_ticker} è {prezzo}")  # Print the current price
    else:
        print(f"Impossibile recuperare il prezzo corrente di {nome_ticker}.")  # Print error message if unable to retrieve the price