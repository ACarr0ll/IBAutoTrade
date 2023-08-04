from flask import Flask, request, render_template
import json
import asyncio
import nest_asyncio
import yfinance as yf
from ib_insync import *
import pandas as pd


nest_asyncio.apply()

ib = IB()

async def get_stock_info_async(ticker):
    try:
        stock_data = yf.Ticker(ticker)   
        stock_info = stock_data.info
        return stock_info
    except Exception as e:
        print(f"Error occurred: {e}")
        return None  

def get_stock_info(ticker):
    return asyncio.get_event_loop().run_until_complete(get_stock_info_async(ticker))

app = Flask(__name__)

@app.route("/")
def index():   
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/search", methods=['GET', 'POST'])
def searchSymbol():
    stock_info = None
    ticker = request.form.get('query')
    stock_info = get_stock_info(ticker)
    return render_template('chart.html', stock_info=stock_info)


app.run(host="0.0.0.0", port=80)
    