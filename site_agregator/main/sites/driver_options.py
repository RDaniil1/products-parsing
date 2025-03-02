from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from fake_useragent import UserAgent
from fp.fp import FreeProxy


class DiverOptions:
    def __init__(self):
        self.ip = '' 
        self.port = ''
        
        self.profile = webdriver.FirefoxProfile()
        self.options = Options()

        self.possible_browsers = ["Chrome", "Firefox", "Edge", "Opera", "Yandex Browser"]
    
    def create(self):
        self.set_proxy_info()
        self.set_profile()
        self.set_options()

    def set_proxy_info(self):
        proxy = FreeProxy().get()
        proxy = proxy.replace('http://', '')
        self.ip, self.port = proxy.split(':')

    def set_profile(self):
        self.profile.set_preference('network.proxy.type', 1)
        self.profile.set_preference('network.proxy.http', self.ip)
        self.profile.set_preference('network.proxy.http_port', int(self.port))
        self.profile.set_preference("general.useragent.override", UserAgent(browsers=self.possible_browsers).random)
        self.profile.set_preference("dom.webdriver.enabled", False)
        self.profile.set_preference('useAutomationExtension', False)

    def set_options(self):
        # self.options.add_argument("--headless")
        self.options.profile = self.profile