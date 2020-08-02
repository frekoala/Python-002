from selenium import webdriver
import time
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs

try:
    browser = webdriver.Chrome()
    browser.get('https://shimo.im/login?from=home')

    time.sleep(1)
    browser.find_element_by_name('mobileOrEmail').send_keys('111@qq.com')
    browser.find_element_by_name('password').send_keys('111111')
    time.sleep(1)

    browser.find_element_by_xpath('//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]').click()

    cookies = browser.get_cookies()
    # print(cookies)
    time.sleep(10)

    # browser.get('https://shimo.im/inbox')
    # # 打印收件箱里的标题
    # card_info = browser.find_elements_by_xpath('//div[@class="card-title"]')
    # for card in card_info:
    #     print(card.get_attribute('textContent'))

    # time.sleep(10)
except Exception as e:
    print(e)
finally:
    browser.close()


# 尝试selenium直接用cookies打开页面
try:
    browser2 = webdriver.Chrome()
    # selenium模拟不像requests访问时直接带cookie;要先访问url,再加cookie，再访问url
    browser2.get('https://shimo.im/inbox')
    print(cookies)
    print('-----------')
    for cookie in cookies:
        browser2.add_cookie(cookie)
    print(browser2.get_cookies())
    browser2.get('https://shimo.im/inbox')
    # 打印网页
    print(browser2.page_source)

    time.sleep(10)
except Exception as e:
    print(e)
finally:
    browser2.close()

# 尝试requests直接用cookies打开页面
# user_agent = UserAgent(path='fake_useragent.json').random
# headers = {
#     'user_agent': user_agent,
#     'referer': 'https://shimo.im/login?from=home',
#     'x-requested-with': 'XmlHttpRequest'
# }

# url2 = 'https://shimo.im/inbox'
# newsession = requests.Session()
# for cookie in cookies:
#     newsession.cookies.set(cookie['name'], cookie['value'])
# print('--------------')
# print(newsession.cookies)
# print('--------------')
# response2 = newsession.get(url2, headers=headers)

# print(response2.text)
# bs_info = bs(response2.text, 'html.parser')
# card_info = bs_info.find_all('div', attrs={'class': 'Div-sc-2H_geb eDqDc'})
# print(card_info)
