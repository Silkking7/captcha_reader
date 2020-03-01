import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.anses.gob.ar/fecha-de-cobro-beneficio"
img_id = "anses_captcha"
reload_captcha_id = "edit-reload-captcha"

driver = None
try:
	driver = webdriver.Chrome(executable_path=r"/home/silkking/Workspace/faraday/tests/selenium/chromedriver")
	driver.get(url)
	wait = WebDriverWait(driver, 10)

	for i in range(0, 200):
		img = wait.until(
		    EC.presence_of_element_located((By.ID, img_id))
		)
		src = img.find_element_by_tag_name("img").get_attribute("src").replace("data:image/jpeg;base64,","")
		imgdata = base64.b64decode(src)
		ts = time.time()
		filename = '_' + str(ts) + '.jpg'  # I assume you have a way of picking unique filenames
		with open(filename, 'wb') as f:
		    f.write(imgdata)
		driver.refresh()
		# urllib.urlretrieve(src, "captcha.png")
		# captcha_reloader = driver.find_element_by_id("edit-reload-captcha")
		# captcha_reloader.click()

finally:
	if(driver is not None):
		driver.close()





