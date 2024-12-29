import tkinter as tk
from tkinter import messagebox
import requests
import time

# Replace with your API key from Alpha Vantage
API_KEY = '0BX1ECAQ97N0YMQO'
BASE_URL = 'https://www.alphavantage.co/query'

# Portfolio data
portfolio = {}

# List of common stock symbols
common_symbols = [
    "AAPL - Apple Inc.", 
    "MSFT - Microsoft Corp.", 
    "TSLA - Tesla, Inc.", 
    "GOOGL - Alphabet Inc.", 
    "AMZN - Amazon.com, Inc.", 
    "META - Meta Platforms, Inc.", 
    "NFLX - Netflix, Inc.", 
    "NVDA - NVIDIA Corp.",
    "RELIANCE - Reliance Industries Ltd.",
    "TCS - Tata Consultancy Services Ltd.",
    "HDFCBANK - HDFC Bank Ltd.",
    "INFY - Infosys Ltd.",
    "ICICIBANK - ICICI Bank Ltd.",
    "HINDUNILVR - Hindustan Unilever Ltd.",
    "ITC - ITC Ltd.",
    "SBIN - State Bank of India",
    "BHARTIARTL - Bharti Airtel Ltd.",
    "ADANIENT - Adani Enterprises Ltd.",
    "WIPRO - Wipro Ltd.",
    "KOTAKBANK - Kotak Mahindra Bank Ltd."
]

def get_stock_price(symbol):
    """Fetch the current price of a stock using Alpha Vantage API."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if 'Time Series (1min)' in data:
        latest_time = list(data['Time Series (1min)'].keys())[0]
        price = float(data['Time Series (1min)'][latest_time]['1. open'])
        return price
    else:
        return None

def update_portfolio_display():
    """Update the portfolio display on the right side of the screen."""
    portfolio_display.delete(1.0, tk.END)
    if portfolio:
        for symbol, details in portfolio.items():
            portfolio_display.insert(tk.END, f"{symbol}: {details['quantity']} shares @ ${details['price']:.2f}\n")
    else:
        portfolio_display.insert(tk.END, "Portfolio is empty.")

def add_stock():
    """Add a stock to the portfolio."""
    symbol = entry_symbol.get().upper()
    try:
        quantity = int(entry_quantity.get())
    except ValueError:
        messagebox.showerror("Error", "Quantity must be an integer.")
        return

    if not symbol:
        messagebox.showerror("Error", "Stock symbol cannot be empty.")
        return

    price = get_stock_price(symbol)
    if price is not None:
        if symbol in portfolio:
            portfolio[symbol]['quantity'] += quantity
        else:
            portfolio[symbol] = {'quantity': quantity, 'price': price}
        messagebox.showinfo("Success", f"{symbol} added with quantity {quantity}.")
        entry_symbol.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        update_portfolio_display()
    else:
        messagebox.showerror("Error", f"Failed to fetch data for {symbol}. Check the stock symbol.")

def remove_stock():
    """Remove a stock from the portfolio."""
    symbol = entry_symbol.get().upper()
    if symbol in portfolio:
        del portfolio[symbol]
        messagebox.showinfo("Success", f"{symbol} removed from portfolio.")
        update_portfolio_display()
    else:
        messagebox.showerror("Error", f"{symbol} not found in portfolio.")
    entry_symbol.delete(0, tk.END)

# Create GUI
root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.geometry("800x500")
root.configure(bg="#b7e3f5")

# Left Frame for Stock Symbols
left_frame = tk.Frame(root, width=200, bg="#b7e3f5")
left_frame.pack(side="left", fill="y")

label_common = tk.Label(left_frame, text="Stock Symbols", bg="#b7e3f5", font=("Times New Roman", 12, "bold"))
label_common.pack(pady=10)

for symbol in common_symbols:
    tk.Label(left_frame, text=symbol, bg="#b7e3f5", font=("Times New Roman", 10)).pack(anchor="w", padx=10)

# Main Frame for Inputs and Buttons
main_frame = tk.Frame(root, bg="#d0effb")
main_frame.pack(side="left", fill="both", expand=True)

# Labels and Entries
label_symbol = tk.Label(main_frame, text="Stock Symbol:", bg="#d0effb")
label_symbol.pack(pady=5)
entry_symbol = tk.Entry(main_frame, width=30)
entry_symbol.pack(pady=5)

label_quantity = tk.Label(main_frame, text="Quantity:", bg="#d0effb")
label_quantity.pack(pady=5)
entry_quantity = tk.Entry(main_frame, width=30)
entry_quantity.pack(pady=5)

# Buttons
btn_add = tk.Button(main_frame, text="Add Stock", command=add_stock)
btn_add.pack(pady=10)

btn_remove = tk.Button(main_frame, text="Remove Stock", command=remove_stock)
btn_remove.pack(pady=10)

btn_exit = tk.Button(main_frame, text="Exit", command=root.quit)
btn_exit.pack(pady=10)

# Right Frame for Portfolio Display
right_frame = tk.Frame(root, bg="#d0effb", width=200)
right_frame.pack(side="right", fill="both", expand=True)

label_portfolio = tk.Label(right_frame, text="Portfolio", bg="#d0effb", font=("Times New Roman", 12, "bold"))
label_portfolio.pack(pady=10)

portfolio_display = tk.Text(right_frame, width=30, height=20, bg="#e3f7fc", state="normal")
portfolio_display.pack(padx=10, pady=10)

update_portfolio_display()

# Run the GUI
root.mainloop()
