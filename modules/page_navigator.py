from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException
)
import time
import random

class PageNavigator:
    def __init__(self, driver, min_stay_time, max_stay_time):
        self.driver = driver
        self.min_stay_time = min_stay_time
        self.max_stay_time = max_stay_time

    

    def slow_smooth_scroll(self, scroll_step_min=50, scroll_step_max=100):
        """Gradually scrolls down the page in small steps to mimic smooth user behavior."""
        current_scroll_position = self.driver.execute_script("return window.pageYOffset;")
        max_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

        while current_scroll_position < max_scroll_height:
            # Scroll by a small, random step each time
            scroll_step = random.randint(scroll_step_min, scroll_step_max)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            current_scroll_position += scroll_step

            # Small pause to simulate reading or scanning behavior
            time.sleep(random.uniform(0.3, 0.7))

            # Stop if reached the bottom of the page
            if current_scroll_position >= max_scroll_height:
                break

    def scroll_through_page(self):
        """Smoothly scrolls through the target page with randomized steps and pauses, and then scrolls back up."""
        print("Scrolling through the page after link found...")
        current_scroll_position = 0
        max_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

        # Scroll down with randomized steps and pauses
        while current_scroll_position < max_scroll_height:
            scroll_step = random.randint(150, 300)  # Random scroll step size
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            current_scroll_position += scroll_step
            time.sleep(random.uniform(1, 3))  # Random pause to simulate reading

            # Stop if reached the bottom of the page
            if current_scroll_position >= max_scroll_height:
                break

        # Scroll back up smoothly with randomized steps and pauses
        while current_scroll_position > 0:
            scroll_step = random.randint(150, 300)  # Random scroll step size for upward scroll
            self.driver.execute_script(f"window.scrollBy(0, {-scroll_step});")
            current_scroll_position -= scroll_step
            time.sleep(random.uniform(1, 2))  # Slightly faster randomized pause for upward scroll

            # Stop if reached the top of the page
            if current_scroll_position <= 0:
                break



    def is_access_denied(self):
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            return "access denied" in body_text or "forbidden" in body_text
        except NoSuchElementException:
            return False
        
    def find_and_click_target_link(self, target_link, target_title):
        print(f"Searching for link: {target_link} with title: {target_title}")
        rank = 1
        target_found = False
        current_scroll_position = 0
        max_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

        while not target_found:
            try:
                # Gradual scrolling
                scroll_step = random.randint(100, 200)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                current_scroll_position += scroll_step
                time.sleep(random.uniform(0.5, 1))  # Pause for realism

                # Check for links visible in viewport
                results = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'http')]")
                for result in results:
                    # Check if the element is within the viewport
                    is_in_viewport = self.driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect();"
                        "return (rect.top >= 0 && rect.left >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && rect.right <= (window.innerWidth || document.documentElement.clientWidth));",
                        result
                    )
                    if is_in_viewport:
                        link = result.get_attribute("href")
                        if (target_link and target_link in link) or (target_title and target_title.lower() in link.lower()):
                            print(f"Potential target found at rank {rank}: {link}")
                            
                            # Scroll to center the element in view
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result)
                            time.sleep(random.uniform(1, 2))  # Mimic user hesitation
                            
                            # Click the link
                            result.click()
                            self.scroll_through_page()  # Optional: scroll through the target page
                            time.sleep(random.uniform(self.min_stay_time, self.max_stay_time))
                            return True, rank, link
                    rank += 1

                # Check if reached the bottom of the page
                if current_scroll_position >= max_scroll_height:
                    # Check for "More Results" button if target link not found
                    more_results_button = self._find_more_results_button()
                    if more_results_button:
                        print("Clicking 'More Results' button to load more results...")
                        more_results_button.click()
                        time.sleep(1)
                        current_scroll_position = 0  # Reset scroll position
                        max_scroll_height = self.driver.execute_script("return document.body.scrollHeight")  # Update max scroll height
                    else:
                        break  # Exit loop if no more results button is found
            except Exception as e:
                print(f"Error during scrolling or link finding: {e}")
                break

        return False, rank, None












    def randomized_scroll(self, scroll_step_min=200, scroll_step_max=400):
        """Randomized scroll behavior with varied pauses to mimic natural user actions."""
        current_scroll_position = self.driver.execute_script("return window.pageYOffset;")
        max_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

        # Continuously scroll until reaching the bottom
        while current_scroll_position < max_scroll_height:
            # Scroll by a random step value
            scroll_step = random.randint(scroll_step_min, scroll_step_max)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            current_scroll_position += scroll_step

            # Randomized pause to simulate natural reading behavior
            time.sleep(random.uniform(0.5, 1.5))

            # Update the max scroll height in case of dynamic page loading
            max_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

            # Stop if we’ve reached or exceeded the max scroll height
            if current_scroll_position >= max_scroll_height:
                break





    




    def _find_more_results_button(self):
        # Tries to locate the "More Results" button specifically
        try:
            return self.driver.find_element(By.XPATH, "//a[@aria-label='Другие результаты поиска']")
        except NoSuchElementException:
            return None


    def slow_scroll_to_element(self, element):
        """Scroll slowly to the given element to mimic slower user scrolling behavior."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", element)
        current_scroll_position = self.driver.execute_script("return window.scrollY")
        element_position = self.driver.execute_script("return arguments[0].getBoundingClientRect().top + window.scrollY;", element)

            # Slowly scroll to the element position
        while current_scroll_position < element_position:
            scroll_step = random.randint(50, 100)  # Smaller scroll steps for slower movement
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            current_scroll_position += scroll_step
            time.sleep(random.uniform(0.5, 0.8))  # Slower pause between scrolls

                # Update the element position in case it changes
            element_position = self.driver.execute_script("return arguments[0].getBoundingClientRect().top + window.scrollY;", element)







    def _find_next_button(self):
        # Tries to find the next button with multiple methods for reliability
            next_button = None
            try:
                next_button = self.driver.find_element(By.ID, "pnnext")
            except NoSuchElementException:
                try:
                    next_button = self.driver.find_element(By.LINK_TEXT, "Next")
                except NoSuchElementException:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next page']")
                    except NoSuchElementException:
                        try:
                            next_button = self.driver.find_element(By.XPATH, "//span[@class='ULf8Gc']/div[@class='aVlTpc KArJuc']")
                        except NoSuchElementException:
                            return None
            return next_button
