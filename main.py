import requests as rq
from flask import Flask, render_template, redirect, url_for, request
from babel.numbers import get_currency_symbol
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')

ep = "https://api.coingecko.com/api/v3/coins/markets"
def get_info(coin, currency):
    headers = {
        "x-cg-demo-api-key": os.getenv('API_KEY'),
    }
    params = {
        "ids": coin,
        "vs_currency": currency,
    }
    response = rq.get(ep, headers=headers, params=params)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def home():
    price = None
    error = None
    more_info = None
    img_url = None
    if request.method == "POST":
        form = request.form
        coin = form['coin']
        currency = form['currency'].lower()
        action = form['action']
        try:
            response = get_info(coin, currency)
            data = response[0]
            img_url = data['image']
            try:
                symbol = get_currency_symbol(currency.upper(), locale="en_US")
            except:
                symbol = ""
            if action == "price":
                price_data = data["current_price"]
                price = f"{symbol}{price_data:,}"
            elif action == "more":
                more_info = {
                    "high_24h": f"{symbol}{data.get('high_24h', 0):,.2f}",
                    "low_24h": f"{symbol}{data.get('low_24h', 0):,.2f}",
                    "price_change_24h": f"{symbol}{data.get('price_change_24h', 0):,.2f}",
                    "price_change_percentage_24h": f"{data.get('price_change_percentage_24h', 0):,.2f}"
                }
        except Exception as e:
            error = f"Could not retrieve data. Check your inputs. ({e})"
    return render_template('index.html', price=price, error=error, more_info=more_info, image=img_url)

if __name__ == "__main__":
    app.run(debug=True)
