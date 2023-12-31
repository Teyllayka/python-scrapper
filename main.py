import sys
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import json

SCROLL_PAUSE_TIME = 0.5


def main():
    with open("data.json", "r") as outfile:
       data = json.load(outfile)


    url = f"https://www.pinterest.com/search/pins/?q={'%20'.join(sys.argv[2:])}&rs=typed"

    options = webdriver.ChromeOptions() 
    options.add_argument("--headless=new")
    options.page_load_strategy = 'none' 
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 
    driver = Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(6)

    driver.get(url) 


    last_height = driver.execute_script("return document.body.scrollHeight")
    pics = []
    while len(pics) < int(sys.argv[1]):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(2)
        breads = driver.find_elements(By.TAG_NAME, "img")
        for i in breads:
            if len(pics) < int(sys.argv[1]):
                if i not in pics:
                    pics.append(i.get_attribute("src").replace(".com/236x/", ".com/564x/"))
            else:
                break

    dictionary = { "next_post_date": data["next_post_date"], "post_id": data["post_id"],  "urls": pics}
    with open("data.json", "w") as outfile:
        json.dump(dictionary, outfile)

while True:
    try:
        main()
        break  # If the script successfully completes, break the loop
    except Exception as e:
        print(f"An error occurred: {e}. Restarting...")
