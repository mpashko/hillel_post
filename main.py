from selenium.webdriver.chrome.webdriver import WebDriver

selenium = WebDriver()
selenium.implicitly_wait(5)

selenium.get('https://www.olx.ua/')

search_bar = selenium.find_element_by_id('headerSearch')
search_bar.send_keys('playstation 5')

search_btn = selenium.find_element_by_id('submit-searchmain')
search_btn.submit()

resp = selenium.find_elements_by_class_name('offer')

print(len(resp))

selenium.quit()
