from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    print(token)
