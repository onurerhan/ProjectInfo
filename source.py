from selenium import webdriver
import time
import telegram
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
bot = telegram.Bot(token=config['DEFAULT']['telegram_api_key'])
options = webdriver.ChromeOptions()
options.add_argument('headless')
path = config['DEFAULT']['browser_path']

lykke = webdriver.Chrome(executable_path=path, chrome_options=options)
lykke.get("https://www.lykke.com/")
paribu = webdriver.Chrome(executable_path=path, chrome_options=options)
paribu.get("https://www.paribu.com/")
xe = webdriver.Chrome(executable_path=path, chrome_options=options)
xe.get("http://www.xe.com/currencyconverter/convert/?From=USD&To=TRY")


def close_browser():
    lykke.close()
    paribu.close()
    xe.close()


lykke_usd = float(lykke.find_element_by_class_name("pair__value").text)
paribu_header = paribu.title
paribu_tl = float(''.join(filter(lambda x: x.isdigit(), paribu_header)))
xe_usd = float(xe.find_element_by_class_name("uccResultAmount").text)
difference = (lykke_usd * xe_usd) - paribu_tl
print("lykke        " + str(lykke_usd * xe_usd))
print("paribu       " + str(paribu_tl))
print("difference   " + str(difference))
if difference > paribu_tl * 0.0005:
    bot.send_message(chat_id=config['DEFAULT']['chat_id'], text="lan al hemen")

close_browser()
