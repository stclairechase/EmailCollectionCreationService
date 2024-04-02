from general.util import website_request, check_for_valid_website, seperate_url
from threading import Thread
from pandas import read_csv
import pandas as pd

def url_creator(domain: str, endpoints: list) -> list: 

    endpoints = ['sitemap_index.xml', 'site-map-index.xml',
                 'site-map.xml', 'sitemap', 'site-map']
    
    end_of_domain = domain[-1]
    if '/' != end_of_domain:
        domain = domain + '/'

    url_options = []
    for endpoint in endpoints:
        potential_url = domain + endpoint
        url_options.append(potential_url)
    
    return url_options

def site_map_processor(url: str): 

    base_url, url = seperate_url(url)

    sitemap_endpoints = ['sitemap_index.xml', 'site-map-index.xml',
                        'site-map.xml', 'sitemap', 'site-map']
    site_map_urls = url_creator(base_url, sitemap_endpoints)

    raw, soup = check_for_valid_website(site_map_urls)


df = read_csv('/Users/chasestclaire/Desktop/coding_projects/github/AutomatedEmailCreation/EmailCollectionCreationService/data/example_input_data/20.rowss.testing.20.feb.csv')
URL = df['URL'].tolist()
urls = [x for x in URL if not pd.isna(x)]

for url in urls: 
    site_map_processor(url)