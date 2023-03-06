from logger import logger
import configs
from telethon import TelegramClient, events
import re
from binance_bot import place_spot_trade, place_future_order, client as bc
from message_patterns import futures_pattern, spot_pattern
from utils import extract_match, emit_collect_success, match_signal
from intro import introduction
# Telegram API keys
api_id = configs.TELEGRAM_APP_ID
api_hash = configs.TELEGRAM_APP_HASH
phone_number = configs.PHONE_NUMBER
channel_name = configs.CHANNEL_NAME
risk = configs.RISK_PERCENTAGE
buy_percentage =  configs.BUY_PERCENTAGE
# Connect to the Telegram channel
client = TelegramClient(phone_number, api_id, api_hash)
client.start()
# ========================
#  INTRODUCTION
introduction()
# ========================


@client.on(events.NewMessage(chats=channel_name))
async def handle_spot_message(event):
    message = event.message.message
    if "Exchange:   BINANCE" in message:
        logger.info("===== Handling Spot Signal Messages =====")
        # Parse the signal from the message
        match = match_signal(spot_pattern, message)
        if match:
            symbol = extract_match(match, [1, 2])
            buy_price = float(extract_match(match, [3]))
            targets = re.findall(r"%(\d+).*?([\d.]+)", message)
            if targets:
                stop_loss = re.search(
                    r"Trailing SL:   ([\d.]+)", message
                ).group(1)
                # Place a Binance buy order
                balance = bc.get_asset_balance(asset=symbol)
                logger.info(f"Current Asset balance: {balance}")
                # run
                if balance is not None:
                    quantity = (
                        float(balance["free"]) * buy_percentage
                    )  # Buy 10% of available balance
                    place_spot_trade(
                        pair=symbol,
                        price=buy_price,
                        side="BUY",
                        quantity=quantity,
                    )
                    # Place take-profit orders
                    for target in targets:
                        target_price = float(target[1])
                        percentage = int(target[0])
                        if target_price > buy_price:
                            side = "SELL"
                            price = buy_price * (1 + percentage / 100)
                        else:
                            side = "BUY"
                            price = buy_price * (1 - percentage / 100)
                        place_spot_trade(
                            pair=symbol,
                            price=price,
                            side=side,
                            quantity=quantity,
                        )
                    # Place stop-loss order
                    place_spot_trade(
                        pair=symbol,
                        price=stop_loss,
                        side="SELL",
                        quantity=quantity,
                    )
            else:
                print("Could not parse signal from message:", message)
        print("Spot: None or Insufficient asset.")


# Define the regex pattern to extract the symbol, leverage, entries, targets, and stop loss


@client.on(events.NewMessage(chats=channel_name))
async def handle_signal_message(event):
    # Define the possible keywords for a signal
    keywords = ["SHORT", "LONG", "🛑", "✳️"]

    # Check if the message contains any of the keywords
    if any(keyword in event.raw_text for keyword in keywords):
        logger.info("===== Handling Futures Signal Messages =====")

        # Extract the symbol, leverage, side, entry price, and stop loss price from the signal
        symbol = None
        leverage = None
        side = None
        entry = None
        stop_loss = None
        signal_message = event.raw_text.split("\n") 
        for line in signal_message:
            if any(keyword in line for keyword in keywords):
                if "SHORT" in line:
                    symbol = line.split()[0].replace("/", "")
                    side = "SELL"
                    entry = float(signal_message[2].split(" ")[1])
                    leverage = float(signal_message[1].split(" ")[1].replace("x", ""))
                elif "LONG" in line:
                    symbol = line.split()[0].replace("/", "")
                    side = "BUY"
                    entry = float(signal_message[2].split(" ")[1])
                    leverage = float(signal_message[1].split(" ")[1].replace("x", ""))
                elif "🛑" in line:
                    symbol = line.split()[0].replace("/", "")
                    side = "SELL"
                    entry = float(signal_message[2].split(" ")[1])
                    leverage = float(signal_message[1].split(" ")[1].replace("x", ""))
                elif "✳️" in line:
                    symbol = line.split()[0].replace("/", "")
                    side = "BUY"
                    entry = float(signal_message[2].split(" ")[1])
                    leverage = float(signal_message[1].split(" ")[1].replace("x", ""))
                    print("✳️", entry)
                if "SL" or "Sl" in line:
                    stop_loss = float(signal_message[-1].split(" ")[1])
        emit_collect_success(symbol, side, entry, leverage, type="Complex Version")
    else:
        logger.info("===== Handling Futures Signal Messages =====")
        signal_message = event.raw_text.split(" ") 
        symbol = None
        leverage = None
        side = None
        entry = None
        for line in signal_message:
            if "short" in line:
                symbol: str = signal_message[0] + "USDT"
                side = "SELL"
                entry = float(signal_message[2])
                leverage = float(20)
            elif "long" in line:
                symbol: str = signal_message[0] + "USDT"
                side = "BUY"
                entry = float(signal_message[2])
                leverage = float(20)

        emit_collect_success(symbol, side, entry, leverage, type="Minimal Version")

        # Place the limit order with the extracted information
    order = None
    print("Passed Colection, creating order now ...")
    if symbol is not None and side is not None and entry is not None:
        try:
            order = place_future_order(symbol, side, entry, leverage=leverage)
            logger.info(f"Placed limit {side.lower()} futures order")
        except Exception as err:
            logger.warning(f"Error placing order: {str(err)}")
            return
    # Define the take profit and stop loss prices
    if order is not None:
        take_profit_price = entry * (1 + risk) if side == "BUY" else entry * (1 - risk)
        stop_loss_price = stop_loss if stop_loss is not None else entry * (1 - risk) if side == "BUY" else entry * (1 - risk)

        # Set up the loop to check the order status and update the take profit and stop loss orders
        while True:
            # Get the current order status
            if order is not None:
                order_status = bc.get_order(symbol=symbol, orderId=order["orderId"])

                # If the order has been filled or canceled, break the loop
                if order_status["status"] == "FILLED" or order_status["status"] == "CANCELED":
                    break

                # Update the take profit and stop loss orders if necessary
                if order_status["status"] == "NEW":
                    place_future_order(symbol, side, stop_loss_price, leverage=leverage)
                    place_future_order(symbol, side, take_profit_price, leverage=leverage)
                    logger.info(f"Placed limit futures {side.lower()} order with {stop_loss_price} stop loss and {take_profit_price} take profit for {symbol}")

            logger.info("No available futures order(s)")
            break

# Start the event loop
with client:
    client.run_until_disconnected()

