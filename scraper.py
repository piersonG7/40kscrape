from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from dataclasses import dataclass

from time import sleep

from json import dump

@dataclass
class Match():
    player:str
    event:str
    date:str
    record:str
    players:str
    listlink:str
    eventlink:str


driver = webdriver.Chrome()
driver.get("https://armylists.rmz.gs/?losses=all&faction=Space+Marines&detachment=Stormlance+Task+Force&rounds=all&offset=100&player_count=all")

elem = driver.find_elements(By.TAG_NAME, "select")

faction_ref = Select(elem[0])


def reset_offset(driver:webdriver.Chrome):
    
    urllist = driver.current_url.split("&")
    urllist[-2] = "offset=0"
    driver.get('&'.join(urllist))


for i, faction_name in enumerate(faction_ref.options):
    if i==0:
        continue

    faction = Select(driver.find_elements(By.TAG_NAME, "select")[0])
    faction.select_by_index(i)

    detach = Select(driver.find_elements(By.TAG_NAME, "select")[1])

    for i, detachment_name in enumerate(detach.options):
        if i==0:
            continue

        detach = Select(driver.find_elements(By.TAG_NAME, "select")[1])
        detach.select_by_index(i)

        reset_offset(driver)

        matches = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

        for match in matches:

            # Get data from all columns
            cols = match.find_elements(By.TAG_NAME, 'td')



            # Get data from links

            links = match.find_elements(By.TAG_NAME, 'a')

            # These Lines bring up and close the pop-up windows for each row, but 
            # they don't appear to be necessary 
            ## match.click()
            ## webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()



        detach = Select(driver.find_elements(By.TAG_NAME, "select")[1])


            
        
