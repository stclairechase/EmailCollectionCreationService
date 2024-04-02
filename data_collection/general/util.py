from requests import session, Response
from bs4 import BeautifulSoup
from threading import Thread
from re import findall

def website_request(url: str, parser = None) -> tuple[str, BeautifulSoup]: 

    if parser == None: 
        parser = 'html.parser'

    session_ = session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    raw: Response = session_.get(url, headers)
    status: int = raw.status_code
    VALID_STATUS_CODE = 200
    if status != VALID_STATUS_CODE: 
        return None, None

    raw_data: str = raw.text
    soup = BeautifulSoup(raw_data, parser)
    
    session_.close()
    return raw_data, soup

def check_for_valid_website(url_list: list[str]) -> tuple[str, BeautifulSoup]:

    raw = None 
    soup = None

    threads: list[Thread] = []
    for url in url_list:
        thread = Thread(target=website_request, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads: 
        thread.join()
        raw, soup = thread.result
        if raw != None:
            break

    return raw, soup

def seperate_url(url: str): 
    """splits_article"""

    front_part_of_url = 'http://www.'
    
    extension_pattern = '[.][a-z]+[/]'
    extension = findall(extension_pattern, url)[0]
    extension_split = url.split(extension)[0]

    base_url = (extension_split + extension).replace(front_part_of_url, '')

    return base_url, url