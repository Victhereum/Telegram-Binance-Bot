# Binance Telegram BOT
## How To Run

Create a virtual enviroment using virtualenv and activate it

```sh
    $ virtualenv venv
    $ source venv/bin/activate
```
## Install dependencies

```sh
    $ pip install -r requirements.txt
```



 Create a .env file within the root folder and then copy the content of the .env-example to that file

Explanation:
```sh
    BINANCE_API_KEY= Your binance api key, which can be gotten from binance official website
    BINANCE_API_SECRET_KEY= Your binance secret
    TELEGRAM_APP_ID= Your telegram APP_ID get it here https://my.telegram.org/apps
    TELEGRAM_APP_HASH= Your telegram app hash, get it from the same web address above
    PHONE_NUMBER= The phone number which is subscribed to the channel
    CHANNEL_NAME= The channel name e.g "alwayswintrade"
    RISK_PERCENTAGE= The percentage to take profit or stop loss 3% by default. Any integer between 1 - 100
    BUY_PERCENTAGE=The percentage to be deducted from your account in order to place the trade, 10% by default
```

Finally run the start the telegram session by running the code below in your terminal

### Note:
    A code will be sent to you on telegram, copy the code and paste in the terminal in order 
    for telegram to verify it's you

```sh
    $ python telegram.py
```

