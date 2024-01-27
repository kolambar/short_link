import logging
import os

import dotenv


dotenv.load_dotenv()

symbols = os.getenv("SYMBOLS")
domain = os.getenv("DOMAIN")
logging.basicConfig(filename='info', level=logging.INFO, encoding="utf-8")

if __name__ == "__main__":
    print(symbols)
    print(domain)
