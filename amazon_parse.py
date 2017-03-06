import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException        
from ryan_tools import *  
import shutil
import glob
import datetime
import time
import easygui



amazon_url = 'https://sellercentral.amazon.com/gp/transactions/actionableOrderPickup.html'

downloads_folder = os.path.join( os.getenv('USERPROFILE'), 'Downloads')

driver = ''

def download_orders_txt():
    amazon_user_name,amazon_password  = easygui.multenterbox('AMAZON CREDENTIALS', fields= ['USERNAME', 'PASSWORD'] )

    for file in glob.glob('*.txt'):
        os.remove(file)
        
    global driver
    driver = webdriver.Chrome()
    driver.get(amazon_url)
    driver.maximize_window()
    driver.find_element_by_id('ap_email').send_keys(amazon_user_name)
    driver.find_element_by_id('ap_password').send_keys(amazon_password)
    driver.find_element_by_id('signInSubmit').click()
    driver.find_element_by_id('Request ReportID').click()
    driver.refresh()
    driver.refresh()
    time.sleep(12)

    temp = 0
    while( temp == 0):
        driver.refresh()
        time.sleep(5)
        buttons = driver.find_element_by_xpath('//*[@id="reportStatusDataDiv"]/table/tbody/tr[2]/td[7]')
        if 'not ready' in buttons.text.lower():
            time.sleep(5)

        if 'download' in buttons.text.lower():
            buttons = driver.find_element_by_xpath('//*[@id="reportStatusDataDiv"]/table/tbody/tr[2]/td[7]')
            buttons.click()
            temp = 1
            break
        
    directory = os.getcwd()
    os.chdir(downloads_folder)
    a = 0
    while a == 0:
        for file in glob.glob('*.txt'):
            shutil.move( file , directory)
            a = 1

    os.chdir(directory)
    driver.quit()
    return 


