import requests
import json
from datetime import datetime, timedelta
import schedule
import time

url = "https://api-mainnet.magiceden.dev/v2/collections/frootsnft/stats"
telegram_base_url = "https://api.telegram.org/bot5537571435:AAFKu1oQTN7mz4vvvf0XZ-7hgbCMxH3ezXM/sendMessage?chat_id=-646227103&text={}"
latest_price = 0


def process():
    global latest_price
    res = requests.get(url)
    data = json.loads(res.text)
    if latest_price == data["floorPrice"]:
        return
    latest_price = data["floorPrice"]
    requests.get(
        telegram_base_url.format(str(data["floorPrice"] / 1000000000) + " SOL")
    )


schedule.every(0.1).minutes.do(process)

while True:
    schedule.run_pending()
    time.sleep(1)
