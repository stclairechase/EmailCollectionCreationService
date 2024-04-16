from re import findall
from bs4 import BeautifulSoup
from threading import Thread, Lock
from os.path import exists
from pandas import read_csv

from app.extraction.siteMapScraper import site_map_locater
from app.data_management.general import setup_data, directory_path_finder
from app.general.util import website_request, seperate_url, find_contact_url


thread_lock = Lock()

def soup_email_check(data: BeautifulSoup or str) -> list: 
    if data == None: 
        return []
    possible_emails = []
    if type(data) == BeautifulSoup: 
        split_data = data.text.split('\n')
    else: 
        split_data = data.split(' ')

    for inner_data in split_data: 
        if '@' in inner_data: 
            possible_emails.append(inner_data)
    return possible_emails

def modified_findall(soup: BeautifulSoup, tag: str, html_data: list) -> list:

    if tag == 'a': 
        findall = soup.findAll(tag, href=True, recursive=True)
    else:
        findall = soup.find_all(tag, recursive=True)

    with thread_lock: 
        html_data.extend(findall)

def site_map_search(base_url: str) -> list:

    site_map_url = site_map_locater(base_url)
    if site_map_url == None: 
        return []
    
    raw, soup = website_request(site_map_url)
    possible_emails = soup_email_check(soup)

    return possible_emails

def raw_web_search(contact_url: str) -> list: 

    if contact_url == None: 
        return []
    raw, soup = website_request(contact_url)

    possible_emails: list = soup_email_check(soup)
    return possible_emails

def html_tag_search(url: str):

    soup, raw = website_request(url)

    html_tags = ['a', 'div', 'p']

    threads: list[Thread] = []
    html_data: list[str] = []

    for tag in html_tags: 
        thread = Thread(target=modified_findall, args=(soup, tag, html_data, ))
        thread.start()
    for thread in threads: 
        thread.join()

    raw_possible_emails: list[str] = []
    threads: list[Thread] = []

    for inner_data in html_data: 
        thread = Thread(target=soup_email_check, args=(inner_data, ))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    return raw_possible_emails

def regex_filter(possible_email: str, email_list: list) -> None:

    pattern = '[a-zA-Z.]+[@][a-zA-Z]+[.][a-z]+$'
    if possible_email == None: 
        return 
    discovered_emails = findall(pattern, possible_email)
    with thread_lock:
        email_list.extend(discovered_emails)

def verifyier(possible_emails: list) -> list[str]: 
    valid_emails: list[str] = []

    threads = []
    for email in possible_emails: 
        thread = Thread(target=regex_filter, args=(email, valid_emails, ))
        thread.start()
        threads.append(thread)
    for thread in threads: 
        thread.join()

    filtered_dups = list(set(valid_emails))
    return filtered_dups

def direct_search(url: str, email_list: list) -> list: 

    raw_text, soup = website_request(url)
    if raw_text != None:
        regex_filter(raw_text, email_list)
    if soup != None:
        regex_filter(soup.text, email_list)

def check_historical_data(base_url: str, email_list: list[dict]) -> bool: 

    current_base_urls = [x['base_url'] for x in email_list]
    if base_url not in current_base_urls: 
        return True

    directory_path = directory_path_finder()
    data_file = 'data/created_data/raw_email_data.csv'
    file_path = directory_path + data_file

    if not exists(file_path): 
        return True 
    
    df = read_csv(file_path)
    mask = (df['base_url'] == base_url) 

    filtered_df = df[mask]
    if filtered_df.empty: 
        return True
    
    return False

def process(url: str, email_list: list) -> list[dict]: 

    possible_emails = []

    base_url, url = seperate_url(url)
    contact_url = find_contact_url(base_url)

    scraped_data_check: bool = check_historical_data(base_url, email_list)
    if scraped_data_check == False: 
        return []

    site_map_emails: list = site_map_search(base_url)
    possible_emails.extend(site_map_emails)

    raw_web_emails: list = raw_web_search(contact_url)
    possible_emails.extend(raw_web_emails)

    raw_main_url_search: list = raw_web_search(url)
    possible_emails.extend(raw_main_url_search)

    direct_search(url, email_list)
    direct_search(contact_url, email_list)

    if possible_emails == []:
        return []
    verified_emails = verifyier(possible_emails)
    email_data_to_dict = lambda x : {'email': x, 'base_url': base_url}
    filtered_emails = [email_data_to_dict(email) for email in verified_emails]

    email_list.extend(filtered_emails)
    return email_list




