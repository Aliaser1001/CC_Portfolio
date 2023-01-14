from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

s = Service('/usr/local/bin/chromedriver')
chromeOptions = Options()
chromeOptions.headless = False


url = 'https://app.powerbi.com/view?r=eyJrIjoiNDAyMWRhZWUtMDEyMi00MGNhLTkyMjYtNjcwMjg5NmEyYzA0IiwidCI6IjZmMjdmNjhjLWFmMTYtNDkzZC1iNDgzLTAxOTI2OGY1YTFiOCIsImMiOjl9&pageName=ReportSection6662b568d03574de783f'
driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.get(url)

"""consent_button = driver.find_element(By.XPATH, '//*[@id="cookies"]/div[2]/div')
consent_button.click()
iframes = driver.find_elements(By.TAG_NAME, 'iframe')
driver.switch_to.frame(iframes[0])"""
data = []

try:
        try:
            element = WebDriverWait(driver, timeout=30).until(EC.visibility_of_all_elements_located((By.XPATH,
                                                                       '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[12]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[4]/div/div/div')))
            for i in range(20):
                names = driver.find_element(By.XPATH,
                                            f'//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[12]/transform/div/div[2]/div/visual-modern/div/div/div[2]/div[1]/div[4]/div')

                print(names.text)
                data.append(names)
        except:

            print("iframe hasn't loaded yet")
except TimeoutException:
    print("Took too much time to load the element")
