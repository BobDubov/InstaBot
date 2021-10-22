import random
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from login import username, password
import pickle
import os
from bs4 import BeautifulSoup

def log_in(username, password):
    # Скрываем использование робота Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-plugins-discovery")
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x935')
    browser = webdriver.Chrome('webdriver/chromedriver.exe', options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
              const newProto = navigator.__proto__
              delete newProto.webdriver
              navigator.__proto__ = newProto
              """
    })

    try:
        browser.get('https://www.instagram.com/')
        time.sleep(1)
        if os.path.exists('insta_chrome_coockies'):
            for cookie in pickle.load(open('insta_chrome_coockies', 'rb')):
                browser.add_cookie(cookie)
            time.sleep(1)
            browser.refresh()
            time.sleep(1)
        else:
            print(0)
            user = browser.find_element_by_name('username')
            user.clear()
            user.send_keys(username)
            print(1)
            time.sleep(0.5)
            psw = browser.find_element_by_name('password')
            psw.clear()
            psw.send_keys(password)
            print(2)
            time.sleep(0.5)
            browser.find_element_by_css_selector("button[type='submit']").click()
            print(3)
            time.sleep(2)
            try:
                if browser.find_element_by_css_selector('p#slfErrorAlert'):
                    print('Фсепропало!!!')
                    time.sleep(2)
                    browser.close()
                    browser.quit()
            except Exception as ex:
                print('Кажись вошли! - ')
                pickle.dump(browser.get_cookies(), open('insta_chrome_coockies', "wb"))

        browser.get('https://www.instagram.com/tat0ha62/')
        time.sleep(2)
        browser.find_element_by_css_selector('a[href="/tat0ha62/following/"]').click()
        time.sleep(2)


        if browser.find_element_by_css_selector("div[aria-label='Ваши подписки']"):
            time.sleep(2)
            print('Нашли список подписок')
            for step in range(250):
                div_subscr = browser.find_element_by_css_selector(
                    "div[aria-label='Ваши подписки']").find_elements_by_css_selector('button.sqdOP')[-1]
                time.sleep(1)
                div_subscr.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)

            urls = browser.find_element_by_css_selector(
                "div[aria-label='Ваши подписки']").find_elements_by_css_selector('a.notranslate')

            all_urls = set()
            for idx, url in enumerate(urls):
                print(idx, url.get_attribute('href'))
                all_urls.add(url.get_attribute('href'))
        else:
            print('Ooops! Не нашли список подписок')

    except Exception as ex:
        print(ex)
    finally:
        pickle.dump(browser.get_cookies(), open('insta_chrome_coockies', "wb"))
        browser.close()
        browser.quit()
        return all_urls


all_url = log_in(username, password)

with open('subscrib.json', 'w') as file:
    json.dump(list(all_url), file, indent=4, ensure_ascii=False)