import requests

BOT_TOKEN = '7130840623:AAGQ-IXQ5qI3SK3BfiVVi7MdEztrOA_N4-Q'
BOT_CHATID = '1286703400'


def send_message(bot_message: str):
    send_text = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={BOT_CHATID}&parse_mode=Markdown&text={bot_message}'

    response = requests.get(send_text)
    return response.json()
