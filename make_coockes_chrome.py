from selenium import webdriver
import pickle
import time

def log_in():

    # Скрываем использование робота Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-plugins-discovery")
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
        time.sleep(60)
        pickle.dump(browser.get_cookies(), open('insta_chrome_coockies', "wb"))
        print('Куки записан')
        time.sleep(10)
    except Exception as ex:
        print('[Glob ERR] - ', ex)
    finally:
        browser.close()
        browser.quit()

def main():
    log_in()

if __name__ == '__main__':
    main()
