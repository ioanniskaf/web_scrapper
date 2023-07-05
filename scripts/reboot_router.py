from requests import get
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import dotenv_values

def reboot_router_via_driver():
	'''
	Reboots the router via webdriver from selenium. Router specific.
	'''
	print("Router reboot initiated")
	try:
		# Get env parameters
		env = dotenv_values(".env")
		driver = webdriver.Firefox()
		driver.get(env["ROUTER_URL"])
		driver.find_element(By.ID,"Frm_Username").send_keys(env["ROUTER_USER"])
		driver.find_element(By.ID,"Frm_Password").send_keys(env["ROUTER_PASS"])
		sleep(2)
		driver.find_element(By.ID,"LoginId").click()
		sleep(2)
		driver.find_element(By.ID,"mgrAndDiag").click()
		sleep(2)
		driver.find_element(By.ID,"devMgr").click()
		sleep(2)
		driver.find_element(By.ID,"Btn_restart").click()
		# sleep(2)
		# driver.find_element(By.ID,"confirmOK").click()
		driver.quit()
		print("Router rebooted")
	except Exception as e:
		print(e)

def internet_connected():
	'''
	Checks whether there is live internet connection.
	'''
	try:
		r = get("https://www.google.com", timeout=5)
		if r.raise_for_status() is None:
			return True
		else:
			return False
	except Exception as e:
		print(e)
		return False

def reboot_router(max_attempts):
	'''
	Main function to reboot the router. First there is a 60 sec waiting and
	after that betweeb each connectivity check attempt there is a 30 sec delay.
	Maximum attempts variable is user defined. 
	Returns True if there is internet connection and False not. 
	'''
	attempt = 0
	reboot_router_via_driver()
	sleep(6)
	print("Waiting reboot to complete")
	while attempt < max_attempts:
		print(f'Checking internet connection attempt number: {attempt+1}...')
		if internet_connected():
			print("Internet Connection is back!!!")
			attempt=10
			return True
		else:
			attempt+=1
			print("No Internet Connection. Retrying...")
			sleep(3)
	return False