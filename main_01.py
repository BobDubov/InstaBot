from sys import argv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login import username, password
import os
import pickle
import time
import json
import random
import datetime

def log_in(username, password):
    ban_cnt = 1
    new_url = set()
    status = 'Старт'
    hashtags = ['woodwork', 'wooddiy', 'yogagirl', 'fitnessgirl', 'woodtoys']

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
        status = 'Заходим'
        if os.path.exists('insta_chrome_coockies'):
            for cookie in pickle.load(open('insta_chrome_coockies', 'rb')):
                browser.add_cookie(cookie)
            time.sleep(1)
            status = 'Загрузили куки'
            browser.refresh()
            status = 'Обновились после загрузки куки'
        else:
            status = 'Нужно ввести логин - пароль'
            time.sleep(3)
            inp_user = browser.find_element_by_name('username')
            print(inp_user.text)
            inp_user.clear()
            inp_user.send_keys(username)
            inp_psw = browser.find_element_by_name('password')
            inp_psw.clear()
            inp_psw.send_keys(password)
            print(inp_psw.text)
            browser.find_element_by_css_selector("button[type='submit']").click()
            time.sleep(2)
            try:
                status = 'Проверяем логин-пароль'
                if browser.find_element_by_css_selector('p#slfErrorAlert'):
                    print('Фсепропало!!!')
                    status = 'Не пускают'
                    time.sleep(2)
                    browser.close()
                    browser.quit()
            except Exception as ex:
                status = 'Вошли в учетку'
                print('Кажись вошли! - ', datetime.datetime.now().strftime("%H:%M %d.%m.%Y"))
                pickle.dump(browser.get_cookies(), open('insta_chrome_coockies', "wb"))

        start_time = datetime.datetime.now().replace(microsecond=0)
        print(f'Старт в {start_time.strftime("%H:%M %d.%m.%Y")}')
        hashtag = hashtags[random.randrange(0,5)]
        time.sleep(2)
        status = 'Ищем посты по хэштегу'
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(2)

        for step in range(random.randrange(5, 25)):
            status = 'Листаем результат поиска по хэштегу'
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        status = 'Получаем список ссылок поиска по хэштегу'
        urls = browser.find_elements_by_css_selector('div.v1Nh3')
        link_cnt = len(urls)
        print(f'Собрали {link_cnt} ссылок \n {"* " * 10}')
        for link in urls:
            url = link.find_element_by_css_selector('a').get_attribute('href')
            new_url.add(url)
        link_cnt = len(new_url)
        start_item = datetime.datetime.now()

        status = 'Начинаем переходить по ссылкам постов'
        for idx, link in enumerate(list(new_url)[::-1]):
            pickle.dump(browser.get_cookies(), open('insta_chrome_coockies', "wb"))
            time.sleep(2)
            browser.get(link)
            time.sleep(2)

            ''' Ищем кнопку лайка и ставм лайк 30-50% постов '''
            status = 'Ищем кнопку лайка'
            like_post = browser.find_element_by_tag_name('article').find_element_by_tag_name(
                'section').find_element_by_tag_name('button')
            status = 'Если лайк не стоит и они счастливчики, ставим лайк'
            if like_post.find_element_by_tag_name('svg').get_attribute('aria-label') == 'Нравится' and (idx + 1) % random.randrange(2, 5) == 0:
                like_post.click()               #  Ставим лайк посту
                time.sleep(15 + random.randrange(15, 45))
                status = 'Если кнопка лайка поменялась, плюсуем лайк'
                if like_post.find_element_by_tag_name('svg').get_attribute('aria-label') == 'Не нравится':
                    print(datetime.datetime.now().strftime("%H:%M") + f' [+] [LIKE] ...{link[-10:-1]} - ' + str(datetime.datetime.now() - start_item))

            ''' Крутанем пост вниз и переходим на автора поста '''
            status = 'Листаем страницу поста'
            for step in range(random.randrange(1, 3)):
                time.sleep(1)
                browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            status = 'Ищем ссылку на страницу автора поста'
            time.sleep(1 + random.randrange(1,3))
            user_link = browser.find_element_by_css_selector('div.e1e1d > span > a').get_attribute('href')

            ''' Читаем список наших пописок и если автора поста
                нет в списке, то подписываемся на 60-75% авторов '''
            status = 'Читаем список наших подписок'
            with open('subscrib.json') as file:
                subscrid = json.load(file)
            old_user_link = set(subscrid)

            status = 'Если автора поста нет в нашем списке переходим к нему'
            if user_link not in old_user_link:
                browser.get(user_link)
                time.sleep(random.randrange(5, 10))
                try:
                    status = 'Если автору повезло - ищем кнопку подписки'
                    if idx % random.randrange(1, 3) == 0:
                        button_sub = browser.find_element_by_tag_name('main').find_element_by_tag_name(
                            'section').find_element_by_tag_name('button')
                        status = 'Если кнока Подписаться есть - подписываемся'
                        if button_sub.text == 'Подписаться':
                            button_sub.click()
                            time.sleep(3)
                            status = 'После нажатия, повторно ищем кнопку Подписка и автора поста'
                            button_sub = browser.find_element_by_tag_name('main').find_element_by_tag_name(
                                'section').find_element_by_tag_name('button')
                            status = 'Проверяем изменение статуса кнопки Подписка и автора поста'
                            if button_sub.text != 'Подписаться':
                                time.sleep(60 + (random.randrange(10, 180)))
                                old_user_link.add(user_link)
                                with open('subscrib.json', 'w') as file:
                                    json.dump(list(old_user_link), file, indent=4, ensure_ascii=False)
                                print(datetime.datetime.now().strftime("%H:%M") + f' [+] [{idx + 1}/{link_cnt}] {user_link} - ' + str(datetime.datetime.now() - start_item))
                                start_item = datetime.datetime.now()
                            else:
                                time.sleep(60 + (random.randrange(10, 180)))
                                print(datetime.datetime.now().strftime("%H:%M") + f' [-] [{idx + 1}/{link_cnt}] Банят! Syki!!! - ' + str(datetime.datetime.now() - start_item))
                                start_item = datetime.datetime.now()
                                if ban_cnt > 2:
                                    print('[INFO] Слишком много банов')
                                    return
                                ban_cnt += 1

                except Exception as ex:
                    print(datetime.datetime.now().strftime("%H:%M") + f' [ER] {status} -  Ошибка {ex[:15]}...' + str(datetime.datetime.now() - start_item))
                time.sleep(random.randrange(1,5))
                browser.back()
            time.sleep(random.randrange(1,10))
            browser.back()

        time.sleep(5)
    except Exception as ex:
        browser.get_screenshot_as_file("error.png")
        print(f'[Glob ERR] - {status} - ', ex)
    finally:
        browser.close()
        browser.quit()
        finish_time = datetime.datetime.now().replace(microsecond=0)
        print(f'Финиш в {finish_time.strftime("%H:%M %d.%m.%Y")}')
        print(f'Успели за {finish_time - start_time}')

def main():
    log_in(username, password)

if __name__ == '__main__':
    main()
