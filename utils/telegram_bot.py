import requests
from utils.token import BOT_CHATID, BOT_TOKEN

def send_message(bot_message: str):
    send_text = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={BOT_CHATID}&parse_mode=Markdown&text={bot_message}'

    response = requests.get(send_text)
    return response.json()
