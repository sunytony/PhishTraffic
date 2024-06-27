import threading
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import queue
import time
import sys
from scapy.all import*
from urllib import parse

conf.use_pcap = True

options = ChromeOptions()
options.add_argument('incognito')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_experimental_option('prefs', {'safebrowsing.enabled':False})

def process_domain(domain, result):
    time.sleep(1)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print("tests")
    response = 200	
    try:
        print(domain)
        driver.get(domain)
        WebDriverWait(driver, 10)
        source_code = driver.page_source
        domain = domain.replace("https:", '')
        domain = domain.replace("http:", '')
        domain = domain.replace("/", '')
        domain = domain.replace("\n", '')
        
        
    except:
        print("502 error")
        response = 502

    result.put(response)
    driver.close()
    

def main():
	result = queue.Queue()
	with open("/home/seungmin/phish/files/%s"%(sys.argv[1]), 'r') as file:
		domain_names = file.readlines()

	for domain in domain_names:
		thread = threading.Thread(target=process_domain, args=(domain, result))

		thread.start()
		pcap_file = sniff(iface='ens33', timeout=10, filter='tcp')
		thread.join()

		if result.get() == 200:
			file_name = "/home/seungmin/phish/traffic/chrome/%s.pcap"%(domain.replace("/",''))
			try:
				wrpcap(str(file_name), pcap_file)
			except:
				print("Pcap upload Error")

if __name__ == "__main__":
	main()
