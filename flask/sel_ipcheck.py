from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import hashlib

def get_virustotal(ip):
    ip = "http://" + str(ip) + "/"
    text = ip.encode('utf-8')
    hashed = hashlib.new("sha256")
    hashed.update(text)
    result = hashed.hexdigest()
    url = "https://www.virustotal.com/gui/url/" + result + "/detection"

    # headless Chrome setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')         # 보안성 주의
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # browser driver settings
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    
    def expand_shadow_element(element):
        shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root
    
    browser.get(url)
    browser.implicitly_wait(10)

    root1 = browser.find_element_by_tag_name("url-view")
    shadow_root1 = expand_shadow_element(root1)

    root2 = shadow_root1.find_element_by_css_selector("vt-ui-detections-list")
    root2_2 = shadow_root1.find_element_by_css_selector("vt-ui-url-card")
    shadow_root2 = expand_shadow_element(root2)
    shadow_root2_2 = expand_shadow_element(root2_2)

    root3 = shadow_root2.find_element_by_css_selector("#detections")
    root3_2 = shadow_root2_2.find_element_by_css_selector("p")

    # get from webdriver
    soup = BeautifulSoup(root3.text, "lxml")

    if soup.find("p") == None:      # No match
        return "None"

    text = soup.find("p").get_text()
    detections = text.split('\n')
    print(detections)

    soup_2_text = BeautifulSoup(root3_2.text, "lxml").get_text()
    print(soup_2_text)
    return soup_2_text

