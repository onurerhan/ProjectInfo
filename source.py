from selenium import webdriver
import time
import telegram
import configparser


counter = 0
config = configparser.ConfigParser()
config.read('/home/notroot/PycharmProjects/ProjectInfo/config')
bot = telegram.Bot(token=config['DEFAULT']['telegram_api_key'])
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
difference_limit = float(config['DEFAULT']['difference_limit'])
sleep_time = int(config['DEFAULT']['sleep_time'])


def close_browser():
    lykke.close()
    paribu.close()
    xe.close()


while True:
    lykke = webdriver.Firefox(firefox_options=options)
    lykke.get("https://www.lykke.com/")
    paribu = webdriver.Firefox(firefox_options=options)
    paribu.get("https://www.paribu.com/")
    xe = webdriver.Firefox(firefox_options=options)
    xe.get("http://www.xe.com/currencyconverter/convert/?From=USD&To=TRY")

    xe_usd = float(xe.find_element_by_class_name("uccResultAmount").text)
    lykke_tl = xe_usd * float(lykke.find_element_by_class_name("pair__value").text)
    paribu_header = paribu.title
    paribu_tl = float(''.join(filter(lambda x: x.isdigit(), paribu_header)))

    difference_prb_to_ly = paribu_tl/lykke_tl
    if difference_prb_to_ly > difference_limit:
        difference_limit = difference_prb_to_ly
        bot.send_message(chat_id=config['DEFAULT']['chat_id'],
                         text="paribu:     {0}\nlykke:    {1}\nfark:      {2}\nyüzde:   {3}"
                         .format(str(paribu_tl), str(lykke_tl), str(paribu_tl - lykke_tl), str((difference_limit - 1) * 100)))

    else:
        counter += 1

    if counter > 10:
        counter = 0
        difference_limit = int(config['DEFAULT']['difference_limit'])

    close_browser()
    time.sleep(sleep_time)
