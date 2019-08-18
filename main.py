from dotenv import load_dotenv
import os

from bot import bot

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    if token is None:
        print("Environment variable \"TOKEN\" not set")
        exit(0)
    bot.run(token)
