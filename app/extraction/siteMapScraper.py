from app.general.util import website_request, check_for_valid_website, seperate_url
from app.general.nameScraper import spacey_search
from app.processing.filterNames import filter_out_names

from threading import Thread
from pandas import read_csv
import pandas as pd


def url_creator(domain: str, endpoints: list) -> list: 
    
    end_of_domain = domain[-1]
    if '/' != end_of_domain:
        domain = domain + '/'

    url_options = []
    for endpoint in endpoints:
        potential_url = domain + endpoint
        url_options.append(potential_url)
    
    return url_options
    
def site_map_locater(url: str) -> str: 

    sitemap_endpoints = ['sitemap_index.xml', 'site-map-index.xml',
                        'site-map.xml', 'sitemap', 'site-map']
    site_map_urls = url_creator(url, sitemap_endpoints)
    valid_url = check_for_valid_website(site_map_urls)

    return valid_url

def search_site_map_url(url: str) -> str:

    created_urls = []

    endpoints = ['author', 'writer', 'team', 'contact']
    for endpoint in endpoints:
        temp_url = f'{url}/{endpoint}'
        created_urls.append(temp_url)

    valid_url = check_for_valid_website(created_urls)
    return valid_url

def process_site_map_search(base_url: str):

    valid_site_map = site_map_locater(base_url)
    if valid_site_map != None: 
        return None
    
    valid_team_map: str = search_site_map_url(valid_site_map)
    if valid_team_map == None: 
        return None
    
    raw_text, soup = website_request(valid_team_map)
    possible_names = spacey_search(raw_text)
    valid_names = filter_out_names(possible_names)
    
    if valid_names == []:
        return None
    return valid_names
