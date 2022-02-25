import os
import random
import sys
from datetime import datetime

import requests
import eel
import win32api
from pypresence import Presence
from selenium.common.exceptions import TimeoutException
from tinydb import TinyDB, Query
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telebot
import requests
import re
import time
from pandas.io import clipboard
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import webbrowser
import emoji
import plyer.platforms.win.notification
from plyer import notification


db = TinyDB('settings.json')
cfg = Query()
lic = False
stop = False

version = "2.2.0-DEV"
key = bytes("fTjWnZr4t7w!z%C*", 'utf-8')
channel_id = "839951254276014145"
RPC = Presence("891402276386799616")

user_id = ""
accepted_roles = 0
asked_roles = 0
accept_reaction = "✅"
stats_reaction = "🇸"

global_driver = None
session = requests.session()
backend = default_backend()

fractions = {
    "FBI": ["FBI", "ФБР"],
    "LSPD": ["LSPD", "ЛСПД"],
    "SFPD": ["SFPD", "СФПД"],
    "RCSD": ["RCSD", "РКПД", "RCPD", "РКШД"],
    "LVPD": ["LVPD", "ЛВПД", "SWAT", "СВАТ"],
    "Правительство LS": ["GOV", "Прав-во", "Правительство"],
    "Инструкторы": ["ГЦЛ", "АШ"],
    "Страховая компания": ["IC", "СК"],
    "Центральный Банк": ["ЦБ", "CB"],
    "Больница LS": ["LSMC", "ЛСМЦ"],
    "Больница SF": ["SFMC", "СФМЦ"],
    "Больница LV": ["LVMC", "ЛВМЦ"],
    "TV студия": ["CNN LS", "СМИ ЛС"],
    "TV студия SF": ["CNN SF", "СМИ СФ"],
    "TV студия LV": ["CNN LV", "СМИ ЛВ"],
    "Армия ЛС": ["LSA", "ЛСА"],
    "Армия СФ": ["SFA", "СФА"],
    "Тюрьма строгого режима LV": ["MSP", "ТСР", "ТЮРЬМА"],
    "Warlock MC": ["WMC", "W-MC"],
    "Russian Mafia": ["RM", "РМ"],
    "La Cosa Nostra": ["LCN", "ЛКН"],
    "Yakuza": ["YAKUZA", "ЯКУДЗА"],
    "Grove Street": ["GROVE", "ГРУВ"],
    "East Side Ballas": ["BALLAS", "БАЛЛАС"],
    "Los Santos Vagos": ["VAGOS", "ВАГОС"],
    "Night Wolves": ["NW", "НВ"],
    "The Rifa": ["RIFA", "РИФА"],
    "Varrios Los Aztecas": ["AZTEC", "АЦТЕК"],
}
fractions_numbered = {
    "3": ["FBI", "ФБР"],
    "1": ["LSPD", "ЛСПД"],
    "4": ["SFPD", "СФПД"],
    "2": ["RCSD", "РКПД", "RCPD", "РКШД"],
    "23": ["LVPD", "ЛВПД", "SWAT", "СВАТ"],
    "6": ["GOV", "Прав-во", "Правительство"],
    "9": ["ГЦЛ", "АШ"],
    "29": ["IC", "СК"],
    "21": ["ЦБ", "CB"],
    "5": ["LSMC", "ЛСМЦ"],
    "8": ["SFMC", "СФМЦ"],
    "22": ["LVMC", "ЛВМЦ"],
    "10": ["CNN LS", "СМИ ЛС"],
    "26": ["CNN SF", "СМИ СФ"],
    "24": ["CNN LV", "СМИ ЛВ"],
    "20": ["LSA", "ЛСА"],
    "27": ["SFA", "СФА"],
    "7": ["MSP", "ТСР", "ТЮРЬМА"],
    "19": ["WMC", "W-MC"],
    "16": ["RM", "РМ"],
    "18": ["LCN", "ЛКН"],
    "17": ["YAKUZA", "ЯКУДЗА"],
    "11": ["GROVE", "ГРУВ"],
    "13": ["BALLAS", "БАЛЛАС"],
    "12": ["VAGOS", "ВАГОС"],
    "25": ["NW", "НВ"],
    "15": ["RIFA", "РИФА"],
    "14": ["AZTEC", "АЦТЕК"],
}


def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F1F2-\U0001F1F4"  # Macau flag
                               u"\U0001F1E6-\U0001F1FF"  # flags
                               u"\U0001F600-\U0001F64F"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U0001F1F2"
                               u"\U0001F1F4"
                               u"\U0001F620"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'', clean_text)

    return text


def aes_ecb_encrypt(message):
    global key
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(cipher.algorithm.block_size).padder()
    padded = padder.update(message.encode()) + padder.finalize()
    return b64e(encryptor.update(padded) + encryptor.finalize())


def aes_ecb_decrypt(ciphertext):
    global key
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
    padded = decryptor.update(b64d(ciphertext)) + decryptor.finalize()
    return unpadder.update(padded) + unpadder.finalize()


def get_version():
    global version

    r = requests.get("https://raw.githubusercontent.com/AbcChannelMC/sptool/main/update.json").json()
    print(r, version)

    files = os.listdir()
    if "chromedriver.exe" in files:
        pass
    else:
        notification.notify("Отсутствует драйвер Chrome", "Подождите, идёт загрузка..")
        open("chromedriver.exe", 'wb').write(requests.get(r['chromedriver']).content)

    if version == r["version"] or "DEV" in version:
        pass
    else:
        notification.notify("Новая версия бота " + r["version"], "Идёт загрузка новой версии, это может занять минуту времени..")
        print("found new version, trying to get update..")
        file = requests.get(aes_ecb_decrypt(r["link"]).decode("utf-8"))
        name = 'sptool-' + r["version"] + '.exe'
        open(name, 'wb').write(file.content)
        print("update finished")
        eel.got_update(name)


def copy_to_clip(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)


def get_cfg(val):
    for item in db:
        return item[val]


def check_prikol():
    r = requests.get("https://api.vprikol.tech/online/16/3")
    if r.status_code == 500:
        return False
    return True


@eel.expose
def get_build_version():
    global version
    return str(version)


@eel.expose
def get_id():
    return aes_ecb_encrypt(str(win32api.GetVolumeInformation("C:\\")[1])).decode("utf-8")


def start():
    global RPC
    RPC.connect()
    RPC.update(state="Trying to catch another role", details="Catching roles",
               start=int(datetime.now().timestamp()), large_image="logo")


@eel.expose
def change_rpc(text):
    global RPC
    RPC.update(state="Trying to catch another role", details=text,
               start=int(datetime.now().timestamp()), large_image="logo")


def get_user():
    return session.get("https://discordapp.com/api/v6/users/@me").json()


def make_reaction(_channel, _message, _reaction):
    reaction_url = "https://discord.com/api/v9/channels/{}/messages/{}/reactions/{}/@me".format(_channel, _message, _reaction)
    session.put(reaction_url)


def check_reaction(_channel, _message, _reaction):
    reaction_url = "https://discord.com/api/v9/channels/{}/messages/{}/reactions/{}?limit=3".format(_channel, _message, _reaction)
    return session.get(reaction_url).json()


def get_guild_user(_guild, _member):
    r = session.get(f"https://discord.com/api/v9/guilds/{_guild}/members/{_member}")
    return r.json()


def patch_roles(_guild, _member, _roles):
    r = session.patch(f"https://discord.com/api/v9/guilds/{_guild}/members/{_member}", json={"roles": _roles})
    return r.json()


def get_messages():
    return session.get("https://discord.com/api/v9/channels/839951254276014145/messages?limit=1").json()


def validate_nickname(user):
    url = "http://api.vprikol.tech/online/16/"
    nick = user
    match = re.compile(" ?\[.{1,10}\] ?").findall(nick)
    if len(match) < 2 and get_cfg("only_form"):
        print("Ник не по форме")
        return "false"
    fraction = str(match[0]).replace("[", "").replace("]", "").replace(" ", "").lower()

    for tag in match:
        nick = nick.replace(tag, "")

    if "_" not in user:
        nick = nick.replace(" ", "_")
    found = "false"

    number = ""
    for k in fractions_numbered:
        for i in range(len(fractions_numbered[k])):
            if fraction == fractions_numbered[k][i].replace(" ", "").lower() and number == "":
                number = k

    resp = requests.get(url + str(number)).json()
    for member in resp["members"]:
        if str(member[0]).lower() == nick.lower():
                found = str(resp["title"]).replace(" ", "") + "|" + member[0] + "|" + member[1]

        if not found == "false":
            break
    print(found)
    return found


def validate_nickname_v2(user):
    url = "http://vprikol.xyz/mon/{}/".format(get_cfg("server"))
    nick = user
    match = re.compile(" ?\[.{1,10}\] ?").findall(nick)
    fraction = str(match[0]).replace("[", "").replace("]", "").replace(" ", "").lower()

    if "прокурор" in fraction:
        return None

    for tag in match:
        nick = nick.replace(tag, "")
    nick = give_emoji_free_text(nick).replace("!", "").replace("*", "").replace("@", "").replace("#", "")

    if "_" not in user:
        nick = nick.replace(" ", "_")
    found = "false"

    tags = []
    all_tags = ["|", "/", "\\"]
    for _tag in all_tags:
        if _tag in fraction:
            tags = fraction.split(_tag)

    number = ""
    if len(tags) > 0:
        for t in tags:
            for k in fractions_numbered:
                for i in range(len(fractions_numbered[k])):
                    if t == fractions_numbered[k][i].replace(" ", "").lower() and number == "":
                        number = k
    else:
        for k in fractions_numbered:
            for i in range(len(fractions_numbered[k])):
                if fraction == fractions_numbered[k][i].replace(" ", "").lower() and number == "":
                    number = k

    if number == "":
        return None
    resp = requests.get(url + str(number)).json()
    for member in resp["members"]:
        if str(member[0]).lower() == nick.lower():
                found = str(resp["title"]).replace(" ", "") + "|" + member[0] + "|" + member[1]

        if not found == 'false':
            break

    return found


def catch_role(driver):
    global stop, user_id, session, channel_id, asked_roles, accepted_roles

    bot = telebot.TeleBot(get_cfg("telegram_token"), parse_mode=None)
    tid = get_cfg("telegram_id")

    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[text()="Discord » Запрос о выдаче роли организации."]')))

    msg = get_messages()[0]
    message_id = msg["id"]
    nickname = msg["embeds"][0]["fields"][1]["value"]

    div = message.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
        '..').find_element_by_xpath('..')

    print(nickname)
    delay = random.randint(int(get_cfg("min_delay")), int(get_cfg("max_delay")))
    if_found = str(msg["embeds"][0]["fields"][3]["value"])

    if "Rank" in if_found:
        if ("[9]" in nickname.lower() or "[ix]" in nickname.lower() or "[9/10]" in nickname.lower() or "[10/10]" in nickname.lower() or "[10]" in nickname.lower() or "[x]" in nickname.lower() or "[l]" in nickname.lower()) and not get_cfg("allow_leader"):
            print("У чела 9-ый/10-ый ранг")
        else:
            bot.send_message(tid, "Одобрение роли  игроку {}, фракция {}".format(nickname, "AUTOMATED"))
            stats = WebDriverWait(div, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@alt="🇸"]')))
            if delay >= 1:
                eel.sleep(delay)
            print("Одобрение роли автоматически")
            #accept = div.find_element_by_xpath('//*[@alt="✅"]')
            #accept.click()
            reacted = False
            while not reacted:
                make_reaction(channel_id, message_id, accept_reaction)
                msg = get_messages()[0]
                if "одобрил запрос от" in msg['content']:
                    reacted = True
                    if user_id in msg['content']:
                        accepted_roles += 1
                        eel.set_accepted(accepted_roles)
                if reacted:
                    break

        return

    result = validate_nickname_v2(nickname)
    if "false" in result:
        if get_cfg("ask_stats"):
            bot.send_message(tid, "Запрос статистики у игрока {}".format(nickname))
            print("Запрос статистики у игрока")
            stats = WebDriverWait(div, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@alt="🇸"]')))
            if delay >= 1:
                eel.sleep(delay)
            #stats.click()
            reacted = False
            while not reacted:
                make_reaction(channel_id, message_id, stats_reaction)
                msg = get_messages()[0]
                if "запросил статистику" in msg['content']:
                    reacted = True
                    if user_id in msg['content']:
                        asked_roles += 1
                        eel.set_asked(asked_roles)
                if reacted:
                    break
    else:
        if ("[9]" in nickname.lower() or "[ix]" in nickname.lower() or "[9/10]" in nickname.lower()) and not get_cfg(
                "allow_leader"):
            print("У чела 9-ый ранг")
        else:
            split_result = result.split("|")

            bot.send_message(tid, "Одобрение роли  игроку {}, фракция {}".format(nickname, split_result[0]))
            stats = WebDriverWait(div, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@alt="🇸"]')))
            if delay >= 1:
                eel.sleep(delay)
            print("Фракция найдена в мониторинге")

            if get_cfg("anti_flood"):
                print("Выдача роли в обход баллов")
                member_id = str(msg["embeds"][0]["fields"][0]["value"]).replace("@", "").replace("<", "").replace(">", "")
                role_id = str(msg["embeds"][0]["fields"][2]["value"]).replace("@", "").replace("<", "").replace(">", "").replace("&", "")
                member = get_guild_user(get_cfg("server"), member_id)
                roles = member["roles"]
                roles.append(role_id)
                patch_roles(get_cfg("server"), member_id, roles)
                eel.sleep(1)
                patch_roles(get_cfg("server"), member_id, roles)
                eel.sleep(2)

            reacted = False
            while not reacted:
                make_reaction(channel_id, message_id, accept_reaction)
                msg = get_messages()[0]
                if "одобрил запрос от" in msg['content'] or "запросил статистику" in msg["content"]:
                    reacted = True
                    if user_id in msg['content']:
                        print("Успешно словлена роль")
                        accepted_roles += 1
                        eel.set_accepted(accepted_roles)
                    else:
                        print("Роль словил кто-то другой")
                if reacted:
                    break
                eel.sleep(0.2)


def working_thread():
    global stop, user_id, session

    headers = {
        "authorization": get_cfg("discord_token")
    }
    session.headers.update(headers)

    user = get_user()
    try:
        if user['message'] == "401: Unauthorized":
            eel.showNotification('top', 'center', 'danger', 'Указанный <b>токен</b> неверный')
        else:
            eel.showNotification('top', 'center', 'danger', 'Произошла <b>ошибка</b> в авторизации')
        return
    except:
        pass
    user_id = user['id']
    eel.showNotification('top','center', 'success', 'Успешный вход под <b>' + user["username"] + '</b>')


    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--mute-audio")
    options.add_argument('--no-sandbox')
    options.headless = get_cfg("hide_browser")

    driver = webdriver.Chrome(options=options)
    driver.get("https://discord.com/channels/839951251449839686/839951254276014145")
    eel.sleep(3)
    driver.execute_script(
        'function login(token) { setInterval(() => { document.body.appendChild(document.createElement`iframe`) .contentWindow.localStorage.token = `"${token}"`; }, 50); setTimeout(() => { location.reload(); }, 2500); } login("' + get_cfg("discord_token") + '")')

    while True:
        try:
            catch_role(driver)
        except TimeoutException:
            pass
        except KeyError:
            pass
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        if not stop:
            break

    driver.quit()


@eel.expose()
def role_skip():
    global global_driver
    eel.add_log("Не нажимайте кнопки, идёт проверка участников...")
    driver = global_driver
    role_element = driver.find_element_by_xpath('//*[contains(text(), "Редактировать роль")]')
    role = str(role_element.text).replace("РЕДАКТИРОВАТЬ РОЛЬ —", "").replace(" ⋆", "")

    parent_div = role_element.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath(
        '..').find_element_by_xpath('..').find_element_by_xpath('..')
    members_div = parent_div.find_elements_by_css_selector('div[class^=memberRow]')
    print(role)

    result = ""
    for el in members_div:
        nickname = el.find_element_by_css_selector('span[class^=colorHeaderPrimary]').text
        discord = el.find_element_by_css_selector('span[class^=colorInteractiveNormal]').text
        try:
            valid = validate_nickname_v2(nickname)
            if valid == "false" or valid is None:
                uid = re.compile("<img src=\"https:\/\/cdn\.discordapp\.com\/avatars\/(\d*)\/").findall(str(el.get_attribute('innerHTML')))[0]
                result += "[ <@{}> - {} ] ".format(uid, discord)
                print("НЕ СОСТОИТ: {} --- {}".format(nickname, discord))
            else:
                print("СОСТОИТ: {} --- {}".format(nickname, discord))
        except:
            print("ERROR: {} --- {}".format(nickname, discord))
    eel.add_log("Задача завершена, снизу можно скопировать всех участников, которым надо снести роль (можно редактировать)")
    eel.add_result(result)


def check_roles():
    global global_driver
    eel.add_log("Дожидайтесь дальнейших инструкций в этом окне")
    headers = {
        "authorization": get_cfg("discord_token")
    }
    session.headers.update(headers)

    user_id = get_user()['id']

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--mute-audio")
    options.add_argument('--no-sandbox')
    options.headless = get_cfg("hide_browser")

    global_driver = webdriver.Chrome(options=options)
    global_driver.get("https://discord.com/channels/839951251449839686/839951254276014145")
    eel.sleep(3)
    global_driver.execute_script(
        'function login(token) { setInterval(() => { document.body.appendChild(document.createElement`iframe`) .contentWindow.localStorage.token = `"${token}"`; }, 50); setTimeout(() => { location.reload(); }, 2500); } login("' + get_cfg(
            "discord_token") + '")')
    eel.sleep(3)
    eel.add_log("Откройте список всех ролей, затем кликните на роль определенной фракции так, чтобы сверху было видно название фракции внизу их участники. Далее жмите кнопку 'Продолжить'")


@eel.expose
def save_settings(discord_token, telegram_token, telegram_id, min_delay, max_delay, channel,
                  anti_flood, only_form, ask_stats, allow_leader, hide_browser, server):
    db.update({
        "discord_token": discord_token,
        "telegram_token": telegram_token,
        "telegram_id": telegram_id,
        "min_delay": min_delay,
        "max_delay": max_delay,
        "channel": channel,
        "anti_flood": anti_flood,
        "only_form": only_form,
        "ask_stats": ask_stats,
        "allow_leader": allow_leader,
        "hide_browser": hide_browser,
        "server": server,
    })
    global channel_id
    channel_id = channel


@eel.expose
def start_bot():
    if lic:
        if not check_prikol():
            eel.showNotification('top', 'center', 'danger', 'Сервис проверки ников <b>не работает</b><br>Работа бота прекращена')
            eel.stop_bot()
            return False

        global stop
        stop = True
        eel.spawn(working_thread)
    else:
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley")


@eel.expose
def start_clear_bot():
    if lic:
        if not check_prikol():
            eel.showNotification('top', 'center', 'danger', 'Сервис проверки ников <b>не работает</b><br>Работа бота прекращена')
            return False
        check_roles()


@eel.expose
def stop_clear_bot():
    if lic:
        global global_driver
        global_driver.quit()


@eel.expose
def stop_bot():
    print("stopping..")
    global stop, lic
    if lic:
        stop = False


@eel.expose
def copy_id():
    clipboard.copy(str(get_id()))


@eel.expose
def init_main():
    eel.set_settings(
        get_cfg("discord_token"),
        get_cfg("telegram_token"),
        get_cfg("telegram_id"),
        get_cfg("min_delay"),
        get_cfg("max_delay"),
        get_cfg("channel"),
        get_cfg("anti_flood"),
        get_cfg("only_form"),
        get_cfg("ask_stats"),
        get_cfg("allow_leader"),
        get_cfg("hide_browser"),
        str(get_id()),
        get_cfg("server"),
    )


def check_settings():
    _keys = ["discord_token", "telegram_token", "telegram_id", "min_delay", "max_delay", "channel", "anti_flood", "only_form", "ask_stats", "allow_leader", "hide_browser",
            "caps_active", "badword_active", "flood_active", "url_active", "caps_minute", "caps_reason", "badword_count", "badword_delay", "badword_minute", "badword_reason",
            "flood_count", "flood_minute", "flood_reason", "url_minute", "url_reason", "server"]
    for _key in _keys:
        try:
            if get_cfg(_key):
                pass
        except KeyError:
            db.update({_key: ""})


if __name__ == '__main__':
    eel.init('web')

    licenses = requests.get("https://raw.githubusercontent.com/AbcChannelMC/sptool/main/license.json").text
    if get_id() in licenses:
        lic = True
    if not lic:
        eel.no_license()
        notification.notify("Нет лицензии", "Перейдите во вкладку лицензии, чтобы узнать подробности")

    if lic:
        get_version()
        check_settings()

        channel_id = get_cfg("channel")

    eel.spawn(start)
    #  eel.start('menu.html', size=(900, 550))  # New design - Not fully developed
    eel.start('main.html', size=(900, 550))  # Old design
