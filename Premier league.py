from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time



# Open main-link
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.premierleague.com/results")
time.sleep(1)

cookies = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[@id='onetrust-consent-sdk']/div["
                                              "@id='onetrust-banner-sdk']/div[@class='ot-sdk-container']/div["
                                              "@class='ot-sdk-row']/div[@id='onetrust-button-group-parent']/div["
                                              "@id='onetrust-button-group']/div["
                                              "@class='banner-actions-container']/button["
                                              "@id='onetrust-accept-btn-handler']")))
cookies.click()

pgdown = driver.find_element(By.XPATH, "/html/body/footer[@class='mainFooter']/div[@class='footerCorporate']/div["
                                       "@class='wrapper col-12']/ul/li[4]/a")

pgdown.send_keys(Keys.END)
pgdown.send_keys(Keys.PAGE_UP)
pgdown.send_keys(Keys.END)
time.sleep(2)
pgsour = driver.page_source

pattern = re.findall(r'www.premierleague.com/match/\d*', pgsour)
match = []
# Web sometimes has duplicates, thus this step is needed
[match.append(x) for x in pattern if x not in match]

with open('links.txt', 'w', encoding='utf-8') as file:
    for i in match:
        file.write(f'{i}\n')
