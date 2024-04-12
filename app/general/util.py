from requests import session, Response
from bs4 import BeautifulSoup
from threading import Thread
from re import findall

def website_request(url: str, valid_url=None) -> tuple[str, BeautifulSoup]:

    if url == None or type(url) != str: 
        return None, None

    session_ = session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    if 'http' not in url: 
        url = 'https://' + url
    try:
        raw: Response = session_.get(url, headers=headers)
        status: int = raw.status_code
        VALID_STATUS_CODE = 200
        if status != VALID_STATUS_CODE: 
            return None, None
    except: 
        return None, None

    raw_data: str = raw.text
    if 'xml' in url: 
        soup = BeautifulSoup(raw_data, features='xml')
    else:
        soup = BeautifulSoup(raw_data, features='html.parser')
    
    session_.close()
    return raw_data, soup

def validate_url(trial_url: str, valid_url: list):

    raw, soup = website_request(trial_url)
    if valid_url == [] and raw != None:
        valid_url.append(trial_url)

def check_for_valid_website(url_list: list[str]) -> tuple[str, BeautifulSoup]:

    raw = None 
    soup = None
    valid_url=[]

    threads: list[Thread] = []
    for url in url_list:
        thread = Thread(target=validate_url, args=(url, valid_url, ))
        thread.start()
        threads.append(thread)

    for thread in threads: 
        thread.join()
    
    if valid_url == []:
        return None
    return valid_url[0]

def seperate_url(url: str): 
    """splits_article"""

    front_part_of_url = 'http://www.'
    
    extension_pattern = '[.][a-z]+[/]'
    extension = findall(extension_pattern, url)[0]
    extension_split = url.split(extension)[0]

    base_url = (extension_split + extension).replace(front_part_of_url, '')

    return base_url, url
