import threading
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import queue
import time
import sys
from scapy.all import*
from urllib import parse

conf.use_pcap = True

options = EdgeOptions()
options.add_argument('incognito')
options.add_argument('--v=1')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_experimental_option('prefs', {'safebrowsing.enabled':False})
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

def process_domain(domain, result):
    time.sleep(1)
    driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)
    response = 200	
    try:
        domain = domain.replace("\n", '')
        print(domain)
        driver.get("https://" + domain)
        WebDriverWait(driver, 10)
    
        
    except:
        print("502 error")
        response = 502
    
    result.put(response)
    driver.close()
    

def main():
	result = queue.Queue()
	with open("/home/seungmin/phish/benign/%s"%(sys.argv[1]), 'r') as file:
		domain_names = file.readlines()

	for domain in domain_names:
		# if int(domain.split(',')[0]) < 13675:
		# 	continue
		thread = threading.Thread(target=process_domain, args=(domain.split(',')[1], result))

		thread.start()
		pcap_file = sniff(iface='ens33', timeout=10, filter='tcp')
		thread.join()

		if result.get() == 200:
			file_name = "/home/seungmin/phish/benign/traffic/edge/%s.pcap"%(domain.replace("/",''))
			try:
				wrpcap(str(file_name), pcap_file)
			except:
				print("Pcap upload Error")

if __name__ == "__main__":
	main()
