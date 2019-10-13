import requests

def send_req(auth):
    burp0_url = ""
    burp0_cookies = {"auth": auth}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
                     "Upgrade-Insecure-Requests": "1"}
    print requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).content