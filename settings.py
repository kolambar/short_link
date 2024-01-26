import os
import dotenv


dotenv.load_dotenv()

symbols = os.getenv("SYMBOLS")
domain = os.getenv("DOMAIN")

if __name__ == "__main__":
    print(symbols)
    print(domain)
