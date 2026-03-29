# Updated main.py

import yfinance as yf
import time


def load_data():
    print("Loading data from yfinance...")
    # Your logic to load data using yfinance


def start_command():
    print("/start command received. Preparing to execute...")
    load_data()
    print("Data loaded successfully!")


if __name__ == "__main__":
    start_command()