from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep, strftime
from datetime import datetime
import os
import json

path = os.getcwd()
with open(path + '\\env.json') as f:
  data = json.load(f)

dizu_login = data["dizu_login"]
dizu_password = data["dizu_password"]
instagram_logins = data["instagram_logins"]
instagram_passwords = data["instagram_passwords"]
max_loading_time = int(data["max_loading_time"])
time_per_account = int(data["time_per_account"])

# Set up Firefox
geckodriver = path + '\\geckodriver.exe'
opts = webdriver.FirefoxOptions()
opts.headless = True
driver = webdriver.Firefox(executable_path=geckodriver,options=opts)

# Writing in Browser
def insert_text(text, path):
    wait = WebDriverWait(driver, max_loading_time)
    insert_xpath = path
    element = wait.until(EC.element_to_be_clickable((By.XPATH, insert_xpath)))
    insert = driver.find_elements_by_xpath(insert_xpath)
    insert[0].send_keys(text)

# Clicking in browser
def click(path):
    wait = WebDriverWait(driver, max_loading_time)
    button_xpath = path
    element = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    sleep(1)
    button = driver.find_elements_by_xpath(button_xpath)
    button[0].click()

for j in range (0,100): 

    # Lopping the proccess
    for i in range(0,len(instagram_logins)):

        # Opening Dizu login page
        
        driver.install_addon('C:\\Users\\davil\\projects\\Dizu\\dizu-1.0.3-an+fx.xpi', temporary=True)        
        driver.get('https://dizu.com.br/login')

        # logging in on Dizu
        insert_text(dizu_login,'//*[@id="login"]')
        insert_text(dizu_password,'//*[@id="senha"]')
        click('/html/body/div[1]/section/form/div[5]/button/p')

        # Getting to the 'Conectar e Ganhar' page
        sleep(5)
        click('/html/body/div[1]/div/div[1]/div[2]/ul/li[3]/a/p')

        # Selecting the Account and Tasks
        click(('/html/body/div[1]/div/div[2]/div[2]/div/div[4]/div/form/div[1]/div/select/option[%d]' % (i+2)))
        try:
            click('//*[@id="tarefas10"]')
        except:
            pass

        try:
            click('//*[@id="curtida05"]')
        except:
            pass

        # Initializing Dizu Extension
        click('//*[@id="iniciarTarefasExtensao"]')
        driver.switch_to.window(driver.window_handles[0])

        # Logging in on Instagram
        insert_text(instagram_logins[i],'/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
        insert_text(instagram_passwords[i],'/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
        click('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div')

        print ("[%s] - Login number %s with @%s" % (datetime.now().strftime("%H:%M:%S"),(j+1),instagram_logins[i]))

        # Time that Dizu's plugin operates in a certain account
        sleep(time_per_account)        
    
        # Close Firefox
        driver.quit()
        print ("[%s] - Closing @%s" % (datetime.now().strftime("%H:%M:%S"),instagram_logins[i]))
        driver = webdriver.Firefox(executable_path=geckodriver,options=opts)
