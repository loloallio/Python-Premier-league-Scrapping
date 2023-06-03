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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # , #options=chrome_options)

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
time.sleep(6)
pgsour = driver.page_source

pattern = re.findall(r'www.premierleague.com/match/\d*', pgsour)
match = []
# Web sometimes has duplicates, thus this step is needed
[match.append(x) for x in pattern if x not in match]

with open('links1.txt', 'w', encoding='utf-8') as file1, \
        open('links2.txt', 'w', encoding='utf-8') as file2, \
        open('links3.txt', 'w', encoding='utf-8') as file3, \
        open('links4.txt', 'w', encoding='utf-8') as file4, \
        open('links5.txt', 'w', encoding='utf-8') as file5:
    counter = 0
    for i in match:
        if counter == 0:
            file1.write(f"{i}\n")
            counter += 1
        elif counter == 1:
            file2.write(f"{i}\n")
            counter += 1
        elif counter == 2:
            file3.write(f"{i}\n")
            counter += 1
        elif counter == 3:
            file4.write(f"{i}\n")
            counter += 1
        elif counter == 4:
            file5.write(f"{i}\n")
            counter = 0

