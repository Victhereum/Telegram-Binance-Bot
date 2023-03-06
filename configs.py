from environs import Env

# environs setup
env = Env()
env.read_env()

# read binance api keys
BINANCE_API_KEY: str = env("BINANCE_API_KEY")
BINANCE_API_SECRET: str = env("BINANCE_API_SECRET_KEY")

# read telegram api keys
TELEGRAM_APP_ID: int = env.int("TELEGRAM_APP_ID")
TELEGRAM_APP_HASH: str = env("TELEGRAM_APP_HASH")
PHONE_NUMBER: str = env("PHONE_NUMBER")

# BOT constants
_RISK_PERCENTAGE: int = env.int("RISK_PERCENTAGE", 3)
_BUY_PERCENTAGE: int = env.int("_BUY_PERCENTAGE", 10)

RISK_PERCENTAGE: float = _RISK_PERCENTAGE / 100
BUY_PERCENTAGE: float = _BUY_PERCENTAGE / 100

CHANNEL_NAME: str = env("CHANNEL_NAME")
