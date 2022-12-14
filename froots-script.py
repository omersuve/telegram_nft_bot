import requests
import json
from datetime import datetime, timedelta
import schedule
import time
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import threading
import sys
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://api-mainnet.magiceden.dev/v2/collections/frootsnft/stats"
url_changed = "https://api-mainnet.magiceden.dev/v2/collections/"
telegram_base_url = (
    "https://api.telegram.org/bot"
    + os.getenv("TELEGRAM_KEY")
    + "/sendMessage?chat_id="
    + os.getenv("CHAT_ID")
    + "&text={}"
)
latest_price = 0
stop = True
wrong_project_given = False


def handle_change(update, context):
    global latest_price
    global wrong_project_given
    global stop
    command_name = str(update.message.text).lower()
    try:
        project_name = command_name.split()[1]
    except:
        update.message.reply_text("You need to type a project name!")
        latest_price = 0
        wrong_project_given = True
        stop = True
        return
    print("project_name:", project_name)
    url = url_changed[:]
    url += project_name + "/stats"
    print("url:", url)
    print("wrong_project_given", wrong_project_given)

    def thread1(update, context):
        global latest_price
        global stop
        global wrong_project_given
        if not stop:
            update.message.reply_text(
                "You have to stop before changing the project! (type: /stop)"
            )
            return
        stop = False
        while True:
            if stop and not wrong_project_given:
                print("while looptan çıktı")
                sys.exit()
                return
            res = requests.get(url, verify=False)
            if res is None:
                print("none döndü")
                sys.exit()
                return
            data = json.loads(res.text)
            if stop and not wrong_project_given:
                print("while looptan çıktı")
                sys.exit()
                return
            try:
                if latest_price == data["floorPrice"]:
                    wrong_project_given = False
                    time.sleep(3)
                    continue
                latest_price = data["floorPrice"]
                requests.get(
                    telegram_base_url.format(
                        str(data["floorPrice"] / 1000000000) + " SOL"
                    )
                )
                print("başarılı bir şekilde değiştirdi")
                wrong_project_given = False
            except:
                update.message.reply_text("There is no such a project! Try again.")
                wrong_project_given = True
                latest_price = 0
                stop = True
                print("bulamadı")
                sys.exit()
                return

    t1 = threading.Thread(target=thread1, args=(update, context))
    t1.start()


def handle_stop(update, context):
    global stop
    global latest_price
    stop = True
    latest_price = 0
    print("stop:", stop)


def error(update, context):
    print(f"Update {update} caused error: {context.error}")


updater = Updater(os.getenv("TELEGRAM_KEY"))
dp = updater.dispatcher
dp.add_handler(CommandHandler("project_change", handle_change))
dp.add_handler(CommandHandler("stop", handle_stop))
dp.add_error_handler(error)
updater.start_polling()
updater.idle()
