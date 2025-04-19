from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from dataclasses import dataclass
import dataclasses

from time import sleep

from json import dump

@dataclass
class Match():
    faction:str
    detachment:str
    player:str
    event:str
    date:str
    record:str
    players:str
    listlink:str
    eventlink:str


driver = webdriver.Chrome()
driver.get("https://armylists.rmz.gs/?losses=all&faction=Space+Marines&detachment=Stormlance+Task+Force&rounds=all&offset=0&player_count=30")

elem = driver.find_elements(By.TAG_NAME, "select")

faction_ref = Select(elem[0])


def set_offset(driver:webdriver.Chrome, offset:int):
    
    urllist = driver.current_url.split("&")
    urllist[-2] = f"offset={str(offset)}"
    driver.get('&'.join(urllist))


for i, _ in enumerate(faction_ref.options):
    if i==0:
        continue


    faction = Select(driver.find_elements(By.TAG_NAME, "select")[0])
    faction.select_by_index(i)
    faction_name = faction.options[i].text

    detach = Select(driver.find_elements(By.TAG_NAME, "select")[1])

    for i, _ in enumerate(detach.options):
        if i==0:
            continue



        match_data:list[Match] = []

        detach = Select(driver.find_elements(By.TAG_NAME, "select")[1])
        detach.select_by_index(i)
        detachment_name = detach.options[i].text

        current_offset = 0

        while True:

            set_offset(driver, current_offset)

            matches = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            if not matches:
                break

            for match in matches:

                # Get data from all columns
                cols = match.find_elements(By.TAG_NAME, 'td')

                # Get data from links

                links = match.find_elements(By.TAG_NAME, 'a')

                match_data.append(dataclasses.asdict(Match(
                    faction=faction_name,
                    detachment=detachment_name,
                    player=cols[1].text,
                    event=cols[2].text,
                    date=cols[3].text,
                    record=cols[4].text,
                    players=cols[5].text,
                    listlink=links[0].get_attribute('href'),
                    eventlink=links[1].get_attribute('href')
                )))

            current_offset += 50



            # These Lines bring up and close the pop-up windows for each row, but 
            # they don't appear to be necessary 
            ## match.click()
            ## webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        with open(f"results/{faction_name}_{detachment_name}.json", 'w') as f:
            dump(match_data, f, indent=4)


        


            
        
