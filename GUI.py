import matplotlib.pyplot as plt

def mostra_ratios(ticker, ratio_type):
    years = list(range(2000, 2024))
    if ratio_type == 'PE':
        ratios = [15 + i * 0.5 for i in range(len(years))]
    elif ratio_type == 'PB':
        ratios = [1.5 + i * 0.05 for i in range(len(years))]
    else:
        print("Tipo di ratio non valido")
        return
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, ratios, marker='o', linestyle='-', color='purple')
    plt.xlabel("Anno")
    plt.ylabel(f"{ratio_type} Ratio")
    plt.title(f"{ratio_type} Ratio Storico per {ticker}")
    plt.grid()
    plt.show()
