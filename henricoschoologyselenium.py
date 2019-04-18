from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import json
import requests
user = ""
pwd = ""
options = Options()
options.headless = False
driver = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(driver, 10)
#driver.get("https://app.schoology.com/login")
driver.get("https://henrico.schoology.com/home#")
# These are the login codes
google_email = wait.until(expected_conditions.element_to_be_clickable((By.ID,"identifierId")))
email = "hcps-malanis1@henricostudents.org"
google_email.send_keys(email)
next_button = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"RveJvd")))
next_button.click()
time.sleep(3)
if driver.title == "adfs.henrico.k12.va.us":
    school_afds_username = wait.until(expected_conditions.element_to_be_clickable((By.ID,"input_1")))
    user="hcps-malanis1"
    school_afds_username.send_keys(user)
    school_afds_password = wait.until(expected_conditions.element_to_be_clickable((By.ID,"input_2")))
    password = "Knoxfor'1jkl" 
    school_afds_password.send_keys(password)
    school_afds_logon = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"credentials_input_submit")))
    school_afds_logon.click()

if driver.title == "Sign in - Google Accounts":
    # sometimes this google page shows up, if so click to continue
    continue_button = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"RveJvd")))
    continue_button.click()
    
# upcoming_list = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"upcoming-events-wrappersEventUpcoming-processed")))
list_of_events = []
events_details = {}
# upcoming list acquired
# get tooltip for subject, and text of what is the event
time.sleep(5)
upcoming_or_overdue = 0
for upcoming_or_overdue in range(0,2):
    time.sleep(4)
    upcoming_list = wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,".upcoming-list")))
    upcoming_list = driver.find_elements_by_css_selector('.upcoming-list')
    non_overdue_items = upcoming_list[upcoming_or_overdue-1].find_elements_by_css_selector(".upcoming-event")
    if upcoming_or_overdue == 0:
        due_or_over = "overdue"
    else:
        due_or_over = "pending"
    item_num = 0
    for item_num in range(len(non_overdue_items)-1):
        time.sleep(3)
        upcoming_list = wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,".upcoming-list")))
        upcoming_list = driver.find_elements_by_css_selector('.upcoming-list')
        non_overdue_items = upcoming_list[upcoming_or_overdue].find_elements_by_css_selector(".upcoming-event")
        name_of_item = non_overdue_items[item_num].find_element(By.TAG_NAME,'a').get_attribute('innerHTML')
        # hover_on_object = ActionChains(driver).move_to_element(non_overdue_items[0])
        # hover_on_object.perform()
        # Did not need this code
        # class_of_assignment = WebDriverWait(non_overdue_items[0], 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"div.realm-main-title"))).text
        # class_of_assignment = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"div.realm-main-title"))).text
        class_of_assingment = non_overdue_items[item_num].find_element_by_css_selector("div.realm-main-titles").get_attribute('innerHTML')
        non_overdue_items[item_num].click()
        time.sleep(3)
        if driver.title == "Home | Schoology":
            type_of = "assignment"
            clickable = non_overdue_items[item_num].find_element(By.TAG_NAME,"a").click()
            due_date = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#main-inner > div.assignment-details > p"))).text.replace("Due: ","")
            description = ""
            try:
                description = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#main-inner > div.info-container > div > div > p"))).text
            except TimeoutException:
                date_due_and_description = [due_date,description]
        else:
            table_items_with_target_info = wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,"tr.odd")))
            num = 0
            type_of = "event"
            date_due_and_description = []
            for num in range(len(table_items_with_target_info)):
                date_due_and_description.append(table_items_with_target_info[num].find_element(By.TAG_NAME,"td").text)
        try:
            attachement = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#main-inner > div.attachments > div > div > span.attachments-file-name > a:nth-child(1)"))).get_attribute("href")
            r = requests.get(attachement)
            name_of_attachment = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#main-inner > div.attachments > div > div > span.attachments-file-name > a:nth-child(1) > span"))).text
            filename = "Schoolfiles/"+class_of_assingment+"/"+name_of_attachment
            with open(filename, 'wb') as f:  
                f.write(r.content)
        except:
            pass
        list_of_events.append(name_of_item)
        events_details[name_of_item] = {}
        events_details[name_of_item]["class"],events_details[name_of_item]["due_date"],events_details[name_of_item]["description"],events_details[name_of_item]["type"],events_details[name_of_item]["due"] = class_of_assingment,date_due_and_description[0],date_due_and_description[1],type_of,due_or_over
        home_button = driver.find_element_by_css_selector("a._2JX1Q._1LY8n._2SVA_._9GDcm.util-height-six-3PHnk.util-width-sixteen-JiX3r.sExtlink-processed").click()
#  "div.realm-title-course-title"
# hover = ActionChains(firefox).move_to_element(element_to_hover_over)
# hover.perform()
# hover method found online
# for tag in upcoming_list.find_elements(By.TAG_NAME,'span'):
#     print(tag.text)
#     list_of_events.append(tag.text)
# print(list_of_events)
driver.quit()
with open('Schoology-items.json','w') as file:
    json.dump(events_details,file)