import re

import configs
from binance.client import Client
from logger import logger
from message_patterns import scientific_pattern
# Binance API keys
api_key = configs.BINANCE_API_KEY
api_secret = configs.BINANCE_API_SECRET
risk_percent = configs.RISK_PERCENTAGE
client = Client(api_key, api_secret)

# Function to place a Spot trade
def place_spot_trade(pair, price, side, quantity):
    try:
        order = client.create_order(
            symbol=pair,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )
        logger.info(f"Placed {side} order for {pair} at price {price}")
    except Exception as e:
        logger.info(f"Error placing {side} order for {pair}: {str(e)}")

    return order
# function to place a futures trade
def place_future_order(symbol, side, price, leverage):
    # Calculate the quantity to trade based on the account balance and the percentage risk
    balances = client.get_account()["balances"]
    balance = sum([float(balance['free']) for balance in balances])
    price = float(round(price, 8))
    if balance > 0:
        unsafe_quantity = (balance * risk_percent) / price
        quantity = float(round(unsafe_quantity, 8))
        if re.match(scientific_pattern, str(quantity)):
            quantity = "{:.8f}".format(quantity)
            price = round(price, 8)
        # Place the order
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=price,
            leverage=leverage
        )
        client.futures_change_leverage()
        print(
            f"Placed {side} order for {symbol} at {price}."
        )

        return order

