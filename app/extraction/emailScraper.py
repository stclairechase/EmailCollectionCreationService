from pandas import read_html
from io import StringIO
from bs4 import BeautifulSoup

from app.extraction.siteMapScraper import site_map_locater
from app.data_management.general import setup_data
from app.general.util import website_request, seperate_url, check_for_valid_website

def soup_check(soup: BeautifulSoup) -> list: 
    possible_emails = []
    split_soup = soup.text.split('\n')
    for data in split_soup: 
        if '@' in data: 
            possible_emails.append(data)
    return possible_emails

def site_map_search(base_url: str) -> list:

    site_map_url = site_map_locater(base_url)
    if site_map_url == None: 
        return []
    
    raw, soup = website_request(site_map_url)
    possible_emails = soup_check(soup)
    return possible_emails

def raw_web_search(base_url: str) -> list: 

    endpoints = [
        'contact', 'contacts', 'contact-us', 'info', 'support',
        'team', 'mail', 'about', 'email'
    ]
    possible_urls = [base_url + endpoint for endpoint in endpoints]
    valid_url = check_for_valid_website(possible_urls)
    if valid_url == None: 
        return []
    raw, soup = website_request(valid_url)
    possible_emails = soup_check(soup)
    return possible_emails

def process(url: str, email_list: list): 

    base_url, url = seperate_url(url)

    site_map_emails: list = site_map_search(base_url)
    email_list.extend(site_map_emails)

    raw_web_emails: list = raw_web_search(base_url)
    email_list.extend(raw_web_emails)



