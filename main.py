# main.py
from modules.config_loader import ConfigLoader
from modules.browser_manager import BrowserManager
from modules.vpn_manager import VPNManager
from modules.page_navigator import PageNavigator
from modules.report_writer import ReportWriter
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException
)
from selenium.webdriver.support.ui import WebDriverWait


import random
import time
import csv

# Load configurations
config = ConfigLoader.load_general_config()
targets = ConfigLoader.load_targets()
viewports = ConfigLoader.load_viewports()
servers = ConfigLoader.load_servers()
user_agents = ConfigLoader.load_user_agents()

vpn_manager = VPNManager(config["vpn_path"], servers)
browser_manager = BrowserManager(viewports, user_agents)
report_writer = ReportWriter(config["detailed_report_path"], config["summary_report_path"])

# Access general time settings
min_stay_time = config["min_stay_time"]
max_stay_time = config["max_stay_time"]

# Initialize clicks count for each target from the summary report file
clicks_count = {target["link"]: 0 for target in targets}
try:
    with open(config["summary_report_path"], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            link, keyword, total_clicks = row
            if link in clicks_count:
                clicks_count[link] = int(total_clicks)
except FileNotFoundError:
    pass

# Continue until all targets have reached their required number of clicks
while any(clicks_count[target["link"]] < target["clicks_needed"] for target in targets):
    # Shuffle the targets list to process them in a random order
    random.shuffle(targets)

    for target in targets:
        if clicks_count[target["link"]] >= target["clicks_needed"]:
            continue

        target_link = target["link"]
        target_title = target.get("title", "")
        search_query = random.choice(target["keywords"])
        print(f"Using keyword for search: {search_query}")

        vpn_manager.change_vpn()
        driver = browser_manager.create_driver()
        page_navigator = PageNavigator(driver, min_stay_time, max_stay_time)
        
        # Navigate to Google and input search query
        driver.get("https://www.google.com")
        time.sleep(2)  # Allow time for Google page to load

        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            print(f"Successfully entered keyword: {search_query}")
        except TimeoutException:
            print("Search box not found or Google failed to load.")
            driver.quit()
            continue

        # Execute the search and click functionality
        success, rank, link = page_navigator.find_and_click_target_link(target_link, target_title)
        
        if success:
            report_writer.write_detailed_report(target_link, search_query, success, rank, link)
            report_writer.update_summary_report(target_link, search_query)
            clicks_count[target_link] += 1
        driver.quit()

print("Process completed.")

