from ...general.util import website_request
from threading import Thread

def url_creator(domain: str) -> list: 

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