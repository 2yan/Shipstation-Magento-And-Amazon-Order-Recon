import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException        
from ryan_tools import *  
import shutil
import glob
import datetime
import easygui



def download_orders_csv(start_date, end_date ):
    fields = ['URL', 'Username', 'Password']
    magento_url, magento_user_name, magento_password= easygui.multenterbox('Magento Credientials', fields= fields )
    magento_url = magento_url.replace('www.', 'https://' )
    downloads_folder = os.path.join( os.getenv('USERPROFILE'), 'Downloads')
    try:
        os.remove('orders.csv')
    except FileNotFoundError:
        pass

    driver = webdriver.Chrome()
    driver.get(magento_url)
    driver.maximize_window()
    driver.find_element_by_id("username").send_keys(magento_user_name)
    driver.find_element_by_id("login").send_keys(magento_password)
    driver.find_element_by_class_name('form-button').click()
    driver.get(magento_url + '/sales_order/index/key/')
    
    driver.find_element('name','created_at[from]' ).send_keys( get_date_str(start_date))
    driver.find_element('name','created_at[to]' ).send_keys( get_date_str(end_date ))
    
    Select(driver.find_element_by_id('sales_order_grid_filter_status' )).select_by_visible_text('Processing')
    driver.execute_script('sales_order_gridJsObject.doFilter()')
    
    directory = os.getcwd()
    os.chdir(downloads_folder)
    
    a = 0
    while a == 0:
        try:
            driver.execute_script('sales_order_gridJsObject.doExport()')
        except WebDriverException:
            driver.refresh()
        
        for file in glob.glob('orders.csv'):
            driver.quit()
            shutil.move('orders.csv' , directory)
            a = 1

    os.chdir(directory)
    return 

